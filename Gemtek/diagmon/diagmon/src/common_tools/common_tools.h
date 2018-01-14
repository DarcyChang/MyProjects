#ifndef _DAIG_COMMON_TOOLS_H_
#define _DAIG_COMMON_TOOLS_H_

DIAG_CODE common_tools(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE common_tools_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_version(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_version(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_version_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_base_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_base_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_base_mac_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_base_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_base_mac(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_base_mac_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_restore_to_default(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_restore_to_default(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE restore_to_default_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_system_reboot(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_system_reboot(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE system_reboot_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_get_sn_code(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_get_sn_code(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_sn_code_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_sn_code(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_sn_code(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_sn_code_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_show_system_run_level(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_show_system_run_level(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE show_system_run_level_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_set_system_run_level(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_set_system_run_level(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE set_system_run_level_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_system_poweroff(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_system_poweroff(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE system_poweroff_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE get_param_system_halt(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE run_system_halt(IO_DATA *pio_data, DIAG_RESULT *prst);
DIAG_CODE system_halt_uid_handle(IO_DATA *pio_data, DIAG_RESULT *prst);

DIAG_CODE check_mac_address(IO_DATA *pio_data);


DIAGS_NODE diag_common_tools_menu[]={
{'0', NULL, "Common Tools Menu\0", NULL, NULL, YES, NO, NO, NULL},
{'0', "cmn01", "Show Version\0", get_param_show_version, run_show_version, YES, YES, YES, show_version_uid_handle},
{'0', "cmn02", "Show Base MAC\0", get_param_show_base_mac, run_show_base_mac, YES, YES, YES, show_base_mac_uid_handle},
{'0', "cmn03", "Set Base MAC\0", get_param_set_base_mac, run_set_base_mac, YES, YES, YES, set_base_mac_uid_handle},
{'0', "cmn04", "Restore System Configuration to Default\0", get_param_restore_to_default, run_restore_to_default, YES, YES, YES, restore_to_default_uid_handle},
{'0', "cmn05", "System Reboot\0", get_param_system_reboot, run_system_reboot, YES, YES, YES, system_reboot_uid_handle},
{'0', "cmn06", "Get SN Code\0", get_param_get_sn_code, run_get_sn_code, YES, YES, YES, get_sn_code_uid_handle},
{'0', "cmn07", "Set SN Code\0", get_param_set_sn_code, run_set_sn_code, YES, YES, YES, set_sn_code_uid_handle},
{'0', "cmn08", "Show System Mode\0", get_param_show_system_run_level, run_show_system_run_level, YES, YES, YES, show_system_run_level_uid_handle},
{'0', "cmn09", "Set System Mode\0", get_param_set_system_run_level, run_set_system_run_level, YES, YES, YES, set_system_run_level_uid_handle},
{'0', "cmn10", "System Power Off\0", get_param_system_poweroff, run_system_poweroff, YES, YES, YES, system_poweroff_uid_handle},
{'0', "cmn11", "System Halt\0", get_param_system_halt, run_system_halt, YES, YES, YES, system_halt_uid_handle}
};

#define SIZE_COMMON_TOOLS_MENU (sizeof diag_common_tools_menu / sizeof(DIAGS_NODE))

#endif

