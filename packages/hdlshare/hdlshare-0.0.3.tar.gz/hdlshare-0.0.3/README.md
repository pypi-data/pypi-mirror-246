# Prepare Usage

## Create Certificates

1. Setup a PKI-Certificate Server (Preferably in the same subaccount but it is not a requirement)
2. Download Service-key

Run sapcert-cmd
```shell
sapcert -p service_keys/xpm-hdlfs-ds.json -d certificates -v 60 -t DAYS <CN>
```

![certificate chain verification](images/certificate_chain.png)

Creates 2 files
- <CN>.key - private key
- <CN>.pem - certificate chain

## Create HDLFS Instance

Using the [Service Manager API](https://service-manager.cfapps.eu10.hana.ondemand.com/api/#/Service%20Instances/getAllServiceInstances).

The subaccount needs a running **Service Manager** in the subaccount. 

For creating and managing HDL instances I have developed a commandline tool **hldinst**.


Using default service-key file: service_keys/sm-sk.txt

List instances
```shell
hdlinstance  list
```

Access Parameter
```shell
hdlinst params xpm-mt1
```

Instance Details
```shell
hdlinst details xpm-mt1
```

Currently the hdlfs-endpoint is not provided by the hdl-instance details but must be build by

<service id>.files.hdl.<regional hana cloud domain>, e.g. 

40e60329-e854-46e2-89d4-728093fb7576.files.hdl.prod-us30.hanacloud.ondemand.com

The following command adds a config section to the configuration file: $HOME/.hdlfscli.config.json

```shell
hdlinst add2config xpm-mt1 -C hdlmt1
```

To create a new hdl-instance
```shell
hdlinst create xpm-hdl-mt1 --CommonName hdlmt1 -c
```
This uses a template file in folder *'./configs/hdlfs_template.json'*. The argument '-c' is needed for using the subject of the certificate with the name \<certificates-folder>\<CommonName\>.pem as the user subject for the HDLFs authentication. 


## Additional Requirements for HDL Instance management

1. Adding API for deleting an HDLFS instance
2. Adding an API for managing the user/parameter of HDL instance. Important when havin many hdl-instances to adminster. 

# Delta Sharing with SAP HDL

Resources:

- [Git Documentation](https://github.wdf.sap.corp/DBaaS/Docs/blob/master/docs/designs/hanadatalake/hdlf/hdl-files-delta-sharing.md#jwts-and-transport)
- [Swagger for hdlfs-service](https://github.wdf.sap.corp/DBaaS/hdl-files-service/blob/master/doc/api-spec/src/webhdfs-swagger.yaml)

## Overview

The usage of Spark is required for big data that needs a cluster of compute nodes and cheap storage (delta lake). The result of processing big data needs to be HANA tables that can be consumed by DataSphere. In order to share the results with other applications you either need a 

1. **system - to - system** integration where the credentials of the target applications are shared or
2. **"data product"**-kind of integration where you expose the data to external users with an external access management like "delta sharing". 

![use case](images/e2e_usecase.png)

Delta Sharing is internally used as a data sharing technology that separates the internals of the data producer from the data consumer and adds further options to govern the access. For each **HANA Cloud, Data Lake** instance a Delta Sharing server can be activated. For the time being this is only enabled for internal use. Once we have thoroughly tested this API by productive usage within SAP and if this service can be offered to the main Hyperscaler we might consider opening this service for SAP customer. 

## URLs

### Catalog API

<instance-uuid>.files.hdl.<hld-cluster-endpoint>/catalog/v2
<instance-uuid>.files.hdl.<hld-cluster-endpoint>/policies/v2


### Audience in JWT
<instance-uuid>.files.<hld-cluster-endpoint>

### Delta Sharing

- Token Access: <instance-uuid>.sharing.hdl.<hld-cluster-endpoint>/shares/v1/
- Cert Access: <instance-uuid>.files.hdl.<hld-cluster-endpoint>/shares/v1/



## Overview HDL Tools

Currently the only way to manage **Delta Sharing** are mainly using RestAPIs. For testing purpose how to best use the **Delta Sharing** management I have developed a command line tools.

### hdlfscli
For manageing the files on HDLfs the Command line tool **hdlfscli** used. This can be downloaded from git [bigdataservices/hdlfs-cli](https://github.wdf.sap.corp/bigdataservices/hdlfs-cli).

```shell
hdlfscli -h
hdlfscli manages interaction with HDLFiles cloud service.

Find more information at: https://help.sap.com/docs/hana-cloud-data-lake/client-interfaces/hdlfscli-data-lake-files-utility

Storage Commands (Cloud Storage):
  ls or list      List a file or directory
  lsr or tree     List a file or directory with recursive traversal
  upload          Upload a file or directory to remote file storage from local file storage, creating remote directories suitably
  rm or delete    Delete a file or directory. Use with the flag '-f' for directories e.g., 'rm -f <directory>' to delete a directory
  mv              Move a remote file from remote source path to remote destination path
  cat             Open a file
  download        Copy a file or directory from remote storage to local file storage

JWT Commands (Manage JSON Web Tokens):
  jwt             Manage JWT

Usage For Storage Commands:
  hdlfscli [storage-options] storage-command [arguments]

Usage For JWT Commands:
   hdlfscli jwt [jwt-command] [jwt-options]

Use "hdlfscli storage-options" for a list of global command-line options (applies to all storage commands).
Use "hdlfscli jwt-options" for a list of jwt command-line options (applies to all jwt commands).
```

This **hdlfscli** uses a configuration file at $HOME/.hdlfscli.config.json. This config is also been used for the commandline apps *"hdlshare"* and *"hdlpolicy"*. 

For convenience reasons I have created a
1. 'default' - config-section in .hdlfscli.config.json. This is used when no config is given but required
2. alias with hdl='hdlfscli -config'

### Example
```shell
% hdl default ls data/deltalake
DIRECTORY  nobody nogroup 0            0     FR
DIRECTORY  nobody nogroup 0            0     DE
DIRECTORY  nobody nogroup 0            0     US
% hdl default upload data/US/customer data/deltalake/US/customer
```

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


## HDL Share
Creates and manages shares. The command line app is using the RestAPI ([Swagger for hdlfs-service](https://github.wdf.sap.corp/DBaaS/hdl-files-service/blob/master/doc/api-spec/src/webhdfs-swagger.yaml))

```shell
delta_sharing_python_client % hdlshare -h
usage: Manage HDLFS shares [-h] [-r] [-m] [-C] [-p PATH] [-c CONFIG] {list,add,delete,get} [target ...]

positional arguments:
  {list,add,delete,get}
                        Command for 'target'-argument
  target                share schema table (optional)

options:
  -h, --help            show this help message and exit
  -r, --recursive       List recursively
  -m, --metadata        Show metadata of table (action=list)
  -C, --cascade         Drop cascade when deleting share (action=delete)
  -p PATH, --path PATH  HDLFS data folder
  -c CONFIG, --config CONFIG
                        HDLFs config in '.hdlfscli.config.json'

```

### Examples

List data on hdlfs:
```shell
% hdl default ls data/deltalake/US                                    
DIRECTORY  nobody nogroup 0            0     persons
```

List all shares and tables 
```shell
% hdlshare list -r

shares
├── sbm
├── hxm
└── crm
    └── us
        └── customer

```

Add new table to share
```shell
% hdlshare add hxm us employees --path data/deltalake/persons
Table successfully added: hxm: us.employees
% hdlshare list -r
shares
├── sbm
├── hxm
│   └── us
│       └── employees
└── crm
    └── us
        └── customer
```

Details of Share:schema:table:
```shell
% hdlshare list -rm
shares
├── sbm
├── hxm
│   └── us
│       └── employees
│           ├── data/deltalake/persons
│           ├── DELTA
│           └── cdf: True
└── crm
    └── us
        └── customer
            ├── data/deltalake/US/customer
            ├── DELTA
            └── cdf: True
```



## hdlpolicy
Create and manage policies. 

- [Documentation](https://github.wdf.sap.corp/DBaaS/Docs/blob/master/docs/designs/hanadatalake/hdlf/hdl-files-policies.md)
- [swagger](https://github.wdf.sap.corp/DBaaS/hdl-files-service/blob/master/doc/api-spec/src/policies-swagger.yaml)



```shell
% hdlpolicy -h
usage: Manage HDLFS share policies [-h] [-p POLICY] [-s SUBJECT] [-R RESOURCE] [-P PRIVILEGE] [-C CONSTRAINT] [-D DAYS]
                                   [-c CONFIG]
                                   {list,add,delete,copy,token,showtoken} [policy_names ...]

positional arguments:
  {list,add,delete,copy,token,showtoken}
                        Action
  policy_names          Policy name (for 'copy' arg 2 policies)

options:
  -h, --help            show this help message and exit
  -p POLICY, --policy POLICY
                        Policy content (json)
  -s SUBJECT, --subject SUBJECT
                        subject/user to add or delete from policy and for showing or generating tokens
  -R RESOURCE, --resource RESOURCE
                        Resource to add or delete from policy
  -P PRIVILEGE, --privilege PRIVILEGE
                        Privilege to add or delete from policy
  -C CONSTRAINT, --constraint CONSTRAINT
                        Constraint to add or delete from policy
  -D DAYS, --days DAYS  Days before expiring from now on.
  -c CONFIG, --config CONFIG
                        HDLFs config in '.hdlfscli.config.json'
```

### Examples

List all policies
```shell
% hdlpolicy list
```
![hdlpolicy_list](images/hdlpolicy_list.png)

Copy policy
```shell
% hdlpolicy copy de_region nl_region
```

Add resource to policy
```shell
% hdlpolicy add nl_region -R share:crm
```

Delete subject/user to policy
```shell
% hdlpolicy delete nl_region -s user:de_admin
```

Add subject/user to policy
```shell
% hdlpolicy add nl_region -s user:hr_nl
```

Create token for user
```shell
% hdlpolicy token -s hr_nl
```
![hdlpolicy_token](images/hdlpolicy_token.png)

## hdlclient - Delta Sharing Client

```shell
hdlclient -h
usage: hdlclient [-h] [-r] [-p PATH] [-m] [-v VERSION] [-e END_VERSION] [-c CONFIG] [-H] [-s]
                 profile {list,download,metadata} [target ...]

positional arguments:
  profile               Profile of delta sharing
  {list,download,metadata}
                        Action
  target                (optional) Target: <share> [<schema>] [<table>]].

options:
  -h, --help            show this help message and exit
  -r, --recursive       Sync files with hana
  -p PATH, --path PATH  Directory to store data.
  -m, --meta            Download metadata as csn-file to edit before starting the replication.
  -v VERSION, --version VERSION
                        Start version (Warning: overruled by metadata stored version)
  -e END_VERSION, --end_version END_VERSION
                        Version end
  -c CONFIG, --config CONFIG
                        Config-file for HANA access (yaml with url, user, pwd, port)
  -H, --Hana            Upload to hana
  -s, --sync            Sync files with hana

```

### Examples

List avaliable shares
```shell
% hdlclient admin list -r

shares
├── sbm
├── hxm
│   └── us
│       └── employees
└── crm
    └── us
        └── customer

% hdlclient hxm_md list

shares
└── hxm
    └── us
        └── employees

```


