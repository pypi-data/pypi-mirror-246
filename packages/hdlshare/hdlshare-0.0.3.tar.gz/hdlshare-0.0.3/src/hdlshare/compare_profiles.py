import argparse
import json
from pathlib import Path
import re
import base64
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
    import hdlshare.termprint as tp
except ModuleNotFoundError:
    import hdlshare.termprint as tp

HDLFSCONFIGFILE = ".hdlfscli.config.json"

claim_name = {'iss': 'issuer', 'sub': 'subject', 'aud': 'audience', 'exp': 'expiration date',
              'nbf': 'not before time', 'iat': 'issued at time', 'jti': 'unique identifier', 
              'roles': 'roles', 'alg': 'algorithm', 'typ': 'type', 'x5c': 'key chain',
               'x5t#S256': 'fingerprint (1st x5c)'}

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

def main():

    parser = argparse.ArgumentParser("Compare profiles")
    parser.add_argument("config", help=f"HDLFs config in \'{HDLFSCONFIGFILE}\'")
    parser.add_argument("file1", help=f"First file to compare")
    parser.add_argument("file2", help=f"Second file to compare")
    parser.add_argument('-p', '--profile_dir', help=f"Profiles folder (default=./profiles)", default='./profiles/')
    args = parser.parse_args()

    with open(Path.home() / HDLFSCONFIGFILE  ) as fp:
        params = json.load(fp)["configs"][args.config]

    with open(Path(args.profile_dir) / args.file1 ) as fp:
        profile1 = json.load(fp)

    with open(Path(args.profile_dir) / args.file2 ) as fp:
        profile2 = json.load(fp)
    
    table = Table(title='Profile diffs', header_style=tp.header_style, title_style=tp.title_style)
    table.add_column('Source', justify="left", style=tp.cinfo)
    table.add_column('Key', justify="left", style=tp.cinfo)
    table.add_column('Value', justify="left", style=tp.cinfo)
    for k, v in profile1.items():
        if v != profile2[k]:
            table.add_row("1", k, str(v))
            table.add_row("2", k, str(profile2[k]))
    rprint(table)
 
    public_key, _, _, _ = load_certs(params['cert'])
    endpoint = params['endpoint'].replace('hdlfs://', 'https://').replace('.files.', '.sharing.')
    audience = str(re.sub('^.*\/\/','', params['endpoint']))
    
    payload1 = jwt.decode(profile1['bearerToken'], public_key, audience=audience, algorithms=["RS256"])
    payload_header1 = jwt.get_unverified_header(profile1['bearerToken']) | payload1

    payload2 = jwt.decode(profile2['bearerToken'], public_key, audience=audience, algorithms=["RS256"])
    payload_header2 = jwt.get_unverified_header(profile2['bearerToken']) | payload2


    table = Table(title='Profile Diffs', header_style=tp.header_style, title_style=tp.title_style)
    table.add_column('Source', justify="left", style=tp.cinfo)
    table.add_column('Claim', justify="left", style=tp.cinfo)
    table.add_column('Value', justify="left", style=tp.cinfo)
    for c, v1 in payload_header1.items():
        if v1 != payload_header2[c]:
            table.add_row("1", c, str(payload_header1[c]))
            table.add_row("2", c, str(payload_header2[c]))
    rprint(table)

    

if __name__ == '__main__':
    main()