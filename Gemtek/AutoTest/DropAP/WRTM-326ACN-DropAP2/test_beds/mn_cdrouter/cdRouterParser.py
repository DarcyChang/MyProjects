#!/usr/bin/env python
# Author: Me
# Purpose: SSH into list of devices and run list of commands

import re,os.path,shutil,os
from stp.test_beds.mn_cdrouter.cdr_rslt_compile import add_to_rslt_file
from datetime import datetime
from stp.test_beds.mn_cdrouter.add_rslt_db import add_rslt

# Ensuring variables exist
resultfile, rslt_path, dbglvl = "default", "default", "default"

def parsefile(resultfile, rslt_path, dbglvl):
    #----------------------------------------
    # Opens files in read mode
    #----------------------------------------
    f1 = open(rslt_path + resultfile, "r")

    passline = []
    failline = []
    gidlistvalues = []
    gidrslt = dict()
    giddesc = dict()
    rsltfile_gid = str()
    rsltfile_rslt = str()
    rsltfile_desc = str()
    test_start_fail = 0
    
    for line in f1.readlines():
        if re.search('Skipping', line, re.I) and re.search('fatal', line, re.I):
            test_start_fail = 1
        elif re.search('^cdr', line, re.I):
            #print("Found Result!")
            if re.search('\+FAIL', line, re.I):
                #print("Adding Failure!")
                failline.append(line.strip())
            elif re.search('Pass', line, re.I):
                #print("Adding Pass!")
                passline.append(line.strip())

    passcnt = len(passline)
    failcnt = len(failline)

    if test_start_fail == 1:
        print("\n\nCD Router test didn't start!")
    else:
        print("\n\nThis is number of pass lines: " + str(passcnt))
        print("This is number of fail lines: " + str(failcnt) + "\n")
    
    if dbglvl == "dbg":
        print("\n#=============================================================================================================")
        print("# Test Cases that have Passed!")
        print("#-------------------------------------------------------------------------------------------------------------")
    for i in range(len(passline)):
        #print(len(passline))
        #print("Line info for Pass Line " + str(i) + ": " + passline[i])
        linepass = re.split('\|',passline[i])
        passinfo = re.split('\s+',linepass[0])
        gidlistvalues.append(passinfo[0])
        rsltfile_gid = passinfo[0]
        rsltfile_rslt = passinfo[1]
        rsltfile_desc = linepass[1]
        if dbglvl == "dbg":
            print("Test Case: " + rsltfile_gid + " --> Status: " + rsltfile_rslt + "\nDescription: " + rsltfile_desc + "\n")
        gidrslt[rsltfile_gid] = rsltfile_rslt
        giddesc[rsltfile_gid] = rsltfile_desc.lstrip()
    if dbglvl == "dbg":
        print("\n#=============================================================================================================")
        print("# Test Cases that have Failed!")
        print("#-------------------------------------------------------------------------------------------------------------")
    for i in range(len(failline)):
        #print(len(failline))
        linefail = re.split('\|',failline[i])
        failinfo = re.split('\s+',linefail[0])
        gidlistvalues.append(failinfo[0])
        rsltfile_gid = failinfo[0]
        rsltfile_rslt = failinfo[1]
        rsltfile_desc = linefail[1]
        if dbglvl == "dbg":
            print("Test Case: " + rsltfile_gid + " --> Status: " + rsltfile_rslt + "\nDescription: " + rsltfile_desc + "\n")
        gidrslt[rsltfile_gid] = rsltfile_rslt
        giddesc[rsltfile_gid] = rsltfile_desc.lstrip()
    if dbglvl == "dbg":
        print("Global Test Case IDs:")
        print(gidrslt.keys())
        print("Results:")
        print(gidrslt.values())
        print("\nGlobal Test Case IDs:")
        print(giddesc.keys())
        print("Descriptions:")
        print(giddesc.values())
    f1.close()
    #print(len(gidlistvalues))
    #print(gidlistvalues)
    gidlistvalues.sort()
    return (gidlistvalues,gidrslt,giddesc)

def step(ext, dirname, names):
    #print("\ncreating file list\n")
    fnamelist = []
    ext = ext.lower()
    
    for name in names:
        if name.lower().endswith(ext):
            #print(os.path.join(dirname, name))
            fname = os.path.join(dirname, name)
            if not re.search('start', fname, re.I):
                #print("Not Start")
                if not re.search('final', fname, re.I):
                    #print("Not Final")
                    if not re.search('filelist', fname, re.I):
                        #print("Adding fname: " + fname)
                        fnamelist.append(fname)
    if dbglvl == "dbg":
        print(dirname)
    filelist = open(dirname + 'filelist.txt', "w")
    for i in range(len(fnamelist)):
        filelist.write(fnamelist[i] + "\n")
    filelist.close()
    if dbglvl == "dbg":
        print(fnamelist)
    
def gidvalues(rslt_path):
    gid = str()
    tmod = str()
    tname = str()
    gidlist = dict()
    fnamelst = []
    dbglvl = "dbg"
    
    filelist = open(rslt_path + 'filelist.txt', "r")
    for line in filelist.readlines():
        #print(line.strip())
        fnamelst.append(line.strip())
    filelist.close()
    #print(len(fnamelst))
    
    for i in range(len(fnamelst)):
        if dbglvl == "dbg":
            print("Filename list count: " + str(i))
            print("This is fPath/fName: " + fnamelst[i])
        f2 = open(fnamelst[i], "r")
        f3 = open(fnamelst[i], "r")
        #Test cdr-mp-3187: Verify IPv6 DNS proxy does not cache DNS entry when DNS TTL is 0
        #Module: dns-v6.tcl
        #Name: ipv6_dns_10
        found_gid = False
        while found_gid == False:
            for line in f2.readlines():
                if re.search('^Test', line, re.I) and re.search("cdr", line, re.I):
                    newline = re.split(':',line)
                    globalid = re.split('\s+',newline[0])
                    gid = globalid[1]
                    found_gid = True
        for line in f3.readlines():
            if re.search('^Module', line, re.I):
                tcmodule = re.split(':',line)
                tmod = tcmodule[1]
            elif re.search('^Name', line, re.I):
                tcname = re.split(':',line)
                tname = tcname[1]
        gidlist[gid] = tname.strip()
        if dbglvl == "dbg":
            print("Global ID: " + gid + " --> Module: " + tmod.strip() + " --> TC Name: " + tname.strip() + "\n")
        f2.close()
        f3.close()
    if dbglvl == "dbg":
        print(gidlist.keys())
        print(gidlist.values())
    return gidlist

def cmprslt(gidrslt, giddesc, gidlist):
    print("something")
    

#---------------------------------------------------
# Execute Procedure(s)
#---------------------------------------------------
def print2screen(resultfile, rslt_path, cdr_rslt_file, dbglvl):
    d = datetime.now()
    dt = d.strftime('%m%d%Y%H%M%S')
    db_dt = d.strftime('%m/%d/%Y %H:%M:%S')
    print(dt)
    #----------------------------------------
    # This prints the given arugments
    #----------------------------------------
    print('{0:20} {1:50}'.format("Result File: ", resultfile))
    print('{0:20} {1:50}'.format("Result File Path: ", rslt_path))
    print('{0:20} {1:50}'.format("Debug Level: ", str(dbglvl)))

    d = datetime.now()
    print('{0:20} {1:50}'.format("Compiled Results: ", str(d)))

    # The top argument for walk. The
    # Python27/Lib/site-packages folder in my case
    topdir = rslt_path

    # The arg argument for walk, and subsequently ext for step
    exten = '.txt'
    gidlistvalues,gidrslt,giddesc = parsefile(resultfile, rslt_path, dbglvl)
    os.path.walk(topdir, step, exten)
    gidlist = gidvalues(rslt_path)
    if len(gidlistvalues) == 0:
        return False
    if dbglvl == "dbg":
        print("\n---------------------------------------------------------------------------------------------------")
        print("\nGlobal ID to TC Name Mapping:")
        print(gidlist)
        print("\nGlobal ID to TC Result Mapping:")
        print(gidrslt)
        print("\nGlobal ID to TC Description Mapping:")
        print(giddesc)

    if dbglvl == "dbg":
        print(len(gidlistvalues))
        for i in range(len(gidlistvalues)):
            gidchkval = gidlistvalues[i]
            print('{0:20} {1:50}'.format(("\n\nIndex " + str(i) + ":"), ("CD Router Global ID: " + gidchkval)))
            print('{0:20} {1:50}'.format("Test Suite ID: ", gidlist[gidchkval]))
            print('{0:20} {1:50}'.format("Test Case Result: ", gidrslt[gidchkval]))
            print('{0:20} {1:50}'.format("Test Case Desc: ", giddesc[gidchkval]))
    if dbglvl == "info":
        print("\n\n#------------------------------------------------------------------------------------------------")
        print("# Passing TCs:")
        print("#------------------------------------------------------------------------------------------------")
        for i in range(len(gidlistvalues)):
            gidchkval = gidlistvalues[i]
            if re.search('Pass', gidrslt[gidchkval], re.I):
                print('{0:25} {1:6} {2:8} {3:55}'.format(gidlist[gidchkval], ": PASS", "| Desc: ", giddesc[gidchkval]))
    if dbglvl == "info":
        print("\n\n#------------------------------------------------------------------------------------------------")
        print("# Failing TCs:")
        print("#------------------------------------------------------------------------------------------------")
        for i in range(len(gidlistvalues)):
            gidchkval = gidlistvalues[i]
            if re.search('Fail', gidrslt[gidchkval], re.I):
                print('{0:25} {1:6} {2:8} {3:55}'.format(gidlist[gidchkval], ": FAIL", "| Desc: ", giddesc[gidchkval]))

    #----------------------------------------------------------------------------------
    # Add CD Router Results to file cdr_rslt_file
    #
    pass_cnt = 0
    fail_cnt = 0
    tmp_suite_name = cdr_rslt_file.split('_')
    if len(tmp_suite_name) == 5:
        suite_name = tmp_suite_name[0] + "_" + tmp_suite_name[1] + "_" + tmp_suite_name[2]
        vut = tmp_suite_name[3]
        eut = tmp_suite_name[4]
        eut = eut.split('.')[0]
    elif len(tmp_suite_name) == 6:
        suite_name = tmp_suite_name[0] + "_" + tmp_suite_name[1] + "_" + tmp_suite_name[2] + "_"  + tmp_suite_name[3]
        vut = tmp_suite_name[4]
        eut = tmp_suite_name[5]
    elif len(tmp_suite_name) == 7:
        suite_name = tmp_suite_name[0] + "_" + tmp_suite_name[1] + "_" + tmp_suite_name[2] + "_"  + tmp_suite_name[3] + "_"  + tmp_suite_name[4]
        vut = tmp_suite_name[5]
        eut = tmp_suite_name[6]
    eut = eut.split('.')[0]
    web_path = '/cdr_results/' + suite_name + '_' + vut + '_' + eut + '/' + dt + '/'
    add_to_rslt_file(cdr_rslt_file,"# CDR Test Suite: " + str(suite_name))
    add_to_rslt_file(cdr_rslt_file,"# Test Completed: " + str(d))
    add_to_rslt_file(cdr_rslt_file,"#------------------------------------------------------------------------------------------------")
    add_to_rslt_file(cdr_rslt_file,"# Passing TCs:")
    add_to_rslt_file(cdr_rslt_file,"#------------------------------------------------------------------------------------------------")
    for i in range(len(gidlistvalues)):
        gidchkval = gidlistvalues[i]
        if re.search('Pass', gidrslt[gidchkval], re.I):
            pass_cnt += 1
            add_to_rslt_file(cdr_rslt_file, gidlist[gidchkval] + ": PASS" + "| Desc: " + giddesc[gidchkval])
            # Add Pass Result to DB
            add_rslt(eut=eut, vut=vut.replace('-','.'), test_suite=suite_name, tc_name=gidlist[gidchkval], tc_desc=giddesc[gidchkval], tc_rslt='PASS', tc_dt=db_dt, web_path=web_path)
    add_to_rslt_file(cdr_rslt_file,"#------------------------------------------------------------------------------------------------")
    add_to_rslt_file(cdr_rslt_file,"# Pass Count: " + str(pass_cnt))
    add_to_rslt_file(cdr_rslt_file,"#------------------------------------------------------------------------------------------------")
    add_to_rslt_file(cdr_rslt_file, "\n")
    add_to_rslt_file(cdr_rslt_file,"#------------------------------------------------------------------------------------------------")
    add_to_rslt_file(cdr_rslt_file,"# Failing TCs:")
    add_to_rslt_file(cdr_rslt_file,"#------------------------------------------------------------------------------------------------")
    make_dir = True
    for i in range(len(gidlistvalues)):
        gidchkval = gidlistvalues[i]
        if re.search('Fail', gidrslt[gidchkval], re.I):
            fail_cnt += 1
            add_to_rslt_file(cdr_rslt_file, gidlist[gidchkval] + ": FAIL" + "| Desc: " + giddesc[gidchkval])
            make_rslt_dirs(dt, cdr_rslt_file, gidlist[gidchkval], rslt_path)
            # Add Fail Result to DB
            add_rslt(eut=eut, vut=vut.replace('-','.'), test_suite=suite_name, tc_name=gidlist[gidchkval], tc_desc=giddesc[gidchkval], tc_rslt='FAIL', tc_dt=db_dt, web_path=web_path)
    add_to_rslt_file(cdr_rslt_file,"#------------------------------------------------------------------------------------------------")
    add_to_rslt_file(cdr_rslt_file,"# Fail Count: " + str(fail_cnt))
    add_to_rslt_file(cdr_rslt_file,"#========================================== END OF TEST =========================================")
    add_to_rslt_file(cdr_rslt_file, "\n")


def make_rslt_dirs(dt, cdr_rslt_file, fail_txt, rslt_path):
    #---------------------------------------------------------
    # Code to copy failed test case txt file to CD Router Results directory on Cafe Machine
    #
    tmp_dir_name = cdr_rslt_file.split('.')
    suite_dir = tmp_dir_name[0]
    dst_fail_path = '/opt/home/bmelhus/stp/test_beds/mn_cdrouter/results/cdr_results/'
    os.chdir(dst_fail_path)
    src_fail_txt = fail_txt + '.txt'
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
    return True
# END

#Usage: python C:\Auto_Scripts\PythonScripts\cdRouterParser.py -f final.txt -r P:/20150616/20150616004217/ -d 0
