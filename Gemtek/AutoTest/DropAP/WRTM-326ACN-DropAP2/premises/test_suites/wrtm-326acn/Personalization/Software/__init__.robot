*** Settings ***
Suite Setup       my_suite_setup
Suite Teardown    my_suite_teardown
Resource          base.robot

*** Keywords ***
my_suite_setup
    [Documentation]
    [Arguments]
    log to console           "Enter P800 suite setup"

    log to console           "Get switch port of current running VM according to hostname"
#    &{vmports} =             Create Dictionary      nanlnx-ccafe76=2           nanlnx-ccafe135=47       nanlnx-ccafe136=48
#    &{client_ips} =          Create Dictionary      nanlnx-ccafe76=192.168.1.76     nanlnx-ccafe135=192.168.1.135     nanlnx-ccafe136=192.168.1.136
#    set global variable      ${vm_port}              &{vmports}[%{HOSTNAME}]
    set global variable      ${client_ip}            ${vm.nanlnx_ccafe66.ip}
    #log to console           "Current switch port is ${vm_port.%{HOSTNAME}}"
    log to console           "Current client ip is ${client_ip}"
#
#    P800_suite_setup         ${switch_session}      ${dut_ethport_onswitch}    ${dut_ethport_pvlan}     ${vm_port}    ${vm_pvlan}

my_suite_teardown
    [Documentation]
    [Arguments]
    log to console          "Enter P800 suite teardown"
    #P800_suite_teardown     ${switch_session}    ${dut_ethport_onswitch}    ${dut_ethport_pvlan}    ${vm_port}    ${vm_pvlan}
