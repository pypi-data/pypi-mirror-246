
import json
import re
import argparse
from pathlib import Path

import requests
from urllib.error import HTTPError
import pandas as pd
import fsspec
from pyarrow.dataset import dataset
from rich import print as rprint
from rich.table import Table


try:
    import termprint as tp
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp

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

def get_source(source: str):
    params = source.split('.')
    match len(params):
        case 1:
            return params[0], None, None
        case 2: 
            return params[0], params[1], None
        case 3: 
            return params[0], params[1], params[2]

def download_file(url: str) -> pd.DataFrame:
    pa_dataset = dataset(source=url, format="parquet", filesystem=fsspec.filesystem("http"))
    return pa_dataset.to_table().to_pandas(date_as_object=True, use_threads=False, 
                                           split_blocks=True, self_destruct=True)


def format_metadata(metadata: dict) -> dict:
    metadata['schema'] = json.loads(metadata['schemaString'])['fields']
    metadata['schema'] = { c['name']: c for c in metadata['schema']}
    metadata.pop('schemaString')
    return metadata

def last_version(metadata: dict) -> int:
    return max([ m['version'] for m in metadata])


def compare_schemas(s1:dict, s2: dict) -> dict:
    new_columns = {c2:s2[c2] for c2 in s2 if c2 not in s1}
    changed_types = {c2:s2[c2] for c2 in s2.keys() if c2 not in new_columns and s2[c2]['type'] != s1[c2]['type']}
    if len(new_columns) == 0  and len(changed_types) == 0:
        return None
    return {'new_columns': new_columns, 'changed_types': changed_types}
    
def print_request_info(method, endpoint, path, headers, params):
    table = Table(title="Request Info", header_style=tp.header_style, title_style=tp.title_style,
                  expand=True)
    table.add_column("Key", justify="left", style=tp.cinfo)
    table.add_column("Value", justify="left", style=tp.cinfo,overflow="fold")
    table.add_row("method", method)
    table.add_row("endpoint", endpoint)
    table.add_row("resource path", path)
    for k, v in headers.items():
        if k == 'Authorization':
            v = v[: 50] + '...'
        table.add_row(k,str(v))
    table.add_section()
    for k, v in params.items():
        table.add_row(k,str(v))
    rprint(table, '\n')


def ds_api(method: str) -> dict:
    """
    DECORATOR for all API-calls
    :param method: HTTP-method [get, put, ..]
    :param operation: RESTAPI name
    :return: response of Rest API
    """
    def inner_api(func):
        def call_api(profile, format=True, verify=True, debug=False, **kwargs):
            if not 'bearerToken' in profile and not 'cert' in profile:
                raise ValueError("Profile needs either \'bearerToken\' or \'cert/key\' for authentication!")

            if 'hanacloud.ondemand.com' in profile['endpoint']:
                container = re.match(r".+\/\/([^.]+)", profile['endpoint']).group(1)
                headers = {"x-sap-filecontainer": container}
            else:
                headers = {}

            updated, response_func, format_func = func(profile, **kwargs)

            if 'path' in updated and len(updated['path']) > 0 and updated['path'][0] =='/':
                updated['path'] = updated['path'][1:]
            resource_path = updated.pop('path', '')
            endpoint = profile['endpoint'] + '/' +str(resource_path)
            
            if 'headers' in updated:
                headers = headers | updated['headers']
            params = updated['params'] if 'params' in updated else {}
            data = json.dumps(updated['data'] if 'data' in updated else {}) if 'data' in updated else ""

            if 'bearerToken' in profile:
                headers['Authorization'] =  'Bearer '+ profile['bearerToken']
                r = requests.request(method, endpoint, headers=headers, params=params, data=data, verify=verify)
            else: 
                r = requests.request(method, endpoint, headers=headers, params=params, data=data, 
                                     cert=(profile['cert'],profile['key']), verify=verify)
            
            match r.status_code:
                case 401:
                    tp.error(f"{r.status_code} Remote Exception")
                    print(str(r.content))
                    return None
                case 403:
                    rprint(f"[{tp.cerror}]{r.status_code} User has not enough privileges.")
                    return None
                case 404:
                    rprint(f"[{tp.cerror}]{r.status_code} Requested resource does not extist: \n")
                    print_request_info(method=method, endpoint=profile['endpoint'],
                                       path=resource_path, headers=headers, params=params)
  
                    return None
                case 400:
                    rprint(f"[{tp.cerror}]Malformed request. Error code: {r.status_code}\n")
                    rprint(f"[{tp.cerror}]{r.text}")
                    print_request_info(method=method, endpoint=profile['endpoint'],
                                       path=resource_path, headers=headers, params=params)
                    return None
                case 200:
                    if debug:
                        print_request_info(method=method, endpoint=profile['endpoint'],
                                       path=resource_path, headers=headers, params=params)
                    if format:
                        return format_func(r)
                    else: 
                        return response_func(r)

        return call_api
    return inner_api


@ds_api(method='get')
def list_shares(profile: dict, format=True, max_results=None, next_page_token=None,
                 verify=True, debug=False) -> dict:
    """
    Lists all shares
    :param profile: delta sharing profile for endpoint and bearer token
    :maxResults: Max number of results per page
    :nextPageToken: Specifies a page token to use
    :param verify: Enables/ disables server verification
    :return: response
    """
    def response_func(resp: requests.Response):
        if not resp:
            return {}   
        return json.loads(resp.text)
            
    
    def format_func(resp: requests.Response):
        # result = json.loads(resp.text)
        return [s['name'] for s in json.loads(resp.text)['items']]

    params = {'path': 'shares', 'params': {}, 'data':{}}
    if max_results:
        params['params']['maxResults'] = max_results
    if next_page_token:
        params['params']['nextPageToken'] = next_page_token
    
    return params, response_func, format_func


@ds_api(method='get')
def get_share(profile: dict, share: str, verify=True) -> dict:
    """
    Get id of share
    :param profile: delta sharing profile for endpoint and bearer token
    :param share: Share for id
    :param verify: Enables/ disables server verification
    :return: response
    """
    def response_func(resp: requests.Response):
        if not resp:
            return {}   
        return json.loads(resp.text)
    
    def format_func(resp: requests.Response):
        return json.loads(resp.text)

    params = {'path': 'shares/'+share, 'params': {}}
    
    return params, response_func, format_func


@ds_api(method='get')
def list_schemas(profile: dict, share: str, max_results=None, next_page_token=None, verify=True) -> dict:
    """
    Lists all schemas in a share
    :param profile: delta sharing profile for endpoint and bearer token
    :param share: Share of schemas
    :param verify: Enables/ disables server verification
    :return: response
    """
    def response_func(resp: requests.Response):
        if not resp:
            return {}   
        return json.loads(resp.text)
    
    def format_func(resp: requests.Response):
        return [s['name'] for s in json.loads(resp.text)['items']]
    
    params = {'path': 'shares/'+share+'/schemas', 'params': {}}
    if max_results:
        params['params']['maxResults'] = max_results
    if next_page_token:
        params['params']['nextPageToken'] = next_page_token
    
    return params, response_func, format_func


@ds_api(method='get')
def list_schema_tables(profile: dict, share: str, schema: str, max_results=None, next_page_token=None, verify=True) -> dict:
    """
    List all tables in a schema
    :param profile: delta sharing profile for endpoint and bearer token
    :param share: Share of schema
    :param schema: Schema of tables
    :param verify: Enables/ disables server verification
    :return: response
    """
    def response_func(resp: requests.Response):
        if not resp:
            return {}   
        return json.loads(resp.text)
    
    def format_func(resp: requests.Response):
        return [table['name']for table in json.loads(resp.text)['items']]
    
    params = {'path': 'shares/'+share+'/schemas/'+schema+'/tables', 'params': {}, 'data':{}}
    if max_results:
        params['params']['maxResults'] = max_results
    if next_page_token:
        params['params']['nextPageToken'] = next_page_token
    
    return params, response_func, format_func


@ds_api(method='get')
def list_all_tables(profile: dict, share: str, max_results=None, next_page_token=None, verify=True) -> dict:
    """
    Lists all tables in a share
    :param profile: delta sharing profile for endpoint and bearer token
    :param share: Share of all tables
    :param verify: Enables/ disables server verification
    :return: response
    """
    def response_func(resp: requests.Response):
        if not resp:
            return {}   
        return json.loads(resp.text)
    
    def format_func(resp: requests.Response):
        return [f"{table['share']}.{table['schema']}.{table['name']}" for table in json.loads(resp.text)['items']]
    
    params = {'path': 'shares/'+share+'/all-tables', 'params': {}, 'data':{}}
    if max_results:
        params['params']['maxResults'] = max_results
    if next_page_token:
        params['params']['nextPageToken'] = next_page_token
    
    return params, response_func, format_func


@ds_api(method='get')
def table_version(profile: dict, share: str, schema: str, table: str, 
                        starting_timestamp=None, verify=True) -> dict:
    """
    Query table version
    :param profile: delta sharing profile for endpoint and bearer token
    :param share: Share of table
    :param schema: Schema of table
    :param table: table name
    :param verify: Enables/ disables server verification
    :return: response
    """
    def response_func(resp: requests.Response) -> int:
        if not resp:
            return -1
        return int(resp.headers['delta-table-version'])

        
    
    def format_func(resp: requests.Response) -> int:
        return  int(resp.headers['delta-table-version'])
    
    params = {'path': 'shares/'+share+'/schemas/'+schema+'/tables/'+table+'/version',
                'params': {}, 'data':{}}
    
    if starting_timestamp:
        params['params']['startingTimestamp'] = starting_timestamp

    return params, response_func, format_func


@ds_api(method='get')
def table_metadata(profile: dict, share: str, schema: str, table: str, 
                         version=None, verify=True) -> dict:
    """
    Query table version
    :param profile: delta sharing profile for endpoint and bearer token
    :param share: Share of table
    :param schema: Schema of table
    :param table: table name
    :param version: table version
    :param verify: Enables/ disables server verification
    :return: response
    """
    def response_func(resp: requests.Response):
        if not resp:
            return {}
        metadata = {"version": resp.headers['delta-table-version']}
        lines = resp.text.split('\n')
        for line in lines:
            if not line:
                continue
            line = json.loads(line) 
            if "protocol" in line:
                metadata["protocol"] = line['protocol']
            elif 'metaData' in line:
                metadata.update(format_metadata(line['metaData']))
            else: 
                rprint(f"[{tp.cwarn}]Warning: unknown data: {line}")
        return metadata
    
    def format_func(resp: requests.Response):
        metadata = {"version": resp.headers['delta-table-version']}
        lines = resp.text.split('\n')
        for line in lines:
            if not line:
                continue
            line = json.loads(line) 
            if 'metaData' in line:
                metadata.update(format_metadata(line['metaData']))
        return metadata['metadata']
    
    params = {'path': 'shares/'+share+'/schemas/'+schema+'/tables/'+table+'/metadata',
              'headers': {'Delta-Table-Version': version}}
    
    return params, response_func, response_func


@ds_api(method='post')
def read_data(profile: dict, share: str, schema: str, table: str, 
              start_version=None, end_version=None, limit=None,
              predictateHints=None, jsonPredicateHints=None, verify=True) -> dict:
    """
    Query table version
    :param profile: delta sharing profile for endpoint and bearer token
    :param share: Share of table
    :param schema: Schema of table
    :param table: table name
    :param verify: Enables/ disables server verification
    :return: response
    """
    data = {}
    if start_version: data['startingVersion'] =  start_version
    if end_version: data['enndingVersion'] =  end_version
    if limit: data['limitHint'] = limit
    if predictateHints: data['predictateHints'] = predictateHints
    if jsonPredicateHints: data['jsonPredicateHints'] = jsonPredicateHints
    params = {'path': f"shares/{share}/schemas/{schema}/tables/{table}/query",
              'headers': {'Content-Type': 'application/json; charset=utf-8'},
              'data':data}
    
    def response_func(resp: requests.Response):
        if not resp:
            return {}
        lines = resp.text.split('\n')
        df_list = list()
        metadata =  {"version":resp.headers['delta-table-version'],
                     'timestamp':resp.headers['date'],'adds':[],'files':[]}
        for line in lines:
            if not line:
                continue
            line = json.loads(line) 
            if "protocol" in line:
                metadata["protocol"] = line['protocol']
            elif 'metaData' in line:
                metadata.update(format_metadata(line['metaData']))
            elif 'file' in line:
                line['file']['stats'] = json.loads(line['file']['stats']) 
                df = download_file(line['file']['url'])
                line['file'].pop('url')
                line['file'].pop('expirationTimestamp')
                metadata['files'].append(line)
                if '_change_type' in df.columns:
                    df.drop(columns=['_change_type'],inplace=True)
                df_list.append(df)
            else:
                rprint(f"[{tp.cwarn}]Warning: Uncovered data line: {line}")
        return metadata, pd.concat(df_list)
    
    def format_func(resp: requests.Response):
        lines = resp.text.split('\n')
        df_list = list()
        metadata =  {"version":resp.headers['delta-table-version']}
        for line in lines:
            if not line:
                continue
            line = json.loads(line) 
            if 'metaData' in line:
                metadata.update(format_metadata(line['metaData']))
            elif 'file' in line:
                df = download_file(line['file']['url'])
                if '_change_type' in df.columns:
                    df.drop(columns=['_change_type'],inplace=True)
                df_list.append(df)
        return metadata, pd.concat(df_list)

    return params, response_func, format_func


@ds_api(method='get')
def read_cdf(profile: dict, share: str, schema: str, table: str, start_version: int,
             end_version=None, start_time=None, end_time=None, incl_hm = True, verify=True) -> dict:
    """
    Query table version
    :param profile: delta sharing profile for endpoint and bearer token
    :param share: Share of table
    :param schema: Schema of table
    :param table: table name
    :param verify: Enables/ disables server verification
    :return: response
    """
    def response_func(resp: requests.Response):
        if not resp:
            return None, None
        lines = resp.text.split('\n')
        df_list = list()
        cdfdata =  {"version":resp.headers['delta-table-version'],
                    'metadata': [], 'add':[],'remove':[], 'cdf': []}
        for line in lines:
            if not line:
                continue
            line = json.loads(line) 
            if "protocol" in line:
                cdfdata["protocol"] = line['protocol']
            elif 'metaData' in line:
                cdfdata["metadata"].append(format_metadata(line['metaData']))
            elif 'cdf' in line:
                df = download_file(line['cdf']['url'])
                df['_commit_version'] = line['cdf']['version']
                df['_commit_timestamp'] = line['cdf']['timestamp']
                df_list.append(df)
                cdfdata["cdf"].append({"version": line['cdf']['version'], 
                                          "timestamp": line['cdf']['timestamp'],
                                          "size":line['cdf']['size']})
            elif 'remove' in line:
                df = download_file(line['remove']['url'])
                df['_change_type'] = 'delete'
                df['_commit_version'] = line['remove']['version']
                df['_commit_timestamp'] = line['remove']['timestamp']
                df_list.append(df)
                cdfdata["remove"].append({"version": line['remove']['version'], 
                                          "timestamp": line['remove']['timestamp'],
                                          "size":line['remove']['size']})
            elif 'add' in line:
                df = download_file(line['add']['url'])
                df['_change_type'] = 'insert'
                df['_commit_version'] = line['add']['version']
                df['_commit_timestamp'] = line['add']['timestamp']
                df_list.append(df)
                cdfdata["add"].append({"version": line['add']['version'], 
                                       "timestamp": line['add']['timestamp'],
                                       "size":line['add']['size']})
            else:
                rprint(f"[{tp.cerror}]Warning: Uncovered data line: {line}")
        cdfdata['metadata'] = sorted(cdfdata['metadata'], key=lambda d: d['version']) 
        for i in range(1,len(cdfdata['metadata']),2):
            if cs:= compare_schemas(cdfdata['metadata'][i-1]['schema'],cdfdata['metadata'][i]['schema']):
                cdfdata['metadata'][i]['changed_schema'] = cs
                rprint(f"Schema change:[{tp.cerror}] {cdfdata['metadata'][i-1]['version']} "\
                      f"-> {cdfdata['metadata'][i]['version']}")
        cdfdata['last_schema_version'] = max([m['version'] for m in cdfdata['metadata']])
        return cdfdata, pd.concat(df_list)
    
    def format_func(resp: requests.Response):
        lines = resp.text.split('\n')
        df_list = list()
        cdfdata =  {"version_starting":resp.headers['delta-table-version'],
                    'metadata': []}
        for line in lines:
            if not line:
                continue
            line = json.loads(line) 
            if 'metaData' in line:
                cdfdata["metadata"].append(format_metadata(line['metaData']))
            elif 'cdf' in line:
                df = download_file(line['cdf']['url'])
                df['_commit_version'] = line['cdf']['version']
                df['_commit_timestamp'] = line['cdf']['timestamp']
                df_list.append(df)
            elif 'remove' in line:
                df = download_file(line['remove']['url'])
                df['_change_type'] = 'delete'
                df['_commit_version'] = line['remove']['version']
                df['_commit_timestamp'] = line['remove']['timestamp']
                df_list.append(df)
            elif 'add' in line:
                df = download_file(line['add']['url'])
                df['_change_type'] = 'insert'
                df['_commit_version'] = line['add']['version']
                df['_commit_timestamp'] = line['add']['timestamp']
                df_list.append(df)

        cdfdata['metadata'] = sorted(cdfdata['metadata'], key=lambda d: d['version']) 
        for i in range(1,len(cdfdata['metadata']),2):
            if cs:= compare_schemas(cdfdata['metadata'][i-1]['schema'],cdfdata['metadata'][i]['schema']):
                cdfdata['metadata'][i]['changed_schema'] = cs
                print(f"Schema change:[{tp.cerror}] {cdfdata['metadata'][i-1]['version']} "\
                      f"-> {cdfdata['metadata'][i]['version']}")
        cdfdata['last_schema_version'] = max([m['version'] for m in cdfdata['metadata']])
        
        return cdfdata, pd.concat(df_list)
    
    
    params = {'path': f"shares/{share}/schemas/{schema}/tables/{table}/changes", 
              'params': {'includeHistoricalMetadata': incl_hm}}
    
    params['params']['startingVersion'] = start_version
    if end_version:   params['params']['endingVersion'] = end_version
    if start_time:    params['params']['startingTimestamp'] = start_time
    if end_time:      params['params']['endingTimestamp'] = end_time
    
    return params, response_func, format_func


def main():
    api_choices = ['shares', 'schemas','schematables', 'getshare', 
                   'alltables', 'version', 'metadata',
                    'readdata', 'readcdf']
    parser = argparse.ArgumentParser("Calls Delta Sharing APIs")
    parser.add_argument("profile", help="Profile of delta sharing.")
    parser.add_argument('api', help="Delta Sharing API.", choices=api_choices)
    parser.add_argument('source', nargs='?', help="Source: table=<share>.<schema>.<table>, schema=<share>.<schema> or share: <share>")
    parser.add_argument('-v', '--version', type=int, help="Start version for readdata or readcdf", default=None)
    parser.add_argument('-p', '--path', help="Output path")
    parser.add_argument('-l', '--limit', type=int, help="Data download limit of records", default=None)
    
    args = parser.parse_args()
    api_call = args.api
    if args.source: 
        share, schema, table = get_source(args.source)
    version = args.version
    limit = args.limit
    path = Path(args.path) if args.path else Path('.')

    print(f"Read profile: {args.profile}")
    profile = read_profile(args.profile)

    match api_call:
        case 'shares':
            shares = list_shares(profile)
            print("List shares:")
            for share in shares :
                print(f"Shares: [{tp.variable}]{share}")
        case 'getshare':
            share_detail = get_share(profile, share=share)
            print(f"Share: [{tp.variable}]{share_detail['share']['name']} ({share_detail['share']['id']})") 
        case 'schemas':
            schemas = list_schemas(profile, share=share)
            print(f"Schemas of share [{tp.variable}]{share}:")
            for schema in schemas:
                print(f"- [{tp.variable}]{schema}")  
        case 'schematables':           
            tables = list_schema_tables(profile, share=share, schema=schema)
            print(f"Tables of schema [{tp.variable}]{share}.{schema}:")  
            for table in tables:
                print(f"- [{tp.variable}]{table}") 
        case 'alltables':
            tables = list_all_tables(profile, share=share)
            print(f"All tables of share [{tp.variable}]{share}:") 
            for table in tables:
                print(f"- [{tp.variable}]{table}")  
        case 'version':
            version = table_version(profile, share=share, schema=schema, table=table)
            print(f"Table version: [{tp.variable}]{version}")  
        case 'metadata':
            metadata = table_metadata(profile, share=share, schema=schema, table=table)
            print(f"Metadata of [{tp.variable}]{share}.{schema}.{table}: ")
            print(f"[{tp.variable}]{json.dumps(metadata, indent=4)}")
            with open(path / f"{share}_{schema}_{table}.json", "w") as jp:
                json.dump(metadata,jp, indent=4)
        case 'readdata':
            metadata, df = read_data(profile, share=share, schema=schema, table=table, version=version,
                                    limit=limit)
            print(f"Data [{tp.variable}]{share}.{schema}.{table}: ")
            print(f"Version:[{tp.variable}] {metadata['version']}")
            print(f"Data:[{tp.variable}]")
            print(df.tail(10))
            print(f"Number of rows: [{tp.variable}]{df.shape[0]}")
        case 'readcdf':
            cdfdata, df = read_cdf(profile, share=share, schema=schema, table=table,
                                   start_version=version,  incl_hm = True)
            print(f"Data [{tp.variable}]{share}.{schema}.{table}: ")
            if 'version' in cdfdata:
                print(f"Versions: [{tp.variable}]{cdfdata['version']} -> {cdfdata['version_ending']}")
            print(f"First data:[{tp.variable}]")
            print(df.head(10))
            print(f"Last data:[{tp.variable}]")
            print(df.tail(10))
            csv_filename = Path(f"{share}_{schema}_{table}.csv")
            json_filename = Path(f"{share}_{schema}_{table}.json")
            df.to_csv(path / csv_filename, index=False)
            with open(path / json_filename, "w") as jp:
                json.dump(cdfdata,jp, indent=4)


if __name__ == "__main__":
    main()