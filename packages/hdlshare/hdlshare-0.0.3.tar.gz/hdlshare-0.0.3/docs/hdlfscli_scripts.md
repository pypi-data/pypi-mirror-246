
# hdlfscli scripts

## Create JWT

### Save to file 

```shell
hdlfscli jwt create  --cert ./certificates/hdlfsdsXPM.pem --key ./certificates/hdlfsdsXPM.key --aud 8b7ffad5-b195-423b-be97-e8a06fc4069b.files.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com --sub usmd > profiles/token_usmd.txt
```

### Save to variable
```shell
TOKEN=`hdlfscli jwt create  --cert ./certificates/hdlfsdsXPM.pem --key ./certificates/hdlfsdsXPM.key --aud 8b7ffad5-b195-423b-be97-e8a06fc4069b.files.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com --sub usmd`; 
echo $TOKEN> ./profiles/token.txt
```

## create token with entitlement
```shell
TOKEN=`hdlfscli jwt create  --cert ./certificates/hdlfsdsXPM.pem --key ./certificates/hdlfsdsXPM.key --aud 8b7ffad5-b195-423b-be97-e8a06fc4069b.sharing.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com --sub admin -entitlements $(realpath ./entitlements/admin.json) -expiration=$(date -v +47H +"%Y-%m-%dT%H:%M:%SZ")`; echo $TOKEN > ./profiles/token.txt
```

## create token without entitlement
ATTENTION NOT WORKING because aud=.sharing. instead aud=.files.
```shell 
TOKEN=`hdlfscli jwt create  --cert ./certificates/hdlfsdsXPM.pem --key ./certificates/hdlfsdsXPM.key --aud 8b7ffad5-b195-423b-be97-e8a06fc4069b.sharing.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com --sub admin -expiration=$(date -v +47H +"%Y-%m-%dT%H:%M:%SZ")`; echo $TOKEN > ./profiles/token.txt
```

aud FILES
```shell
TOKEN=`hdlfscli jwt create  --cert ./certificates/hdlfsdsXPM.pem --key ./certificates/hdlfsdsXPM.key --aud 8b7ffad5-b195-423b-be97-e8a06fc4069b.files.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com --sub admin -expiration=$(date -v +47H +"%Y-%m-%dT%H:%M:%SZ")`; echo $TOKEN > ./profiles/token.txt
```

```shell
TOKEN=`hdlfscli jwt create  --cert ./certificates/hdlfsdsXPM.pem --key ./certificates/hdlfsdsXPM.key --aud 8b7ffad5-b195-423b-be97-e8a06fc4069b.files.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com --sub admin -expiration="2023-12-22T14:15:16"`; echo $TOKEN > ./profiles/token.txt
```

## Get Shares with certificate
```shell
curl "https://8b7ffad5-b195-423b-be97-e8a06fc4069b.files.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com/sharing/v1/shares" --cert ./certificates/hdlfsdsXPM.pem --key ./certificates/hdlfsdsXPM.key -H "x-sap-filecontainer: 8b7ffad5-b195-423b-be97-e8a06fc4069b" -X GET -v --ipv4 -L
```

## Get Shares with curl and token
```shell
curl "https://8b7ffad5-b195-423b-be97-e8a06fc4069b.sharing.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com/shares/v1/shares" -H "x-sap-filecontainer: 8b7ffad5-b195-423b-be97-e8a06fc4069b" -H "Authorization: Bearer ${TOKEN}" -X GET -v --ipv4 -L
```

```shell
curl "https://8b7ffad5-b195-423b-be97-e8a06fc4069b.files.hdl.bdfsdelta1-hdl-hc-dev.dev-aws.hanacloud.ondemand.com/sharing/v1/shares" -H "x-sap-filecontainer: 8b7ffad5-b195-423b-be97-e8a06fc4069b" -H "Authorization: Bearer ${TOKEN}" --cert ./certificates/hdlfsdsXPM.pem --key ./certificates/hdlfsdsXPM.key -H "x-sap-filecontainer: 8b7ffad5-b195-423b-be97-e8a06fc4069b" -X GET -v --ipv4 -L
```
