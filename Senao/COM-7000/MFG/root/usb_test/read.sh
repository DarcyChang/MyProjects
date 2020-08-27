#!/bin/bash

hdparm -t --direct /dev/sdf3 | tee /tmp/sdf3 &
hdparm -t --direct /dev/sdc | tee /tmp/sdc &
hdparm -t --direct /dev/sdd | tee /tmp/sdd &
hdparm -t --direct /dev/sde | tee /tmp/sde &
