*** Settings ***
Documentation     Test suite for 800E GUI
#Suite Setup
#Suite Teardown
#Test Setup
#Test Teardown
Force Tags        @feature=advanced
Resource          base.robot
Resource          keywords.robot

*** Variables ***
${web_address1}   http://www.baidu.com
${web_address2}   www.sina.com.cn
${web_address3}   google.com
${web_address4}   !@#$%^&*(),?|\`~
${invalid_ip_address}        55555555
${valid_ip_address}     192.168.1.100

*** Test Cases ***
GUI_ADVANCED_FILTER_Verify_default_setting_and_avaliable_value
    [Documentation]  Verify default setting and available values
    ...    Step 1: On PC1, open this page, click “new”, select “IP Address”, input invalid IP address and click “Apply”
    ...    Step 2: Verify text box “website”
    ...    Accepted format is like: xxx.xxx.xxx, http://xxx.xxx.xxx, google.com
    ...    Input invalid character like !@#$%^&*(),?|\`~ , click “Apply”
    ...
    ...    Expect Result:
    ...    After Step1, Page will popup error message IP address is invalid
    ...    After Step2, Page will popup error message website is invalid

    [Tags]    @TMS_ID=    @author=bfan    @Contour_ID=     @Feature=Advanced    CI=844V_0

    login ont     ${browser}    ${url}    ${username}    ${password}
    cpe click     ${browser}    link=Advanced
    cpe click     ${browser}    link=Website Blocking

    #Senario1: Provision invalid ip address
    cpe click     ${browser}    xpath=//button[contains(., "New")]
    input text    ${browser}    xpath=//label[text()="Website Address:"]/parent::div//input    ${web_address1}
    select radio button       ${browser}        associate_website_with_selector        associate_website_with_ip_radio
    input text    ${browser}    xpath=//input[@id='ip_address_field']       ${invalid_ip_address}
    cpe click     ${browser}    xpath=//button[contains(., "Apply")]
    wait until keyword succeeds    10x    2s    element_should_contain    ${browser}    xpath=//div[@id='defaultAlertBoxID']    Ok
    #element should be visible     ${browser}    xpath=//div[@id='defaultAlertBoxID']
    cpe_click    ${browser}    xpath=//button[contains(.,"Ok")]
    cpe click     ${browser}    link=Website Blocking
    element_should_not_contain    ${browser}    xpath=//table[@id="associations_table"]    ${invalid_ip_address}

    #Senario2: Provision three valid website addresses
    Create_website_block_service    ${browser}     ${web_address1}    ${valid_ip_address}
    Create_website_block_service    ${browser}     ${web_address2}    ${valid_ip_address}
    Create_website_block_service    ${browser}     ${web_address3}    ${valid_ip_address}

    #Senario3: Provison invalid website address
    cpe click     ${browser}    xpath=//button[contains(., "New")]
    input text    ${browser}    xpath=//label[text()="Website Address:"]/parent::div//input    ${web_address4}
    cpe click     ${browser}    xpath=//button[contains(., "Apply")]
    wait until keyword succeeds    10x    2s    element_should_contain    ${browser}    xpath=//div[@id='defaultAlertBoxID']    Ok
    #element should be visible     ${browser}    xpath=//div[@id='defaultAlertBoxID']
    cpe_click    ${browser}    xpath=//button[contains(.,"Ok")]
    cpe click     ${browser}    link=Website Blocking
    element_should_not_contain    ${browser}    xpath=//table[@id="associations_table"]    ${web_address4}

    #Remove the service block rule from 844E
    Remove_website_block_service       ${browser}     ${web_address1}
    Remove_website_block_service       ${browser}     ${web_address2}
    Remove_website_block_service       ${browser}     ${web_address3}
    [Teardown]    teardown

*** Keywords ***
teardown
    #run keyword if test failed  login and restore default    ${browser}    ${url}    ${username}    ${password}
    #run keyword if test failed    P800_factory_reset   ${device}
    run keyword if test failed     factory reset via console       ${device}    ${browser}    ${url}
