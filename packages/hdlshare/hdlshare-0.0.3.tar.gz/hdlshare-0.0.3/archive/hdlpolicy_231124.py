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
    import sapcolors as tp
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp


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


def list_policies(endpoint: str, certificate: str, key: str) -> list:
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
    table = Table(title=title, header_style=tp.header_style, title_style=tp.title_style)
    table.add_column('Claim', justify="left", style=tp.cinfo)
    table.add_column('Description', justify="left", style=tp.cinfo)
    table.add_column('Value', justify="left", style=tp.cinfo)
    for c, v in token.items():
        desc = claim_name[c] if c in claim_name else ''
        if c in ['exp', 'iat', 'nbf']:
            if isinstance(v, int) or isinstance(v, float) :
                v = datetime.fromtimestamp(v).strftime("%Y-%m-%d %H:%M:%S")
            else:
                v = v.strftime("%Y-%m-%d %H:%M:%S")
        table.add_row(c, desc, str(v))
    rprint('\n',table, '\n')


# DEPRECATED 
def token2profile(token_file: str, params: dict, profile_folder: str) -> None:
    with open(token_file,"r") as fp:
        token = fp.read().strip()
    public_key, _, _, _ = load_certs(params['cert'])
    endpoint = params['endpoint'].replace('hdlfs://', 'https://').replace('.files.', '.sharing.')
    audience = str(re.sub('^.*\/\/','', params['endpoint']))
    try: 
        decoded = jwt.decode(token, public_key, audience=audience, algorithms=["RS256"])
        print_jwt(decoded)
        profile = { "shareCredentialsVersion": 1,
            "bearerToken": token,
            "endpoint": endpoint + f"/shares/v1",
            "expirationTime": datetime.fromtimestamp(decoded['exp']).strftime("%Y-%m-%d %H:%M:%S"),
            "sub": decoded['sub']}
        profile_file = Path(profile_folder) / (decoded['sub'] + "_hdlfscli.json")
        with open(profile_file, "w") as fp:
            json.dump(profile,fp, indent=4)
        rprint(f"[{tp.cinfo}]Token verified and new profile written[/]: [{tp.variable}]{profile_file}[/]")

    except jwt.exceptions.DecodeError as de:
        rprint(f"[red]{de}")
        rprint(f"[red]Token not verified")
    except jwt.exceptions.ExpiredSignatureError as ese:
        rprint(f"[red]Signature expired!")
        rprint(f"[red]Token not verified!")

def print_token_from_profile(profile, params) -> None:
    public_key, _, _, _ = load_certs(params['cert'])
    audience = str(re.sub('^.*\/\/','', params['endpoint']))
    decoded = jwt.decode(profile['bearerToken'], public_key, audience=audience, algorithms=["RS256"])
    print_jwt(decoded)

def generate_token(user: str, days: int, profile_folder: str, params: dict) -> None:
    private_key = load_key(params['key'])
    endpoint = params['endpoint'].replace('hdlfs://', 'https://').replace('.files.', '.sharing.')
    public_key, sub, chain, fingerprints = load_certs(params['cert'])
    audience = str(re.sub('^.*\/\/','',params['endpoint']))
    profile_file = Path(profile_folder) / (user + "_hdlfscli.json")

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
    
    profile_file = Path(profile_folder) / (user + ".json")
    with open(profile_file, "w") as fp:
        json.dump(profile,fp, indent=4)

    rprint(f"New profile-file created for user [{tp.cinfo}]{jwt_payload['sub']}: "\
           f"[{tp.variable}]{profile_file}[/]\n")


def print_policies(policies) -> None:
    if isinstance(policies, dict):
        policies = [policies]
    table = Table(title="Policies", header_style=tp.header_style, title_style=tp.title_style)
    for c in ['policy','resources','subjects','privileges','constraints','author','createdAt']:
        table.add_column(c, justify="left", style=tp.cinfo)
    for p in policies:
        if 'createdAt' in p: 
            createdAt = datetime.fromtimestamp(p['createdAt']/1000).strftime("%Y-%m-%d %H:%M:%S")
        else: 
            createdAt = ""
        table.add_row(p['name'],'\n'.join(p['resources']),'\n'.join(p['subjects']), '\n'.join(p['privileges']),
                      ','.join(p['constraints']),p['author'],createdAt)
    rprint('\n',table)

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
    
    parser.add_argument("action", choices=['list', 'add', 'delete', 'get', 'token',
                                           'showtoken'], help=f"Action")
    parser.add_argument("policy_name", nargs="?", help=f"Policy name")
    parser.add_argument("-p", "--policy", help=f"Policy content (json)")
    parser.add_argument('-u', '--user', help=f"User/recipient (required for action=\'token\')")
    parser.add_argument('-R', '--resource', help=f"Resource to add or delete from policy")
    parser.add_argument('-S', '--subject', help=f"subject to add or delete from policy")
    parser.add_argument('-P', '--privilege', help=f"Privilege to add or delete from policy")
    parser.add_argument('-C', '--constraint', help=f"Constraint to add or delete from policy")
    parser.add_argument('-D', '--days', type=int, help=f"Days before expiring from now on.", default=30)
    parser.add_argument('-t', '--token', help=f"Verify token (default=./profiles.txt)", default='./profiles/token.txt')
    parser.add_argument('-c', "--config", help=f"HDLFs config in \'{HDLFSCONFIGFILE}\'", default='default')
    args = parser.parse_args()

    with open(Path.home() / HDLFSCONFIGFILE  ) as fp:
        params = json.load(fp)["configs"][args.config]

    match args.action:
        case 'token':
            generate_token(user=args.user, days=args.days, params=params)

        case 'showtoken':
            profile = read_profile(args.user)
            if 'sub' in params and args.user != params['sub']:
                rprint(f"[{tp.cwarn}]User != profile subject. Profile subject ignored.")
            print_token_from_profile(profile, params)

        case 'list':
            policies = list_policies(params['endpoint'], params['cert'], params['key'])
            print_policies(policies)

        case 'add':
            policy = get_policy(args.policy_name, params)
            if not policy:
                policy = new_policy(args.policy_name)

            if args.policy:
                policy = merge_policies(policy, json.loads(args.policy))
                
            if args.subject:
                if args.subject in policy['subjects']:
                    rprint(f"[{tp.cwarn}]Subject is already in policy: {args.subject}")
                else:
                    policy['subjects'].append(args.subject)
            if args.resource:
                if args.resource in policy['resource']:
                    rprint(f"[{tp.cwarn}]Resource is already in policy: {args.resource}")
                else:
                    policy['resource'].append(args.resource)
            if args.privilege:
                if args.privilege in policy['privilege']:
                    rprint(f"[{tp.cwarn}]Privilege is already in policy: {args.privilege}")
                else:
                    policy['privilege'].append(args.privilege)
            if args.constraint:
                if args.constraint in policy['constraint']:
                    rprint(f"[{tp.cwarn}]Constraint is already in policy: {args.constraint}")
                else:
                    policy['constraint'].append(args.constraint)

            add_policy(policy, params)
            get_policy(args.policy_name, params)
            print_policies(policy)
   
        case 'delete':
            if not args.subject and not args.resource \
               and not args.privilege and not args.constraint:
                delete_policy(args.policy_name, params)
                return 1
            policy = get_policy(args.policy_name, params)
            if args.subject in policy['subjects']:
                policy['subjects'].remove(args.subject)
            if args.resource in policy['resources']:
                policy['resources'].remove(args.resource)
            if args.privilege in policy['privileges']:
                policy['privileges'].remove(args.privilege)
            if args.constraint in policy['constraints']:
                policy['constraints'].remove(args.constraint)
            add_policy(policy, params)
            get_policy(args.policy_name, params)
            print_policies(policy)

        case 'get':
            policy = get_policy(args.policy_name, params)
            print_policies(policy)
  

if __name__ == '__main__':
    main()