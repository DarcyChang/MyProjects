#!/bin/sh -x

if [ ! -d logs ]; then
  mkdir logs
fi

echo "STAGE1: ====== verification: getting started ======" >> logs/stage.txt
tpm_version -l debug     >> logs/version.info

# Do We see WG NVinfo defined
tpm_nvinfo -l debug | grep "NVRAM index   : 0x00011120"  >> logs/nvinfo.log
RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo "STAGE1: FAILED: Could not find WG nvinfo on the TPM" \
	  >> logs/stage.txt
  exit 1
else
  echo "STAGE1: SUCCESS: Found WG nvinfo on the TPM" \
	  >> logs/stage.txt
fi

# restore system.data from WG config space
./store_systemdata -r -f /var/lib/tpm/system.data >> logs/restore-systemdata.txt
RESULT=$?
if [ $RESULT -ne 0 ]; then
  echo "STAGE2: FAILED: restore system.data from config block space" \
          >> logs/stage.txt
  exit 1
else
  echo "STAGE2: SUCCESS: restored system.data from config block space" \
          >> logs/stage.txt
fi

# kill tcsd (AM I running as a super user?)
# let the init restart
#   or
# if the user passes the FLAG "--workaround"/"-w", start it
if [ "$1" = "--workaround" -o "$1" = "-w" ]; then
  killall tcsd && sleep 5 && tcsd && sleep 5
  ps aux | grep tcsd
else
  killall tcsd && sleep 10
  ps aux | grep tcsd
fi

# Now, load the keys and see if we can successfully load them
./load_key            >> logs/load_key-verification.log
RESULT=$?

if [ $RESULT -ne 0 ]; then
  echo "STAGE2: FAILED: create and load the TPM keys" \
	  >> logs/stage.txt
  exit 1
else
  echo "STAGE2: SUCCESS: Created and loaded the TPM keys" \
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
