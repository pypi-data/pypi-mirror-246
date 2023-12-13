import requests
from pathlib import Path
from datetime import datetime
import argparse
import json
import os

from rich import print as rprint

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import pkcs7, load_pem_private_key, \
                                                         pkcs12, BestAvailableEncryption
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.exceptions import InvalidSignature

try:
    import termprint as tp
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp

SAP_CA_ROOT_FILENAME = 'sap_cloud_root_ca.crt'


oid_name = { "C": NameOID.COUNTRY_NAME, "ST":NameOID.STATE_OR_PROVINCE_NAME,
             "O": NameOID.ORGANIZATION_NAME, "OU": NameOID.ORGANIZATIONAL_UNIT_NAME,
             "CN":NameOID.COMMON_NAME, "L": NameOID.LOCALITY_NAME,
             "STREET": NameOID.STREET_ADDRESS,"DC": NameOID.DOMAIN_COMPONENT,
             "UID": NameOID.USER_ID}

def subject2list(subject:str)->list:
    s = [('C', subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value),
         ('O',subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value)]
    if subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME):
        s.extend([('OU',v.value) for v in subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)])
    else:
        s.append(('OU', ''))
    if subject.get_attributes_for_oid(NameOID.LOCALITY_NAME):
        s.append(('L', subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value))
    else:
        s.append(('L',''))
    s.append(('CN',subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value))
    return s

def subject2dict(subject:str)->dict:
    s = {'C': subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value,
         'O': subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value}
    if subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME):
        s['OU'] = ', '.join([v.value for v in subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)])
    else:
        s['OU']= ''
    if subject.get_attributes_for_oid(NameOID.LOCALITY_NAME):
        s['L'] = subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value
    else:
        s['L'] = ''
    s['CN'] = subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    return s

def print_subject_chain(certs):
    sfs = [c.subject for c in certs]
    table_entries = []
    for i, sf in enumerate(sfs):
        s = subject2dict(sf)
        verified = 'Y' if i < len(sfs)-1 else 'root'
        table_entries.append([str(i), s['C'], s['O'], s['OU'], 
                              s['L'], s['CN'], verified])
    tp.print_table(columns=['','C','O','OU','L','CN','Verified'], 
                     lists=table_entries,
                     title='Certificates Chain')

def split_subject(subject:str) -> list:
    if subject[0] == '/':
        subject = subject[1:]
    return [ (s.split('=')[0].strip(), s.split('=')[1].strip()) for s in subject.split("/")]


def private_key(filename: Path, password=None) -> str:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    if password: 
        with open(filename, "wb") as f:
            f.write(key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.PKCS8,
                                    encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))))
    else:
        with open(filename, "wb") as f:
            f.write(key.private_bytes(encoding=serialization.Encoding.PEM,
                                    format=serialization.PrivateFormat.PKCS8,
                                    encryption_algorithm=serialization.NoEncryption()))
    return key


def create_sap_csr(subject: str, key) -> str:
    oid_names= x509.Name([x509.NameAttribute(oid_name[sf[0]],sf[1]) for sf in split_subject(subject)])
    csr = x509.CertificateSigningRequestBuilder().subject_name(oid_names).sign(key, hashes.SHA256())
    csr = csr.public_bytes(serialization.Encoding.PEM)

    return  csr.decode('utf-8').strip()


def get_sap_root_cert(timeout=30):
    url = 'https://aia.pki.co.sap.com/aia/SAP%20Cloud%20Root%20CA.crt'
    response = requests.get(url, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    return x509.load_pem_x509_certificates(response.content)


def get_token(cservice: dict, timeout=30):
    url = cservice['uaa']['url'] + "/oauth/token"
    header = {'Content-Type': 'application/x-www-form-urlencoded', 
              'Accept': 'application/json' }
    data = {'grant_type': 'client_credentials','token_format':'bearer',
            'client_id': cservice["uaa"]["clientid"], 'client_secret':cservice['uaa']['clientsecret']}
    response = requests.post(url, data, header, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    return response.json()['access_token']

def request_certificate(url:str, csr:str, validity:int, validity_type:str, bearer_token:str) -> str:
    url = url + "/v3/synchronous/certificate"

    header = {'Authorization': 'Bearer ' + bearer_token,
            'Content-Type': 'application/json', 
            'Accept': 'application/json' }

    data = {'csr': {'value': csr}, 
            'policy': 'sap-cloud-platform-clients', 
            'validity': {'value': validity, 'type':validity_type}}

    response = requests.post(url, json=data, headers=header, timeout=30)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    return response.json()['certificateChain']["value"]

def verify_certificate_chain(crts, root_crt):
    crts.extend(root_crt)
    for i in range(0,len(crts)-1):
        crt= crts[i]
        crt_v = crts[i+1]
        try: 
            crt_v.public_key().verify(crt.signature, crt.tbs_certificate_bytes,
                                      padding.PKCS1v15(), crt.signature_hash_algorithm)
        except InvalidSignature as ie:
            rprint("[red]Invalid Signature chain ({i})[/red]")
            return -1
    rprint(f"[{tp.cinfo}]Successfully verified certificate chain")
    return crts

def get_certificate_info(pem_path: Path) ->dict:
    cert = get_pem_certificate(pem_path)
    return {'subject': subject2list(cert.subject),
            'not valid before': cert.not_valid_before.isoformat(),
            'not valid after': cert.not_valid_after.isoformat(),
            'subject string': cert.subject.rfc4514_string()}


def get_pem_certificate(pem_path: Path) -> x509.Certificate:
    with open(pem_path) as fp:
        cert = x509.load_pem_x509_certificate(fp.read().encode('ascii'))
    return cert

def get_subject_str(pem_path: Path)->dict:
    with open(pem_path) as fp:
        cert = x509.load_pem_x509_certificate(fp.read().encode('ascii'))
    return cert.subject.rfc4514_string()


def save_p12(crts: list, pkey, alias: str, password: str, p12_path: str) -> None:
    tp.info(f"Creating Keystore", p12_path)
    pem_str=''
    for crt in crts: 
        pem_str += crt.public_bytes(encoding=serialization.Encoding.PEM).decode('ascii')
    crt = x509.load_pem_x509_certificate(pem_str.encode('ascii'))
    p12 = pkcs12.serialize_key_and_certificates((alias).encode('ascii'), pkey, crt, None, 
                                                BestAvailableEncryption(password.encode('ascii')))
    with open(p12_path, 'wb') as fp:
        fp.write(p12)

def main():

    parser = argparse.ArgumentParser("Creates, show details and list certificates.")
    parser.add_argument("action", choices=['create', 'list', 'details'], help="Command details (action)")
    parser.add_argument("CN", nargs='?',help="Subject common name (= certificate name)")
    parser.add_argument("-s", "--subject",  help="Subject of lowest certificate", action='store_true')
    parser.add_argument("-L", "--list",  help="List certificates in certificates folder", action='store_true')
    parser.add_argument("-p", "--pkiservice_file",  help="Service key file for PKI service", 
                        default='service_keys/pki_sk.json')
    parser.add_argument("-d", "--cert_dir", help="Certificate directory", default='./certificates')
    parser.add_argument("-v", "--validity", type = int, help="Number", default=1)
    parser.add_argument("-t", "--validity_type", help="Validity type", 
                        choices=['HOURS','DAYS','MONTHS','YEARS'], default='DAYS') 
    parser.add_argument("-l", "--location", help="Subject location", default='Walldorf BW')
    parser.add_argument("-P", "--P12pwd", help="Password for keystore that is created.")
    args = parser.parse_args()


    cert_dir = Path(args.cert_dir)

    match args.action:
        case 'details':
            pem_path = cert_dir / (args.CN+'.pem')
            cert = get_pem_certificate(pem_path=pem_path)
            tp.print_table(columns=['Field','Value'], 
                            lists=subject2list(cert.subject),
                            title=f"Subject Fields of {args.CN}")
            tp.info("Not valid before", cert.not_valid_before.isoformat())
            tp.info("Not valid after ", cert.not_valid_after.isoformat())
            tp.info("Subject         ", cert.subject.rfc4514_string())
            print('\n')
        
        case 'list':
            if not cert_dir.is_dir():
                tp.error(f"Given certificate-folder does not exist: {cert_dir}")
            pem_files = cert_dir.glob('*.pem')
            certkeylist = []
            for p in pem_files:
                creation_date = datetime.fromtimestamp(os.path.getctime(p)).strftime('%Y-%m-%d %H:%M:%S')
                certkeylist.append((p.stem, creation_date))
            certkeylist = sorted(certkeylist, key=lambda x: x[1])
            tp.print_table(columns=["Pem-files",'creation date'],lists=certkeylist,title='Certificate Files')
        

        case 'create':
            pki_service = args.pkiservice_file

            validity = args.validity
            validity_type = args.validity_type

            key_path = cert_dir / (args.CN+'.key')
            pem_path = cert_dir / (args.CN+'.pem')

            with open(pki_service) as fp:
                cservice = json.load(fp)
    
            # create subject
            subject=cservice['certificateservice']['subjectpattern']
            subject = '/'+subject.replace('L=%s', f'L={args.location}').replace('CN=%s', f'CN={args.CN}').replace(', ','/')
            # subject = '/'+subject.replace('CN=%s', f'CN={args.CN}').replace(', ','/')
            rprint(f"[{tp.cinfo}]Subject: [{tp.variable}]{subject}")

            # Private Key and Certificate Request
            pkey = private_key(key_path)
            csr = create_sap_csr(subject, pkey)

            # Token
            bearer_token = get_token(cservice)
            rprint(f"[{tp.cinfo}]Bearer token: Successfully requested  from certificate-service")

            # certificate from certificate service (Get PKCS7)
            cert_req = request_certificate(url=cservice["certificateservice"]["apiurl"],csr=csr, 
                                            validity=validity, validity_type=validity_type,
                                            bearer_token=bearer_token)
            rprint(f"[{tp.cinfo}]Certificate requested from certificate-service")
            
            # write pem-file with certificate chain
            crts = pkcs7.load_pem_pkcs7_certificates(cert_req.encode('ascii'))
            with open(pem_path, 'w') as fp:
                for crt in crts: 
                    fp.write(crt.public_bytes(encoding=serialization.Encoding.PEM).decode('ascii'))
            rprint(f"[{tp.cinfo}]Certificate saved to: [{tp.variable}]{pem_path}")

            crts = verify_certificate_chain(crts, get_sap_root_cert())
            print_subject_chain(crts)
            rprint(f"[{tp.cinfo}]Subject: [{tp.variable}]{crts[0].subject.rfc4514_string()}")

            # create pkcs12 file
            if args.P12pwd:
                p12_path = cert_dir / (args.CN+'.p12')
                save_p12(crts, pkey, args.CN, args.P12pwd, p12_path)

if __name__ == '__main__':
    main()