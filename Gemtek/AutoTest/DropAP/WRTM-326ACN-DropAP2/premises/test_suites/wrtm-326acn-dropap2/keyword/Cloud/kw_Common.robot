*** Settings ***
Resource    base.robot
Library    ImapLibrary
Library           RequestsLibrary
Library           Collections
Library  Process
Library  DateTime
Library  String
*** Variables ***

${g_cloud_deviceInfo}   {"name": "My Device"}
${g_cloud_time}     20170925
${g_cloud_get_auth}     ${true}
${g_cloud_profile}  ${true}
${domainName80}  https://s5-dropap.securepilot.com:80

${pin}      18833648
${002dst}  600097052
${qos}      qos1
${expire}   10000

${command}  wget -d -O test.img "urlhere"
${cwd}  /home/vagrant/Downloads/
${cwd_online}  /home/vagrant/Downloads/online_tool

${android_text}   AAEAAAAAAED//wAAADoAAAAAAAIAAQABAAAAAgABAAIAAAAMZXZlbnRfbm90aWZ5AAMAAAASeyJldmVudF90eXBlIjoiMSJ9

${unregisterUser}   jennie566
${unregisterEmail}   tm8961532@gmail.com
${verifiedEmail}  jill_chou@gemteks.com
${verifiedemail2}  devopsreport@gemteks.com
#${unverifiedEmail}  jill_chou@gemteks.com
#${verifiedEmail}  devopsreport@gemteks.com
${unverifiedUser}   unverify_test01
${unverifiedEmail}   devopsautotest@gmail.com


*** Keywords ***


set user online and waiting
    [Tags]     @AUTHOR=Jill_Chou
    ${output}=  start process    node client2.js   shell=True     cwd=${cwd_online}   alias=myproc
    [Return]   ${output}


Get device status api
    [Tags]     @AUTHOR=Jill_Chou
    [arguments]  ${deviceId}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   cloudId=${deviceId}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/get_device    headers=${headers}      data=${data}
    ${resp}=  To Json  ${resp.content}
    Delete All Sessions
    [Return]   ${resp}


Cloud login by facebook
    [Tags]     @AUTHOR=Jill_Chou
    Create Session  S5  ${g_cloud_domainName}
    ${about}=  create list  {}
    ${data}   Create Dictionary   identifier=Autotest     name=autotest    about=${about}   api_key=${g_cloud_apiKey}   api_token=${g_cloud_apiToken}  time=${g_cloud_time}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /social/v1/login/facebook    headers=${headers}      data=${data}
    Delete All Sessions
    [Return]   ${resp}

Cloud login by google
    [Tags]     @AUTHOR=Jill_Chou
    Create Session  S5  ${g_cloud_domainName}
    ${about}=  create list  {}
    ${data}   Create Dictionary   identifier=Autotest     name=autotest    about=${about}   api_key=${g_cloud_apiKey}   api_token=${g_cloud_apiToken}  time=${g_cloud_time}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /social/v1/login/google    headers=${headers}      data=${data}
    Delete All Sessions
    [Return]   ${resp}

Cloud login by twitter
    [Tags]     @AUTHOR=Jill_Chou
    Create Session  S5  ${g_cloud_domainName}
    ${about}=  create list  {}
    ${data}   Create Dictionary   identifier=Autotest     name=autotest    about=${about}   api_key=${g_cloud_apiKey}   api_token=${g_cloud_apiToken}  time=${g_cloud_time}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /social/v1/login/twitter    headers=${headers}      data=${data}
    Delete All Sessions
    [Return]   ${resp}

check fb login success
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    [Arguments]     ${resp}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1211

set mosquitto_sub user waiting
    [Tags]     @AUTHOR=Jill_Chou
    ${output}=  start process    mosquitto_sub -h 54.254.196.218 -p 80 -u 600097052 -P 83551832 -t "client/600097052/600097052-HA"    shell=True     alias=myproc
    [Return]   ${output}


Generate comment line
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]  ${url}
    ${result}=  Replace String  ${command}  urlhere  ${url}
    [Return]    ${result}

download file and check md5sum
    ${result}=  Run Process  ${DownloadCommand}  shell=True  cwd=${cwd}  alias=myproc
    ${result2}=  Run Process  md5sum test.img  shell=True   cwd=${cwd}   alias=myproc
    ${stdout}=  Get Process Result  myproc  stdout=true
    [Return]    ${stdout[0:32]}


Cloud request FW version
    [Tags]     @AUTHOR=Jill_Chou
    Create Session    S5    https://dm.dropap.com
    ${resp}    Get Request    S5    /dm/v1/fota/latest?model_name=WRTM-326ACN324A-DropAP
    ${resp}=    To Json  ${resp.content}
    Delete All Sessions
    [Return]    ${resp}

Cloud check FW version
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]  ${versionInfo}
    Should Be Equal As Strings    ${versionInfo['version']}    2.3.14


get the serial number
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${stdout}=${VARIABLE}
    ${num}  Evaluate  int('${stdout[10:17]}')
    ${test2}  Evaluate  int('${num}')-1
    ${test2}  convert to string  ${test2}
    [Return]  ${test2}

cloud get message by
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${serial}=${VARIABLE}  ${token}=${VARIABLE2}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${token.json()['global_session']['token']}     serial=${serial}    api_key=${g_cloud_apiKey}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /mec_msg/v1/get    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Delete All Sessions
    [Return]   ${resp2['ret_msg']['messages'][0]['content']}

set mosquitto_sub waiting
    [Tags]     @AUTHOR=Jill_Chou
     ${output}=  start process    mosquitto_sub -h 54.254.196.218 -p 80 -u 600097052 -P 83551832 -t "client/600097052/600097052-HA"    shell=True     alias=myproc
    [Return]   ${output}

set multi mosquitto_sub waiting
    [Tags]     @AUTHOR=Jill_Chou
     ${output1}=  start process    mosquitto_sub -h 54.254.196.218 -p 80 -u 600097052 -P 83551832 -t "client/600097052/600097052-HA"    shell=True     alias=myproc1
     ${output2}=  start process    mosquitto_sub -h 54.254.196.218 -p 80 -u 600097052 -P 83551832 -t "client/600097052/600097052-HA"    shell=True     alias=myproc2
     ${output3}=  start process    mosquitto_sub -h 54.254.196.218 -p 80 -u 600097052 -P 83551832 -t "client/600097052/600097052-HA"    shell=True     alias=myproc3
    [Return]   ${output1}   ${output2}   ${output3}


cloud device login with
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${deviceid}=${VARIABLE}  ${password}=${VARIABLE2}
    ${auth2}=    Create list   ${deviceid}  ${password}
    #device login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth2}    debug=3
    ${resp}=    Get Request    S5    /v1/device/login
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['status']['code']}    1221
    Delete All Sessions
    [Return]   ${resp}

Send TLV command
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${type}=${VARIABLE}  ${token}=${VARIABLE2}
    ${text}=    Get Current Date
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${token.json()['global_session']['token']}  type=${type}   dst=${002dst}    api_token=${g_cloud_apiToken}   api_key=${g_cloud_apiKey}   time=${g_cloud_time}    text=${text}   qos=${qos}      expire=${expire}

    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /mec_msg/v1/send    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    [Return]  ${resp2}   ${text}


Send TLV command use android format
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${type}=${VARIABLE}  ${token}=${VARIABLE2}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${token.json()['global_session']['token']}  type=${type}   dst=${002dst}    api_token=${g_cloud_apiToken}   api_key=${g_cloud_apiKey}   time=${g_cloud_time}    text=${android_text}   qos=${qos}      expire=${expire}

    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /mec_msg/v1/send    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    [Return]  ${resp2}   ${android_text}

end of process
    [Arguments]  ${output}
    Terminate Process      ${output}
    ${stdout}=  Get Process Result  myproc  stdout=true
    [Return]  ${stdout}

end of multi process
    [Arguments]  ${output1}   ${output2}   ${output3}
    Terminate Process      ${output1}
    ${stdout1}=  Get Process Result  myproc1  stdout=true
    Terminate Process      ${output2}
    ${stdout2}=  Get Process Result  myproc2  stdout=true
    Terminate Process      ${output3}
    ${stdout3}=  Get Process Result  myproc3  stdout=true
    [Return]  ${stdout1}   ${stdout2}  ${stdout3}

cloud reset password request
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=  API request pwd reset  ${verifiedemail2}
    ${resp2}=    To Json  ${resp.content}
    [Return]   ${resp}
    Delete All Sessions

cloud reset password request with unverifiedEmail
    [Tags]     @AUTHOR=Jill_Chou
    ${resp}=  API request pwd reset  ${unverifiedEmail}
    ${resp2}=    To Json  ${resp.content}
    [Return]   ${resp}
    Delete All Sessions

API request pwd reset
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]  ${email}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   email=${email}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/user/request_pwd_reset    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    [Return]   ${resp}


check reset password request success
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
    Should Be Equal As Strings    ${resp1.status_code}    200
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1200

received the email
    [Tags]     @AUTHOR=Jill_Chou
    ${result}=  received mail is  ${verifiedemail2}  devops123  smtp.gmail.com
    [Return]   ${result}

received the unregister email
    [Tags]     @AUTHOR=Jill_Chou
    ${result}=  received mail is  ${unverifiedEmail}   gemtek123  smtp.gmail.com
    [Return]   ${result}

received mail is
    [Arguments]  ${Email}  ${PassWord}  ${host}
    Open Mailbox    host=${host}    user=${Email}    password=${PassWord}
    ${LATEST} =    Wait For Email  sender=no-reply@notice.dropap.com     timeout=300
    ${ret} =   Walk Multipart Email   ${LATEST}
    ${payload} =  Get Multipart Payload  decode=True
    ${ret}    Get Links From Email   ${LATEST}
    ${res} =    Get From List    ${ret}    0
    ${result}=    Get Regexp Matches    ${res}    code=(.*)
    Delete Email    ${LATEST}
    Close Mailbox
    [Return]   ${result}


modify old password to new password
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${result}=${VARIABLE1}   ${password}=${VARIABLE}
    modify old password to new password of  devops_test  ${result}   ${password}

modify unregister old password to new password
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${result}=${VARIABLE1}   ${password}=${VARIABLE}
    modify old password to new password of  ${unverifiedUser}  ${result}   ${password}



modify old password to new password of
    [Arguments]  ${username}  ${result}   ${password}
    Create Session  S5  ${domainName80}
    ${data}   Create Dictionary     username=${username}           code=${result[0][5:77]}     new_pwd=${password}      pwd1=${password}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/user/email_pwd_reset   headers=${headers}      data=${data}
    Delete All Sessions



check new password work
    [Tags]     @AUTHOR=Jill_Chou
    ${auth}=    Create List    devops_test    87654321
    Create Digest Session    S5    ${g_cloud_domainName}    auth=${auth}    debug=3
    ${resp1}=    Get Request    S5    /v1/user/login
    ${resp2}=    To Json  ${resp1.content}
    Should Be Equal As Strings    ${resp1.status_code}    200
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1211
    Delete All Sessions

check unvarify new password work
    [Tags]     @AUTHOR=Jill_Chou
    ${auth}=    Create List    ${unverifiedUser}    87654321
    Create Digest Session    S5    ${g_cloud_domainName}    auth=${auth}    debug=3
    ${resp1}=    Get Request    S5    /v1/user/login
    ${resp2}=    To Json  ${resp1.content}
    Should Be Equal As Strings    ${resp1.status_code}    200
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1211
    Delete All Sessions

change unvarify password back
    [Arguments]     ${password}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   email=${unverifiedEmail}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/user/request_pwd_reset    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Delete All Sessions

    Open Mailbox    host=smtp.gmail.com      user=${unverifiedEmail}    password=gemtek123
    ${LATEST} =    Wait For Email    sender=no-reply@notice.dropap.com     timeout=300
    ${ret} =   Walk Multipart Email   ${LATEST}
    ${payload} =   Get Multipart Payload   decode=True
    ${ret}    Get Links From Email   ${LATEST}
    ${res} =    Get From List    ${ret}    0
    ${result}=    Get Regexp Matches    ${res}    code=(.*)
    Delete Email    ${LATEST}
    Close Mailbox


    Create Session  S5  ${domainName80}
    ${data}   Create Dictionary     username=${unverifiedUser}           code=${result[0][5:77]}     new_pwd=${password}      pwd1=${password}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/user/email_pwd_reset   headers=${headers}      data=${data}
    Delete All Sessions


    ${auth}=    Create List    ${unverifiedUser}    12345678
    Create Digest Session    S5    ${g_cloud_domainName}    auth=${auth}    debug=3
    ${resp1}=    Get Request    S5    /v1/user/login
    ${resp2}=    To Json  ${resp1.content}
    Should Be Equal As Strings    ${resp1.status_code}    200
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1211
    Delete All Sessions

change password back
    [Arguments]     ${password}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   email=devopsreport@gemteks.com
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/user/request_pwd_reset    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Delete All Sessions

    Open Mailbox    host=smtp.gmail.com    user=devopsreport@gemteks.com    password=devops123
    ${LATEST} =    Wait For Email    sender=no-reply@notice.dropap.com     timeout=300
    ${ret} =   Walk Multipart Email   ${LATEST}
    ${payload} =   Get Multipart Payload   decode=True
    ${ret}    Get Links From Email   ${LATEST}
    ${res} =    Get From List    ${ret}    0
    ${result}=    Get Regexp Matches    ${res}    code=(.*)
    Delete Email    ${LATEST}
    Close Mailbox


    Create Session  S5  ${domainName80}
    ${data}   Create Dictionary     username=devops_test            code=${result[0][5:77]}     new_pwd=${password}      pwd1=${password}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/user/email_pwd_reset   headers=${headers}      data=${data}
    Delete All Sessions


    ${auth}=    Create List    devops_test    12345678
    Create Digest Session    S5    ${g_cloud_domainName}    auth=${auth}    debug=3
    ${resp1}=    Get Request    S5    /v1/user/login
    ${resp2}=    To Json  ${resp1.content}
    Should Be Equal As Strings    ${resp1.status_code}    200
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1211
    Delete All Sessions

cloud registration but the password is
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${wrongpassword}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   type=EMAIL  pw=${wrongpassword}  username=testest123  email=${verifiedEmail}   reg_service=CVR  send_mail=${g_cloud_get_auth}  host=s5-dropap.securepilot.com
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp2}  Post Request      S5      /v1/user/registration    headers=${headers}      data=${data}
    [Return]   ${resp2}
    Delete All Sessions

check password not allow
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
    Should Be Equal As Strings    ${resp1.status_code}    400
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1400

cloud registration but the username is
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${wrongUsername}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   type=EMAIL  pw=12345678  username=${wrongUsername}  email=${verifiedEmail}   reg_service=CVR  send_mail=${g_cloud_get_auth}  host=s5-dropap.securepilot.com
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp2}  Post Request      S5      /v1/user/registration    headers=${headers}      data=${data}
    [Return]   ${resp2}
    Delete All Sessions

check user name not allow
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
    Should Be Equal As Strings    ${resp1.status_code}    400
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1400

cloud forget password but the email didn't registered
    [Tags]     @AUTHOR=Jill_Chou
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   email=123@yahoo.com.tw
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/user/request_pwd_reset    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Delete All Sessions
    [Return]   ${resp}

check reset fail
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
    Should Be Equal As Strings    ${resp1.status_code}    200
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1411

cloud registration but the email is
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${wrongEmail}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   type=EMAIL  pw=12345678  username=testesttest  email=${wrongEmail}   reg_service=CVR  send_mail=${g_cloud_get_auth}  host=s5-dropap.securepilot.com
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp2}  Post Request      S5      /v1/user/registration    headers=${headers}      data=${data}
    [Return]   ${resp2}
    Delete All Sessions

check Email not allow
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp2}
    Should Be Equal As Strings  ${resp2.status_code}  400
    Should Be Equal As Strings  ${resp2.json()['status']['code']}   1400

check domain name not allow
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp2}
    Should Be Equal As Strings  ${resp2.status_code}  400
    Should Be Equal As Strings  ${resp2.json()['status']['code']}   1429

check email already registered
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp2}
    Should Be Equal As Strings  ${resp2.status_code}  200
    Should Be Equal As Strings  ${resp2.json()['status']['code']}    1217

User list have no user ID check
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1240
    Should Be Equal As Strings    ${resp.json()['user_list']}      	[]

Cloud device remove user
    [Tags]    @AUTHOR=Jill_Chou
     [Arguments]     ${resp1}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${resp1.json()['global_session']['token']}     api_key=${g_cloud_apiKey}    user_id=${g_cloud_userId}    time=${g_cloud_time}    api_token=${g_cloud_apiToken}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/device/rm_user    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1234
    Delete All Sessions

Cloud device login
    [Tags]    @AUTHOR=Jill_Chou
    ${auth}=    Create List    ${g_cloud_deviceid}    ${g_cloud_devicepw}
    Create Digest Session    S5    ${g_cloud_domainName}    auth=${auth}    debug=3
    ${resp1}=    Get Request    S5    /v1/device/login
    Should Be Equal As Strings    ${resp1.status_code}    200
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1221
    [Return]  ${resp1}

Cloud device binding user
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
        Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${resp1.json()['global_session']['token']}     api_key=${g_cloud_apiKey}    user_id=${g_cloud_userId}    time=${g_cloud_time}    api_token=${g_cloud_apiToken}   level=0
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/device/add_user    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1231
    Delete All Sessions

Get user list api
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${resp1.json()['global_session']['token']}     api_key=${g_cloud_apiKey}    get_auth=${g_cloud_get_auth}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/device/get_user_list    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Delete All Sessions
    [Return]    ${resp}

User list user ID check
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp}
    Should Be Equal As Strings  ${resp.status_code}  200
    should be equal as strings    ${resp.json()['user_list'][0]['uid']}     ${g_cloud_userid}
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1240

Let APP binging device
    [Tags]    @AUTHOR=Jill_Chou
    Device reset default
    ${resp}=    Cloud user login
    Cloud user binding device   ${resp}

Device reset default
    [Tags]    @AUTHOR=Jill_Chou
    ${auth}=    Create List    ${g_cloud_deviceid}    ${g_cloud_devicepw}
    Create Digest Session    S5    ${g_cloud_domainName}    auth=${auth}    debug=3
    ${resp1}=    Get Request    S5    /v1/device/login
    Should Be Equal As Strings    ${resp1.status_code}    200
    Should Be Equal As Strings    ${resp1.json()['status']['code']}    1221
    Delete All Sessions

    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${resp1.json()['global_session']['token']}     api_key=${g_cloud_apiKey}    time=${g_cloud_time}    api_token=${g_cloud_apiToken}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/device/reset_default    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1227
    Delete All Sessions

    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${resp1.json()['global_session']['token']}     api_key=${g_cloud_apiKey}    get_auth=${g_cloud_get_auth}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/device/get_user_list    headers=${headers}      data=${data}
    ${resp2}=    To Json  ${resp.content}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1240
    Delete All Sessions

Cloud user login
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${g_cloud_User}     ${g_cloud_User_pw}
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    Should Be Equal As Strings    ${resp.status_code}    200
    Should Be Equal As Strings    ${resp.json()['status']['code']}    1211
    [Return]  ${resp}

Cloud user binding device
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${resp1.json()['global_session']['token']}     api_key=${g_cloud_apiKey}    api_token=${g_cloud_apiToken}   time=${g_cloud_time}   level=0     device_id=${g_cloud_deviceId}   pin=${g_cloud_pin}      device_info=${g_cloud_deviceInfo}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp2}  Post Request      S5      /v1/user/add_device    headers=${headers}      data=${data}
    Should Be Equal As Strings  ${resp2.status_code}  200
    Should Be Equal As Strings    ${resp2.json()['status']['code']}      1231
    Delete All Sessions

Cloud user unbinding device
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${resp1.json()['global_session']['token']}     api_key=${g_cloud_apiKey}    api_token=${g_cloud_apiToken}   time=${g_cloud_time}   device_id=${g_cloud_deviceId}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp2}  Post Request      S5      /v1/user/rm_device    headers=${headers}      data=${data}
    Should Be Equal As Strings  ${resp2.status_code}  200
    Should Be Equal As Strings  ${resp2.json()['status']['code']}    1234
    Delete All Sessions

Get account device api
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp1}
    Create Session  S5  ${g_cloud_domainName}
    ${data}   Create Dictionary   token=${resp1.json()['global_session']['token']}     api_key=${g_cloud_apiKey}    api_token=${g_cloud_apiToken}   time=${g_cloud_time}    profile=${g_cloud_profile}
    ${headers}   Create Dictionary   Content-Type=application/json
    ${resp}  Post Request      S5      /v1/user/get_device_list    headers=${headers}      data=${data}
    Delete All Sessions
    [Return]    ${resp}

Device list device ID check
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1232
    Should Be Equal As Strings    ${resp.json()['device_list'][0]['mac']}      	701a05010003

Device list have no device ID check
    [Tags]     @AUTHOR=Jill_Chou
    [Arguments]     ${resp}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1232
    Should Be Equal As Strings    ${resp.json()['device_list']}      	[]

Cloud login but unregister user
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${unregisterUser}       12345678
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    [Return]  ${resp}

Cloud login with email but unregister user
   [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${unregisterEmail}       12345678
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    [Return]  ${resp}

Cloud login but the account already registered and not verified
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${unverifiedUser}       12345678
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    [Return]  ${resp}

check login success
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    [Arguments]     ${resp}
    Should Be Equal As Strings  ${resp.status_code}  200
    Should Be Equal As Strings    ${resp.json()['status']['code']}      1211

Cloud login by email but the account already registered and not verified
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${unverifiedEmail}       12345678
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    [Return]  ${resp}

check login fail
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    [Arguments]     ${resp}
    Should Be Equal As Strings  ${resp.status_code}  401

Cloud login the account already registered and verified
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${g_cloud_User}       12345678
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    [Return]  ${resp}

Cloud login by email but the account already registered and verified
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${verifiedEmail}       12345678
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    [Return]  ${resp}

Cloud login the password is wrong
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${g_cloud_User}       123456789
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    [Return]  ${resp}

Cloud login by email the password is wrong
    [Documentation]
    [Tags]   @AUTHOR=Jill_Chou
    ${auth}=    Create list     ${verifiedEmail}       123456789
    #user login api
    Create Digest Session    S5    ${g_cloud_domainName}    ${auth}    debug=3
    ${resp}=    Get Request    S5    /v1/user/login
    [Return]  ${resp}





*** Comment ***
2017-12-11     Jill_Chou
Init the script

2017-12-14      Jill_Chou
add 22 keyword

2017-12-29    Jill_Chou
add 6 keyword

2018-01-02   Jill_Chou
modify 2 tab error
add 4 keyword