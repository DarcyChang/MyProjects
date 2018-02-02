*** Settings ***
Resource    base.robot

*** Variables ***
${most_used_web}    com.dropap.dropap:id/mostUsedWebImg
${most_used_app}    com.dropap.dropap:id/mostUsedAppImg
${most_click_web}    com.dropap.dropap:id/mostClickWebImg
${today_top_20}    com.dropap.dropap:id/todayBtn
${seven_days_top_20}    com.dropap.dropap:id/sevenDayBtn
${pie_chart}    com.dropap.dropap:id/pieChart

*** Keywords ***
touch most used web
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${most_used_web}

touch most used app
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${most_used_app}

touch most click web
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${most_click_web}

touch today top 20
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${today_top_20}

touch seven days top 20
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Click Element    ${seven_days_top_20}

verfiy Data Report page
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${pie_chart}

verify most used web
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${most_used_web}

verify most used app
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${most_used_app}

verify most click web
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${most_click_web}

verify today top 20
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${today_top_20}

verify seven days top 20
    [Documentation]
    [Tags]   @AUTHOR=Gavin_Chang
    Page Should Contain Element    ${seven_days_top_20}

*** comment ***

