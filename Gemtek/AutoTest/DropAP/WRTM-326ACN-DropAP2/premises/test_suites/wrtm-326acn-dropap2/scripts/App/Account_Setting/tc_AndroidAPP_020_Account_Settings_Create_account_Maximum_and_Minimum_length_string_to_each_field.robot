*** Settings ***
Resource    base.robot
Library     AppiumLibrary

Test Teardown      Close APP

Force Tags    @FEATURE=Account_Setting    @AUTHOR=Leo_Li

*** Variables ***
${sign_up_username_three_words}    gem
${sign_up_not_valid_Spaces_username_words}    g e m
${sign_up_not_valid_symbols_username_words}    !@#$%&
${not_valid_username_info}    User Name is not valid!
${not_valid_Email_info}    Email is not valid
${sign_up_username_twenty_words}    adminadminadminadmin
${sign_up_email_fifty_words}    adminadminadminadminadminadminadminadminadminadmin
${sign_up_not_valid_Spaces_email_words}    a d m i n @ g e m t e k . c o m
${sign_up_not_valid_symbols_email_words}    !#$%&@#$%&.!#$%&
${sign_up_normal_email}    admin@gemtek.com
${sign_up_password_sixteen_words}    useruseruseruser
${password_note_info}    Password should be between 8 to 15 characters. Spaces or symbols is not allowed.
${sign_up_not_valid_Spaces_password_words}    a d m i n
${sign_up_not_valid_symbols_password_words}    !@#$%&
${not_valid_password_info}    Input Password is not valid!

*** Test Cases ***
tc_AndroidAPP_020_Account_Settings_Create_account_Maximum_and_Minimum_length_string_to_each_field
    [Documentation]  tc_AndroidAPP_020_Account_Settings_Create_account_Maximum_and_Minimum_length_string_to_each_field
    ...    1. Launch the app and go to login page.
    ...    2. Press the ""Sign up"" at Sign in page.
    ...    3. Only input the 3 words in username field.
    ...    4. Press register button.
    ...    5. Input the 20 words in username field.
    ...    6. Press register button.
    ...    7. Input the long length in email field.    #over 50 word
    ...    8. Press register button.
    ...    9. Input the normal length in email field.
    ...    10. Press register button.
    ...    11. Input the 16 words in password.
    ...    12. Press register button.
    [Tags]   @TCID=WRTM-326ACN-210    @DUT=WRTM-326ACN     @AUTHOR=Leo_Li
    [Timeout]

    Launch the app and go to login page
    Press the Sign up at Sign in page
    Only input the 3 words in username field
    Press register button
    Input the 20 words in username field
    Sceond Press register button                   #same name defined multiple times
    Input the long length in email field
    Third Press register button                    #same name defined multiple times
    Input the normal length in email field
    Fourth Press register button                   #same name defined multiple times
    Input the 16 words in password
    Fifth Press register button                    #same name defined multiple times

*** Keywords ***
Launch the app and go to login page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Launch APP

Press the Sign up at Sign in page
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch sign up

Only input the 3 words in username field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${sign_up_username}    ${sign_up_username_three_words}

Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${not_valid_Email_info}
    Click Element    ${OK_button}
    Clear Text    ${sign_up_username}
    Input Text    ${sign_up_username}    ${sign_up_not_valid_Spaces_username_words}
    touch create new account
    Page Should Contain Text    ${not_valid_username_info}
    Click Element    ${OK_button}
    Clear Text    ${sign_up_username}
    Input Text    ${sign_up_username}    ${sign_up_not_valid_symbols_username_words}
    touch create new account
    Page Should Contain Text    ${not_valid_username_info}
    Click Element    ${OK_button}


Input the 20 words in username field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Clear Text    ${sign_up_username}
    Input Text    ${sign_up_username}    ${sign_up_username_twenty_words}

Sceond Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${not_valid_Email_info}
    Click Element    ${OK_button}

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
    Clear Text    ${sign_up_email}
    Input Text    ${sign_up_email}    ${sign_up_not_valid_Spaces_email_words}
    touch create new account
    Page Should Contain Text    ${not_valid_Email_info}
    Click Element    ${OK_button}
    Clear Text    ${sign_up_email}
    Input Text    ${sign_up_email}    ${sign_up_not_valid_symbols_email_words}
    touch create new account
    Page Should Contain Text    ${not_valid_Email_info}
    Click Element    ${OK_button}

Input the normal length in email field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Clear Text    ${sign_up_email}
    Input Text    ${sign_up_email}    ${sign_up_normal_email}

Fourth Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    touch create new account
    Page Should Contain Text    ${password_note_info}
    Click Element    ${OK_button}

Input the 16 words in password
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Input Text    ${sign_up_password}    ${sign_up_password_sixteen_words}

Fifth Press register button
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li

    touch create new account
    Page Should Contain Text    ${password_note_info}
    Click Element    ${OK_button}
    Clear Text    ${sign_up_password}
    Input Text    ${sign_up_password}    ${sign_up_not_valid_Spaces_password_words}
    touch create new account
    Page Should Contain Text    ${not_valid_password_info}
    Click Element    ${OK_button}
    Clear Text    ${sign_up_password}
    Input Text    ${sign_up_password}    ${sign_up_not_valid_symbols_password_words}
    touch create new account
    Page Should Contain Text    ${not_valid_password_info}
    Click Element    ${OK_button}

*** comment ***
2017-12-17 Gavin_Chang
1. Using Clear Text instead of back to previous page and sign up again.
2. Add Hide Keyword to ensure the element is clickable.

2017-11-27    Leo_Li
Add negative test scripts

2017-11-17    Leo_Li
Init the script