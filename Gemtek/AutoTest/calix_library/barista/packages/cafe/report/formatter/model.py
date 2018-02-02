#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

__author__ = 'David Qian'

"""
Created on 07/21/2016
@author: David Qian

"""


class IVisitable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit(self, visitor):
        pass


class Line(IVisitable):
    def __init__(self, key, value):
        self.key = str(key)
        self.value = str(value)

    def visit(self, visitor):
        visitor.visit_line(self)


class Section(IVisitable):
    def __init__(self, title=''):
        self.title = title
        self.sections = []
        self.lines = []

    def add_line(self, *args):
        if len(args) == 1 and isinstance(args[0], Line):
            line = args[0]
        else:
            line = Line(*args)
        self.lines.append(line)

    def add_section(self, section):
        self.sections.append(section)

    def get_max_key_len(self):
        return max(map(lambda x: len(x.key), self.lines))

    def visit(self, visitor):
        visitor.visit_section(self)


class Report(IVisitable):
    def __init__(self, title=''):
        self.title = title
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)

    def visit(self, visitor):
        visitor.visit_report(self)
