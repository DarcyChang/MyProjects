*** Settings ***
Resource          ../base.robot
Resource          ./P800_kw.robot
Library           Collections
#Library           Selenium2Library

#import gui  keywords
Resource    keyword/FW/kw_Common.robot
Resource    keyword/FW/kw_Main_Menu.robot
Resource    keyword/FW/kw_wifi_common.robot
Resource    keyword/FW/Device_Management/kw_Firmware.robot
Resource    keyword/FW/Device_Management/kw_System.robot
Resource    keyword/FW/Device_Management/kw_Reboot_Reset.robot
Resource    keyword/FW/Networking/kw_Diagnostics.robot
Resource    keyword/FW/Networking/kw_Internet_Connection.robot
Resource    keyword/FW/Networking/kw_Wireless.robot
Resource    keyword/FW/Networking/kw_Wireless_Extender.robot
Resource    keyword/FW/Status/kw_DMS.robot
Resource    keyword/FW/Status/kw_Overview.robot
Resource    keyword/FW/kw_tgn_common.robot
Resource    keyword/App/kw_Common.robot
Resource    keyword/App/Middle/kw_Main_Screen.robot
Resource    keyword/App/Middle/kw_Expand_Button.robot
Resource    keyword/App/Right/kw_Data_Report.robot
Resource    keyword/App/Top/kw_Title.robot
Resource    keyword/App/Top/kw_Account_info.robot
Resource    keyword/App/Top/kw_Notitications.robot
Resource    keyword/App/Left/kw_Parental_Control.robot
Resource    keyword/App/Front/kw_Welcome.robot
Resource    keyword/Cloud/kw_Common.robot
Resource    keyword/FW/kw_cisco_server.robot
Resource    keyword/FW/kw_Security_Attack.robot
Resource    keyword/FW/kw_l2tp_server.robot