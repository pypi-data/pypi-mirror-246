
import argparse
from pathlib import Path
from datetime import datetime
import json
import subprocess
import os 

from rich import print as rprint
from rich.table import Table
import pandas as pd
from deltalake import write_deltalake, DeltaTable
from faker import Faker

try:
    import termprint as tp
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp

HDLFSCONFIGFILE = ".hdlfscli.config.json"
MAX_ROWS = 100
locales = {'US':'en_US', 'DE':'de_DE', 'ES': 'es_ES', 'UK': 'en_GB','FR': 'fr_FR', 'IT': 'it_IT'}
countries = ['US','DE', 'FR', 'ES', 'UK', 'IT']

def new_customer(id_num: int, country: str) -> dict:  
    fake = Faker(locales[country])
    return { "account_no": id_num,
            "name": fake.name(),
            "address": fake.address().replace('\n', ', '),
            "services": 0,
            "active":  True,
            # "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "updated": datetime.utcnow().replace(microsecond=0),
            "comment":" "}


def sync_local2hdl(hdlfs_config, source, target):
    rprint(f"[{tp.cinfo}]Sync local folder with hdlfs ({hdlfs_config}): \n"
           f"[{tp.variable}]{source} -> {target}\n")
    
    cmd = ['hdlfscli', '-config', hdlfs_config, 'upload', str(source), str(target)]
    # rprint(f"[{sapc.variable}]{' '.join(cmd)}")
    subprocess.run(cmd, stdout = open(os.devnull,"w") )

def main():

    parser = argparse.ArgumentParser("Generate data person and save as deltalake file")
    parser.add_argument("action", choices=['insert','update','delete','show'], help="Action")
    parser.add_argument("country", choices=['US','DE', 'FR', 'ES', 'UK', 'IT'],  help="Country")
    parser.add_argument("dataname",  help="Target data folder (datapath/country/[dataname])")
    parser.add_argument("-n", "--num", type=int, help="Number of new customers.", default=10)
    parser.add_argument("-v", "--version", type=int, help="Version.")
    parser.add_argument("-x", "--cdf", help="Enable CDF.", action='store_true')
    parser.add_argument("-l", "--local",  help="Local Data path", default='data')
    parser.add_argument("-H", "--HDLpath",  help="HDL root path", default='data/deltalake')
    parser.add_argument("-c", "--HDLFSconfig",  help="HDLFS config", default='default')

    args = parser.parse_args()
    country = args.country
    offset = 0 

    local_path = Path(args.local) / country / args.dataname
    hdl_path = Path(args.HDLpath) / country / args.dataname
    name = f"{country.lower()}_{args.dataname}"

    with open(Path.home() / HDLFSCONFIGFILE  ) as fp:
        params = json.load(fp)["configs"][args.HDLFSconfig]

    if local_path.is_dir():
        rprint(f"[{tp.cinfo}]Data path found: [{tp.variable}]{local_path}")
        if (local_path / "_delta_log").is_file():
            rprint(f"[{tp.cerror}]No file \'_delta.log\' found! - delete target folder first.")
        dt = DeltaTable(local_path, version=args.version)
        df = dt.to_pandas()
    else: 
        rprint(f"[{tp.cinfo}]No data path found. Create new one: [{tp.variable}]{local_path}")
        dt = None
        df = pd.DataFrame()

    match args.action:
        case 'show':
            tp.delta_schema(dt)
            df = df.sort_values(by=['account_no'])
            tp.dataframe(df, title="List Table", max_rows=100)
            tp.delta_metadata(dt.version(), dt.metadata())
            tp.delta_history(dt.history())
        case 'insert':
            if dt:
                offset = df['account_no'].max() + 1
            dfs = pd.DataFrame([new_customer(i, country) for i in range(offset, offset+args.num)])
            tp.dataframe(dfs, title=f"New Records for Country: {country}")
            if not dt:
                config = {}
                rprint(f"[{tp.cinfo}]Create new deltalake file: [{tp.variable}]{name}")
                if args.cdf: 
                    config = {'enableChangeDataFeed':'true'}
                write_deltalake(local_path, dfs,mode='overwrite', name=name, configuration=config)
            else:
                write_deltalake(local_path, dfs,mode='append')
            sync_local2hdl(args.HDLFSconfig, local_path, hdl_path)
        case 'delete':
            if not dt:
                raise ValueError("Cannot delete records from an empty DataFrame")
            sample_indices = df.sample(args.num).index
            for i in sample_indices:
                account_no = df.loc[i, 'account_no']
                dt.delete(predicate=f"account_no = {account_no}")
            rprint(tp.print_dataframe(df.loc[sample_indices], title="Delete Records"))
            sync_local2hdl(args.HDLFSconfig, local_path, hdl_path)
        case 'update':
            if not dt:
                raise ValueError("Cannot delete records from an empty DataFrame")
            sample_indices = df.sample(args.num).index
            df.loc[sample_indices,'active'] = ~df.loc[sample_indices,'active']
            df.loc[sample_indices,'comment'] = 'modified'
            df.loc[sample_indices,'services'] = df.loc[sample_indices,'services'] + 1
            df.loc[sample_indices,'updated'] = datetime.utcnow().replace(microsecond=0)
            for i in sample_indices:
                updates = {"active": str(df.loc[i, 'active']), 
                        "services": str(df.loc[i, 'services']),
                        "comment": "\'commentary\'",
                        "updated": f"\'{df.loc[i,'updated']}\'"}
                predicate = f"account_no = {df.loc[i,'account_no']}"
                dt.update(updates=updates, predicate=predicate)
            df = dt.to_pandas()
            rprint(tp.print_dataframe(df.sort_values(by=['account_no']), title="After Update all Records"))
            sync_local2hdl(args.HDLFSconfig, local_path, hdl_path)


if __name__ == '__main__':
    main()