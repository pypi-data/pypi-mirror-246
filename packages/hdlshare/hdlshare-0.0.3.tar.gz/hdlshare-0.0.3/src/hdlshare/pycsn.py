import argparse
import json
from pathlib import Path
from dataclasses import dataclass
import re
from datetime import date
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)

@dataclass
class C:
	n: str = "\033[0m"
	red: str = "\033[31m"
	green: str = "\033[32m"
	yellow: str = "\033[33m"
	blue: str = "\033[34m"
	magenta: str = "\033[35m"
	cyan: str = "\033[36m"

DEFAULT_STRING_LENGTH = 100

class PyCSN():
    def __init__(self, obj, table_name=None, buffer=1) -> None: 
        self.buffer = buffer
        match obj:
            case pd.DataFrame():
                self.init_csn_dict()
                if not table_name:
                    raise Exception("Table name required!")
                self.add(obj, table_name)
            case dict():
                if isinstance(obj[list(obj)[0]], pd.DataFrame):
                    self.init_csn_dict()
                    for table_name, elem in obj.items():
                        self.add(elem,table_name)
                elif 'definitions' in obj:
                    self.csn = obj
                    logging.info("pycsn initialized with csn-formatted dict.")
                elif 'schema' in obj and 'configuration' in obj:
                    self.from_meta(obj,table_name)
                else: 
                    raise ValueError(f"Unknown format of dict for init pycsn!")
            case str():
                file = Path(obj)
                self.name = file.stem
                with open(obj) as fp:
                     js= json.load(fp) 
                if file.suffix == '.json' and 'name' in js and 'format' in js:
                    if not js['name']:
                         file_parts = str(file.stem).replace('_meta','').split('_')
                    js['name'] = file_parts[1]+'.'+file_parts[2]
                    self.from_meta(js)
                else: 
                     self.csn = js

            case Path() | str():
                self.name = obj.stem
                with open(obj) as fp:
                    js = json.load(fp)

                if obj.suffix == '.json' and 'name' in js and 'format' in js:
                    self.csn = self.from_meta(js)
                else: 
                     self.csn = js
            case _:
                raise ValueError(f"{C.red}Unsupported obj:{type(obj)}{C.n}")

    # Class methods
    pd2cds_map = {
        "object": "cds.String",
        "int64": "cds.Int64",
        "float64": "cds.Double",
        "bool": "cds.Boolean",
        "datetime64": "cds.DateTime"
    }
    cds2pd = {
        "cds.String": "object",
        "cds.Int64": "int64",
        "cds.Double": "float64",
        "cds.Boolean": "bool",
        "cds.DateTime": "datetime64[ns]"
    }

    sql2pd = {
        "string": "object",
        "bigint": "int64",
        "double": "float64",
        "boolean": "bool",
        "datetime": "datetime64[ns]"
    }

    cds2sql = {
        "cds.String": "NVARCHAR",
        "cds.Int64": "BIGINT",
        "cds.Double": "DOUBLE",
        "cds.Boolean": "BOOLEAN",
        "cds.DateTime": "TIMESTAMP"
    }

    delta2cds_map = {
        "string": "cds.String",
        "long": "cds.Int64",
        "double": "cds.Double",
        "float": "cds.Float",
        "smallint": "cds.Int",
        "bool": "cds.Boolean",
        "timestamp": "cds.DateTime"
    }

    

    cds_numeric_types = ["cds.Int64", "cds.Double"]

    def init_csn_dict(self):
        self.csn = { "definitions": {},
                "version": {
                    "creator": "pycsn",
                    "csn": "0.1.99"
                }
            }

    def dt_records2pd(records: list) -> pd.DataFrame:
        cols = { rec['col_name']: pd.Series(dtype=PyCSN.sql2pd[rec['data_type'].lower()]) 
                for rec in records}
        return pd.DataFrame(cols)
    
    def cdstype(data_type) ->str:
        dt = str(data_type)
        if 'datetime64' in dt:
            dt = 'datetime64'
        return PyCSN.pd2cds_map[dt]
    
    def pd2cds(df: pd.DataFrame, name: str) -> str:
        csn = PyCSN(df, name).csn
        cds=""
        for dk, d in csn['definitions'].items():
            if d['kind'] == 'entity':
                cds=f"entity {dk} : {{\n"
                if 'elements' in d:
                    for ek, elem in d['elements'].items():
                        cds += f"  {ek:<8} : {elem['type'].split('.')[1]}\n"    
            cds += "}\n"
        return cds
    
    
    def search_elem(node: dict, key: str) -> dict:
        if key in node: 
            return node[key]
        for k, v in node.items():
            if isinstance(v,dict):
                elem = PyCSN.search_elem(v, key)
                if elem is not None:
                    return elem

    def is_numeric(dtype: str) -> bool:
        return True if dtype in PyCSN.cds_numeric_types else False
    
    # Instance methods
    def __str__(self) -> str:
        return json.dumps(self.csn, indent=4)
    
    def add(self, df: pd.DataFrame, table_name: str) -> dict:
        if table_name not in self.csn["definitions"]:
            self.csn["definitions"][table_name] = {"elements": dict()}
        csncols = self.csn["definitions"][table_name]["elements"]
        for c in df.index.names:
            if c:
                dt = PyCSN.cdstype(df.index.get_level_values(c).dtype)
                csncols[c] = {"type": dt, "key": True}
                if dt == 'cds.String':
                    max_length = df.index.get_level_values(c).str.len().max() + self.buffer
                    csncols[c]["length"] = int(max_length)
        for c in df.columns:
            dt = PyCSN.cdstype(df[c].dtype)
            csncols[c] = {"type": dt}
            if dt == 'cds.String':
                if not df.empty:
                    max_length = df[c].str.len().max() + self.buffer
                else:
                    max_length = DEFAULT_STRING_LENGTH
                csncols[c]["length"] = int(max_length)
    
    def write(self, filename=None, format='csn') -> str:        
        match format:
            case 'cds':
                cds = self.cds()
                with open(filename, 'w') as fp:
                    fp.write(cds)
                print(f"CDS-file written: {C.green}{filename}{C.n}")
            case 'csn':
                with open(filename, 'w') as js:
                    json.dump(self.csn, js, indent=4)
                print(f"CSN-file written: {C.green}{filename}{C.n}")
            case _:
                raise ValueError(f"{C.red}Unknown format: {C.green}{format}{C.n}")
  
    def update_df(self, df: pd.DataFrame, name: str) -> pd.DataFrame:

        # Check if csn and df have equal columns
        df_cols = set(df.columns)
        if df.index.names[0]: # in case there is not index set
            df_cols.update(df.index.names)
        table = self.csn['definitions'][name]['elements']
        csn_cols = set(table.keys())
        if csn_cols != df_cols:
            raise ValueError(f"Columns of csn and DataFrame({name}) are not equal: {csn_cols} <-> {df_cols}")
        
        # update keys
        csn_keys = set([ c for c,elem in table.items() if 'key' in elem and elem['key'] == True])
        df_keys = set(df.index.names)
        if csn_keys and csn_keys != df_keys:
            print(f"{C.red}Keys are not equal: csn({csn_keys}) <-> df({df_keys}){C.n}")
            if df.index.names[0]:
                df.reset_index(inplace=True)
            csn_keys = list(map(lambda x: x, csn_keys))
            df.set_index(csn_keys,inplace=True)

        # Check on data types
        for c in df.columns:
            pd_dtype = PyCSN.cds2pd[table[c]['type']]
            if pd_dtype != str(df[c].dtype):
                print(f"{C.green}Column dtypes are not equal:{C.n} cds:{pd_dtype} <-> df:{str(df[c].dtype)}")
                df[c] = df[c].astype(pd_dtype)

    def cds(self):
        cds=""
        for dk, d in self.csn['definitions'].items():
            if d['kind'] == 'entity':
                cds=f"entity {dk}  {{\n"
                if 'elements' in d:
                    for ek, elem in d['elements'].items():
                        key_elem = ek
                        if 'key' in elem and elem['key'] == True:
                            key_elem = 'key '+ ek
                        elem_type = elem['type'].split('.')[1]
                        if 'length' in elem:
                            elem_type += f"({elem['length']})"
                        cds += f"  {key_elem:<12} : {elem_type};\n"    
            cds += "}\n"
        return cds
    
    def set_primary_keys(self, pks) -> None:
        if isinstance(pks, str):
            pks = [pks]
        for pk in pks:
            for t in self.csn['definitions']:
                table = self.csn['definitions'][t]
                if 'elements' not in table:
                    continue
                if pk in table['elements']:
                    table['elements'][pk]['key'] = True


    def add_annotation(self, key_name: str, annotations: dict) -> None:
        elem = PyCSN.search_elem(self.csn, key_name)
        if elem :
            for a, v in annotations.items():
                if a[0] != '@':
                    a = '@' + a
                elem[a] = v
        else:
            raise ValueError(f"Entity \"{key_name}\" not found in csn.")

    def add_version_format(self, version: str) -> None:
        if re.match("\d+\.\d+\.\d+", version):
            self.csn['version']['@format'] = version
            self.csn['version']['@creation_date'] = str(date.today())
        else:
            raise ValueError(f"Version format not matched %d.%d.%d!")
        
    def set_col_length(self, table: str, column: str, length: int) -> None:
        elem = PyCSN.search_elem(self.csn, table)       
        if 'elements' not in elem:
            raise ValueError(f"Table \"{table}\"has no columns (elements)!")
        elem['elements'][column]['length'] = length

    def set_col_type(self, table: str, column: str, dtype: str, length=None) -> None:
        elem = PyCSN.search_elem(self.csn, table)       
        if 'elements' not in elem:
            raise ValueError(f"Table \"{table}\"has no columns (elements)!")
        elem['elements'][column]['type'] = dtype
        if PyCSN.is_numeric(dtype) and 'length' in elem['elements'][column]: 
            elem['elements'][column].pop('length')
        elif dtype == 'cds.String':
            elem['elements'][column]['length'] = length if length else DEFAULT_STRING_LENGTH

    def create_table_sql(self,table: str):
        sql = f"CREATE COLUMN TABLE {table} ( \n"
        if table in self.csn['definitions']:
            t = self.csn['definitions'][table]
        elif table.lower() in self.csn['definitions']:
            t = self.csn['definitions'][table.lower()]
        else:
            raise KeyError(f"{C.red}Table not found in csn-file:{C.green} \"{table}\" or \"{table.lower()}\"{C.n}")
        pks = ''
        for col in t['elements']:
            c = t['elements'][col]
            not_null = "" if "notNull" not in c or "notNull" == False else "not null"
            length = f"({c['length']})" if 'length' in c  else ''
            sql += f"\t{col} {PyCSN.cds2sql[c['type']]}{length} {not_null},\n"
            if 'key' in c and c['key']:
                pks += f"\t\t{col},\n"
        if len(pks) >0 :
            pks = f"\tPRIMARY KEY(\n{pks})"
            sql = (sql + pks)[:-3] + "\n\t)\n)"
        else:
            sql = (sql + pks)[:-2] + "\n)"
        print(f"Create table sql: \n{C.green}{sql}{C.n}")
        return sql
    
    def from_meta(self, meta: dict, table_path: str):
        _, schema, table = table_path.split('.')
        name = schema+'.'+table
        self.init_csn_dict()
        if name not in self.csn["definitions"]:
            self.csn["definitions"][name] = {"elements": dict()}
        csncols = self.csn["definitions"][name]["elements"]
        for c, v in meta['schema'].items():
            dt = PyCSN.delta2cds_map[v['type']]
            csncols[c] = {"type": dt}
            if dt == 'cds.String':
                csncols[c]["length"] = int(DEFAULT_STRING_LENGTH)
            if 'nullable' in v:
                csncols[c]['notNull'] = v['nullable']
 


def main():

    parser = argparse.ArgumentParser(prog='pycsn',
                                     description='Creates csn-file from pandas DataFrame.')
    parser.add_argument('filenames', nargs='+', help='Data Filenames (csv)')
    parser.add_argument('-o', '--output', help='Overwrite default filename')
    parser.add_argument('-p', '--primary_keys', nargs='+', help='Add primary keys (Attention for all tables!).')
    parser.add_argument('-n', '--names', nargs='+', help='Set table names.')
    parser.add_argument('-s', '--sql', help='Create table sql.',action='store_true')
    parser.add_argument('-b', '--buffer', help='Additional string buffer', type=int, default=1)
    parser.add_argument('-m', '--meta', help='Create csn from deltalake metadata', action='store_true')
    parser.add_argument('-t', '--test', help=argparse.SUPPRESS, action='store_true')
    args = parser.parse_args()


    if args.meta:
        csn = PyCSN(args.filenames[0])
        print(csn)
        return 0

    if args.names and len(args.names) != len(args.filenames):
        print(f"{C.red}Number of csv-files and names must be equal!{C.n}")
        return -1

    dfs = dict()
    for i, f in enumerate(args.filenames):
        print(f"Read data-file:{C.green} {f}{C.n}")
        fp = Path(f)
        df = pd.read_csv(fp)
        if args.names:
            dfs[str(args.names[i])] = df
        else:
            dfs[str(fp.stem)] = df
        print(f"Table name:{C.green} {fp.stem}{C.n}")
    csn=PyCSN(dfs, buffer=args.buffer)

    if args.primary_keys:
        csn.set_primary_keys(args.primary_keys)

    if args.sql:
        for t in dfs.keys():
            csn.create_table_sql(t)


    if args.test:
        dt_dict = [{'col_name': 'country', 'data_type': 'string', 'comment': None}, 
                {'col_name': 'article_id', 'data_type': 'bigint', 'comment': None}, 
                {'col_name': 'category', 'data_type': 'string', 'comment': None}, 
                {'col_name': 'name', 'data_type': 'string', 'comment': None}, 
                {'col_name': 'size', 'data_type': 'string', 'comment': None}, 
                {'col_name': 'store_id', 'data_type': 'string', 'comment': None},
                {'col_name': 'transaction_id', 'data_type': 'bigint', 'comment': None}]
        csn = PyCSN(dt_dict, name='storex')
        csn.set_col_length('storex','category', 25)
        csn.set_col_type('storex','store_id', 'cds.Int64')
        csn.set_col_type('storex','transaction_id', 'cds.String', 25)
        print(csn)

    if args.output:
        csn.write(args.output)
    else: 
        if len(args.filenames) > 1:
            csn.write("tables.csn")
        else:
            csn.write(Path(args.filenames[0]).with_suffix('.csn'))


if __name__ == '__main__':
    main()