*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Jujung_Chang    norun

*** Variables ***
${image}     /home/vagrant/CalixImage/fake.bin
*** Test Cases ***
tc_fw_upgrade_dummy
    [Documentation]   tc_fw_upgrade_dummy
    ...    1. Create two libraries to get cell value, the library can be called by Wait Until Keyword Succeeds to avoid dynamic java script web data reflash
    ...    2. Table Data Should Not Be Empty will also return cell value when the keyword succeeds
    [Tags]
    [Timeout]
    [Teardown]      remove file    ${image}

    #create fake image, it should be removed in the teardown section
    create file    ${image}

    #Login Web GUI
    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Firmware Upgrade
    Wait Until Keyword Succeeds    5x    3s    click links    web    Upgrade Image
    #execute upload image java script to show file upload dialog
    execute javascript    web    document.getElementById("fileUploadFrameObjId").style.display='block'
    select_frame    web    id=fileUploadFrameObjId
    choose file   web    id=fileObjectID    ${image}
    unselect_frame    web
    cpe click    web    id=upgrade_button
    sleep    10


*** Keywords ***
case setup
    [Documentation]
    [Arguments]
    log    Enter case setup


case teardown
    [Documentation]
    [Arguments]    ${image}
    logout ont    ff
    remove file    ${g_fw_location}
    log    Enter case teardown
