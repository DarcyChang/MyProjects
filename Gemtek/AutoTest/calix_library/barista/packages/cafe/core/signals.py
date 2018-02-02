__author__ = 'kelvin'

#Python code failure signal: signal code block 0100-500
CODE_EXCEPTION_RAISED = "code: 0101 - code exception raised"
CODE_PARAM_FILE_ERROR = "code: 0102 - param file error"

#response map failure signal: signal code block 0401 - 0500
RESPONSE_MAP_ERROR = "code: 0401 - response map error"
RESPONSE_MAP_MATCH_NOT_FOUND_ERROR = "code: 0402 - response map match not found error"
RESPONSE_MAP_MATCH_GROUP_NOT_EXIST_ERROR = "code: 0403 - response map match group not found error"

#topology failure signal: signal code block 0501 - 0600
TOPOLOGY_ERROR = "code: 0501 - topology error"

#util error signal: singal code block 0601-0700
GENERATOR_INVALID_EXPRESSION = 'code: 0601 - invalid generator expression'
GENERATOR_INVALID_PARAMETER = 'code: 0602 - invalid generator parameter'
GENERATOR_INVALID_POOL_EXPRESSION = 'code: 0603 - invalid generator pool expression'

#SESSION failure signal: singal code block 1000-1099
SESSION_ID_ALREADY_EXIST = "code: 1001 - session id already existed"
SESSION_TYPE_NOT_SUPPORTED = "code: 1002 - session type not supported"
SESSION_SSH_INVALID_INPUT = "code: 1011 - ssh invalid input argument"
SESSION_SSH_LOGIN_FAILED = "code: 1012 - ssh login failed"
SESSION_SSH_LOSS_OF_CONNECTION = "code: 1013 - ssh loss of connection"
SESSION_SSH_RECEIVE_ERROR = "code: 1014 - ssh receive error"
SESSION_SSH_ERROR = "code: 1015 - ssh error"

SESSION_WINEXE_LOGIN_FAILED = "code: 1016 - winexe login failed"

SESSION_TELNET_INVALID_INPUT = "code: 1021 - telnet invalid input argument"
SESSION_TELNET_LOGIN_FAILED = "code: 1022 - telnet login failed"
SESSION_TELNET_LOSS_OF_CONNECTION = "code: 1023 - telnet loss of connection"
SESSION_TELNET_RECEIVE_ERROR = "code: 1024 - telnet receive error"
SESSION_TELNET_ERROR = "code: 1025 - telnet error"
SESSION_SHELL_TIMEOUT = "code: 1026 - shell session execute command timeout"


SESSION_MANAGER_ERROR = "code: 1031 - session manager error"
SESSION_SERVER_ERROR = "code: 1041 - session server error"

SESSION_TCL_ERROR = "code: 1051 - tcl session error"
SESSION_SHELL_ERROR = "code: 1061 - shell session error"
SESSION_NETCONF_ERROR = "code: 1071 - netconf session error"
SESSION_RESTFUL_ERROR = "code: 1081 - RESTFUL session error"



#DB failure signal: signal code block 2000-2099
DB_CONNECT_FAILED = "code: 2001 - database connect FAILED"
DB_TESTSUITE_CREATE_FAILED = "code: 2002 - test suite create FAILED"
DB_TESTCASE_CREATE_FAILED = "code: 2003 - test case create FAILED"
DB_TESTSTEP_CREATE_FAILED = "code: 2004 - test step create FAILED"
DB_TESTSUITE_EDIT_FAILED = "code: 2005 - test suite edit FAILED"
DB_TESTCASE_EDIT_FAILED = "code: 2006 - test case edit FAILED"
DB_TESTSUITE_GET_ID_FAILED = "code: 2007 - test suite id get FAILED"
DB_TESTCASE_GET_ID_FAILED = "code: 2008 - test case id get FAILED"

#Calix equipment
#EXA failure signal: signal code block 3000-3099
EXA_SESSION_ERROR = "code: 3001 - exa session error"

#Calix equipment
#E7 failure signal: signal code block 3100-3199
E7_SESSION_ERROR = "code: 3101 - e7 session error"

#3rd party equipment
#STC failure signal: signal code block 4000-4099
STC_SESSION_ERROR = "code: 4001 - stc session error"

#GUI session formmap
FORMMAP_SESSION_ERROR = "code: 5001 - gui session error"
FORMMAP_ELEMENT_ERROR = "code: 5002 - gui element error"

#IXIA failure signal: signal code block 4000-4099
IXIA_SESSION_ERROR = "code: 6001 - ixia session error"
