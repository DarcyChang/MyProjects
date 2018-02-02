*** Settings ***

Resource      ./base.robot

Force Tags    @FEATURE=LED    @AUTHOR=Jujung_Chang    norun

*** Variables ***
${image}     /home/vagrant/CalixImage/CALIX_844F_12.1.0.92.bin
*** Test Cases ***
tc_fw_upgrade
    [Documentation]   tc_fw_upgrade
    ...    1. Execute upload image java script to show file upload dialog
    ...    2. select file upload frame and input file name to file input box
    ...    3. clide upgade button to upgrade
    [Tags]
    [Timeout]
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

