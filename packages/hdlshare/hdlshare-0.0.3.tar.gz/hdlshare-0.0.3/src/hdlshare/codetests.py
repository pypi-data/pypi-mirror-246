from datetime import datetime
import json
from rich import print as rprint
from pathlib import Path

startv = "4"
endv = "6"

startt = "2023-04-01 05:00:30.001000"
endt = "2023-04-02 05:03:30.001000"

def change_params(start: str, end: str) -> int:
    try:
        a = int(start)
        b = int(end)
        return {"starting_version": a, "ending_version":b}
    except ValueError as ae:
        a = datetime.fromisoformat(start)
        b = datetime.fromisoformat(end)
        return {"starting_timestamp": a, "ending_timestamp":b}

# print(change_params(start = startv, end = endv))
# print(change_params(start = startt, end = endt))

# c = iter([0,1,2,3,4,5,6,7,8,9])
# for i in c:
#     j = next(c)
#     print(f"{i} {j}")

# testlist1 = {"a": 1, "b":2, "c":3}
# testlist2 = {"d": 4, "e":5, "f":6}

# elem = 'f'
# match elem:
#     case _ if elem in testlist1:
#         print(f"{elem} in testlist1: {testlist1[elem]}")
#     case _ if elem in testlist2:
#         print(f"{elem} in testlist2: {testlist2[elem]}")
#     case _:
#         print(f"{elem} not in any list")

SPLITTING = False
if SPLITTING:
    param = 'share'
    params = param.split('.')
    match len(params):
        case 1:
            share = params[0]
            print(f"share: {share}")
        case 2: 
            share, schema = params
            print(f"share: {share}, schema: {schema}")
        case 3: 
            share, schema, table = params
            print(f"share: {share}, schema: {schema},  table: {table}")

DECORATORS = False
if DECORATORS:
    def ds_api(method: str, operation: str) -> dict:
        def inner_api(func):
            def call_api(b):
                params, result_gen = func(b)

                print(f"Parameters: {params}")
                return result_gen(params)
            return call_api
        return inner_api
            
    @ds_api("getshares", "listshares")
    def evenodd(a: int):
        def result_gen(b):
            if b%2==0:
                return f"Even number: {b}"
            else:
                return f"Odd number: {b}"
        return a, result_gen 

    print(evenodd(3))

COMPARE_SCHEMAS = False
if COMPARE_SCHEMAS:
    with open("data2/schema1.json") as j1:
        schema1 = json.load(j1,)
    with open("data2/schema2.json") as j2:
        schema2 = json.load(j2)
    
    # test if new keys
    def compare_schemas(s1:dict, s2: dict) -> dict:
        new_columns = {c2:s2[c2] for c2 in s2 if c2 not in s1}
        changed_types = {c2:s2[c2] for c2 in s2.keys() if c2 not in new_columns and s2[c2]['type'] != s1[c2]['type']}
        if len(new_columns) == 0  and len(changed_types) == 0:
            return None
        return {'new_columns': new_columns, 'changed_types': changed_types} 
    
    if changes := compare_schemas(schema1, schema1):
        print(json.dumps(changes, indent=4))

RICH = False
if RICH:
    from rich.table import Table
    subject='subject=C = DE, O = SAP SE, OU = SAP Cloud Platform Clients, OU = 22dcd6a6-566a-40f5-8151-6ff91b52251a, L = Walldorf BW, CN = hdlfsdsXPM'
    subs = subject[8:].split(',')
    subs = { s.split('=')[0].strip():s.split('=')[1].strip()  for s in subs}
    table = Table(title="Subjects")
    table.add_column("Field", justify="left", style="magenta")
    table.add_column("Value", justify="left", style="cyan", no_wrap=True)
    for n,v in subs.items():
        table.add_row(n, v)
    rprint(table)


RICH = False
if RICH:
    from rich.columns import Columns
    from rich.panel import Panel

    sap_orange = "rgb(238,171,48)"
    panels = [Panel(f"[rgb(175,0,255)][b]Hallo1 [/b]\n[white]next", expand=True),
                Panel(f"[cyan][b]Hallo 2[/b]\n[white]next", expand=False),
                Panel(f"[cyan][b]Hallo 3[/b]\n[white]next", expand=True)]

    rprint(Columns(panels))

    rprint(Panel(f"[{sap_orange}][b]Hallo 1 [/b]\n[white]next", expand=False))
    rprint(Panel(f"[darkgrey][b]Hallo 2 [/b]\n[white]next", expand=True))

CRYPTO = False
if CRYPTO:
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography import x509
    from cryptography.x509.oid import NameOID


    def private_key(file: Path) :
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        with open(file, "wb") as f:
            f.write(key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                #format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
            ))

    key = private_key(Path("pkeyPKCS8.pem"))

    # csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
    #             # Provide various details about who we are.
    #             x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    #             x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
    #             x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
    #             x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
    #             x509.NameAttribute(NameOID.COMMON_NAME, u"mysite.com")])).sign(key, hashes.SHA256())
    # # Write our CSR out to disk.
    # with open("path/to/csr.pem", "wb") as f:
    #     f.write(csr.public_bytes(serialization.Encoding.PEM))


# for i in range(1,10,2):
#     print(f"{i-1} - {i}")
    
    # def compare_schemas(s1: dict, s2: dict) -> int:
    #     for col in s2:
    #         if col not in s1

    # res = compare_schemas(schema1, schema2)

SPLIT_SUBJECT = False
if SPLIT_SUBJECT:
    subject = "C=DE, O=SAP SE, OU=SAP Cloud Platform Clients, OU=22dcd6a6-566a-40f5-8151-6ff91b52251a, L=%s, CN=%s"
    k = [ (s.split('=')[0].strip(), s.split('=')[1].strip()) for s in subject.split(",")]
    print(k)

TEST_HDLFSCONFIGFILE = False
if TEST_HDLFSCONFIGFILE:
    HDLFSCONFIGFILE = ".hdlfscli.config.json"
    config_file = Path.home() / HDLFSCONFIGFILE
    with open(config_file) as fp:
        params = json.load(fp)
    print(params)

    profile = Path('profiles/admin')
    print(profile.suffix)
    if not profile.suffix:
        profile = profile.parent / (profile.name +  '.json')
    print(profile)
    if profile.is_file():
        print("jep")
    elif (Path("profiles") / profile).is_file():
        print("jepjep")


h = "hello"
print(h.encode('ascii'))