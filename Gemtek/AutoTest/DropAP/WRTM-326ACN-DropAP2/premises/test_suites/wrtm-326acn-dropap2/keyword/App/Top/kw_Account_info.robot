*** Settings ***
Resource    base.robot

*** Variables ***
${account_info_menu}    com.dropap.dropap:id/menuImg
${account_uesername}    com.dropap.dropap:id/userNameTxt
${add_dropap}    com.dropap.dropap:id/addDeviceTxt
${buy_dropap}    com.dropap.dropap:id/buyDropAPTxt
${buy_dropap_web}    android:id/content
${user_manual}    com.dropap.dropap:id/userManualTxt
${user_manual_web}    android:id/content
${contact_us}    com.dropap.dropap:id/contactUsTxt
${contact_us_web}    android:id/content
${about}    com.dropap.dropap:id/aboutTxt
${about_web}    android:id/content
${sign_out}    com.dropap.dropap:id/signInOutTxt
${sign_out_web}    com.dropap.dropap:id/imvSignIn
${privacy_policy}    com.dropap.dropap:id/privacyTxt
${privacy_policy_web}    android:id/content
${version}    com.dropap.dropap:id/versionTxt
${version_info}    com.dropap.dropap:id/versionInfoTxt

*** Keywords ***
touch account menu
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${account_info_menu}
    sleep  1

touch close account info menu
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${account_info_menu}
    sleep  1

verify account info menu
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${account_info_menu}

touch add dropap
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${add_dropap}
    sleep  1

touch buy dropap
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${buy_dropap}
    sleep  1

touch user manual
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${user_manual}
    sleep  1

touch contact us
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${contact_us}
    sleep  1

touch about
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${about}
    sleep  1

touch sign out
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${sign_out}

touch privacy policy
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${privacy_policy}

verify the account info
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element     ${add_dropap}
    Page Should Contain Element     ${buy_dropap}
    Page Should Contain Element     ${user_manual}
    Page Should Contain Element     ${contact_us}
    Page Should Contain Element     ${about}
    Page Should Contain Element     ${sign_out}
    Page Should Contain Element     ${privacy_policy}
    Page Should Contain Element     ${version}
    Page Should Contain Element     ${version_info}

verify Buy DropAP web status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${buy_dropap_web}

verify user manual web status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${user_manual_web}

verify contact us web status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${contact_us_web}

verify privacy policy web status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${privacy_policy_web}

verify about web status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${about_web}

verify sign out web status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${sign_out_web}

verify app version web status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${version_info}

wait Buy DropAP web
    Wait Until Page Contains Element    ${buy_dropap_web}    timeout=30

wait user manual web
    Wait Until Page Contains Element    ${user_manual_web}    timeout=30

wait contact us web
    Wait Until Page Contains Element    ${contact_us_web}    timeout=30

wait about web
    Wait Until Page Contains Element    ${about_web}    timeout=30

wait sign out web
    Wait Until Page Contains Element    ${sign_out_web}    timeout=30

wait privacy policy web
    Wait Until Page Contains Element    ${privacy_policy_web}    timeout=30

*** comment ***
2017-11-10     Leo_Li
Init basic AP common keyword
