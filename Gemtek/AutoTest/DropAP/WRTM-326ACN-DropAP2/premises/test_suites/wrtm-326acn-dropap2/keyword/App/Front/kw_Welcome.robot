*** Settings ***
Resource    base.robot

*** Variables ***
${email}    com.dropap.dropap:id/emailEdt
${username}    com.dropap.dropap:id/emailEdt
${password}    com.dropap.dropap:id/passwordEdt
${reset_password_icon}    com.dropap.dropap:id/resetPasswordBtn
${forgot_password_btn}    com.dropap.dropap:id/btnForgotPassword
${reset_password_done}    com.dropap.dropap:id/btnDone
${sign_in}    com.dropap.dropap:id/signInBtn
${email_resend}    com.dropap.dropap:id/buttonDefaultPositive
${end_btn}    com.dropap.dropap:id/sendBtn
${Done_btn}    com.dropap.dropap:id/btnDone
${sign_up}    com.dropap.dropap:id/signUpTxt
${Back_sign_in}    com.dropap.dropap:id/ivBarLeft
${sign_up_username}    com.dropap.dropap:id/nameEdt
${sign_up_email}    com.dropap.dropap:id/emailEdt
${sign_up_password}    com.dropap.dropap:id/passwordEdt
${create_new_account}    com.dropap.dropap:id/btnCreateAccount
${OK_button}    com.dropap.dropap:id/positiveBtn
${facebook_sign_in}    com.dropap.dropap:id/facebookBtn
${twitter_sign_in}    com.dropap.dropap:id/twitterBtn
${googleplus_sign_in}    com.dropap.dropap:id/googleplusBtn

${Configure_DropAP_btn}    com.dropap.dropap:id/btnWithBackground
${Set_Up_Your_DropAP}    com.dropap.dropap:id/btnWithBackground
${Bind_the_Existing_DropAP_Router_btn_master}    com.dropap.dropap:id/btnWithoutBackground
${Change_Internet_Connection_Type_btn}    com.dropap.dropap:id/btnWithoutBackground
${add_a_DropAP}    com.dropap.dropap:id/tvAddDropAP
${Bind_the_Existing_DropAP_Router_btn_slave}    com.dropap.dropap:id/tvBindExistDropAP
${DropAP_is_powered_on}    com.dropap.dropap:id/btnPositive
${plugged_in_the_ethernet_cable}    com.dropap.dropap:id/btnPositive
${next_step}    com.dropap.dropap:id/btnPositive
${OK_btn}    com.dropap.dropap:id/btnOK
${internet_connection_next}    com.dropap.dropap:id/btnNext
${internet_connection_retry}    com.dropap.dropap:id/btnRetry
${Change_Internet_Connection_Type_btn}    com.dropap.dropap:id/btnChangeConfig


${Input_Authorization_Code}    com.dropap.dropap:id/etEnterMasterCode
${Enter}    com.dropap.dropap:id/ivEnter
${add_success_info}    com.dropap.dropap:id/tvInfo
${Sent_Authorization_Request}    com.dropap.dropap:id/btnSendRequest
${ok_Request_send}    com.dropap.dropap:id/positiveBtn

${account_info_menu}    com.dropap.dropap:id/menuImg
${close_account_info_menu}    com.dropap.dropap:id/menuImg
${Account_username}    com.dropap.dropap:id/userNameTxt
${Account_useremail}    com.dropap.dropap:id/userEmailTxt

${Set_Up_a_New_DropAP_btn}    com.dropap.dropap:id/btnSetUpNewDropAP
*** Keywords ***
input email
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${email}    ${g_app_email}

input username
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${username}    ${g_app_username}

input password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${password}    ${g_app_password}

touch sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${sign_in}

wait sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains Element    ${username}    timeout=20

touch sign up
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${sign_up}
    sleep  1

touch Back sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Back_sign_in}

input sign up username
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${sign_up_username}    ${g_app_username}

input sign up email
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${sign_up_email}    ${sign_up_email_info}

input sign up password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${sign_up_password}    ${g_app_password}

touch create new account
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    Click Element    ${create_new_account}
    sleep  1

touch facebook sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${facebook_sign_in}
    sleep  1

touch twitter sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${twitter_sign_in}
    sleep  5

touch google+ sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${googleplus_sign_in}
    sleep  5

verify facebook sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${facebook_sign_in}

verify twitter sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${twitter_sign_in}

verify googleplus sign in
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${googleplus_sign_in}


touch add a DropAP
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${add_a_DropAP}
    sleep    1

touch DropAP is powered on
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${DropAP_is_powered_on}

touch plugged in the ethernet cable
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${plugged_in_the_ethernet_cable}

touch next step
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${next_step}

touch Input Authorization Code
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Input_Authorization_Code}

touch Enter
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Enter}

touch Sent Authorization Request
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Sent_Authorization_Request}

touch ok Request send
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${ok_Request_send}


touch account info menu
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${account_info_menu}

touch close account info menu
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${close_account_info_menu}

verify Account username
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Account_username}

verify Account useremail
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Account_useremail}

wait Bind the Existing DropAP Router Slave
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Page Contains Element    ${Bind_the_Existing_DropAP_Router_btn_slave}    timeout=60

touch reset password icon
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${reset_password_icon}

reset password
    [Documentation]
    [Arguments]    ${reset_email}
    [Tags]   @AUTHOR=Gavin_Chang
    Input Text    ${email}    ${reset_email}
    Click Element    ${forgot_password_btn}
    Wait Until Page Contains Element    ${reset_password_done}    timeout=30
    Click Element    ${reset_password_done}

*** comment ***
2017-11-24     Leo_Li
Modified one Keywords content

2017-11-10     Leo_Li
Init basic AP common keywords