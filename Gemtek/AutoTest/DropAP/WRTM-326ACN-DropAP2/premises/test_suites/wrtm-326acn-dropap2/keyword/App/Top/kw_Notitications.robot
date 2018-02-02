*** Settings ***
Resource    base.robot

*** Variables ***
${notifications_info_num}    com.dropap.dropap:id/notificationNumImg
${notifications_info_menu}    com.dropap.dropap:id/notificationImg
${notifications_field}    com.dropap.dropap:id/notificationTxt
${delete_all_notifications_info}    com.dropap.dropap:id/deleteAllImg
${delete_all_notifications_content_info}    com.dropap.dropap:id/content
${delete_all_notifications_negative}    com.dropap.dropap:id/buttonDefaultNegative
${delete_all_notifications_positive}    com.dropap.dropap:id/buttonDefaultPositive
${notifications_day_field}    com.dropap.dropap:id/dayTxt
${Accept_guest}    com.dropap.dropap:id/acceptBtn
${Decline_guest}    com.dropap.dropap:id/declineBtn

*** Keywords ***
verify notifications info num
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${notifications_info_num}

verify notifications info menu
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${notifications_info_menu}

touch notifications info menu
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${notifications_info_menu}
    Sleep    2s

close notifications info menu
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element    ${notifications_info_menu}

verify notifications field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${notifications_field}

touch delete all notifications info
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element       ${delete_all_notifications_info}
    Click Element       ${delete_all_notifications_positive}

touch not delete all notifications info
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Click Element       ${delete_all_notifications_info}
    Click Element       ${delete_all_notifications_negative}

verify if show want to clear all notifications
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${delete_all_notifications_content_info}

verify notifications day field
    [Documentation]
    [Tags]   @AUTHOR=Leo_Li
    Page Should Contain Element    ${notifications_day_field}

*** comment ***
2017-12-05     Leo_Li
Modified keywords variable name

2017-11-10     Leo_Li
Init basic AP common keyword