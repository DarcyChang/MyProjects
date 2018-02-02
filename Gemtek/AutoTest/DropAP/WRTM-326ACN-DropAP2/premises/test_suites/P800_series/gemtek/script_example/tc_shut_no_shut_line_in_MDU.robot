*** Settings ***
Resource      ./base.robot
Force Tags    @FEATURE=LED    @AUTHOR=Thomas_Chen    norun

#You can run multi keywords in `suite setup` or `suite teardown` step with keyword `Run keywords`
Suite Setup       Run keywords    No Shut Line Interface
Suite Teardown    Run keywords    No Shut Line Interface


*** Variables ***
${MDU_SESSION}    e5
${bonding_group}    gbond4
${bonding_int1}     ethernet gfast7
${bonding_int2}     ethernet gfast8
${bonding_line1}    line line7
${bonding_line2}    line line8

*** Test Cases ***
tc_shut_no_shut_line_in_MDU
    [Documentation]    tc_shut_no_shut_line_in_MDU
    [Tags]   @DUT=844FB  @DUT=844F
    [Timeout]

    login ont    web    ${g_844fb_gui_url}    ${g_844fb_gui_user}    ${g_844fb_gui_pwd}
    #Go to Service WAN VLANs Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Support
    Wait Until Keyword Succeeds    5x    3s    click links    web    Service WAN VLANs
    Wait Until Element Is Visible    web    xpath=//button[contains(., 'Edit')]
    #Go to Wide Area Network (WAN) Settings Page
    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    name=conn_admin_status
    #Disable WAN Service and Select IPoE Service
    select radio button    web    conn_admin_status    disabled
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Wide Area Network (WAN) Settings Page
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Edit')]
    Wait Until Element Is Visible    web    name=conn_admin_status
    #Enable WAN Service and Select IPoE Service
    select radio button    web    conn_admin_status    enabled
    Wait Until Keyword Succeeds    5x    3s    cpe click    web    xpath=//button[contains(., 'Apply')]
    #Go to Status Page
    Wait Until Keyword Succeeds    5x    3s    click links    web    Status
    #Check IP Gateway Table
    Wait Until Element Is Visible    web    id=gateway_tab
    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    5x    5s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Connected

    #Login MDU
    cli    ${MDU_SESSION}    cli

    #Shutdown ${MDU_SESSION} line interface
    cli    ${MDU_SESSION}   config
    cli    ${MDU_SESSION}   interface ${bonding_line1}
    cli    ${MDU_SESSION}   shutdown
    cli    ${MDU_SESSION}   interface ${bonding_line2}
    cli    ${MDU_SESSION}   shutdown
    cli    ${MDU_SESSION}   exit

    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    5x    5s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Disconnected

    #No Shutdown ${MDU_SESSION} line interface
    cli    ${MDU_SESSION}   config
    cli    ${MDU_SESSION}   interface ${bonding_line1}
    cli    ${MDU_SESSION}   no shutdown
    cli    ${MDU_SESSION}   interface ${bonding_line2}
    cli    ${MDU_SESSION}   no shutdown
    cli    ${MDU_SESSION}   exit
    #Check Wide Area Network (WAN) status by checking cell value
    Wait Until Keyword Succeeds    5x    5s     Cell Data Should Contain    web    xpath=//table[@id='conn_tab']    2    2    Connected




*** Keywords ***
No Shut Line Interface
    [Arguments]
    [Documentation]    Initial setup for the test
    #Login MDU
    cli    ${MDU_SESSION}    cli

    #Shutdown ${MDU_SESSION} line interface
    cli    ${MDU_SESSION}   config
    cli    ${MDU_SESSION}   interface ${bonding_line1}
    cli    ${MDU_SESSION}   no shutdown
    cli    ${MDU_SESSION}   interface ${bonding_line2}
    cli    ${MDU_SESSION}   no shutdown
    cli    ${MDU_SESSION}   end

*** comment ***
##############################
interface bonded-group gbond4
 description thomas_bonding
 service-role uni
  service 913
   match-list 913
   no shutdown
  !
  service 914
   match-list 914
   no shutdown
   igmp multicast-profile 914
  !
 !
 no shutdown
!
##############################
interface ethernet gfast5
shut
  no service-role bonded-group
  service-role bonded-group
  group-name gbond3
no sh

interface ethernet gfast6
shut
  no service-role bonded-group
  service-role bonded-group
  group-name gbond3
no sh


 ##############################

interface line line7
 shutdown

interface line line8
 shutdown

interface line line7
no shutdown

interface line line8
no shutdown
