#!/bin/sh

file="logs/stage.txt"
if [ -e $file ]; then
   echo "WG tpm programming report:"
   cat $file
else
  echo "FAILED: $file does not exist"
  exit 1
fi
