from datetime import datetime

from rich import print as rprint
from rich.table import Table
from rich.tree import Tree as rTree
from rich.pretty import pprint

import pandas as pd

MAX_ROWS = 30


blue2 = "rgb(209,239,255)"
blue4 = "rgb(137,209,255)"
blue6 = "rgb(27,144,255)"
blue7 = "rgb(0,112,242)"
red7 = "rgb(210,10,10)"
mango4 = "rgb(255,201,51)"
mango2 = "rgb(255,243,184)"
mango6 = "rgb(231,101,0)"


cinfo = blue4
variable = blue7
cvar = blue7
header_style = f"bold {blue7}"
title_style = f"italic {blue7}"
item_style = blue4
bullet_style = blue7
cerror = red7
cwarn = mango4
cwarning = mango4
treelevel = ['bold white', blue6, blue4, blue2, blue2, blue2, blue2, blue2, blue2, blue2, blue2, blue2]

def error(msg: str) -> None:
    rprint(f"[{cerror}]{msg}")

def warning(msg: str) -> None:
    rprint(f"[{cwarn}]{msg}")

def info(info: str, msg=None) -> None:
    if msg:
        rprint(f"[{cinfo}]{info}: [{cvar}]{msg}")
    else: 
        rprint(f"[{cinfo}]{info}")

def bullet_list(items: list, title=None) -> None:
    if title:
        rprint(f"[{title_style}]{title}")
    for i in items:
        rprint(f"[{bullet_style}]\u2022  [{item_style}]{i}")
    print('\n')

def dict2tree(tree: rTree, data, level=1) -> rTree:
    if not data:
        return tree
    elif isinstance(data, list):
        for i in data:
            tree.add(f"[{treelevel[level]}]{i}[/]")
    elif isinstance(data, dict):
        for k, v in data.items():
            stree = tree.add(f"[{treelevel[level]}]{k}[/]")
            dict2tree(stree, v, level+1)
    else:
        raise ValueError("Wrong format in dict!")
    
def print_tree(tree,name='shares')-> None:
    rtree = rTree(f"[{treelevel[0]}]{name}[/]")
    dict2tree(rtree, tree)
    rprint('\n',rtree, '\n')


def dataframe(df: pd.DataFrame, title='DataFrame', max_rows = MAX_ROWS) -> Table:
    max_rows = max_rows if df.shape[0] > MAX_ROWS else df.shape[0]
    table = Table(title=title, header_style=header_style, title_style=title_style)
    for c in df.columns:
        table.add_column(c, justify="left", style=cinfo, no_wrap=True)
    for _, row in df.tail(max_rows).iterrows():
        vals = [ str(r) for r in row.values]
        table.add_row(*vals)
    rprint(table)

def print_table(columns: list, lists:list, title='Lists', max_rows = MAX_ROWS) -> None:
    max_rows = max_rows if len(lists) > MAX_ROWS else len(lists)
    table = Table(title=title, header_style=header_style, title_style=title_style )
    for c in columns:
        table.add_column(c, justify="left", style=cinfo, no_wrap=False)
    for row in lists[:max_rows]:
        vals = [ str(r) for r in row]
        table.add_row(*vals)
    rprint('\n',table,'\n')

def dictionary(data: dict, title='Dictionary', columns=['Key','Value'],max_rows = MAX_ROWS) -> None:
    max_rows = max_rows if len(data) > MAX_ROWS else len(data)
    table = Table(title=title, header_style=header_style, title_style=title_style )
    for c in columns:
        table.add_column(c, justify="left", style=cinfo, no_wrap=False)
    for k,v  in data.items():
        table.add_row(str(k),str(v))
    rprint('\n',table,'\n')

def listdicts(data:list, title='Dictionaries', columns=['Key','Value'],max_rows = MAX_ROWS) -> None:
    max_rows = max_rows if len(data) > MAX_ROWS else len(data)
    table = Table(title=title, header_style=header_style, title_style=title_style )
    table.add_column(columns[0], justify="left", style=cinfo, no_wrap=False)
    table.add_column(columns[1], justify="left", style=cinfo, no_wrap=False)
    for i, d in enumerate(data):
        table.add_row(str(i),"")
        table.add_section()
        for k,v  in d.items():
            table.add_row(str(k),str(v))
    rprint('\n',table,'\n')

def delta_schema(delta_table)->None:
    if delta_table:
        fields = delta_table.schema().fields
        fields = [ (i+1, f.name,f.type.type, f.nullable) for i, f in enumerate(fields)]
        print_table(["Seq","Field",'Dtype','Nullable'],fields,'Data Types')

def delta_metadata(version, metadata)->None:
    if metadata:
        table = Table(title=f"Metadata", header_style=header_style, title_style=title_style )
        table.add_column('Key', justify="left", style=cinfo, no_wrap=False)
        table.add_column('Value', justify="left", style=cinfo, no_wrap=False)
        table.add_row('version',str(version))
        table.add_row('name',metadata.name)
        table.add_row('description',metadata.description)   
        table.add_row('id',str(metadata.id)) 
        table.add_row('partition columns',str(metadata.partition_columns)) 
        table.add_row('created at',datetime.fromtimestamp(int(metadata.created_time/1000)).isoformat())
        table.add_section()
        for k, v in metadata.configuration.items(): 
            table.add_row(k, v) 
        rprint('\n',table)

def delta_history(history: dict) -> None:
    table = Table(title=f"History", header_style=header_style, title_style=title_style )
    table.add_column('Version', justify="left", style=cinfo)
    table.add_column('Timestamp', justify="left", style=cinfo)
    table.add_column('Operation', justify="left", style=cinfo)
    table.add_column('Client Version', justify="left", style=cinfo)
    for h in history:
        table.add_row(str(h['version']),datetime.fromtimestamp(int(h['timestamp']/1000)).isoformat(),
                      h['operation'], h['clientVersion'])
    rprint('\n', table)



def print_share_metadata(table_path, metadata):
    rprint(f"[{header_style}]{table_path}:\n")
    table1 = Table(title=f"Metadata", header_style=header_style, title_style=title_style )
    table1.add_column('Metadata', justify="left", style=cinfo, no_wrap=False)
    table1.add_column('Value', justify="left", style=cinfo, no_wrap=False)
    table1.add_row("Version",metadata['version'])
    if 'enableChangeDataFeed' in metadata['configuration']:
        table1.add_row("CDF enabled",metadata['configuration']['enableChangeDataFeed'])
    if 'size' in metadata:
        table1.add_row("Size",metadata['size'])
    if 'partitionColumns' in metadata:
        table1.add_row("Partition Columns",str(metadata['partitionColumns']))
    rprint(table1,"\n")
    table2 = Table(title=f"Schema", header_style=header_style, title_style=title_style )
    table2.add_column('Column Name', justify="left", style=cinfo, no_wrap=False)
    table2.add_column('Data Type', justify="left", style=cinfo, no_wrap=False)
    table2.add_column('Nullable', justify="left", style=cinfo, no_wrap=False)
    for c,v in metadata['schema'].items():
        table2.add_row(c,v['type'],str(v['nullable']))
    rprint(table2)

def print_request_info(method, endpoint, path, headers, params):
    table = Table(title="Request Info", header_style=header_style, title_style=title_style,
                  expand=True)
    table.add_column("Key", justify="left", style=cinfo)
    table.add_column("Value", justify="left", style=cinfo,overflow="fold")
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

