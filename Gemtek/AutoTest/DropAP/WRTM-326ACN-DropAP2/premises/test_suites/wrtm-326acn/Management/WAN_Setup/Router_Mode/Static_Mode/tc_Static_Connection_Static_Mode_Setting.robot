*** Settings ***

Resource      ./base.robot
    
Force Tags    @FEATURE=WAN_Static_IP    @AUTHOR=Gemtek_Thomas_Chen

Suite Setup    Run keywords    Common Setup
Suite Teardown    Run keywords    Common Cleanup

*** Variables ***


*** Test Cases ***
tc_Static_Connection_Wan_Connection
    [Documentation]    DUT can setting of WAN IP Address, Mask, default gateway and DNS information in DUT, and meet DUT of wan status.
    [Tags]   @tcid=WRTM-326ACN-19    @DUT=wrtm-326acn     @AUTHOR=Gemtek_Thomas_Chen
    [Timeout]

    Configure WAN Internet connection type to be Static mode.
    #Setting the WAN IP Address and make sure the IP Address will avoid the broadcast IP Address and multicast IP Address.
    #Setting the Subnet Mask and make sure the illegal Subnet Mask will not be accepted.
    #Setting the Default Gateway and make sure the IP Address will avoid the broadcast IP Address and multicast IP Address.
    #Setting the DNS Address and make sure the IP Address will avoid the broadcast IP Address and multicast IP Address.
    Verify the WAN IP Address Information at the WAN Status if correct.


*** Keywords ***
Configure WAN Internet connection type to be Static mode.
    [Arguments]
    [Documentation]    Test Step
    
    Config Static WAN    web    ${g_dut_static_ipaddr}    ${g_dut_static_netmask}    ${g_dut_static_gateway}    ${g_dut_static_dns1}
    

Verify the WAN IP Address Information at the WAN Status if correct.
    [Arguments]
    [Documentation]    Test Step
    
    Internet Status Should be Up    web


Common Setup
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    
    Login Web GUI
    
Login Web GUI
    [Arguments]
    [Documentation]    Configure prerequisite value of testing
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
        
    login ont    web    ${g_dut_gui_url}    ${g_dut_gui_user}    ${g_dut_gui_pwd}


Common Cleanup
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    
    Restore WAN Setting
    
Restore WAN Setting    
    [Arguments]
    [Documentation]    Clean up all setting
    [Tags]    @AUTHOR=Gemtek_Hans_Sun
    
    Config DHCP WAN and Check Internet     web




*** comment ***
2017-09-02     Gemtek_Thomas_Chen
1. Add test case id and wait until keyword succeed to retry fail tests

2017-08-24     Gemtek_Thomas_Chen
Init the script
