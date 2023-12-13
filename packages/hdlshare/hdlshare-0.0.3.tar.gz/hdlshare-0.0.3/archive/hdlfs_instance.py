
from pathlib import Path
import argparse
import json
import subprocess

import requests
from rich import print as rprint
from rich.pretty import pprint
from rich.panel import Panel

sap_orange = "rgb(238,171,48)"

def get_token(sk, timeout=30) -> str:

    url = sk['url'] + "/oauth/token"
    header = {'Accept': 'application/json' }
    data = {'grant_type': 'client_credentials',
            'client_id': sk["clientid"],
            'client_secret':sk['clientsecret']}
    response = requests.post(url, data, header, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    return response.json()['access_token']

def all_services(token, url, timeout=30) -> str:
    url = url + "/v1/service_offerings"
    header = {'Authorization': 'Bearer ' + token }
    response = requests.get(url, headers=header, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    offerings = response.json()
    return [n['name'] for n in offerings['items']]


def get_service(token, url, name, timeout=30) -> str:
    url_service = url + "/v1/service_offerings"
    header = {'Authorization': 'Bearer ' + token }
    params = {"fieldQuery": f"name eq \'{name}\'"}
    response = requests.get(url_service, params=params, headers=header, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    offerings = response.json()
    if len(offerings['items'])>1:
        rprint(f"[red]Warning[/red] - number of offerings if name [green]{name}: {len(offerings['items'])}")
        rprint("Using only first item!")
    if len(offerings['items']) == 0:
        rprint(f"[red]No match for service: {name}")
        service_names = all_services(token,url)
        pprint(service_names)
        raise ValueError("[red]No match for service: {name}")
    return offerings['items'][0]['id']

def get_plan(token, url, service_id, name, timeout=30):
    url = url + "/v1/service_plans"
    header = {'Authorization': 'Bearer ' + token }
    params = {"fieldQuery": f"service_offering_id eq \'{service_id}\' "\
              f"and name eq \'{name}\'"}
    response = requests.get(url, params=params, headers=header, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    plans = response.json()
    if len(plans['items'])>1:
        rprint(f"[red]Warning[/red] - number of plans for id [green]{service_id}: {len(plans['items'])}")
        rprint("Using only first item!")
    if len(plans['items']) == 0:
        raise ValueError(f"[red]No match for service plan: {service_id} - {name}")
    return plans['items'][0]['id']

def create_instance(token, url, service_plan_id, name, data, timeout=30):
    url = url + "/v1/service_instances"
    header = {'Authorization': 'Bearer ' + token }
    rdata = {"async": False, "name":name, "service_plan_id":service_plan_id}
    rdata['parameters'] = data
    rprint(rdata)
    response = requests.post(url, json=rdata, headers=header, timeout=timeout)
    if response.status_code not in[201, 202]:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    instance = response.json()

    return instance

def login(service_key_file: Path, subdomain: str) -> None:
    with open(service_key_file) as fp:
        sk = json.load(fp)

    sk['sm_url'], sk['clientid'], sk['clientsecret']

    cmd = ['smctl', 'login', '-a', sk['sm_url'], '--auth-flow', 'client-credentials',
           '--param', f'subdomain={subdomain}', '--client-id', sk['clientid'], 
           '--client-secret', sk['clientsecret']]
    print(' '.join(cmd))
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")
    rprint(Panel(f"Logged in successfully to service manager of [sap_orange] {subdomain}",
                 expand=False))

def provision(instance_name: str, config) -> None:

    if isinstance(config, Path):
        with open(config) as fp:
            config = fp.read()

    cmd = ['smctl', 'provision', instance_name, 'hana-cloud-dev', 'relational-data-lake', 
           '-c', str(config)]
    print("\n\n" + ' '.join(cmd)+'\n\n')
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")
    rprint(Panel(f"\n\nProvision of HDLFS: [sap_orange]{instance_name}",
                 expand=False))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("service_key_file",  help="Service Manager key file (json-format)")
    parser.add_argument("subdomain",  help="Subdomain")
    parser.add_argument("common_name",  help="Common Name")
    parser.add_argument("hdlfs_name",  help="HDLFS instance name")
    parser.add_argument("-H", "--HanaServicename",  help="SAP BTP HANA Service Name", default='hana-cloud-dev')
    parser.add_argument("-s", "--serviceplan",  help="SAP BTP service plan", default='relational-data-lake')
    parser.add_argument("-t", "--template",  help="File-Template to configure HDLFS instance", default="certificates/hdlfs_template.json")
    parser.add_argument("-c", "--ca_certificate",  help="Trusted CA certificate file", default="certificates/sap_cloud_root_ca.crt")

    args = parser.parse_args()

    CN = args.common_name

    template_file =  Path(args.template)
    ca_root_file =  Path(args.ca_certificate)
    hdlfs_conf_file = template_file.parent / (args.hdlfs_name + '.json')

    with open(ca_root_file) as fp:
        ca_root = fp.read()

    with open(hdlfs_conf_file) as fp:
        hdlfs_conf = json.load(fp)

    for a in hdlfs_conf["data"]["filecontainer"]["authorizations"]:
        a['pattern'] = f"^.*CN={CN},.*$"
    for a in hdlfs_conf["data"]["filecontainer"]["trusts"]:
        a["certData"]=ca_root

    with open(args.service_key_file) as fp:
        sk = json.load(fp)

    token = get_token(sk)
    service_id = get_service(token, sk['sm_url'], args.HanaServicename)
    plan_id = get_plan(token,sk['sm_url'], service_id=service_id, name=args.serviceplan)
    instance = create_instance(token, sk['sm_url'], service_plan_id=plan_id, 
                               name=args.hdlfs_name, data=hdlfs_conf )
    rprint(instance)
    with open("instance.json", 'w') as fp:
        json.dump(instance, fp)



    # with open(hdlfs_conf_file, "w") as fp:
    #     json.dump(hdlfs_conf, fp)
    # rprint(f"Config-file written: [sap_orange{hdlfs_conf_file}")

    # with open(hdlfs_conf_file) as fp:
    #     hdlfs2 = json.load(fp)
    # rprint(hdlfs_conf)

    # login(args.service_key_file, args.subdomain)
    # provision(args.hdlfs_name, hdlfs_conf_file)
    # provision(args.hdlfs_name, json.dumps(hdlfs_conf))
    

if __name__ == '__main__':
    main()