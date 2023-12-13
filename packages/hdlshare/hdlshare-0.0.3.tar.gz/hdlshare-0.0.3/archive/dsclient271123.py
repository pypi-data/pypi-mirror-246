
import logging
import argparse
from pathlib import Path
import json

import yaml
import pandas as pd

from rich import print as rprint
from rich.table import Table
from rich.padding import Padding

DEBUG = False

try:
    from pycsn import PyCSN
    from dsapi import list_all_tables, list_shares, list_schemas, list_schema_tables, \
                    read_profile, table_metadata, read_data, read_cdf
    from to_hana import table_exists, schema_exists, create_schema, execute_sql, upload, insert, \
                        delete, update, insert_batch, truncate
    import sapcolors as tp
except (ModuleNotFoundError, ImportError):
    from hdlshare.pycsn import PyCSN
    from hdlshare.dsapi import list_all_tables, list_shares, list_schemas, read_profile, \
                               list_schema_tables, table_metadata, read_data, read_cdf
    from hdlshare.to_hana import table_exists, schema_exists, create_schema, execute_sql, upload, insert, \
                        delete, update, insert_batch, truncate
    import hdlshare.termprint as tp


logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", help="Profile of delta sharing")
    parser.add_argument("action", choices=['list', 'download', 'metadata'], help="Action")
    parser.add_argument('target', nargs='*', help="(optional) Target: <share> [<schema>] [<table>]].")
    parser.add_argument("-r", "--recursive", help="Sync files with hana", action="store_true")
    parser.add_argument("-p", "--path", help="Directory to store data." )
    parser.add_argument("-m", "--meta", help="Download metadata as csn-file to edit before starting the replication.", action="store_true")
    parser.add_argument("-v", "--version", type=int, help="Start version (Warning: overruled by metadata stored version)")
    parser.add_argument("-e", "--end_version", type=int, help="Version end", default=None)
    parser.add_argument("-c", "--config", help="Config-file for HANA access (yaml with url, user, pwd, port)", default="config.yaml")
    parser.add_argument("-H", "--Hana", help="Upload to hana", action="store_true")
    parser.add_argument("-s", "--sync", help="Sync files with hana", action="store_true")
    args = parser.parse_args()

    profile = read_profile(args.profile)
    
    target = args.target if args.target else []

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
                rprint(f"[{tp.cerror}]Error: specify table by <share> <schema> <table> for metadata!")
            share, schema, table = args.target
            metadata = table_metadata(profile, share=share, schema=schema, table=table)
            if not metadata:
                return -1
            tp.print_share_metadata(table_path=f"{share}.{schema}.{table}", metadata=metadata)
        case 'download':
            if len(target) !=3:
                rprint(f"[{tp.cerror}]Error: specify table by <share> <schema> <table> for download!")
            
            share, schema, table = args.target
            table_path = '.'.join(target)
            table_file = '_'.join(target)

            # Cmd option PATH
            if args.path:
                data_path = Path(args.path)
                if not data_path.is_dir():
                    data_path.mkdir()
            else:
                data_path = Path('.')

            # filenames
            csn_filename = data_path /  Path(table_file + '.csn')
            init_filename = data_path /  Path(table_file + '.csv')
            delta_filename = data_path /  Path(table_file + '_delta.csv')
            meta_filename = data_path /  Path(table_file + '.json')
            delta_meta_filename = data_path /  Path(table_file + '_delta.json')
            hana_filename = data_path /  Path(table_file + '_hana.txt')

            # metadata and cdf flag
            metadata = table_metadata(profile, share=share, schema=schema, table=table)
            cdf = False
            # if not metadata:
            #     cdf = True
            #     rprint(f"[{sapc.warn}]FOR TEST ONLY. Metadata not retrieved successfully. Set cdf = True.")
            # else: 
            if 'enableChangeDataFeed' in metadata['configuration'] and \
                metadata['configuration']['enableChangeDataFeed']:
                cdf = True

            # Version settings
            end_version = args.end_version   
            local_version = 0
            if cdf and delta_meta_filename.is_file():
                with open(delta_meta_filename) as fp:
                    last_metadata = json.load(fp)
                local_version = int(last_metadata['version'])
                if args.version:
                    rprint(f"[{tp.cwarn}]Command option version overruled by version stored in \"meta_filename\": {local_version} -> {args.version}")
            elif meta_filename.is_file():
                with open(meta_filename) as fp:
                    last_metadata = json.load(fp)
                local_version = int(last_metadata['version'])
                if args.version:
                    rprint(f"[{tp.cwarn}]Command option version overruled by version stored in \"meta_filename\": {local_version} -> {args.version}")
            elif args.version:
                local_version = int(args.version)
    
            # last hana version
            hana_last_version = 1
            if hana_filename.is_file():
                hana_last_version = int(open(hana_filename).readline())

            if not args.meta and args.Hana:
                if csn_filename.is_file():
                    csn = PyCSN(csn_filename)
                else:
                    rprint(f"[{tp.cerror}]Error: No csn-file \"{csn_filename}\" for uploading data to HANA.\n"\
                        " For creating cs-file use cmd option --meta.")

            if args.meta:    
                tp.print_share_metadata(table_path=table_path, metadata=metadata)
                PyCSN(metadata, table_path).write(filename=csn_filename)
                # WARNING: Metadata should not be stored because the version of the metadata controls the sync version

            elif args.sync:
                rprint(f"Sync table [{tp.variable}]{table}")
                last_version = int(open(data_path / Path(f'{table_file}_version.txt')).readline())
                hana_last_version = int(open(data_path / Path(f'{table_file}_hana_version.txt')).readline())
                if last_version ==  hana_last_version:
                    rprint(f"Table [{tp.variable}]{table} is in sync (file:{last_version} = hana:{hana_last_version} ")
                    return 0
                df = pd.read_csv(data_path / Path(f'{table_file}_delta.csv'))
                df = df.loc[df['_commit_version'] > hana_last_version]
                with open(args.config) as yamls:
                    db = yaml.safe_load(yamls)

                columns = [c for c in df.columns if c not in ['_change_type','_commit_version','_commit_timestamp']]

                for v in range(hana_last_version+1, last_version+1):
                    df_insert = df.loc[(df["_change_type"]=='insert') & (df["_commit_version"]==v),columns]
                    if not df_insert.empty:
                        insert(db, schema=schema, table=table, df=df_insert)
                        insert_batch(db, schema=schema, table=table, df=df_insert)
                    
                    df_delete = df.loc[(df["_change_type"]=='delete') & (df["_commit_version"]==v),columns]
                    if not df_delete.empty:
                        delete(db, schema=schema, table=table, columns=columns, df=df_delete)

                    df_update = df.loc[((df["_change_type"]=='update_preimage') | (df["_change_type"]=='update_postimage'))
                                        & (df["_commit_version"]==v),columns]
                    if not df_update.empty:
                        update(db, schema=schema, table=table, df=df_update)
                open(data_path / Path(f'{table_file}_hana_version.txt'), 'w').write(str(last_version))

            else:
                if cdf and local_version != 0:
                    if local_version == int(metadata['version']): 
                        rprint(f"No new version to download!  local: {local_version} -> available: {metadata['version']}")
                        return 0
                    
                    rprint(f"Download >= version: [{tp.variable}]{local_version+1}")
                    cdf_metadata, df = read_cdf(profile=profile, share=share, schema=schema, table=table, 
                                                start_version=local_version+1, end_version=end_version)  
                    tp.print_share_metadata(table_path=f"{share}.{schema}.{table}")     
                    tp.print_dataframe(df,title="", max_rows=40)
                    if not delta_filename.is_file(): 
                        rprint(f"Save to new file: [{tp.variable}]{delta_filename}")
                        df.to_csv(delta_filename, index=False)
                    else: 
                        rprint(f"Append to file: [{tp.variable}]{delta_filename}")
                        df.to_csv(delta_filename, mode='a', header=False, index=False)

                    rprint(f"Save metadata-file:[{tp.variable}]{delta_meta_filename}")
                    with open(delta_meta_filename, "w") as fp:
                        json.dump(cdf_metadata, fp, indent=4)

                    if args.Hana:
                        if hana_last_version != last_version:
                            raise ValueError("Hana last version not equal file last version! Sync first delta files to hana. ")
                        with open(args.config) as yamls:
                            db = yaml.safe_load(yamls)

                        columns = [c for c in df.columns if c not in ['_change_type','_commit_version','_commit_timestamp']]
                        for v in range(last_version,local_version+1):
                            rprint(f"Process version: {v}")
                            df_insert = df.loc[(df["_change_type"]=='insert') & (df["_commit_version"]==v),columns]
                            if not df_insert.empty:
                                insert(db, schema=schema, table=table, df=df_insert)
                            
                            df_delete = df.loc[(df["_change_type"]=='delete') & (df["_commit_version"]==v),columns]
                            if not df_delete.empty:
                                delete(db, schema=schema, table=table, columns=columns, df=df_delete)

                            df_update = df.loc[((df["_change_type"]=='update_preimage') | (df["_change_type"]=='update_postimage'))
                                                & (df["_commit_version"]==v),columns]
                            if not df_update.empty:
                                update(db, schema=schema, table=table, df=df_update)
                        open(hana_filename, 'w').write(str(local_version))

                else: 
                    metadata, df = read_data(profile, share=share, schema=schema, table=table, version=local_version)
                    tp.print_dataframe(df=df, title=table_path,max_rows=30)
                    tp.print_share_metadata(table_path=table_path,metadata=metadata)
                    
                    rprint(f"Save data to file:[{tp.variable}]{init_filename}")  
                    df.to_csv(init_filename, index=False)
                    rprint(f"Save metadata-file:[{tp.variable}]{meta_filename}")
                    with open(meta_filename, "w") as fp:
                        json.dump(metadata, fp, indent=4)

                    if args.Hana:
                        with open(args.config) as yamls:
                            db = yaml.safe_load(yamls)

                        if not schema_exists(db,schema=schema):
                            rprint(f"[{tp.cerror}]Schema is not existing: [{tp.variable}]\"{schema.upper()}\"")
                            create_schema(db, schema)
                        
                        if not table_exists(db,schema=schema, table=table):
                            rprint(f"[{tp.cerror}]Table is not existing -> create table: [{tp.variable}]\"{schema}\".\"{table}\"")
                            execute_sql(db,csn.create_table_sql(f"{schema.upper()}.{table.upper()}"))

                        rprint(f"Save data to hana [{tp.variable}]{db['host']}")
                        truncate(db, schema=schema, table=table)
                        upload(db, schema=schema, table=table, df=df)


if __name__ == "__main__":
    main()