import requests
import argparse
import json
import re
from pathlib import Path

from rich import print as rprint
from rich.pretty import pprint 
from rich.table import Table
from rich.tree import Tree as rTree

try:
    import termprint as tp
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp

HDLFSCONFIGFILE = ".hdlfscli.config.json"


def dict2tree(tree: rTree, data, level=1) -> rTree:
    if isinstance(data, list):
        for i in data:
            tree.add(f"[{tp.treelevel[level]}]{i}[/]")
    elif isinstance(data, dict):
        for k, v in data.items():
            stree = tree.add(f"[{tp.treelevel[level]}]{k}[/]")
            dict2tree(stree, v, level+1)
    else:
        raise ValueError("Wrong format in dict!")
    
def print_tree(tree:dict)-> None:
    shares_tree = rTree(f"[{tp.treelevel[0]}]{'shares'}[/]")
    dict2tree(shares_tree, tree)
    rprint('\n',shares_tree, '\n')


def list_schemas(params, filter=None, omit_tables=False) -> dict:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v2/schemas"
    headers = {'x-sap-filecontainer': container}
    #ot = 'true' if omit_tables else 'false'
    # parameter = {'omitTables':omit_tables}
    # if filter:
    #     parameter['filter']=filter
    # r = requests.get(url, cert=(certificate, key), headers=headers, params=parameter)
    r = requests.get(url, cert=(certificate, key), headers=headers)

    if r.status_code != 200: 
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    return [s['name'] for s in json.loads(r.text)['schemas']]

def list_tables(share: str, schema: str, params) -> list:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v2/shares/{share}/schemas/{schema}/tables"
    headers = {'x-sap-filecontainer': container}
    r = requests.get(url, cert=(certificate, key), headers=headers)

    if r.status_code not in [200, 201]: 
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    return [t['name'] for t in json.loads(r.text)['tables']]

def add_schema(schema: str, description: str, params: dict) -> None:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v1/schemas"
    headers = {'x-sap-filecontainer': container, 'content-type': 'application/json'}
    data = json.dumps({"description": description, "required": True})
    r = requests.post(url, cert=(certificate, key), headers=headers, data=data)

    if r.status_code == 201:
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    rprint(f"Schema successfully created: [{tp.variable}]{schema}[/{tp.variable}]")

def get_schema(schema: str, params: dict, omit_tables=False) -> list:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v1/schemas/{schema}"
    headers = {'x-sap-filecontainer': container}
    ot = 'true' if omit_tables else 'false'
    parameter = {'omitTables':ot}
    r = requests.get(url, cert=(certificate, key), headers=headers, params=parameter)

    if r.status_code != 200: 
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    return json.loads(r.text)

def add_table(share: str, schema: str, table: str, hdl_path: str, cdf: bool, params) -> None:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v2/shares/{share}/schemas/{schema}/tables/{table}"
    headers = {'x-sap-filecontainer': container, 'content-type': 'application/json' }
    data = json.dumps({"name": table, "location": hdl_path, "cdfEnabled": cdf})
    r = requests.put(url, cert=(certificate, key), headers=headers, data=data)

    if r.status_code not in [200, 201]:
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    rprint(f"Table successfully added: [{tp.variable}]{share}: {schema}.{table}")

def delete_share(share: str, drop_cascade: bool, params) -> None:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v2/shares/{share}"
    headers = {'x-sap-filecontainer': container}
    params = {'dropCascade': 'true' if drop_cascade else 'false'}
    r = requests.delete(url, cert=(certificate, key), headers=headers, params=params)

    if r.status_code != 200:
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    rprint(f"Share successfully deleted: [{tp.variable}]{share}[/{tp.variable}]")

def delete_table(share: str, schema: str, table: str, params) -> None:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v2/shares/{share}/schemas/{schema}/tables/{table}"
    headers = {'x-sap-filecontainer': container }
    r = requests.delete(url, cert=(certificate, key), headers=headers)

    if r.status_code  != 200:
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    rprint(f"Table successfully deleted: [{tp.variable}]{share}: {schema}.{table}")

def get_table(share: str, schema: str, table: str, params) -> list:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v2/shares/{share}/schemas/{schema}/tables/{table}"
    headers = {'x-sap-filecontainer': container}
    r = requests.get(url, cert=(certificate, key), headers=headers)

    if r.status_code != 200: 
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    return json.loads(r.text)


## CATALOG
def get_versions(params: dict) -> list:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/versions"
    headers = {'x-sap-filecontainer': container}
    r = requests.get(url, cert=(certificate, key), headers=headers)

    if r.status_code != 200: 
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    
    # return [s['name'] for s in json.loads(r.text)['shares']]
    return json.loads(r.text)['versions']

def get_server_info(params: dict) -> list:
    endpoint = params['endpoint']
    certificate = params['cert']
    key = params['key']
    container = re.match(r".+\/\/([^.]+)", endpoint).group(1)
    url = endpoint.replace('hdlfs://', 'https://') + f"/catalog/v1/serverinfo"
    headers = {'x-sap-filecontainer': container}
    r = requests.get(url, cert=(certificate, key), headers=headers)

    if r.status_code != 200: 
        raise ValueError(f"Unsuccessful API-call - Status code: {r.status_code} - {r.text}")
    
    # return [s['name'] for s in json.loads(r.text)['shares']]
    return json.loads(r.text)


def main():

    parser = argparse.ArgumentParser("Manage HDLFS shares")
    parser.add_argument("action", choices=['versions','server_info','list', 'add', 'delete', 'get'], help=f"Command for \'target\'-argument")
    parser.add_argument("target", nargs="*", help="share schema table (optional)")
    parser.add_argument("-r", "--recursive", help="List recursively", action="store_true")
    parser.add_argument("-m", "--metadata", help="Show metadata of table (action=list)", action="store_true")
    parser.add_argument("-C", "--cascade", help="Drop cascade when deleting share (action=delete)", action="store_true")
    parser.add_argument("-p", "--path", help="HDLFS data folder")
    parser.add_argument("-c", "--config", help=f"HDLFs config in \'{HDLFSCONFIGFILE}\'", default ='default')
    

    args = parser.parse_args()

    with open(Path.home() / HDLFSCONFIGFILE  ) as fp:
        hdlfs_params = json.load(fp)["configs"][args.config]

    hdl_path = args.path if args.path else None

    target = args.target
    cascade = args.cascade

    match args.action:
        case  'versions':
            versions = get_versions(hdlfs_params)
            tp.listdicts(versions)
 
        case 'server_info':
            server_info = get_server_info(hdlfs_params)
            print(server_info)
            tp.info('Server info version',server_info['version'])

        case 'list':
            tree = None
            match len(target):
                case 0:
                    schemas = list_schemas(hdlfs_params,omit_tables=False)
                    print(schemas)
                case 1:
                    pass

                case 2:
                    share, schema = target 
                    tree = {share: {schema: list_tables(share, schema, hdlfs_params)}}
                    if args.metadata:
                        tree[share][schema] = dict.fromkeys(tree[share][schema],list())
                        for table in tree[share][schema].keys():
                            metadata = get_table(share, schema, table, hdlfs_params)
                            tree[share][schema][table] = [metadata['location'], metadata['type'],
                                                            'cdf: '+ str(metadata['cdfEnabled'])]
                case _:
                    rprint(f"[{tp.cerror}]Only 2 parameters (share, schema) expected for argument list")
                    return -1 
            # print_tree(tree)


        case  'add':
            match len(target):
                case 0:
                    rprint(f"[{tp.cwarn}]No target given: share, ((schema), (table))")
                case 1: 
                    add_schema(target[0], target[0], hdlfs_params)
                case 2: 
                    rprint(f"[{tp.cwarn}]Only adding share or adding share, schema and table are implemented")
                case 3:
                    add_table(share=target[0], schema=target[1], table=target[2], hdl_path=hdl_path, cdf=cdf, 
                            params=hdlfs_params)


        case 'delete':
            match len(target):    
                case 0:
                    rprint(f"[{tp.cwarn}]No target given: share or share-schema-table")
                case 1: 
                    delete_share(target[0], cascade, hdlfs_params)
                case 2: 
                    rprint(f"[{tp.cwarn}]Only shares or share-schema-tables can be deleted")
                case 3:
                    delete_table(share=target[0], schema=target[1], table=target[2], params=hdlfs_params)

        case 'get':
            match len(target):
                case 0:
                    tp.error("No schema given")
                case 1:
                    schema = get_schema(params=hdlfs_params, schema=target[0])
                    print(schema)
        

if __name__ == '__main__':
    main()