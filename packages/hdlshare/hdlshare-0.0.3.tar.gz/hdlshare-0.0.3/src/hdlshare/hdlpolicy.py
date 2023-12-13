import requests
import argparse
import json
import re
import base64
from pathlib import Path
from datetime import datetime, timedelta

from rich import print as rprint
from rich.table import Table
from rich.tree import Tree as rTree
from rich.pretty import pprint

import jwt
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID

try:
    import termprint as tp
    import sapcert
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp
    from hdlshare import sapcert


HDLFSCONFIGFILE = ".hdlfscli.config.json"

claim_name = {'iss': 'issuer', 'sub': 'subject', 'aud': 'audience', 'exp': 'expiration date',
              'nbf': 'not before time', 'iat': 'issued at time', 'jti': 'unique identifier', 
              'roles': 'roles', 'alg': 'algorithm', 'typ': 'type', 'x5c': 'key chain',
               'x5t#S256': 'fingerprint (1st x5c)'}


def load_key(filename: str):
    with open(filename, 'rb') as fp:
        pemlines = fp.read()
    private_key = load_pem_private_key(pemlines, password=None)
    return private_key

def load_certs(filename: str):
    with open(filename, 'rb') as fp:
        pemlines = fp.read()
    certs = x509.load_pem_x509_certificates(pemlines)
    key = certs[0].public_key()
    sub = certs[0].subject.rfc4514_string()
    fingerprints = []
    chain = []
    for c in certs:
        cstr = c.public_bytes(encoding=serialization.Encoding.PEM).decode('utf-8')
        chain.append(re.sub('--+.+--+\\n','',cstr).replace('\n',''))
        fingerprints.append(base64.b64encode(c.fingerprint(hashes.SHA256())).decode('ascii'))
    return key, sub, chain, fingerprints

def read_profile(filename: str) -> dict:
    filename = Path(filename)
    if not filename.suffix:
        filename = filename.parent / (filename.name +  '.json')
    if filename.is_file():
        pass
    elif (Path("profiles") / filename).is_file():
        filename = Path("profiles") / filename
    else:
        raise FileNotFoundError('Profile file not found!')
    with open(filename) as fp:
        profile = json.load(fp=fp)
    return profile


def list_policies(params: dict) -> list:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/policies/v1"
    headers = {'x-sap-filecontainer': container}
    r = requests.get(url, cert=(certificate, key), headers=headers)

    if r.status_code not in [200, 201]: 
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    policies = json.loads(r.text)['policies']

    return policies

def add_policy(policy: dict, params: dict) -> None:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/policies/v1/{policy['name']}"
    headers = {'x-sap-filecontainer': container, 'content-type': 'application/json' }
    data = json.dumps(policy)
    r = requests.put(url, cert=(certificate, key), headers=headers, data=data)

    if r.status_code not in [200, 201]:
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    # rprint(f"Policy added successfully: [{sapc.variable}]{policy['name']}")

def delete_policy(policy_name: str, params: dict) -> None:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/policies/v1/{policy_name}"
    headers = {'x-sap-filecontainer': container}
    r = requests.delete(url, cert=(certificate, key), headers=headers)

    if r.status_code != 202:
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    #rprint(f"Policy successfully deleted: [{sapc.variable}]{policy_name}")

def get_policy(policy_name: str, params: dict) -> None:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/policies/v1/{policy_name}"
    headers = {'x-sap-filecontainer': container}
    r = requests.get(url, cert=(certificate, key), headers=headers)

    if r.status_code == 404:
        rprint(f"[{tp.cwarn}]Policy not found: [{tp.variable}]{policy_name}")
        return {}
    
    elif r.status_code == 200:
        return json.loads(r.text)
    else:
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    

def print_jwt(token: dict, title='JWT') -> None:
    entries = []
    for c, v in token.items():
        desc = claim_name[c] if c in claim_name else ''
        if c in ['exp', 'iat', 'nbf']:
            if isinstance(v, int) or isinstance(v, float) :
                v = datetime.fromtimestamp(v).strftime("%Y-%m-%d %H:%M:%S")
            else:
                v = v.strftime("%Y-%m-%d %H:%M:%S")
        entries.append([c, desc, str(v)])
    tp.print_table(columns=['Claim', 'Description', 'Value'], lists=entries, title=title)

def print_token_from_profile(profile, params) -> None:
    public_key, _, _, _ = load_certs(params['cert'])
    audience = str(re.sub('^.*\/\/','', params['endpoint']))
    decoded = jwt.decode(profile['bearerToken'], public_key, audience=audience, algorithms=["RS256"])
    print_jwt(decoded)

def generate_token(user: str, days: int, params: dict) -> None:
    private_key = load_key(params['key'])
    endpoint = params['endpoint'].replace('hdlfs://', 'https://').replace('.files.', '.sharing.')
    _, sub, chain, fingerprints = load_certs(params['cert'])
    audience = str(re.sub('^.*\/\/','',params['endpoint']))
    # audience = str(re.sub('^.*\/\/','',endpoint))
    jwt_payload = {"nbf": int(datetime.utcnow().timestamp()), 
                    "exp": int((datetime.utcnow() + timedelta(days=days)).timestamp()),
                    "iss": sub,
                    "aud": audience, 
                    "sub": user,
                    "roles": "", 
                    "iat": int(datetime.utcnow().timestamp())}  
    print_jwt(jwt_payload, title='JWT Payload')
    token = jwt.encode(jwt_payload, private_key, algorithm="RS256", 
                       headers={'x5c':chain, 'x5t#S256':fingerprints[0]})
    # decoded = jwt.decode(token, public_key, audience=audience, algorithms=["RS256"])
    print_jwt(jwt.get_unverified_header(token), title='JWT Header')

    profile = { "shareCredentialsVersion": 1,
                "bearerToken": token,
                "endpoint": endpoint + "/shares/v1",
                "expirationTime":  datetime.fromtimestamp(jwt_payload['exp']).isoformat(),
                "sub": jwt_payload['sub']}
    
    profile_file = Path((user + ".json"))
    if Path('./profiles').is_dir():
        profile_file = Path('./profiles') / profile_file
    with open(profile_file, "w") as fp:
        json.dump(profile,fp, indent=4)

    rprint(f"New profile-file created for user [{tp.cinfo}]{jwt_payload['sub']}: "\
           f"[{tp.variable}]{profile_file}[/]\n")

def save_profile_with_cert(params, subject):
    cert = Path(params['cert']).parent / (subject+'.pem')
    key  = Path(params['key']).parent / (subject+'.key')
    if not cert.is_file():
        tp.error(f"Certificate-file is not existing: {cert}")
    if not key.is_file():
        tp.error(f"Key-file is not existing: {key}")

    cert_info = sapcert.get_certificate_info(cert)

    endpoint = params['endpoint'].replace('hdlfs://', 'https://')

    profile = { "shareCredentialsVersion": 1,
                "cert": str(cert),
                "key": str(key),
                "endpoint": str(endpoint + "/shares/v1"),
                "notValidBefore": cert_info['not valid before'],
                "notValidAfter": cert_info['not valid after'],
                "subject": cert_info['subject string']}
    
    profile_file = Path((subject + ".json"))
    if Path('./profiles').is_dir():
        profile_file = Path('./profiles') / profile_file
    with open(profile_file, "w") as fp:
        json.dump(profile,fp, indent=4)

    tp.info("New profile-file created",profile_file)


def print_policies(policies) -> None:
    if isinstance(policies, dict):
        policies = [policies]

    table =[]
    for p in policies:
        if 'createdAt' in p: 
            createdAt = datetime.fromtimestamp(p['createdAt']/1000).strftime("%Y-%m-%d %H:%M:%S")
        else: 
            createdAt = ""
        table.append([p['name'],'\n'.join(p['resources']),'\n'.join(p['subjects']), '\n'.join(p['privileges']),
                       ','.join(p['constraints']),p['author'],createdAt])
    tp.print_table(title='Policies',columns=['policy','resources','subjects','privileges','constraints','author','createdAt'],
                   lists=table)


def new_policy(policy_name) -> dict:
    return  {'resources': [], 'privileges': [], 'subjects': [], 
              'constraints': [], 'name': policy_name}

def merge_policies(policy1: dict, policy2: dict) -> dict:
    if 'name' in policy1 and 'name' in policy2 and policy1['name'] != policy2['name']:
        raise ValueError(f"Policy names clash: {policy1['name']} <-> {policy2['name']}")
    for p in policy2:
        policy1[p] = list(set(policy1[p] + policy2[p]))
    return policy1


def main():

    parser = argparse.ArgumentParser("Manage HDLFS share policies")
    
    parser.add_argument("action", choices=['list', 'add', 'delete', 'copy', 'token',
                                           'showtoken','cert_profile'], help=f"Action")
    parser.add_argument("policy_names", nargs="*", help=f"Policy name (for \'copy\' arg 2 policies)")
    parser.add_argument("-p", "--policy", help=f"Policy content (json)")
    parser.add_argument('-s', '--subject', help=f"subject/user to add or delete from policy and "\
                        "for showing or generating tokens")
    parser.add_argument('-R', '--resource', help=f"Resource to add or delete from policy")
    parser.add_argument('-P', '--privilege', help=f"Privilege to add or delete from policy")
    parser.add_argument('-C', '--constraint', help=f"Constraint to add or delete from policy")
    parser.add_argument('-D', '--days', type=int, help=f"Days before expiring from now on.", default=30)
    parser.add_argument('-c', "--config", help=f"HDLFs config in \'{HDLFSCONFIGFILE}\'", default='default')
    
    args = parser.parse_args()

    with open(Path.home() / HDLFSCONFIGFILE  ) as fp:
        params = json.load(fp)["configs"][args.config]

    policy_name = None
    if len(args.policy_names) == 1:
        policy_name = args.policy_names[0]

    match args.action:
        case 'token':
            if not args.subject:
                tp.error("Subject-argument required for generating!")
                return -1
            generate_token(user=args.subject, days=args.days, params=params)

        case 'showtoken':
            if not args.subject:
                tp.error("User-argument required for reading token from profile!")
                return -1
            profile = read_profile(args.subject)
            if 'sub' in params and args.subject != params['sub']:
                tp.warning("User != profile subject!")
            print_token_from_profile(profile, params)
            
        case 'cert_profile':
            if not args.subject:
                tp.error("Subject-argument required for generating!")
                return -1
            save_profile_with_cert(params, args.subject)
            
        
        case 'list':
            if policy_name:
                policies = get_policy(policy_name, params)
            else: 
                policies = list_policies(params)
            print_policies(policies)

        case 'add':
            if not policy_name:
                tp.error("Policy name is required for adding a new policy!")
                return -1
            policy = get_policy(policy_name, params)
            if not policy:
                policy = new_policy(policy_name)

            if args.policy:
                if '{' in args.policy:
                    policy2 = json.loads(args.policy)
                else:
                    with open(args.policy) as fp:
                        policy2 = json.load(fp)
                policy = merge_policies(policy, policy2)

            if args.subject:
                if args.subject in policy['subjects']:
                    rprint(f"[{tp.cwarn}]Subject is already in policy: {args.subject}")
                else:
                    policy['subjects'].append(args.subject)
            if args.resource:
                if args.resource in policy['resources']:
                    rprint(f"[{tp.cwarn}]Resource is already in policy: {args.resource}")
                else:
                    policy['resources'].append(args.resource)
            if args.privilege:
                if args.privilege in policy['privileges']:
                    rprint(f"[{tp.cwarn}]Privilege is already in policy: {args.privilege}")
                else:
                    policy['privileges'].append(args.privilege)
            if args.constraint:
                if args.constraint in policy['constraints']:
                    rprint(f"[{tp.cwarn}]Constraint is already in policy: {args.constraint}")
                else:
                    policy['constraints'].append(args.constraint)

            add_policy(policy, params)
            policy = get_policy(policy_name, params)
            print_policies(policy)
   
        case 'delete':
            if not args.subject and not args.resource \
               and not args.privilege and not args.constraint:
                delete_policy(policy_name, params)
                return 1
            policy = get_policy(policy_name, params)
            if args.subject in policy['subjects']:
                policy['subjects'].remove(args.subject)
            if args.resource in policy['resources']:
                policy['resources'].remove(args.resource)
            if args.privilege in policy['privileges']:
                policy['privileges'].remove(args.privilege)
            if args.constraint in policy['constraints']:
                policy['constraints'].remove(args.constraint)
            add_policy(policy, params)
            get_policy(policy_name, params)
            print_policies(policy)

        case 'copy':
            source_policy = args.policy_names[0]
            target_policy = args.policy_names[1]
            rprint(f"[{tp.cinfo}]Copy policy: [{tp.variable}]{source_policy} -> {target_policy}")
            policy = get_policy(source_policy, params)
            policy['name'] = target_policy
            add_policy(policy, params)
            policies = list_policies(params)
            print_policies(policies)
  

if __name__ == '__main__':
    main()