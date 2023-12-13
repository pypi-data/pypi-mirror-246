
import argparse
from pathlib import Path
from datetime import datetime
import json

from rich import print as rprint
from rich.table import Table
import pandas as pd
from pandas.api.types import is_numeric_dtype
from pandas.core.dtypes.common import is_datetime64_dtype
from deltalake import write_deltalake, DeltaTable
from faker import Faker
from  hdlfs.hdlfsystem import HDLFileSystem
from pyarrow import fs

HDLFSCONFIGFILE = ".hdlfscli.config.json"

blue4 = "rgb(137,209,255)"
blue7 = "rgb(0,112,242)"

info = blue4
variable = blue7

MAX_ROWS = 20

def new_customer(id_num: int) -> dict:  
    fake = Faker()
    return { "account_no": id_num,
            "name": fake.name(),
            "address": fake.address().replace('\n', ', '),
            "services": 0,
            "active":  True,
            # "updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "updated": datetime.utcnow().replace(microsecond=0),
            "comment":" "}

def df2table(df: pd.DataFrame, title='DataFrame', max_rows = MAX_ROWS) -> Table:
    max_rows = max_rows if df.shape[0] > MAX_ROWS else df.shape[0]
    table = Table(title=title, header_style=variable)
    for c in df.columns:
        table.add_column(c, justify="left", style=info, no_wrap=False)
    for _, row in df.tail(max_rows).iterrows():
        vals = [ str(r) for r in row.values]
        table.add_row(*vals)
    return table

def lists2table(columns: list, lists:list, title='Lists', max_rows = MAX_ROWS) -> Table:
    max_rows = max_rows if len(lists) > MAX_ROWS else len(lists)
    table = Table(title=title, header_style=variable)
    for c in columns:
        table.add_column(c, justify="left", style=info, no_wrap=False)
    for row in lists[:max_rows]:
        vals = [ str(r) for r in row]
        table.add_row(*vals)
    return table

def print_schema(delta_table)->None:
    if delta_table:
        fields = delta_table.schema().fields
        fields = [ (i+1, f.name,f.type.type, f.nullable) for i, f in enumerate(fields)]
        rprint(lists2table(["Seq","Field",'Dtype','Nullable'],fields,'Data Types'))

def main():

    parser = argparse.ArgumentParser("Generate data (customer registration)")
    parser.add_argument("action", choices=['read','insert','update','delete','list'], help="Number of new customers.", default=10)
    parser.add_argument("-n", "--num", type=int, help="Number of new customers.", default=10)
    parser.add_argument("-d", "--datapath",  help="Data path", default='.')
    parser.add_argument("-f", "--format", choices=['csv','delta'], help="Output format (csv or delta)", default='csv')
    parser.add_argument("-H", "--HDLFS_config", help="Output to HDLFs config", default='canaryds')
    args = parser.parse_args()

    path = args.datapath
    if args.HDLFS_config:
        # filesystem = fs.SubTreeFileSystem(path, HDLFileSystem(args.HDLFS_config))
        filesystem = HDLFileSystem(args.HDLFS_config)
        with open(Path.home() / HDLFSCONFIGFILE  ) as fp:
            hdlfs_params = json.load(fp)["configs"][args.HDLFS_config]
    else: 
        filesystem = fs.SubTreeFileSystem(path, fs.LocalFileSystem())

    df = pd.DataFrame()
    dt = None
    offset = 0 
    # READ Data
    if args.format == 'csv':
        datafile = Path(args.datapath) / 'customers.csv'
        if datafile.is_file():
            df = pd.read_csv(datafile)
    else:
        datafile = Path(args.datapath) / 'customers'
        if datafile.is_dir() and (datafile / "delta.log").is_file():
            dt = DeltaTable(datafile)
            df = dt.to_pandas()
            print_schema(dt)

    if args.action == 'list':
        df = df.sort_values(by=['account_no'])
        rprint(df2table(df, title="List Table", max_rows=100))  
        return 0 
    else:  
        if args.format == 'csv':
            match args.action:
                case 'insert':
                    if not df.empty:
                        offset = df['account_no'].max() + 1
                    customers = [new_customer(i) for i in range(offset, offset+args.num)]
                    rprint(df2table(customers),title="Customers")   
                    df = pd.concat([df,pd.DataFrame(customers)], ignore_index=True)
                case 'delete':
                    sample_indices = df.sample(args.num).index
                    df.drop(sample_indices, axis=0, inplace=True)
                case 'update':
                    sample_indices = df.sample(args.num).index
                    df.loc[sample_indices,'active'] = ~df.loc[sample_indices,'active']
                    df.loc[sample_indices,'comment'] = 'modified'
                    df.loc[sample_indices,'updated'] = datetime.utcnow()
                    df.loc[sample_indices,'services'] = df.loc[sample_indices,'services'] + 1
            df.to_csv(datafile, index=False)
            df.to_csv(datafile, index=False)
        else:
            match args.action:
                case 'insert':
                    if dt:
                        offset = df['account_no'].max() + 1
                    dfs = pd.DataFrame([new_customer(i) for i in range(offset, offset+args.num)])
                    rprint(df2table(dfs, title="New Records"))
                    if not dt:
                        write_deltalake(datafile, dfs,mode='overwrite',filesystem=filesystem)
                    else:
                        write_deltalake(datafile, dfs,mode='append', filesystem=filesystem)
                case 'delete':
                    if not dt:
                        raise ValueError("Cannot delete records from an empty DataFrame")
                    sample_indices = df.sample(args.num).index
                    for i in sample_indices:
                        account_no = df.loc[i, 'account_no']
                        dt.delete(predicate=f"account_no = {account_no}")
                    rprint(df2table(df.loc[sample_indices], title="Delete Records"))
                case 'update':
                    if not dt:
                        raise ValueError("Cannot delete records from an empty DataFrame")
                    sample_indices = df.sample(args.num).index
                    df.loc[sample_indices,'active'] = ~df.loc[sample_indices,'active']
                    df.loc[sample_indices,'comment'] = 'modified'
                    df.loc[sample_indices,'services'] = df.loc[sample_indices,'services'] + 1
                    df.loc[sample_indices,'updated'] = datetime.utcnow().replace(microsecond=0)
                    # rprint(df2table(df.loc[sample_indices].sort_values(by=['account_no']), 
                    #                 title="Update Records - After"))
                    for i in sample_indices:
                        updates = {"active": str(df.loc[i, 'active']), 
                                "services": str(df.loc[i, 'services']),
                                "comment": "\'commentary\'",
                                "updated": f"\'{df.loc[i,'updated']}\'"}
                        predicate = f"account_no = {df.loc[i,'account_no']}"
                        dt.update(updates=updates, predicate=predicate)
                    df = dt.to_pandas()
                    rprint(df2table(df.sort_values(by=['account_no']), title="After Update all Records"))
                

if __name__ == '__main__':
    main()