
import argparse
from pathlib import Path
from datetime import datetime
import json
import subprocess
import os 

from rich import print as rprint
from deltalake import DeltaTable

try:
    import termprint as tp
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp

HDLFSCONFIGFILE = ".hdlfscli.config.json"
MAX_ROWS = 100



def sync_local2hdl(hdlfs_config, source, target):
    rprint(f"[{tp.cinfo}]Sync local folder with hdlfs ({hdlfs_config}): \n"
           f"[{tp.variable}]{source} -> {target}\n")
    
    cmd = ['hdlfscli', '-config', hdlfs_config, 'upload', str(source), str(target)]
    # rprint(f"[{sapc.variable}]{' '.join(cmd)}")
    subprocess.run(cmd, stdout = open(os.devnull,"w") )

def sync_hdl2local(hdlfs_config, source, target):
    rprint(f"[{tp.cinfo}]Sync hdlfs folder with target ({hdlfs_config}): \n"
           f"[{tp.variable}]{source} -> {target}\n")
    
    cmd = ['hdlfscli', '-config', hdlfs_config, 'download', str(source), str(target)]
    # rprint(f"[{sapc.variable}]{' '.join(cmd)}")
    subprocess.run(cmd, stdout = open(os.devnull,"w") )

def main():

    parser = argparse.ArgumentParser("Generate data person and save as deltalake file")
    parser.add_argument("HDLFSconfig", help="HDLFS config")
    parser.add_argument("path", help="Path")
    parser.add_argument("-l", "--local",  help="Local Data path", default='tmp')

    args = parser.parse_args()

    with open(Path.home() / HDLFSCONFIGFILE  ) as fp:
        params = json.load(fp)["configs"][args.HDLFSconfig]

    table_name = (args.path).split('/')[-1]
    target = Path(args.local) / table_name
    rprint(f"[{tp.cinfo}]Download table from [{tp.variable}]{args.path} -> {target}")
    sync_hdl2local(args.HDLFSconfig, args.path, target)
    dt = DeltaTable(target)
    df = dt.to_pandas()
    tp.dataframe(df, title=f"Delta Table: {table_name}", max_rows=100)



if __name__ == '__main__':
    main()