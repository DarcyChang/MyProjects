*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=Wi-Fi    @AUTHOR=Gemtek_Hans_Sun    stable

*** Variables ***
${invalid_pskKey}    key

*** Test Cases ***
tc_GUI_5GWIFI_Security_Verify_input_validation_function
    [Documentation]    tc_GUI_5GWIFI_Security_Verify_input_validation_function
    ...   1. login DUT web guit, and go to 5GWIFI page
    ...   2. Input invalid Security key, and click apply button
    ...   3. Check warnings will be generated if invalid key is inputted
    [Tags]    @TCID=STP_DD-TC-10911    @globalid=1526094    @DUT=844FB    @DUT=844F    @AUTHOR=Gemtek_Hans_Sun

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Wireless 2.4 GHz Control Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Wireless
    Wait Until Keyword Succeeds    5x    3s    click links    web    5G Network
    #Change WiFi 2.4G Security Key
    Wait Until Keyword Succeeds    5x    3s    click links    web    Security
    Wait Until Keyword Succeeds    5x    3s    select_from_list_by_label    web    xpath=//select[@id='security_type']    WPA - WPA2-Personal
    Wait Until Keyword Succeeds    5x    3s    input_text    web    xpath=//input[@id='pskKeyInput']    ${invalid_pskKey}
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    page should contain text     web    The WPA security key is not valid.Please enter a value containing between 8 and 63 characters.
