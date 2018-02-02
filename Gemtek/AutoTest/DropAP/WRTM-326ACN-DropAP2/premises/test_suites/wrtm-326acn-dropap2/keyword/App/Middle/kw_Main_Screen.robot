*** Settings ***
Resource    base.robot

*** Variables ***
${gps}    com.dropap.dropap:id/ivMap
${map_view}    class=android.view.View
${gps_device_name}    com.dropap.dropap:id/tvDevName
${group_circle}    com.dropap.dropap:id/ivGroupCircle
${group_device_name}    com.dropap.dropap:id/tvGroup
${create_family_member_label}    com.dropap.dropap:id/rlCreateMember
${create_family_member_icon}    com.dropap.dropap:id/ivCreateFamilyMember
${input_name}    com.dropap.dropap:id/etInputName
${next}    com.dropap.dropap:id/tvPositive
${cancel}    com.dropap.dropap:id/tvNegative
${pre_k}    com.dropap.dropap:id/rlPreK
${kid}    com.dropap.dropap:id/rlKid
${teen}    com.dropap.dropap:id/rlTeen
${adult}    com.dropap.dropap:id/rlAdult
${done}    com.dropap.dropap:id/tvPositive
${today}    com.dropap.dropap:id/tvDate
${left}    com.dropap.dropap:id/ivBarLeft
${report}    com.dropap.dropap:id/rlHistroyItem
${no_report}    com.dropap.dropap:id/rlEmptyHistory
${refresh_report}    com.dropap.dropap:id/btnRefresh
${pause_resume}    com.dropap.dropap:id/tvPause
${successful_info}    com.dropap.dropap:id/tvInfo
${block_app_btn}    com.dropap.dropap:id/blockAppBtn
${close_dialog_btn}    com.dropap.dropap:id/closeDialogTxt
${block_icon}    com.dropap.dropap:id/ivLock
${visit_this_website}    com.dropap.dropap:id/visitWebBtn
${restore_member}    Lanhost
${restore_device}    app-lanhost

*** Keywords ***
touch gps
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${gps}

verify gps
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${gps}

verify gps device name
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${gps_device_name}

verify map
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Page Contains Element    ${map_view}    timeout=30

touch family member
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${group_circle}

verify family member
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${group_circle}

touch today
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${today}

verify today
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${today}

verify report
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    ${status}    run keyword and return status    Page Should Contain Element    ${report}
    return from keyword if    ${status}==True
    Page Should Contain Element    ${no_report}
touch left
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${left}
    sleep    1s

touch group circle
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${group_circle}

select family member
    [Documentation]
    [Arguments]    ${member_devices}=Lanhost
    [Tags]   @AUTHOR=Gavin_Chang
    Check Default Family Member
    touch family member
    Wait Until Page Contains Element    ${create_family_member_label}    timeout=30
    Click Text    ${member_devices}
    wait family member

touch create family member label
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${create_family_member_label}

touch create family member icon
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${create_family_member_icon}

input family member name
    [Documentation]
    [Arguments]    ${member_name}
    [Tags]   @AUTHOR=Gavin_Chang
    Input Text    ${input_name}    ${member_name}

touch next
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${next}

Create Family Member
    [Documentation]
    [Arguments]    ${member_name}    ${age_level}    ${device}=Unknown
    [Tags]   @AUTHOR=Gavin_Chang
    touch create family member icon
    input family member name    ${member_name}
    ${keyboard_is_visible}    Detect Keyboard Status Is Visible
    Run Keyword If    ${keyboard_is_visible}    Hide Keyboard
    touch next
    Click Text    ${age_level}
    touch next
    run keyword and ignore error    Click Text    ${device}
    touch next
    Wait Until Page Contains Element    ${successful_info}    timeout=30
    Page Should Contain Text    &quot;${member_name}&quot; has been successfully added to your family.
    Click Element    ${successful_info}

Delete Member
    [Documentation]
    [Arguments]    ${member_name}
    [Tags]   @AUTHOR=Gavin_Chang
    touch family member
    Click Text    ${member_name}
    wait main screen
    Swipe To Right
    touch Delete
    touch Delete ok
    wait main screen

wait family member
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Wait Until Page Contains Element    ${group_circle}    timeout=60

touch Pause_Resume
    [Documentation]    Pause or Resume
    [Arguments]    ${original_state}
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${pause_resume}
    Wait Until Page Contains Element    ${pause_resume}    timeout=30
    ${now_state}    Get Text    ${pause_resume}
    Should Not Be Equal    ${now_state}    ${original_state}

Config Blocked Apps settings
    [Documentation]
    [Arguments]    ${blocked_app}
    [Tags]   @AUTHOR=Gavin_Chang
    Click Text    ${blocked_app}
    Wait Until Page Contains Element    ${block_app_btn}    timeout=10
    Click Element    ${block_app_btn}
    wait main screen

Check Default Family Member
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    touch family member
    ${status}    run keyword and return status    Wait Until Page Contains    ${restore_member}    timeout=10
    touch left
    return from keyword if    ${status}==True
    Trigger Device List
    Create Family Member    ${restore_member}    ADULT    ${restore_device}
*** comment ***

