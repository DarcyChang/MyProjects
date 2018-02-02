#import os,sys
import re,os
import sys
import time
from caferobot.command.adapter import CliAdapter
import sqlite3
# import pysftp
import cdrouter_parameters


class cdr_python_keywords(object):
    __shell_prompt="]$"
    __db_prompt = 'sqlite>'
    __traf_prompt = 'traf.'
    _maxtime = 360000

    def cdr_run_package(self, cdr_connection, package_name):
        cmd = "buddyweb -package " + str(package_name)
        print cmd
        res = CliAdapter.cli(cdr_connection, cmd, self.__shell_prompt, None, None)
        #res = "Starting package AQA-800G-CDRouter-apps-auto Requesting http://127.0.0.1:8015/jobs/launch.txt?name=AQA-800G-CDRouter-apps-auto& Package AQA-800G-CDRouter-apps-auto has been started with job id 8564"
        print res
        job_id = re.search(r"job id \d+", res)
        id = re.search(r"\d+", job_id.group())
        return id.group()

    def cdr_check_status(self, cdr_connection, job_id, max_time = _maxtime):
        i = 0
        while i < max_time:
            i += 3
            cmd = "buddyweb -status " + job_id
            print cmd
            res = CliAdapter.cli(cdr_connection, cmd, self.__shell_prompt, None, None)
            print 'blw' + res
            time.sleep(3)
            res = re.search(r"finished", res)
            if res == None:
                continue
            else:
                return 1
        return 0

    def cdr_get_result_id(self, cdr_connection, job_id, is_finished):
        if is_finished == 0:
            return 0
        else:
            cmd = "buddyweb -status " + job_id + " -show-result-id"
            result_id = CliAdapter.cli(cdr_connection, cmd, self.__shell_prompt, None, None)
            dir = re.search(r"\d{14}",result_id)
            return dir.group()


    def cdr_get_result_db_file_name(self, dir):
        res = re.search(r"\d{8}", dir)
        db_path = "/usr/buddyweb/results/" + str(res.group()) + \
                 '/' + dir + '/' + dir + ".bwdb"
        return db_path


    def cdr_sftp_get_db_file_from_cdr(self, cdr_ip, cdr_user_name, cdr_password, db_path):
        temp_db = 'cdr.bwdb'
        connection = pysftp.Connection(cdr_ip, cdr_user_name, password=cdr_password)
        connection.get(db_path, temp_db)
        connection.close()
        print "Upload done"
        return temp_db

    def cdr_make_report(self, cdr_db, assignee, result_id, UserInterface, EUT):
        db = sqlite3.connect(cdr_db)
        res = db.execute("select test_id,status,time from results;")
        res1 = db.execute("select name from tests;")
        result = res.fetchall()
        result.remove(result[0])
        result.remove(result[-1])
        test_name = res1.fetchall()
        test_name.remove(test_name[0])
        test_name.remove(test_name[-1])
        print result
        print test_name
        gid = []
        case = []
        case_all = []
        report = []
        for name in test_name:
            name = list(name)
            global_id = cdrouter_parameters.adict[name[0]]
            global_id_tms = str(global_id) + UserInterface + EUT
            name.append(global_id_tms)
            gid.append(name)
            print gid
        for item in result:
            item = list(item)
            status = str(item[1])
            status = status.lower()
            status = status.title()
            if status == "Pending":
                status = "Untest"
            elif status == "Skip":
                status = "Pass"
            item[1] = status
            # if item[1] == "PASS":
            #     item[1] = "Pass"
            #     else if item[1] == "FAIL"
            case.append(item)
            print case
        for i in range(0, len(result)-1):
            item1 = case[i] + gid[i]
            case_all.append(item1)
            print case_all
        report.insert(0, case_all)
        report.insert(0, result_id)
        report.insert(0, assignee)
        print report
        return report




        # for item in result:
        #     item = list(item)
        #     for name in test_name:
        #         name = list(name)
        #         global_id = cdrouter_parameters.adict[name[0]]
        #         global_id_tms = str(global_id) + UserInterface + EUT
        #         # item.append(name[0])
        #         # item.append(global_id_tms)
        #         # print item
        #     item.append(name[0])
        #     item.append(global_id_tms)
        #     case.append(item)
        #     print case
        # for item in result:
        #     item = list(item)
        #     item[3] = item[3][:-4:]
        #     global_id = cdrouter_parameters.adict[item[3]]
        #     global_id_tms = str(global_id) + UserInterface + EUT
        #     item.append(global_id_tms)
        #     print item
        #     case.append(item)
        #     print case
        # report.insert(0, case)
        # report.insert(0, result_id)
        # report.insert(0, assignee)
        # print report
        # return report
        #


















































            # cmd = "sqlite3 " + db
            # res = CliAdapter.cli(cdr_connection, cmd , self.__db_prompt, None, None)
            # # print "111" + res
            # cmd = "select test_id,status,time,logfile from results;"
            # res = CliAdapter.cli(cdr_connection, cmd , self.__db_prompt, None, None)
            # # print "222" + res
            # cmd = ".quit"
            # CliAdapter.cli(cdr_connection, cmd , self.__db_prompt, None, None)
            # return res

    # def make_report(self, db_info, vm, result_id, package_name):
    #     # p = re.compile()
    #
    #     report = cdr_report()
    #     cmd ="python"
    #     CliAdapter.cli(vm, cmd , self.__db_prompt, None, None)
    #     cmd = getpass.getuser()
    #     report.assignee = CliAdapter.cli(vm, cmd , self.__db_prompt, None, None)
    #
    #     report.result_id = result_id
    #
    #     report.package_name = package_name
    #
    #     case_info = cdr_case_info()


        # while(3:N-1):
        #     # do process data line by line here:   process_data(db_info)
        #     case_info.case_id = ^id|
        #     case_info.case_status = |status|,
        #     case_info.case_time = |time|
        #     case_info.case_name = |name#.txt
        #     report.cases_info.append(case_info)
        #
        # print "123" + db_info
#     _n    umber = 1
#
#     def __init__(self, num):
#         self._number = num
#
#     def group(self):
#         return self._number
#
# job_id = intrger(5)
#
# print job_id
# print job_id.group()


















