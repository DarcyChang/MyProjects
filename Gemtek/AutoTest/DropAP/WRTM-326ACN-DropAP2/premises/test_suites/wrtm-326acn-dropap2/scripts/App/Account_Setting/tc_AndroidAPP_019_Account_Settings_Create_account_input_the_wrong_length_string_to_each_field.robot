*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${sign_up_username_two_words}    gm
${sign_up_username_twenty_one_words}    supportsupportsupport
${sign_up_username_twenty_words}    adminadminadminadmin
${username_note_info}    Username should be between 3 to 20 characters
${sign_up_email_fifty_words}    adminadminadminadminadminadminadminadminadminadmin
${not_valid_Email_info}    Email is not valid
${sign_up_normal_email}    admin@gemtek.com
${sign_up_password_seven_words}    support
${sign_up_password_sixteen_words}    useruseruseruser
${password_note_info}    Password should be between 8 to 15 characters. Spaces or symbols is not allowed.

*** Test Cases ***
tc_AndroidAPP_019_Account_Settings_Create_account_input_the_wrong_length_string_to_each_field
    [Documentation]  tc_AndroidAPP_019_Account_Settings_Create_account_input_the_wrong_length_string_to_each_field
    ...    1. Launch the app and go to login page.
    ...    2. Press the ""Sign up"" at Sign in page.
    ...    3. Input the 2 words in username field.
    ...    4. Press register button.
    ...    5. Input the 21 words in username field.
    ...    6. Press register button.
    ...    7. Input the 20 words in username field.
    ...    8. Input the long length in email field.    #over 50 word
    ...    9. Press register button
    ...    10. Input the normal length in email field.
    ...    11. Press register button.
    ...    12. Input the 7 words in password.
    ...    13. Press register button.
    ...    14. Input the 16 words in password.
    ...    15. Press register button.
    [Tags]   @TCID=WRTM-326ACN-365    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to login page
    Press the Sign up at Sign in page
    Input the 2 words in username field
    Press register button
    Input the 21 words in username field
    Sceond Press register button                   #same name defined multiple times
    Input the 20 words in username field
    Input the long length in email field
    Third Press register button                    #same name defined multiple times
    Input the normal length in email field
    Fourth Press register button                   #same name defined multiple times
    Input the 7 words in password
    Fifth Press register button                    #same name defined multiple times
    Input the 16 words in password
    Sixth Press register button                    #same name defined multiple times

*** Keywords ***
Launch the app and go to login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP

Press the Sign up at Sign in page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch sign up

Input the 2 words in username field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${sign_up_username}    ${sign_up_username_two_words}

Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${username_note_info}
    Click Element    ${OK_button}

Input the 21 words in username field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Clear Text    ${sign_up_username}
    Hide Keyboard
    Input Text    ${sign_up_username}    ${sign_up_username_twenty_one_words}

Sceond Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${username_note_info}
    Click Element    ${OK_button}

Input the 20 words in username field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Clear Text    ${sign_up_username}
    Hide Keyboard
    Input Text    ${sign_up_username}    ${sign_up_username_twenty_words}

Input the long length in email field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${sign_up_email}    ${sign_up_email_fifty_words}

Third Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${not_valid_Email_info}
    Click Element    ${OK_button}

Input the normal length in email field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Clear Text    ${sign_up_email}
    Hide Keyboard
    Input Text    ${sign_up_email}    ${sign_up_normal_email}

Fourth Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${password_note_info}
    Click Element    ${OK_button}

Input the 7 words in password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${sign_up_password}    ${sign_up_password_seven_words}

Fifth Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${password_note_info}
    Click Element    ${OK_button}

Input the 16 words in password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Clear Text    ${sign_up_password}
    Hide Keyboard
    Input Text    ${sign_up_password}    ${sign_up_password_sixteen_words}

Sixth Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${password_note_info}
    Click Element    ${OK_button}

*** comment ***
2017-12-05    Leo_Li
Init the script