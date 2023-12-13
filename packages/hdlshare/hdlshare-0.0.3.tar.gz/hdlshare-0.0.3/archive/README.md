# Delta Sharing with SAP HDL

The usage of Spark is required for big data that needs a cluster of compute nodes and cheap storage (delta lake). The result of processing big data needs to be HANA tables that can be consumed by DataSphere. In order to share the results with other applications you either need a 

1. **system - to - system** integration where the credentials of the target applications are shared or
2. **"data product"**-kind of integration where you expose the data to external users with an external access management like "delta sharing". 

![use case](images/e2e_usecase.png)

Delta Sharing is internally used as a data sharing technology that separates the internals of the data producer from the data consumer and adds further options to govern the access. For each **HANA Cloud, Data Lake** instance a Delta Sharing server can be activated. For the time being this is only enabled for internal use. Once we have thoroughly tested this API by productive usage within SAP and if this service can be offered to the main Hyperscaler we might consider opening this service for SAP customer. 

## Overview HDL Tools

Currently the only way to manage **Delta Sharing** are mainly using RestAPIs. For testing purpose how to best use the **Delta Sharing** management I have developed a command line tools:

### Setup HDL
1. sapcert - create signed certificates
2. hdlinstance - create a HDLinstance using the created instance

### HDL Delta Sharing management
1. hdlshare - manage HDL Delta Shares
2. hdlpolicy - manage HDL Delta Share policys
3. dsclient - Delta Sharing Client to test HDL Delta Sharing

### Installation
1. Clone the git repository 
   ```python -m build```
   ```pip install .```
2. Install via pip (not yet)
  ```pip install hdlshare```




# hdsclient Overview

The following client was developed to use the API of the Databricks delta-sharing-server of the Unity catalog. It downloads the data using a "profile.json"-file and can upload it to a HANA database. It is CDF-enabled, that means it might download only the delta from the last downloaded version. The HANA integration includes creating schemas and tables if not existing. 

For managing the downloads the following tables are created:

- **filename of table**: \<share\>_\<schema\>_\<table\>.csv
- **metadata of table**: \<share\>_\<schema\>_\<table\>_meta.json
- **delta records of tables when CDF-enabled**: \<share\>_\<schema\>_\<table\>_delta.csv
- **CSN table definition**: \<share\>_\<schema\>_\<table\>_delta.csn
- **Last downloaded version**: \<share\>_\<schema\>_\<table\>_version.csn
- **Last uploaded hana version**: \<share\>_\<schema\>_\<table\>_hana.csn

All files are stored in the CWD or to the *path* given in the command options. 


# CSN Support 

The data can be downloaded to a csv-file with the name **\<share\>_\<schema\>_\<table\>.csv** and uploded to a HANA Database. Because the standard spark catalog is based on the delta lake format there is no feature for defining primary keys. The reason might be that there are not inherent tests on a "primary key violation" when a new record is written. A "primary key" might therefore lead to false assumptions. 

For supporting **primary keys** and DB-specific data types a csn-file can be used when a table is created in HANA. The csn-file needs to have the same name as the table file-name but with the ".csn"-extension.

## CSN File Creation
To support the creation of a csn-file you can use 

```shell
pip install pycsn

pyscn -h
pycsn <csv-file> -p [<primary keys>] -n [<table names>]

usage: pycsn [-h] [-o OUTPUT] [-p PRIMARY_KEYS [PRIMARY_KEYS ...]] [-n NAMES [NAMES ...]] [-s] [-b BUFFER] filenames [filenames ...]

Creates csn-file from pandas DataFrame.

positional arguments:
  filenames             Data Filenames (csv)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT Overwrite default filename
  -p PRIMARY_KEYS [PRIMARY_KEYS ...], --primary_keys PRIMARY_KEYS [PRIMARY_KEYS ...] Add primary keys (Attention for all tables!).
  -n NAMES [NAMES ...], --names NAMES [NAMES ...] Set table names.
  -s, --sql Create table sql.
  -b BUFFER, --buffer BUFFER Additional string buffer
```

# Installation

```
pip install dsclient==0.0.2 
```


# Delta Sharing Commandline Client

Lists and downloads files from Delta Sharing.

```angular2html
usage: dsclient.py [-h] [-p PATH] [-d] [-s STARTING] [-e ENDING] [-m] [-c CONFIG_FILE] [-H] [-S] profile [table]

positional arguments:
  profile               Profile of delta sharing
  table                 (optional) Table URL: <share>.<schema>.<table>. If not given table can be selected from available table list.

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Directory to store data.
  -d, --delta           Capture delta feeds
  -s STARTING, --starting STARTING
                        Start version (int, min=1)m or timestamp (str,"2019-09-26T07:58:30.996+0200")
  -e ENDING, --ending ENDING
                        End version (int, min=1) or timestamp (str,"2019-09-26T07:58:30.996+0200")
  -m, --meta            Show metadata
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Config-file for HANA access (yaml with url, user, pwd, port)
  -H, --Hana            Upload to hana
  -S, --Sync            Sync files with hana

```

# End2end process example

1. Databricks Unity Catalog: eating a new table in Databricks Unity CatalogCr
2. Databricks Delta Sharing: Add table to a Delta Sharing share and add recpient
3. hdsclient: Retrieve metadata (create csn-file)
4. hdsclient: Initial download, table creation and data upload
5. Databricks: Data update of source table (insert, delete, update)
6. hdsclient: Download data from last version and upload to table

# PoC Purpose

## 1st Slide
The purpose of this proof of concept is to test the end2end process from a Spark source system, in this case Databricks, via Delta Sharing protocol to HANA.

My name is Thorsten Hapke from the HD&A Cross Product Frontrunner team. 

## 2nd Slide

We have the three applications

1. Databricks as the source for data
2. The replication and db client developed for this PoC called hdsclient and 
3. the Hana DB

1. The first step is to create a table in a Databricks notebook and save this to the Unity Catalog
2. Then I add this table to an existing share with a recipient
3a. Now I can use the hdsclient to download the metadata. The downloaded data is also automatically creating a CSN-file based on the metadata of the table. 
3b. As a manual step I edit the csn-file by adding primary keys and adjust the data types
4a. Then I download the data of the table. Because the table does not exist in HANA, it will be created using the information of the CSN-file.
 4b. A short check in the DB explorer validates that the table has been created according to specifications of the CSN-file
 5. Then the data in the source table is changed (insert, delete and update operations)
 6. The hdsclient downloads the delta and uploads it the HANA table


## DBX notebook
