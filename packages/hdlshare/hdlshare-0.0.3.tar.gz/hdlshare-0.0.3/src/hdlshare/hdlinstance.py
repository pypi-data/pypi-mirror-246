from pathlib import Path
import argparse
import json
import re

import requests
from rich import print as rprint

try:
    import termprint as tp
    import sapcert 
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp
    from hdlshare import sapcert 

HDLFSCONFIGFILE = ".hdlfscli.config.json"
SERVICE_ID = False
test_create = False

STD_CONF = {
      "timeout": 3000000000,
      "cert": "",
      "key": "",
      "skipServerCertificateVerification": True,
      "user": "",
      "role": "",
      "endpoint": "",
      "parallel": 10,
      "format": "TEXT"
    }

def extract_hc_region(url: str) ->str:
    region = re.match('.+\.(.+)\.hanacloud\.ondemand\.com.*',url)
    if region:
        return region.groups(1)[0]
    else:
        rprint(f"[{tp.cerror}]Could not retrieve \'hc-region\'from url!")
        return None

def get_token(sk, timeout=30, debug=False) -> str:
    path = "/oauth/token"
    url = sk['url'] + path
    header = {'Accept': 'application/json' }
    data = {'grant_type': 'client_credentials',
            'client_id': sk["clientid"],
            'client_secret':sk['clientsecret']}
    if debug:
        tp.print_request_info('POST', sk['url'], path, header, data)
    response = requests.post(url, data, header, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    return response.json()['access_token']


def get_hdlfs_service_id(token, url, timeout=30):
    url = url + "/v1/service_plans"
    header = {'Authorization': 'Bearer ' + token }
    params = {"fieldQuery": f"name eq \'relational-data-lake\'"}
    response = requests.get(url, params=params, headers=header, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    plans = response.json()
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

def create_instance(token, url, offering, plan, name, data, timeout=30) -> None:
    url = url + "/v1/service_instances"
    header = {'Authorization': 'Bearer ' + token }
    rdata = {"async": False, "name":name, "service_offering_name":offering, 
             "service_plan_name": plan}
    rdata['parameters'] = data
    with open("apiparams.json","w") as fp:
        json.dump(rdata, fp)
    if test_create:
        rprint(f"[{tp.cerror}]ONLY Test - no instance created")
        return {}
    response = requests.post(url, json=rdata, headers=header, timeout=timeout)
    if response.status_code not in[201, 202]:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")

def get_hdlfs_instances(token, url, name=None, timeout=30):
    service_id = get_hdlfs_service_id(token, url, timeout=30)
    rurl = url + f"/v1/service_instances"
    header = {'Authorization': 'Bearer ' + token, 
              'Accept': 'application/json', 
              'Content-Type': 'application/json'}
    if name:
        params = {"fieldQuery": f"name eq \'{name}\' and service_plan_id eq \'{service_id}\'"}
    else:
        params = {"fieldQuery": f"service_plan_id eq \'{service_id}\'"}
    response = requests.get(rurl, headers=header, params=params, timeout=timeout)
    if response.status_code not in[200, 201, 202]:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    instances = response.json()
    return instances['items']


def get_instance_parameter(token, url, name, timeout=30):
    instances = get_hdlfs_instances(token, url, name=name, timeout=timeout)
    if len(instances) > 1:
        raise ValueError(f"Number of instances >1 for: {name}")
        
    rurl = url + f"/v1/service_instances/{instances[0]['id']}/parameters"
    header = {'Authorization': 'Bearer ' + token, 
               'Accept': 'application/json', 
               'Content-Type': 'application/json'}
    response = requests.get(rurl, headers=header, timeout=timeout)
    if response.status_code not in[200, 201, 202]:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")

    return response.json()

# def get_subject(cert_file) -> dict:
#     sapcert.get_subject(cert_file)

def get_subject(user, cert_path) -> str:
    if not user:
        return None
    certCN_path = Path(cert_path) / (user + '.pem')
    if not certCN_path.is_file():
        rprint(f"[{tp.cwarn}There is no certificate file for[{tp.variable}] {user}: {certCN_path}")
        return None
    else:
        user_sub = sapcert.get_subject_str(certCN_path)
        return user_sub

def print_instance_user(name, parameters: dict) -> None:
    table_entries = list()
    table_entries.append(('allowed networks', parameters["data"]["fileContainer"]["allowedNetworks"]))
    for i, a in enumerate(parameters["data"]["fileContainer"]['authorizations']):
        table_entries.append((f"{i+1}. User", " "))
        table_entries.append((f'   pattern',a['pattern']))
        table_entries.append((f'   rank', a['rank']))
        table_entries.append((f'   roles', ','.join(a['roles'])))
    for role in parameters["data"]["fileContainer"]['roles']:
        table_entries.append((f"\'{role['name']}\'-privileges", ','.join(role['privileges'])))
    tp.print_table(title=f"HDLF {name} Parameter", lists=table_entries, columns=["Parameter", "Value"])

def main():

    parser = argparse.ArgumentParser(description="Utility to create a manage HDL instances via Service Manager API.")
    # positional argument 
    parser.add_argument("action", choices=['list','details','user', 'create', 'delete','add2config'],  help="Action")
    parser.add_argument("name",  nargs="?", help="HDLFS instance name (required for creating instance)")
    # flags with param  
    parser.add_argument("-a", "--admin",  help="User with ADMIN role (required for creating instance) and adding entry to config.")
    parser.add_argument("-u", "--user",  help="User with USER role (required for creating instance).")
    parser.add_argument("-H", "--HanaServicename",  help="SAP BTP HANA Service Name", default='hana-cloud')
    parser.add_argument("-s", "--service_plan",  help="SAP BTP service plan", default='relational-data-lake')
    parser.add_argument("-t", "--template",  help="File-Template to configure HDLFS instance", default="configs/hdlfs_template.json")
    parser.add_argument("-r", "--ca_certificate",  help="Trusted CA certificate file", default="certificates/sap_cloud_root_ca.crt")
    parser.add_argument("-S", "--service_key",  help="Service Manager key file", default='service_keys/sm-sk.txt')
    parser.add_argument("-d", "--dir_certificates",  help="Directory of certificates", default='./certificates')
    args = parser.parse_args()

    # Token
    with open(args.service_key) as fp:
        sk = json.load(fp)
    token = get_token(sk)

    tmp_dir = Path('tmp')
    if not tmp_dir.is_dir():
        tmp_dir = Path('.')
    
    # API Calls
    match args.action:
        case "list":     
            instances = get_hdlfs_instances(token,sk['sm_url'])
            with open(tmp_dir /"instances.json", 'w') as fp:
                json.dump(instances, fp, indent=4)
            table_entries = [(str(i+1), inst['name'], inst['id'])for i, inst in enumerate(instances)]
            tp.print_table(title='HDLFS instances',lists=table_entries, columns=["", "Name", "Instance ID"])
        
        case "details":     
            details = get_hdlfs_instances(token,sk['sm_url'],name=args.name)[0]
            with open(tmp_dir / (args.name+'.json'), 'w') as fp:
                json.dump(details, fp, indent=4)
            #sapc.print_lists(title='HDLFS instances',lists=table_entries, columns=["", "Name", "Instance ID"])
            #sapc.pprint(details)

            context = details.pop('context')
            tp.dictionary(details, f"Details of {args.name}")
            tp.dictionary(context, f"Context of {args.name}")

        case 'user':
            # Instance parameter
            parameters = get_instance_parameter(token, sk['sm_url'], name=args.name)     
            
            print_instance_user(name=args.name, parameters=parameters)
            parameter_file = Path('configs')/ str(args.name + '.json')
            with open(parameter_file, 'w') as fp:
                json.dump(parameters, fp, indent=4)     
            rprint(f"Parameter of [{tp.cinfo}]\"{args.name}\"[/{tp.cinfo}] downloaded to: [{tp.cinfo}]{parameter_file}")
        
        case "add2config":
            if not args.admin:
                rprint(f"[{tp.cerror}]Admin cmd argument required. It is the name of the certificate as well.")
                return -1
            details = get_hdlfs_instances(token,sk['sm_url'],name=args.name)[0]
            config_file = Path.home() / HDLFSCONFIGFILE
            if not config_file.is_file():
                rprint(f"[{tp.cerror}]No hdl-config file: {config_file}")
            with open(config_file) as fp:
                hdl_config = json.load(fp)
            
            cert_path = Path().absolute() / args.dir_certificates
            region = extract_hc_region(details['dashboard_url'])
            # rprint(f"[{tp.info}]Extracted region: [{tp.variable}]{region}")
            endpoint = f"hdlfs://{details['id']}.files.hdl.{region}.hanacloud.ondemand.com"
            
            hdl_config['configs'][args.name] = { 
                    "timeout": 3000000000,
                    "cert": str(cert_path / (args.admin + '.pem')),
                    "key": str(cert_path / (args.admin + '.key')),
                    "skipServerCertificateVerification": True,
                    "user": "",
                    "role": "",
                    "endpoint": endpoint,
                    "parallel": 10,
                    "format": "TEXT"
                    }
            with open(config_file, "w") as fp:
                json.dump(hdl_config, fp, indent=4)

        case 'delete':
            rprint(f"Delete HDLFS instance: [{tp.cinfo}]{args.name}")
            rprint(f"[{tp.cerror}]Deleting HDLFS instances not implemented yet!")
            return -1

        case 'create':
            rprint(f"Create HDLFS instance: [{tp.cinfo}]{args.name}")
            if not args.admin:
                raise ValueError("Admin argument required for creating an instance.")
        
            rprint(f"[{tp.cinfo}]Read template file for creating HDLFS: [{tp.variable}]{args.template}")
            template_file = Path(args.template)
            with open(template_file) as fp:
                hdlfs_conf = json.load(fp)

            rprint(f"[{tp.cinfo}]Read root certificate that signed user certificate: [{tp.variable}]{args.ca_certificate}")
            ca_root_file = Path(args.ca_certificate)

            # HDLFS conf file
            with open(ca_root_file) as fp:
                ca_root = fp.read()
            for a in hdlfs_conf["data"]["fileContainer"]["trusts"]:
                a["certData"]=ca_root.strip()

            # Get user setting from subject
            admin_sub = get_subject(args.admin, args.dir_certificates)
            user_sub = get_subject(args.user, args.dir_certificates)

            # adding user subject to hdlfs template
            for i, a in enumerate(hdlfs_conf["data"]["fileContainer"]["authorizations"]):
                pattern = a['pattern']
                if admin_sub and 'admin' in a['roles']:
                    a['pattern'] = admin_sub
                    rprint(f"[{tp.cinfo}]Authorization pattern changed: [{tp.variable}]{a['pattern']}")
                elif user_sub and 'user' in a['roles']:
                    a['pattern'] = user_sub
                    rprint(f"[{tp.cinfo}]Authorization pattern changed: [{tp.variable}]{a['pattern']}")
                elif 'admin' in a['roles'] and 'CN=%s' in pattern:
                    a['pattern'] =  a['pattern'].replace('CN=%s', f'CN={args.admin}')
                    rprint(f"[{tp.cinfo}]Authorization pattern changed: [{tp.variable}]{a['pattern']}")
                elif 'user' in a['roles'] and 'CN=%s' in pattern:
                    a['pattern'] =  a['pattern'].replace('CN=%s', f'CN={args.user}')
                    rprint(f"[{tp.cinfo}]Authorization pattern changed: [{tp.variable}]{a['pattern']}")
                else:
                    rprint(f"[{tp.cinfo}]Authorization pattern from template used with changes: [{tp.variable}]{a['pattern']}")

            
            print_instance_user(name=args.name, parameters=hdlfs_conf)
            create_instance(token, sk['sm_url'], 
                            offering=args.HanaServicename, plan=args.service_plan,
                            name=args.name, data=hdlfs_conf)



if __name__ == '__main__':
    main()