*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${not_confirm_email}    jamie_chang@gemteks.com
${email_password}    support1234

*** Test Cases ***
tc_AndroidAPP_018_Account_Settings_Create_account_Register_account_but_didn't_confirm_the_Email
    [Documentation]  tc_AndroidAPP_018_Account_Settings_Create_account_Register_account_but_didn't_confirm_the_Email
    ...    1. Launch the app and into the Login page.
    ...    2. Try to use email to login account but didn't confirm the Email.
    ...    3. Check the status.
    [Tags]   @TCID=WRTM-326ACN-209    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and into the Login page
    Try to use email to login account but didn't confirm the Email
    Check the status

*** Keywords ***
Launch the app and into the Login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP
    Wait Until Page Contains Element    ${email}    timeout=60

Try to use email to login account but didn't confirm the Email
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${email}    ${not_confirm_email}
    Input Text    ${password}    ${email_password}
    touch sign in

Check the status
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Wait Until Page Contains    Please confirm your email address. We will re-send the activation mail to you.
    Click Element    ${email_resend}
    Wait Until Page Contains    We will send a confirmation email to the following email address to make sure you own the email address connected to your account.
    Page Should Contain Text    ${not_confirm_email}
    Click Element    ${end_btn}
    Wait Until Page Contains    Please follow the instructions in the email to verify your email.
    Click Element    ${Done_btn}
    Wait Until Page Contains Element    ${email}    timeout=60

*** comment ***
2017-12-26    Leo_Li
Init the script