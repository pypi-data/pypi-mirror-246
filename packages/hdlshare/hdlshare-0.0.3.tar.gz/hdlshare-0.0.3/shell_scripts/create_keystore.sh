#!/bin/zsh

CERTIFICATE_PATH=certificates
PASSPHRASE=password12

#keytool -importkeystore -destkeystore $KEY_STORE_SRC_PATH/keystore.jks -deststorepass $PASSPHRASE -deststoretype PKCS12 -srcstoretype PKCS12 -srckeystore $KEY_STORE_SRC_PATH_TENANT1/keystore.jks -srcstorepass $PASSPHRASE -noprompt
echo "Add first certificate to new keystore: $CERTIFICATE_PATH/keystore.jks"
keytool -importkeystore -destkeystore $CERTIFICATE_PATH/keystore.jks -deststorepass $PASSPHRASE -deststoretype PKCS12 -srcstoretype PKCS12 -srckeystore $CERTIFICATE_PATH/hdlmt1.p12 -srcstorepass $PASSPHRASE -noprompt

#keytool -importkeystore -destkeystore $KEY_STORE_SRC_PATH/keystore.jks -deststorepass $PASSPHRASE -deststoretype PKCS12 -srcstoretype PKCS12 -srckeystore $KEY_STORE_SRC_PATH_TENANT2/keystore.jks -srcstorepass $PASSPHRASE -noprompt
echo "Add first certificate to new keystore: $CERTIFICATE_PATH/keystore.jks"
keytool -importkeystore -destkeystore $CERTIFICATE_PATH/keystore.jks -deststorepass $PASSPHRASE -deststoretype PKCS12 -srcstoretype PKCS12 -srckeystore $CERTIFICATE_PATH/hdlmt2.p12 -srcstorepass $PASSPHRASE -noprompt

keytool -list -keystore $CERTIFICATE_PATH/keystore.jks -storepass $PASSPHRASE -v