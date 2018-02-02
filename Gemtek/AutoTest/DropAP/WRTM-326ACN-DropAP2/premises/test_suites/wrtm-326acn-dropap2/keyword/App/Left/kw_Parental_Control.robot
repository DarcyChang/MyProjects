*** Settings ***
Resource    base.robot

*** Variables ***
${Family_members_icon}    com.dropap.dropap:id/ivGroupCircle
${Select_Devices_Done}    com.dropap.dropap:id/tvPositive
${Select_Devices_Cancel}    com.dropap.dropap:id/tvNegative

${Time_Limit_hour_value}    com.dropap.dropap:id/hours
${Time_Limit_minutes_value}    com.dropap.dropap:id/minutes
${Time_Limit_Save}    com.dropap.dropap:id/btnPositive
${Time_Limit_Cancel}    com.dropap.dropap:id/btnNegative

${Time_Schedule_Switch}    com.dropap.dropap:id/btnTimeScheduleSwitch
${Time_Schedule_Start_Time_arrow}    com.dropap.dropap:id/btnTimeScheduleStart
${Time_Schedule_Start_Time_hour_value}    com.dropap.dropap:id/hours
${Time_Schedule_Start_Time_minutes_value}    com.dropap.dropap:id/minutes
${Time_Schedule_Start_Time_ampm_label}    com.dropap.dropap:id/ampm_label
${Time_Schedule_Start_Time_Save}    com.dropap.dropap:id/btnPositive
${Time_Schedule_Start_Time_Cancel}    com.dropap.dropap:id/btnNegative

${Time_Schedule_Stop_Time_arrow}    com.dropap.dropap:id/btnTimeScheduleStop
${Time_Schedule_Stop_Time_hour_value}    com.dropap.dropap:id/hours
${Time_Schedule_Stop_Time_minutes_value}    com.dropap.dropap:id/minutes
${Time_Schedule_Stop_Time_ampm_label}    com.dropap.dropap:id/ampm_label
${Time_Schedule_Stop_Time_Save}    com.dropap.dropap:id/btnPositive
${Time_Schedule_Stop_Time_Cancel}    com.dropap.dropap:id/btnNegative

${Conten_Filters_btn}    com.dropap.dropap:id/btnContentFilters
${Content_Filters_ADULT_SITES}    com.dropap.dropap:id/ivKidLock
${Content_Filters_SCAM_SITES}    com.dropap.dropap:id/ivPrivacyLock
${Content_Filters_SOCIAL_MEDIA}    com.dropap.dropap:id/ivSocialLock
${Content_Filters_ENTERTAINMENT}    com.dropap.dropap:id/ivEntertainmentLock
${Content_Filters_DOWNLOADS}    com.dropap.dropap:id/ivDownloadLock
${Content_Filters_SHOPPING}    com.dropap.dropap:id/ivShopLock
${Content_Filters_ALL}    com.dropap.dropap:id/ivAllLock
${Content_Filters_Save}    com.dropap.dropap:id/btnPositive
${Content_Filters_Cancel}    com.dropap.dropap:id/btnNegative

${Blocked_Websites_btn}    com.dropap.dropap:id/btnBlockedWebsites
${Blocked_Websites_add_Keyword}    com.dropap.dropap:id/etNewBlockItem
${Blocked_Websites_Save}    com.dropap.dropap:id/btnPositive
${Blocked_Websites_Cancel}    com.dropap.dropap:id/btnNegative
${Blocked_Websites_del}    com.dropap.dropap:id/ivDeleteIcon

${Blocked_Apps_btn}    com.dropap.dropap:id/btnBlockedApps
${Blocked_Apps_Save}    com.dropap.dropap:id/btnPositive
${Blocked_Apps_Cancel}    com.dropap.dropap:id/btnNegative
${Blocked_Apps_del}    com.dropap.dropap:id/ivDeleteIcon

${Clear_Website_and_Apps_Data_btn}    com.dropap.dropap:id/btnClearWebsiteAppsData
${Clear_Website_and_Apps_Data_content}    com.dropap.dropap:id/content
${Clear_Website_and_Apps_Data_ok}    com.dropap.dropap:id/buttonDefaultPositive
${Clear_Website_and_Apps_Data_cancel}    com.dropap.dropap:id/buttonDefaultNegative

${Delete_btn}    com.dropap.dropap:id/btnDelete
${Delete_content}    com.dropap.dropap:id/content
${Delete_ok}    com.dropap.dropap:id/buttonDefaultPositive
${Delete_cancel}    com.dropap.dropap:id/buttonDefaultNegative


*** Keywords ***
verify Family members icon
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Family_members_icon}

verify Family members name
verify Devices num

touch Add Devices
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    640    200

touch Select Devices Done
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Select_Devices_Done}

touch Select Devices Cancel
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Select_Devices_Cancel}


verify Time Limit status

touch Time Limit switch
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    640    200

touch Time Limit value
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    400    340

verify Time Limit hour value
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Time_Limit_hour_value}

verify Time Limit minutes value
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Time_Limit_minutes_value}

touch Time Limit Saves
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Limit_Save}

touch Time Limit Cancel
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Limit_Cancel}


verify Time Schedule status

touch Time Schedule switch
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    650    460

touch Time Schedule Start Time settings
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    540    580

verify Time Schedule Start Time hour value
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Time_Schedule_Start_Time_hour_value}

verify Time Schedule Start Time minutes value
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Time_Schedule_Start_Time_minutes_value}

verify Time Schedule Start Time ampm label
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Time_Schedule_Start_Time_ampm_label}

touch Time Schedule Start Time Saves
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Schedule_Start_Time_Save}

touch Time Schedule Start Time Cancel
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Schedule_Start_Time_Cancel}


touch Time Schedule Stop Time settings
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    540    690

verify Time Schedule Stop Time hour value
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Time_Schedule_Stop_Time_hour_value}

verify Time Schedule Stop Time minutes value
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Time_Schedule_Stop_Time_minutes_value}

verify Time Schedule Stop Time ampm label
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Time_Schedule_Stop_Time_ampm_label}

touch Time Schedule Stop Time Saves
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Schedule_Stop_Time_Save}

touch Time Schedule Stop Time Cancel
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Time_Schedule_Stop_Time_Cancel}


touch Content Filters settings
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    640    590

touch Content Filters ADULT SITES
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_ADULT_SITES}

touch Content Filters SCAM SITES
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_SCAM_SITES}

touch Content Filters SOCIAL MEDIA
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_SOCIAL_MEDIA}

touch Content Filters ENTERTAINMENT
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_ENTERTAINMENT}

touch Content Filters DOWNLOADS
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_DOWNLOADS}

touch Content Filters SHOPPING
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_SHOPPING}

touch Content Filters ALL
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_ALL}

touch Content Filters Save
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_Save}

touch Content Filters Cancel
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Content_Filters_Cancel}


Config Blocked Websites settings
    [Documentation]
    [Arguments]    ${blocked_web_keyword}
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Blocked_Websites_btn}
    Wait Until Page Contains Element    ${Blocked_Websites_Save}    timeout=10
    Input Text    ${Blocked_Websites_add_Keyword}    ${blocked_web_keyword}
    Click Element    ${Blocked_Websites_Save}
    Wait Until Page Contains Element    ${Blocked_Websites_btn}    timeout=30

Delete Blocked Websites settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Blocked_Websites_btn}
    Wait Until Page Contains Element    ${Blocked_Websites_Save}    timeout=10
    Click Element    ${Blocked_Websites_del}
    Click Element    ${Blocked_Websites_Save}
    Wait Until Page Contains Element    ${Blocked_Websites_btn}    timeout=30

Delete Blocked Apps settings
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${Blocked_Apps_btn}
    Wait Until Page Contains Element    ${Blocked_Apps_Save}    timeout=10
    Click Element    ${Blocked_Apps_del}
    Click Element    ${Blocked_Apps_Save}
    Wait Until Page Contains Element    ${Blocked_Apps_btn}    timeout=30

touch Blocked Apps settings
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    640    830

touch Blocked Apps Save
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Blocked_Apps_Save}

touch Blocked Apps Cancel
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Blocked_Apps_Cancel}


touch Clear Website and Apps Data
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element At Coordinates    330    970

verify Clear Website and Apps Data content
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Clear_Website_and_Apps_Data_content}

touch Clear Website and Apps Data ok
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Clear_Website_and_Apps_Data_ok}

touch Clear Website and Apps Data cancel
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Clear_Website_and_Apps_Data_cancel}


touch Delete
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Delete_btn}

verify Delete content content
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${Delete_content}

touch Delete ok
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Delete_ok}

touch Delete cancel
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${Delete_cancel}


*** comment ***
2017-11-10     Leo_Li
Init the script
