#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

import re
from argparse import ArgumentParser

import requests
from multiprocessing import Process

__author__ = 'David Qian'

from robot import libdoc

"""
Created on 03/08/2016
@author: David Qian

"""

__UNKNOW_BRANCH = 'UNKNOWN'
__DEFAULT_RFDOC_SERVER = 'http://cdc-cafe:8000/upload'
__DEFAULT_ROBOT_FILES = [os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../caferobot/cafebase.robot')]


def get_all_keywords_info(robot_file):
    ret_list = []
    with open(robot_file, 'r') as f:
        for line in f:
            line = line.strip()

            if line.startswith('#') or not line.startswith('Library'):
                continue

            info = [e for e in line.split(' ') if e != '']
            class_name = info[1]
            lib_name = class_name.split('.')[-1]
            ret_list.append([class_name, lib_name])

    return ret_list


def get_branch_name():
    try:
        cur_dir = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        info = subprocess.check_output(['git', 'branch'])
    except (OSError, RuntimeError, BaseException):
        info = ''

    finally:
        os.chdir(cur_dir)

    g = re.search(r'\*\s+(.+)', info)
    branch_name = g.group(1) if g else __UNKNOW_BRANCH
    return branch_name


def generate_and_update_rfdoc(info_list, branch_name, doc_server):
    for e in info_list:
        class_name = e[0]
        lib_name = e[1]
        file_name = lib_name + '.xml'

        print '* process %s' % class_name
        generate_and_update_rfdoc_for_lib(class_name, file_name, lib_name, branch_name, doc_server)


def generate_and_update_rfdoc_for_lib(class_name, file_name, lib_name, branch_name, doc_server):
    # generate doc file
    if not file_name.endswith('.xml'):
        file_name += '.xml'

    p = Process(target=libdoc.libdoc_cli, args=([class_name, file_name], ))
    p.start()
    p.join()

    # upload file to doc server
    payload = {
        'override_name': lib_name,
        'override_version': branch_name,
        'override': 'on'
    }

    r = requests.post(doc_server, data=payload, files={'file': open(file_name, 'rb')})
    if r.status_code != 200:
        print 'ERROR: process %s failed, result code is %d' % (class_name, r.status_code)
    os.remove(file_name)


def _process_args(args):
    if args['branch']:
        branch_name = args['branch']
    else:
        branch_name = get_branch_name()
        if branch_name == __UNKNOW_BRANCH:
            print 'Cannot get the branch name.'
            exit(2)

    server = args['server'] if args['server'] else __DEFAULT_RFDOC_SERVER
    robot_files = args['file'] if args['file'] else __DEFAULT_ROBOT_FILES

    return branch_name, server, robot_files


if __name__ == '__main__':
    arg_parser = ArgumentParser(description="Robot keywords doc generator")
    arg_parser.add_argument('-b', '--branch', help='Git branch of these docs')
    arg_parser.add_argument('-s', '--server', help='RF doc server upload interface')
    arg_parser.add_argument('-f', '--file', nargs='+', help='Robot files contain the keywords libraries')

    args = arg_parser.parse_args()
    args = vars(args)

    branch_name, server, robot_files = _process_args(args)
    print 'Branch: %s' % branch_name
    print 'RF doc server: %s' % server
    print 'Robot files:'
    for f in robot_files:
        print ' '*4 + '%s' % f

    print '-'*60

    robot_libraries = []
    for f in robot_files:
        t = get_all_keywords_info(f)
        robot_libraries.extend(t)

    generate_and_update_rfdoc(robot_libraries, branch_name, server)
