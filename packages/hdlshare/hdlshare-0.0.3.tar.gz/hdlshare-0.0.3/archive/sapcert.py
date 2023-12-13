import requests
from pathlib import Path
import argparse
import subprocess
import json

from rich import print as rprint
from rich.table import Table
from rich.panel import Panel

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs7
from cryptography import x509
from cryptography.x509.oid import NameOID

SAP_CA_ROOT_FILENAME = 'sap_cloud_root_ca.crt'
sap_orange = "rgb(238,171,48)"
lily = "rgb(61,17,227)"
turquoise = "rgb(54,220,184)"

oid_name = { "C": NameOID.COUNTRY_NAME, "ST":NameOID.STATE_OR_PROVINCE_NAME,
             "O": NameOID.ORGANIZATION_NAME, "OU": NameOID.ORGANIZATIONAL_UNIT_NAME,
             "CN":NameOID.COMMON_NAME, "L": NameOID.LOCALITY_NAME,
             "STREET": NameOID.STREET_ADDRESS,"DC": NameOID.DOMAIN_COMPONENT,
             "UID": NameOID.USER_ID}


def print_subject_chain(certs):
    sfs = [c.subject for c in certs]
    table = Table(title='Certificates Chain')
    table.add_column("depth", justify="left", style=f"bold {turquoise}", no_wrap=False)
    for c in ['C','O','OU','L','CN']:
        table.add_column(c, justify="left", style=lily, no_wrap=False)
    for i, sf in enumerate(sfs):
        table.add_row(str(i), sf.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value,
                      sf.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value,
                      sf.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value,
                      sf.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value,
                      sf.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value)
    rprint(table)

def split_subject(subject:str) -> list:
    if subject[0] == '/':
        subject = subject[1:]
    return [ (s.split('=')[0].strip(), s.split('=')[1].strip()) for s in subject.split("/")]


def private_key(filename: Path) -> str:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    with open(filename, "wb") as f:
        f.write(key.private_bytes(encoding=serialization.Encoding.PEM,
                                  format=serialization.PrivateFormat.PKCS8,
                                  encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase")))
    return key


def create_sap_csr(subject: str, key, filename: Path) -> str:
    oid_names= x509.Name([x509.NameAttribute(oid_name[sf[0]],sf[1]) for sf in split_subject(subject)])
    csr = x509.CertificateSigningRequestBuilder().subject_name(oid_names).sign(key, hashes.SHA256())
    csr = csr.public_bytes(serialization.Encoding.PEM)
    # Write our CSR out to disk.
    rprint(f"Write certificate request to: [{lily}]{filename}[/{lily}]")
    with open(filename, "wb") as f:
        f.write(csr)
    return  csr.decode('utf-8').strip()


def get_sap_root_cert(timeout=30):
    # curl -s -m 30 -X GET $root_ca_url > "$root_ca_cert_file" &
    url = 'https://aia.pki.co.sap.com/aia/SAP%20Cloud%20Root%20CA.crt'
    response = requests.get(url, timeout=timeout)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTPError: {response.text}")
    return response.content.decode('utf-8').strip()


def subject_fields_from_cert(certificate_file: str) -> dict:
    # openssl x509 -subject -noout -in meca.crt 
    cmd = ["openssl", "x509", "-subject", "-noout", "-in", certificate_file ]
    # rprint(f"Cmd: [green]{' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")

    subs = result.stdout.decode("utf-8")[8:].split(',')
    return { s.split('=')[0].strip() :s.split('=')[1].strip() for s in subs}


def create_certificate_request(key_path: str, csr_path: str, subject: str) -> None:
    cmd = ["openssl", "req", "-new", "-nodes", "-newkey", "rsa:2048", "-out", str(csr_path), \
        '-keyout', str(key_path), "-subj", subject ]
    # rprint(f"Create certificate request with openssl: [green]{' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ValueError(f"Failed to create csr-file with: {' '.join(cmd)}")


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

def p7b2pem(p7b_file: Path, pem_file: Path) -> None:
    cmd = ['openssl', 'pkcs7', '-print_certs', '-in', str(p7b_file), '-out', str(pem_file)]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")

def pem2crt(pem_file: Path, crt_file: Path) -> None:
    # convert to crt
    cmd = ['openssl', 'x509', '-in', str(pem_file), '-out', str(crt_file)]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")
    
def certificate_summary(cert_file):
    cmd = ['openssl', 'x509', '-in', str(cert_file), '-noout', '-subject']
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")
    
    subs = result.stdout.decode("utf-8")[8:].split(',')
    subs = { s.split('=')[0].strip():s.split('=')[1].strip()  for s in subs}
    table = Table(title="Subjects")
    table.add_column("Field", justify="left", style=sap_orange)
    table.add_column("Value", justify="left", style=sap_orange, no_wrap=True)
    for n,v in subs.items():
        table.add_row(n, v)
    print("\n")
    rprint(table)

    cmd = ['openssl', 'x509', '-in', str(cert_file), '-noout', '-startdate']
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")
    valid_from = result.stdout.decode("utf-8")[10:].strip()

    cmd = ['openssl', 'x509', '-in', str(cert_file), '-noout', '-enddate']
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")
    valid_to = result.stdout.decode("utf-8")[9:].strip()
    rprint(Panel(f"Validity:\nfrom: [{sap_orange}]{valid_from}[white]  to: [{sap_orange}]{valid_to}", expand=False))

def verify_certificate(root_ca: str, pem_path: str, crt_path: str) -> None:
    cmd = ['openssl', 'verify', '-show_chain', '-CAfile', str(root_ca), '-untrusted', 
           str(pem_path), str(crt_path)]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise ChildProcessError(f"OS command failed: {result}")
    lines = result.stdout.decode("utf-8").split('\n')
    rprint(f"\nCertificate verification: [b {sap_orange}]{lines[0]}\n")
    table = Table(title=lines[1])
    columns = ['depth','C','O','OU','L','CN']
    for c in columns:
        if c == 'depth':
            table.add_column(c, justify="left", style="bold rgb(91,91,91)", no_wrap=False)
        else:
            table.add_column(c, justify="left", style=sap_orange, no_wrap=False)
    for line in lines[2:]:
        if not line:
            continue
        depth=line[6]
        subs = line[9:].split(',')
        subs = {s.split('=')[0].strip() :s.split('=')[1].strip() for s in subs}
        subs = [subs[c] for c in columns if c != 'depth' and c in subs]
        table.add_row(depth, *subs)
    rprint(table)


def get_sap_root(root_ca: Path):
    if not root_ca.is_file():
        # SAP Root Certificate
        rprint("\nGet SAP root certificate")
        sapcert = get_sap_root_cert()
        with open(root_ca, 'w') as fp:
            fp.write(sapcert)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("CN",  help="Subject common name (= certificate name)")
    parser.add_argument("pkiservice",  help="PKI service file")
    parser.add_argument("-d", "--cert_dir", help="Certificate directory", default='./certificates')
    parser.add_argument("-v", "--validity", type = int, help="Number of months", default=1)
    parser.add_argument("-t", "--validity_type", help="Validity type", 
                        choices=['HOURS','DAYS','MONTHS','YEARS'], default='MONTHS') 
    parser.add_argument("-l", "--location", help="Subject location", default='Walldorf BW')
    args = parser.parse_args()

    pki_service = args.pkiservice
    cert_dir = Path(args.cert_dir)
    root_ca = cert_dir / SAP_CA_ROOT_FILENAME
    csr_path = cert_dir / (args.CN+'.csr')
    key_path = cert_dir / (args.CN+'.key')
    p7b_path = cert_dir / (args.CN+'.p7b')
    pem_path = cert_dir / (args.CN+'.pem')
    crt_path = cert_dir / (args.CN+'.crt')

    validity = args.validity
    validity_type = args.validity_type

    with open(pki_service) as fp:
        cservice = json.load(fp)
    
    # create subject
    subject=cservice['certificateservice']['subjectpattern']
    subject = '/'+subject.replace('L=%s', f'L={args.location}').replace('CN=%s', f'CN={args.CN}').replace(', ','/')
    # rprint(f"Subject of certificate: {subject}")
    rprint(f"Subject: {subject}")
    pkey = private_key(key_path)
    csr = create_sap_csr(subject, pkey,csr_path)

    # create request
    # create_certificate_request(key_path=key_path, csr_path=csr_path, subject=subject)
    # rprint(f"CSR-file \"{csr_path}\" and key-file \"{key_path}\" created sucessfully.")
    # with open(csr_path) as fp:
    #     csr = fp.read()

    # Token
    bearer_token = get_token(cservice)
    rprint(f"[{turquoise}]Bearer token[/{turquoise}]: Successfully requested  from certificate-service")

    # certificate from certificate service
    cert_req = request_certificate(url=cservice["certificateservice"]["apiurl"],csr=csr, 
                                      validity=validity, validity_type=validity_type,
                                      bearer_token=bearer_token)
    rprint(f"[{lily}]Certificate[/{lily}] requested from certificate-service")

    certs = pkcs7.load_pem_pkcs7_certificates(cert_req.encode('ascii'))
    print_subject_chain(certs)

    for i, c in enumerate(certs):
        pem = c.public_bytes(encoding=serialization.Encoding.PEM) # Check
        print(pem.decode('utf8')) 


    return 0

    # convert to crt
    p7b2pem(p7b_path, pem_path)
    pem2crt(pem_path, crt_path)

    # Infos
    certificate_summary(crt_path)

    get_sap_root(root_ca)

    verify_certificate(root_ca, pem_path, crt_path)

    # Remove the unneeded files
    csr_path.unlink()
    p7b_path.unlink()

    rprint("\nFiles created:")
    rprint(Panel(f"[{sap_orange}][b]{key_path}[/b]\n[white]Certificate Key", expand=False))
    rprint(Panel(f"[{sap_orange}][b]{crt_path}[/b]\n[white]Certificate", expand=False))
    rprint(Panel(f"[{sap_orange}][b]{root_ca}[/b]\n[white]SAP Root Certificate", expand=False))
    

if __name__ == '__main__':
    main()