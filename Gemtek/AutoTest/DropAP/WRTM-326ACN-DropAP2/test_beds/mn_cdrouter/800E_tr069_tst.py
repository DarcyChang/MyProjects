__author__ = 'bmelhus'

#from stp.test_beds.mn_cdrouter.ont_serial import ont_rstr_dflt
#from stp.test_beds.mn_cdrouter.ont_serial import rg_chk
from datetime import datetime
import os,shutil,time,sys
import pymysql

# ont_rst_num = 0
# while ont_rst_num <= 2:
#     bogus = ont_rstr_dflt("ipoe")
#
#     time.sleep(90)
#
#     bogus = rg_chk("ipoe")
#
#     print(bogus)
#     ont_rst_num += 1

d = datetime.now()
#print(d)
dt = d.strftime('%m_%d_%Y_%I%M%S')
#print(dt)

def make_rslt_dirs(dt,cdr_rslt_file,rslt_path):
    tmp_dir_name = cdr_rslt_file.split('.')
    suite_dir = tmp_dir_name[0]
    dst_fail_path = '/opt/home/bmelhus/stp/test_beds/mn_cdrouter/results/cdr_results/'
    os.chdir(dst_fail_path)
    src_fail_txt = 'icmpv6_1.txt'
    src_fail_path_txt = rslt_path + '/' + src_fail_txt
    if not os.path.isdir('/opt/home/bmelhus/stp/test_beds/mn_cdrouter/results/cdr_results/' + suite_dir):
        os.mkdir(suite_dir)
        os.chmod(suite_dir,0777)
        os.chdir(suite_dir)
    else:
        os.chdir(suite_dir)
    if not os.path.isdir('/opt/home/bmelhus/stp/test_beds/mn_cdrouter/results/cdr_results/' + suite_dir + '/' + dt):
        os.mkdir(dt)
        os.chmod(dt,0777)
        os.chdir(dt)
    else:
        os.chdir(dt)
    dst_fail_path_txt = dst_fail_path + suite_dir + '/' + dt + '/' + src_fail_txt
    shutil.copyfile(src_fail_path_txt, dst_fail_path_txt)

#make_rslt_dirs(dt,'bogus_info.txt','/mnt/cdrResults/20151029/20151029110617')

# rg_scenario = "6rd-1"
# scenario = rg_scenario.split('-')[0]
# print(scenario)

connection = pymysql.connect(host="localhost" , user="root", passwd="calix123", db="cdr_results")

conn = connection.cursor()
conn.execute("SELECT * FROM `test_results` WHERE 1")
row = conn.fetchall()
print(row[0])

sql = "INSERT INTO `test_results` (`test_case_id`, `test_case_desc`, `test_case_rslt`) VALUES (%s, %s, %s)"

conn.execute(sql, ('test_3', 'Oh boy', 'FAIL'))

conn = connection.cursor()
conn.execute("SELECT * FROM `test_results` WHERE 1")
row = conn.fetchall()
print(row[2])

conn.close()