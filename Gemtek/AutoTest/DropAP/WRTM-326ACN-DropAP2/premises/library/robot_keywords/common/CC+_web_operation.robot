*** Settings ***
Resource          caferobot/cafebase.robot
Library           DateTime

*** Variables ***
${browser}        web
${cc_801f_sw_path}    /home/xlai

*** Keywords ***
CC+_login_web
    [Arguments]    ${browser}    ${g_cc_web_url}    ${g_cc_usrname}    ${g_cc_password}
    [Documentation]    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \ Login to CC+ Frontend Web Page
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | Selenium Web Driver |
    ...    | g_cc_web_url | Web url of CC+ |
    ...    | g_cc_usrname | login username of CC+ Web|
    ...    | g_cc_password| login password of CC+ Web
    ...
    ...    Example:
    ...    CC+_login_web \ \ \ web \ \ \ ${g_cc_web_url} \ \ \ ${g_cc_usrname} \ \ \ ${g_cc_password}
    go_to_page    ${browser}    ${g_cc_web_url}
    input_text    ${browser}    name=userName    ${g_cc_usrname}
    input_text    ${browser}    name=password    ${g_cc_password}
    submit_form    ${browser}

CC+_netops_menu
    [Arguments]    ${browser}
    [Documentation]    Author: Xiaoting Lai
    ...
    ...    Description: \ \ \ \ \ \ \Open Netops menu on CC+
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | Selenium Web Driver |
    ...
    ...    Example:
    ...    CC+_netops_menu \ \ \ web
    click_element    ${browser}    xpath=//*[@id="navConsumerConnect"]/b/em
    Sleep    1
    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    Sleep    1

CC+_netops_sw_image
    [Arguments]    ${browser}    ${image_name}
    [Documentation]    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \Add SW Image on NetOps
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | Selenium Web Driver |
    ...    | image_path | The full path where image file stored to upload to CC+ |
    ...
    ...    Example:
    ...    CC+_netops_sw_image \ \ \ web \ \ \ /tmp/Pre801F_1.1.7.oneimage
    #    click_element    ${browser}    xpath=//*[@id="navConsumerConnect"]/b/em
    #    Sleep    1
    #    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    #    Sleep    1
    click_element    ${browser}    link=Software Image
    Sleep    1
    click_element    ${browser}    xpath=//button[contains(text(),'Add SW Image')]
    input_text    ${browser}    xpath=//label[contains(text(),'File')]/parent::div//input    ${cc_801f_sw_path}/${image_name}
    #click_element    ${browser}    xpath=//button[contains(text(),'Submit')]
    click_element    ${browser}    xpath=//*[@id="btn-submitSWImage"]
    Sleep    1

CC+_del_sw_image
    [Arguments]    ${browser}    ${image_name}
    [Documentation]    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \Delete SW Image created on NetOps
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | Selenium Web Driver |
    ...    | image_name | Image name shows on SW Image of NetOps |
    ...
    ...    Example:
    ...    CC+_del_sw_image \ \ \ web \ \ \ Pre801F_1.1.7.oneimage
    #    click_element    ${browser}    xpath=//*[@id="navConsumerConnect"]/b/em
    #    Sleep    1
    #    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    #    Sleep    1
    click_element    ${browser}    link=Software Image
    Sleep    1
    click_element    ${browser}    xpath=//td[text()='${image_name}']/ancestor::tr//i[@data-original-title='Delete']
    Sleep    1
    click_element    ${browser}    xpath=//button[contains(text(),'Confirm')]
    Sleep    10

CC+_netops_device_group
    [Arguments]    ${browser}    ${sn_801f}
    [Documentation]    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \Add DeviceGroup on NetOps
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | Selenium Web Driver |
    ...    | sn_801f | Using SN of device as name of device group |
    ...
    ...    Example:
    ...    CC+_netops_device_group \ \ \ web \ \ \ CXNKXXXXXXXX
    #    click_element    ${browser}    xpath=//*[@id="navConsumerConnect"]/b/em
    #    Sleep    1
    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    Sleep    1
    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    Sleep    1
    click_element    ${browser}    link=Device Groups
    Sleep    1
    click_element    ${browser}    xpath=//button[contains(text(),'New')]
    input_text    ${browser}    xpath=//label[contains(text(),'Name')]/parent::div//input    ${sn_801f}
    click_element    ${browser}    xpath=//*[@id="addRow-0"]
    select from list by label    ${browser}    xpath=//label[contains(text(),'Rules')]/parent::div//div/div/div[1]/select    FSAN/Serial Number
    select_from_list_by_label    ${browser}    xpath=//label[contains(text(),'Rules')]/parent::div//div/div/div[2]/select    WildCard
    input_text    ${browser}    xpath=//label[contains(text(),'Rules')]/parent::div//div/div/div//input    ${sn_801f}
    click_element    ${browser}    xpath=//button[contains(text(),'ubmit')]

CC+_del_device_group
    [Arguments]    ${browser}    ${sn_801f}
    [Documentation]    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \Delete DeviceGroup created on NetOps
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | Selenium Web Driver |
    ...    | sn_801f | Using SN of device as name of device group |
    ...
    ...    Example:
    ...    CC+_del_device_group \ \ \ web \ \ \ CXNKXXXXXXXX
    #    click_element    ${browser}    xpath=//*[@id="navConsumerConnect"]/b/em
    #    Sleep    1
    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    Sleep    1
    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    Sleep    1
    click_element    ${browser}    link=Device Groups
    Sleep    1
    click_element    ${browser}    xpath=//td[text()='${sn_801f}']/ancestor::tr//i[@class='fa fa-lg fa-fw fa-trash-o']
    Sleep    1
    click_element    ${browser}    xpath=//button[contains(text(),'Confirm')]

CC+_netops_workflow
    [Arguments]    ${browser}    ${sn_801f}    ${wflow_type}    ${available_file}
    [Documentation]    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \Add WorkFlow on NetOps
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | Selenium Web Driver |
    ...    | sn_801f | Using SN of device as name of device group |
    ...    | wflow_type | Currently 3 types are available as shown on CC+, 'Configuration File Donwload', 'Download SW/FW Image' & 'Apply Configuration Profile' |
    ...    | available_file | The file using in this workflow. For 'Download SW/FW Image', it is the name of image file |
    ...
    ...    Example:
    ...    CC+_netops_workflow \ \ \ web \ \ CXNKXXXXXXXX \ \ \ Download SW/FW Image \ \ \ ${g_801f_image}
    #    click_element    ${browser}    xpath=//*[@id="navConsumerConnect"]/b/em
    #    Sleep    1
    #    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    #    Sleep    1
    click_element    ${browser}    link=Workflows
    Sleep    1
    click_element    ${browser}    xpath=//button[contains(text(),'New')]
    ${date} =    Get Current Date
    ${ts_cur}=    Convert Date    ${date}    result_format=%Y%m%d%H%M%S
    input_text    ${browser}    xpath=//label[contains(text(),'Name')]/parent::div//input    ${sn_801f}_${ts_cur}
    click_element    ${browser}    xpath=//a[contains(text(),'Next')]
    select checkbox    ${browser}    //td[text()='${sn_801f}']/ancestor::tr//input[@type='checkbox']
    click_element    ${browser}    xpath=//a[contains(text(),'ext')]
    click_element    ${browser}    xpath=//button[contains(text(),'New')]
    select from list by label    ${browser}    xpath=//label[contains(text(),'Operation')]/parent::div//select    ${wflow_type}
    click_element    ${browser}    xpath=//td[text()='${available_file}']/ancestor::tr//input[@type='radio']
    click_element    ${browser}    xpath=//button[contains(text(),'Done')]
    click_element    ${browser}    xpath=//a[contains(text(),'Next')]
    select from list by label    ${browser}    xpath=//label[contains(text(),'Trigger')]/parent::div//select    Time Scheduler
    input_text    ${browser}    xpath=//label[contains(text(),'Window')]/parent::div//input    5
    click_element    ${browser}    xpath=//a[contains(text(),'Next')]
    click_element    ${browser}    xpath=//a[contains(text(),'Finish')]
    [Return]    ${sn_801f}_${ts_cur}

CC+_del_workflow
    [Arguments]    ${browser}    ${wflow_name}
    [Documentation]    Author: Xiaoting Lai
    ...    Description: \ \ \ \ \ \ \Delete WorkFlow on NetOps
    ...
    ...    Arguments:
    ...    | =Argument Name= | \ =Argument Value= \ |
    ...    | browser | Selenium Web Driver |
    ...    | wflow_name | Workflow name shows on NetOps |
    ...
    ...    Example:
    ...    CC+_del_workflow \ \ \ web \ \ CXNKXXXXXXXX_DWL
    #    click_element    ${browser}    xpath=//*[@id="navConsumerConnect"]/b/em
    #    Sleep    1
    #    click_element    ${browser}    xpath=//*[@id="content-navigation"]/ul/li[2]/ul/li[2]/a/b/em
    #    Sleep    1
    click_element    ${browser}    link=Workflows
    Sleep    1
    click_element    ${browser}    xpath=//td[text()='${wflow_name}']/ancestor::tr//i[@class='fa fa-lg fa-fw fa-trash-o']
    Sleep    1
    click_element    ${browser}    xpath=//button[contains(text(),'Confirm')]
