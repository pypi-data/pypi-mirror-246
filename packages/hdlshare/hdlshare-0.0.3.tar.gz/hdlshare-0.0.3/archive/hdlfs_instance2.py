
from pathlib import Path
import argparse
import json
import subprocess

import requests
from rich import print as rprint
from rich.pretty import pprint
from rich.panel import Panel

sap_orange = "rgb(238,171,48)"
lily = "rgb(61,17,227)"
turquoise = "rgb(54,220,184)"

SERVICE_ID = False
test_create = True

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

def get_plans(token, url, name, timeout=30):
    url = url + "/v1/service_plans"
    header = {'Authorization': 'Bearer ' + token }
    # params = {"fieldQuery": f"service_offering_id eq \'{service_id}\' "\
    #           f"and name eq \'{name}\'"}
    params = {"fieldQuery": f"name eq \'{name}\'"}
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


def create_instance_by_plan_id(token, url, service_plan_id, name, data, timeout=30):
    url = url + "/v1/service_instances"
    header = {'Authorization': 'Bearer ' + token }
    rdata = {"async": False, "name":name, "service_plan_id":service_plan_id}
    rdata['parameters'] = data
    with open("apiparams.json","w") as fp:
        json.dump(rdata, fp)
    response = requests.post(url, json=rdata, headers=header, timeout=timeout)
    if response.status_code not in[201, 202]:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    instance = response.json()

    return instance

def create_instance(token, url, offering, plan, name, data, timeout=30):
    url = url + "/v1/service_instances"
    header = {'Authorization': 'Bearer ' + token }
    rdata = {"async": False, "name":name, "service_offering_name":offering, 
             "service_plan_name": plan}
    rdata['parameters'] = data
    with open("apiparams.json","w") as fp:
        json.dump(rdata, fp)
    if test_create:
        return {}
    response = requests.post(url, json=rdata, headers=header, timeout=timeout)
    if response.status_code not in[201, 202]:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    return response.json()

def get_instances(token, url, name=None, timeout=30):
    rurl = url + f"/v1/service_instances"
    header = {'Authorization': 'Bearer ' + token, 
              'Accept': 'application/json', 
              'Content-Type': 'application/json'}
    if name:
        params = {"fieldQuery": f"name eq \'{name}\'"}
    response = requests.get(rurl, headers=header, params=params, timeout=timeout)
    if response.status_code not in[200, 201, 202]:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    instances = response.json()
    return instances['items'][0]['id']


def get_instance_parameter(token, url, service_instance_id, timeout=30):
    rurl = url + f"/v1/service_instances/{service_instance_id}/parameters"
    header = {'Authorization': 'Bearer ' + token, 
               'Accept': 'application/json', 
               'Content-Type': 'application/json'}
    response = requests.get(rurl, headers=header, timeout=timeout)
    if response.status_code not in[200, 201, 202]:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")

    return response.json()

def main():

    parser = argparse.ArgumentParser()
    # positional argument
    parser.add_argument("service_key_file",  help="Service Manager key file")
    
    # flags without param
    parser.add_argument("-p", "--parameter", help="Parameter of hdlsf instance", action="store_true")
    parser.add_argument("-l", "--list", help="List HDLFS", action="store_true")
    parser.add_argument("-c", "--create_instance", help="Create HDLFS instance", action="store_true")

    # flags with param
    parser.add_argument("-n", "--hdlfs_name",  help="HDLFS instance name (required for creating instance)")
    parser.add_argument("-C", "--CommonName",  help="Common Name (required for creating instance)")
    parser.add_argument("-H", "--HanaServicename",  help="SAP BTP HANA Service Name", default='hana-cloud-dev')
    parser.add_argument("-s", "--serviceplan",  help="SAP BTP service plan", default='relational-data-lake')
    parser.add_argument("-t", "--template",  help="File-Template to configure HDLFS instance", default="configs/hdlfs_template.json")
    parser.add_argument("-r", "--ca_certificate",  help="Trusted CA certificate file", default="certificates/sap_cloud_root_ca.crt")

    args = parser.parse_args()

    # Token
    with open(args.service_key_file) as fp:
        sk = json.load(fp)
    token = get_token(sk)
    
    # API Calls
    if args.list:
        plans = get_plans(token,sk['sm_url'], name=args.serviceplan)
        with open("tmp/plans.json", 'w') as fp:
            json.dump(plans, fp, indent=4)

    # Instance parameter
    if args.parameter:
        instance_name = args.hdlfs_name
        instance_id = get_instances(token, sk['sm_url'], name=instance_name)
        parameter = get_instance_parameter(token, sk['sm_url'], service_instance_id=instance_id)

        parameter_file = Path('configs')/ str(instance_name + '.json')
        with open(parameter_file, 'w') as fp:
            json.dump(parameter, fp)          
        rprint(f"Parameter of [sap_orange]\"{instance_name}\"[/sap_orange] downloaded to: [sap_orange]{parameter_file}")

    if args.create_instance:
        rprint(f"Create HDLFS instance: [sap_orange]{args.hdlfs_name}[/sap_orange]")
        if not args.CommonName:
            raise ValueError("Common Name argument required for creating an instance.")
        CN = args.CommonName
        rprint(f"Read template file for creating HDLFS: [sap_orange]{args.template}")
        template_file = Path(args.template)
        rprint(f"Read root certificate that signed user certificate: [sap_orange]{args.ca_certificate}")
        ca_root_file = Path(args.ca_certificate)
        hdlfs_conf_file = template_file.parent / (args.hdlfs_name + '.json')

        # HDLFS conf file
        with open(ca_root_file) as fp:
            ca_root = fp.read()

        with open(template_file) as fp:
            hdlfs_conf = json.load(fp)

        for a in hdlfs_conf["data"]["filecontainer"]["authorizations"]:
            a['pattern'] = f"^.*CN={CN},.*$"
        for a in hdlfs_conf["data"]["filecontainer"]["trusts"]:
            a["certData"]=ca_root.strip()
        with open(hdlfs_conf_file, "w") as fp:
            json.dump(hdlfs_conf, fp)
        
        rprint(f"Config-file written: [sap_orange]{hdlfs_conf_file}")
        instance = create_instance(token, sk['sm_url'], 
                                   offering=args.HanaServicename, plan=args.serviceplan,
                                   name=args.hdlfs_name, data=hdlfs_conf)
        
        with open("instance.json", 'w') as fp:
            json.dump(instance, fp)


if __name__ == '__main__':
    main()