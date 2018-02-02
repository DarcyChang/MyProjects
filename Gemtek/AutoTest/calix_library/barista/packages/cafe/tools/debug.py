#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from argparse import ArgumentParser

from cafe.util.stacktrace import debug_process

__author__ = 'David Qian'

"""
Created on 06/16/2016
@author: David Qian


"""


if __name__ == '__main__':
    arg_parser = ArgumentParser(description="Cafe running debugger")
    arg_parser.add_argument('pid', help='pid of cafe process')
    args = arg_parser.parse_args()
    args = vars(args)

    pid = int(args['pid'])
    print 'Connecting process {} ...'.format(pid)
    debug_process(pid)
