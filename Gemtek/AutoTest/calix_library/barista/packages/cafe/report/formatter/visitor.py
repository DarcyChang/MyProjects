#!/usr/bin/env python
# -*- coding: utf-8 -*-
from contextlib import contextmanager

__author__ = 'David Qian'

"""
Created on 07/25/2016
@author: David Qian

"""


class ConsoleOutFormatter(object):
    def __init__(self, indent=' '*4, key_value_separator='=', title_formatter='*** %s ***'):
        self._indent = indent
        self.key_value_seperator = key_value_separator
        self._title_formatter = title_formatter
        self._current_section_level = 0
        self._line_padding = 0
        self._formatted = []
        pass

    def visit_report(self, report):
        if report.title:
            self._add_to_formatted(self._title_formatter % report.title)

        for section in report.sections:
            section.visit(self)

        return self._formatted

    def visit_section(self, section):
        with self._enter_section():
            if section.title:
                self._add_to_formatted(self._title_formatter % section.title)

            self._line_padding = section.get_max_key_len()
            for line in section.lines:
                line.visit(self)

            for sub_section in section.sections:
                sub_section.visit(self)

    def visit_line(self, line):
        indent = self._current_section_level * self._indent
        self._add_to_formatted('%s%*s %s %s' %
                               (indent, -self._line_padding, line.key, self.key_value_seperator, line.value))

    def _add_to_formatted(self, s):
        self._formatted.append(s)

    @contextmanager
    def _enter_section(self):
        self._current_section_level += 1
        yield
        self._current_section_level -= 1

    def get_formatted_report(self, report):
        self.visit_report(report)
        return '\n'.join([''] + self._formatted)

