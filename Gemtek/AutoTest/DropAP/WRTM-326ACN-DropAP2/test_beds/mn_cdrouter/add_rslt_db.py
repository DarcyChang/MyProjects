__author__ = 'bmelhus'

import pymysql.cursors

def add_rslt(eut, vut, test_suite, tc_name, tc_desc, tc_rslt, tc_dt, web_path):

    connection = pymysql.connect(host="localhost" , user="root", passwd="calix123", db="cdr_results")

    conn = connection.cursor()

    sql = "INSERT INTO `test_results` (`eut`, `vut`, `test_suite`, `test_case_id`, `test_case_desc`, `test_case_rslt`, `test_case_dt`, `web_path`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    conn.execute(sql, (eut, vut, test_suite, tc_name, tc_desc, tc_rslt, tc_dt, web_path))
    connection.commit()
    connection.close()


#add_rslt(eut='800GH', vut='P11.1M7', tc_name='test_1', tc_desc='Sumpin Sumpin', tc_rslt='PASS', tc_dt='110220150123')