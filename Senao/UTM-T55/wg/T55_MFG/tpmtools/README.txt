
CHECK THE TPM AND VERIFY BASIC FUNCTIONALITY:
=============================================

Presumptions:
  The UNIT is running Linux.
  The UNIT is running a version of CentOS or a version of RHEL.
  Read Pre-requisites.txt

Check if you have the modules:

 $ ls -la /lib/modules/`uname -r`/kernel/drivers/char/tpm

Check if ti already loaded:
 $ lsmod | grep tpm

Load modules:
 $ sudo /sbin/modprobe tpm_bios
 $ sudo /sbin/modprobe tpm
 $ sudo /sbin/modprobe tpm_tis interrupts=0 force=1

If no modules found, may be uit is build into the kernel already:

 $ cat /boot/config-4.2.0-42-generic | grep TCG
   CONFIG_TCG_TPM=y
   CONFIG_TCG_TIS=y
   CONFIG_TCG_TIS_I2C_ATMEL=m
   CONFIG_TCG_TIS_I2C_INFINEON=m
   CONFIG_TCG_TIS_I2C_NUVOTON=m
   CONFIG_TCG_NSC=m
   CONFIG_TCG_ATMEL=m
   CONFIG_TCG_INFINEON=m
   CONFIG_TCG_XEN=m
   CONFIG_TCG_CRB=m
   CONFIG_TCG_TIS_ST33ZP24=m
   CONFIG_TCG_TIS_ST33ZP24_I2C=m
   CONFIG_TCG_TIS_ST33ZP24_SPI=m

Sanity check. Should print a lot of things and then:

$ dmesg | grep -C10 tpm
   ...
   tpm_tis tpm_tis: 1.2 TPM (device-id 0x4A10, rev-id 78)

Install trousers and tpm-tools to communicate with TPM device:

 $ sudo yum install trousers tpm-tools trousers-devel

Check and make sure the tcsd is running:

 $ ps aux | gre tcsd

Check TPM version:

 $ sudo /usr/sbin/tpm_version
   TPM 1.2 Version Info:
   Chip Version:        1.2.7.0
   Spec Level:          2
   Errata Revision:     2
   TPM Vendor ID:       STM 
   TPM Version:         01010000
   Manufacturer Info:   53544d20


USE WG TOOLS TO CREATE THE KEYS
================================

Run the tool which generates the keys.
It happens in 2 parts

  $ ./generate_tpm_keys.sh

USE WG TOOLS TO VERITY THE KEYS
================================

Run the tool which verifies the keys.
Note that to ensure the file system.data was stored properly as part of generate_tpm_keys.sh,
 we need to run this command after a reboot operation. (preferably just before installing Wg-OS )

When do we need to run 'verify_tpm_keys.sh -w'?

	// Do what ever before.
	1. boot Laner MfgOS
	2. create keys (and not verify_tpm_keys.sh right after this)
	3. reboot Laner MfgOS
	4. verify_tpm_keys.sh
	// Do what ever later.

  $ ./verify_tpm_keys.sh

USE WG REPORTING TOOL TO EXAMING FOR ANY ERRORS
===============================================

Run the tool which generates the report.

  $ ./generate_report.sh

If you did re-run the tool, it will apend to the same log.
So, always review beginning from last found "STAGE0"

Begining looks like:
  STAGE0: ====== getting started ======
Example for SUCCESS:
  STAGE1: SUCCESS: Took ownership of the TPM
Example for FAIL:
  STAGE4: FAILED: WG-Sealing.openssl.pem does not exist

Any 'FAILED' in the report has to be treated a failure.
Either retry and contact US.

This will produce a output on the console that looks like sample.console.log.
You will find 2 keys in there. 

Example of what to scrape:

+++++++ WGTPM BINDING key BEGINS HERE +++++++++:
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1RV5hsnyMQQaH0RkNteu
NoEqa/sOOL15+PUtG7fYuFd6v0IzQLMGLlru5Od20xb1tEsKVtMatC0UMnz25xtp
RCsmvieWY2f69B3zDewzrO2O2exRl/hKmzRU3kmbep3kCdtdrQqOcrKc3A+U1A3e
nKIPjtLI22wP1W68JYL8gJEd5H0WsE/iP3owBp7yxDE6Dds1Q9XJ0k6MWdjiDCLp
4dwl0ECry0m7sG3P54icNGKzbSTE7Sz4mQYEiIQ3Dbv9Uve5tt8CVfWF796dBchN
NLPrjgI9f12+/TwebSC8tcRhqhagVK5MqDentgtrOlPgLefyxPtAECCspM7KvCqT
vwIDAQAB
-----END PUBLIC KEY-----
+++++++  WGTPM BINDING key ENDS HERE  +++++++++:


+++++++ WGTPM SIGNING key BEGINS HERE +++++++++:
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvf2m5Wkp7GLuFXs/yD5J
HSe9IHLe+CjWmfpeHtzPbjgMTma/u9hoCcuVP2dcCfblqNb3NC8MUrozxu81yGoN
BkSYdQ2tOVb5U79SoY1cq49rayxQYE7WrPNBFktM3bUSdvKmUklwS5wLlqqP1tPq
/g34QdtU5yXVfFq0tN6ttFk+wefMzXf0xGskQSiW9SiAwh3iNKamarxqc0s634kE
+o2QJYWiKz8apPJHtXj+LfIAAZngrV15+yKrn8+fboRo58DTXYXM/kjP26hLJMSZ
edCrT3BqIknDoGO7zhkM3Clh51DZjPBJaPoMJo1ZWM/+nu6DG2edxm1p8CEfKMjE
lwIDAQAB
-----END PUBLIC KEY-----
+++++++  WGTPM SIGNING key ENDS HERE  +++++++++:

REPORTING BUGS/ISSUES:
======================

Incase of any issue, grab the logs directory as below and send an email
  # tar -zcvf logs.tar.gz logs

