#!/bin/sh

if [ ! -d logs ]; then
  mkdir logs
fi
echo "STAGE0: ====== key-generation: getting started ======" >> logs/stage.txt
tpm_version -l debug     >> logs/version.info
tpm_getpubek -z -l debug >> logs/getpubek.info

tpm_takeownership -y -z -l debug >> logs/takeownership.log
RESULT=$?
if [ $RESULT -ne 0 ]; then
  if [ "$1" = "--force" -o "$1" = "-f" ]; then
    echo "STAGE1: FAILED: Could not take ownership of the TPM" \
	  >> logs/stage.txt
    echo "STAGE1: FAILED: tpm_owner: operation forced, NOT a good practice." \
	  >> logs/stage.txt
    echo "STAGE1: FAILED: tpm_owner: Please TPM_CLEAR and try again ..." \
	  >> logs/stage.txt
    echo "STAGE1: FAILED: tpm_owner: If it is just for debugging, uncomment the 'exit' under this statment and try again" \
	  >> logs/stage.txt
    exit 1
  else
    echo "STAGE1: FAILED: Could not take ownership of the TPM" \
	  >> logs/stage.txt
    exit 1
  fi
else
  echo "STAGE1: SUCCESS: Took ownership of the TPM" \
	  >> logs/stage.txt
fi

./create_register_key >> logs/create_key.log
RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo "STAGE2: FAILED: create the TPM keys" \
	  >> logs/stage.txt
  exit 1
else
  echo "STAGE2: SUCCESS: Created the TPM keys" \
	  >> logs/stage.txt
fi

# time to store the keys away with WG provided tool
./store_systemdata -s -f  /var/lib/tpm/system.data >> logs/store_systemdata.log
RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo "STAGE2: FAILED: store system.data to config block space" \
	  >> logs/stage.txt
  exit 1
else
  echo "STAGE2: SUCCESS: stored system.data to config block space" \
	  >> logs/stage.txt
fi

./load_key            >> logs/load_key.log
RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo "STAGE2: FAILED: load the TPM keys" \
	  >> logs/stage.txt
  exit 1
else
  echo "STAGE2: SUCCESS: Loaded the TPM keys" \
	  >> logs/stage.txt
fi

./openssl-keywrapper  >> logs/openssl.log
RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo "STAGE3: FAILED:generating openssl formatted PEM keys \
	  for BIND/SIGN keys" >> logs/stage.txt
  exit 1
else
  echo "STAGE3: SUCCESS: Generating openssl formatted PEM keys \
	  for BIND/SIGN keys" >> logs/stage.txt
fi

file="WG-Binding.openssl.pem"
if [ -e $file ]; then
   echo "+++++++ WGTPM BINDING key BEGINS HERE +++++++++:"
   cat $file
   echo "+++++++  WGTPM BINDING key ENDS HERE  +++++++++:"
else
  echo "STAGE4: FAILED: $file does not exist" >> logs/stage.txt
  exit 1
fi

file="WG-Signing.openssl.pem"
if [ -e $file ]; then
   echo "+++++++ WGTPM SIGNING key BEGINS HERE +++++++++:"
   cat $file
   echo "+++++++  WGTPM SIGNING key ENDS HERE  +++++++++:"
else
  echo "STAGE4: FAILED: $file does not exist" >> logs/stage.txt
  exit 1
fi
