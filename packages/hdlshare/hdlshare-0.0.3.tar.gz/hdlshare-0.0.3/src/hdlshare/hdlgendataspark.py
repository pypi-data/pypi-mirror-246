import time
import argparse
import json
from pathlib import Path
from datetime import datetime

import pandas as pd
from rich import print as rprint
from faker import Faker

from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import max

try:
    import termprint as tp
    import hdlgendata
except (ModuleNotFoundError, ImportError):
    import hdlshare.termprint as tp
    import hdlshare.hdlgendata

start_time = time.time()

HDLFSCONFIGFILE = ".hdlfscli.config.json"
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


def read_conf(filename: str) -> SparkConf:
    config = dict()
    with open("hdl-spark.conf") as fp:
        line = fp.readline().strip().split()
        while line:
            config[line[0]] = line[1]
            if line[1] == 'True':
                config[line[0]] = True
            elif line[1] == 'False':
                config[line[0]] = False
            elif line[1].isdigit():
                config[line[0]] = int(line[1])
            line = fp.readline().strip().split()
    conf = SparkConf().setAppName("cross")
    for k,v in config.items():
        conf.set(k,v)
    return conf


def main():

    parser = argparse.ArgumentParser(description="Generates data with Spark and writes to HDLFS.")
    parser.add_argument("action", choices=['create','insert','update','delete'], help="Action")
    parser.add_argument("hdlf", nargs="+", help="HDLFS instance(s)", default='default')
    parser.add_argument("-c", "--config",  help="HDL Spark config file", default='hdl-spark.conf')
    parser.add_argument("-y", "--country", choices=countries,  help="Country", default='US')
    parser.add_argument("-u", "--user",  help="User with cross-hdl access role.")
    parser.add_argument("-n", "--num", type=int, help="Number of new customers.", default=10)
    parser.add_argument("-p", "--path",  help="HDL root path", default='data')
    parser.add_argument("-t", "--table",  help="Tablename", default="persons")
    parser.add_argument("-C", "--certificate_dir",  help="Certificate path", default="certificates/")
    args = parser.parse_args()

    country = args.country
    table_path = f"{args.path}/{country}/{args.table}"

    with open(Path.home() / HDLFSCONFIGFILE  ) as fp:
        hdl_params = json.load(fp)["configs"]

    conf = read_conf(args.config)
    conf.setAppName("hdlgendata")
    pem_file = Path(args.certificate_dir) / (args.user + ".pem")
    key_file = Path(args.certificate_dir) / (args.user + ".key")
    if not pem_file.is_file():
        tp.error(f"Certificate file does not exist: {pem_file}")
        raise FileExistsError("Certificate file does not exist: {pem_file}")
    if not key_file.is_file():
        tp.error(f"Certificate file does not exist: {key_file}")
        raise FileExistsError("Certificate file does not exist: {key_file}")
    
    conf.set('spark.hadoop.fs.hdlfs.ssl.certfile', str(Path(args.certificate_dir) / (args.user + ".pem")))
    conf.set('spark.hadoop.fs.hdlfs.ssl.keyfile', str(Path(args.certificate_dir) / (args.user + ".key")))
    tp.info("User", args.user)
    
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    config = spark.sparkContext.getConf().getAll()
    # tp.listlists(columns=['config', 'value'], lists=config, title="Context Configuration", max_rows=100)

    for tenant in args.hdlf:
        hdl_table_path = f"{hdl_params[tenant]['endpoint']}/{table_path}"
        tp.info("Tenant  ", tenant)
        tp.info("Endpoint", hdl_table_path)
        match args.action:
            case 'create':
                tp.info("CREATE","")
                df = pd.DataFrame([new_customer(i+1, country) for i in range(args.num)])
                sdf=spark.createDataFrame(df) 
                sdf.write.format("delta").mode("overwrite").save(hdl_table_path)
            case 'insert':
                tp.info("INSERT","")
                offset = spark.read.format('delta').load(hdl_table_path).agg(max("account_no")).first()[0]+1
                df = pd.DataFrame([new_customer(i, country) for i in range(offset, args.num+offset)])
                sdf=spark.createDataFrame(df) 
                sdf.write.format("delta").mode("append").save(hdl_table_path)
            case 'update':
                pass
            case 'delete':
                pass



if __name__ == '__main__':
    main()