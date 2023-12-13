
import logging
import argparse
from pathlib import Path
import json

import yaml
import pandas as pd

from rich import print as rprint

try:
    import termprint as tp
    from dsapi import list_shares, list_schemas, list_schema_tables, \
                read_profile, table_metadata, read_data, read_cdf, table_version
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp
    from hdlshare.dsapi import list_shares, list_schemas, read_profile, \
                               list_schema_tables, table_metadata, read_data, read_cdf, table_version

logging.basicConfig(level=logging.INFO)
DEBUG = False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", help="Profile of delta sharing")
    parser.add_argument("action", choices=['list', 'download', 'download_changes', 'metadata'], help="Action")
    parser.add_argument('target', nargs='*', help="(optional) Target: <share> [<schema>] [<table>]].")
    parser.add_argument("-r", "--recursive", help="Sync files with hana", action="store_true")
    parser.add_argument("-d", "--directory", help="Directory to store data." )
    parser.add_argument("-m", "--meta", help="Download metadata as csn-file to edit before starting the replication.", action="store_true")
    parser.add_argument("-v", "--version", type=int, help="Start version")
    parser.add_argument("-e", "--end_version", type=int, help="Version end")
    parser.add_argument("-c", "--config", help="Config-file for HANA access (yaml with url, user, pwd, port)", default="config.yaml")
    args = parser.parse_args()

    profile = read_profile(args.profile)
    
    target = args.target if args.target else []

    # Cmd option PATH
    if args.directory:
        data_path = Path(args.directory)
        if not data_path.is_dir():
            data_path.mkdir()
    else:
        data_path = Path('.')

    match args.action:
        case 'list':
            match len(target):
                case 0: 
                    tree = list_shares(profile, debug=DEBUG)
                    if args.recursive:
                        tree = dict.fromkeys(tree,list())
                        for share in tree.keys():
                            tree[share] = dict.fromkeys(list_schemas(profile, share=share),list())
                            for schema in tree[share].keys():
                                tree[share][schema] = list_schema_tables(profile, share=share, schema=schema)
                    tp.print_tree(tree)
                case 1:
                    share = target[0]
                    tree = {share: list_schemas(profile, share=target[0])}
                    if args.recursive:
                        tree[share] = dict.fromkeys(tree[share],list())
                        for schema in tree[share].keys():
                            tree[share][schema] = list_schema_tables(profile, share=share, schema=schema)
                    tp.print_tree(tree)
                case 2:
                    tables = list_schema_tables(profile, share=target[0], schema=target[1])
                    tp.print_tree({target[0]:{target[1]:tables}})
        case 'metadata':
            if len(target) !=3:
                tp.error("Error: specify table by <share> <schema> <table> for metadata!")
            share, schema, table = args.target
            metadata = table_metadata(profile, share=share, schema=schema, table=table)
            if not metadata:
                return -1
            tp.print_share_metadata(table_path=f"{share}.{schema}.{table}", metadata=metadata)

        case 'download':
            if len(target) !=3:
                tp.error("Error: specify table by <share> <schema> <table> for download!")
            
            share, schema, table = args.target
            table_path = '.'.join(target)
            table_file = '_'.join(target)
            # filenames
            filename = data_path /  Path(table_file + '.csv')
            meta_filename = data_path /  Path(table_file + '.json')

            metadata, df = read_data(profile=profile, share=share, schema=schema, table=table, 
                                        start_version=args.version, end_version=args.end_version)
            tp.share_metadata(table_path=f"{share}.{schema}.{table}",metadata=metadata)     
            tp.dataframe(df,title="", max_rows=40)
            if not filename.is_file(): 
                tp.info("Save to new file", filename)
                df.to_csv(filename, index=False)
            else: 
                tp.info("Append to file",filename)
                df.to_csv(filename, mode='a', header=False, index=False)

            tp.info("Save metadata-file", meta_filename)
            with open(meta_filename, "w") as fp:
                json.dump(metadata, fp, indent=4)

        case 'download_changes':
            if len(target) !=3:
                tp.error("Error: specify table by <share> <schema> <table> for download!")
            
            share, schema, table = args.target
            table_file = '_'.join(target)
            # filenames
            filename = data_path /  Path(table_file + '.csv')
            meta_filename = data_path /  Path(table_file + '.json')
            
            if args.version == None:
                if meta_filename.is_file():
                    with open(meta_filename) as fp:
                        local_version = int(json.load(fp)['version']) + 1
                else:
                    local_version = 0
            else:
                local_version = args.version

            source_version = table_version(profile, share=share, schema=schema, table=table)
            if local_version >= source_version:
                tp.warning(f"No newer version available > {source_version}")
                return 0

            tp.info("Start version",local_version)

            resp = read_cdf(profile=profile, share=share, schema=schema, table=table, 
                                    start_version=local_version, end_version=args.end_version)
            if not resp:
                return -1
            else:
                 metadata, df = resp
            tp.print_share_metadata(table_path=f"{share}.{schema}.{table}",metadata=metadata)     
            tp.dataframe(df,title="", max_rows=40)
            if not filename.is_file(): 
                tp.info("Save to new file",filename)
                df.to_csv(filename, index=False)
            else: 
                tp.info("Append to file", filename)
                df.to_csv(filename, mode='a', header=False, index=False)

            rprint(f"Save metadata-file:[{tp.variable}]{meta_filename}")
            with open(meta_filename, "w") as fp:
                json.dump(metadata, fp, indent=4)


if __name__ == "__main__":
    main()