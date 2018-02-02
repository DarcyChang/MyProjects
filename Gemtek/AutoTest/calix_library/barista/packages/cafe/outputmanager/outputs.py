from __future__ import print_function

import sys
import os
import fcntl
import termios
import struct
from outputmanager import output_manager
from outputstream import OutputStream

RAW_STDOUT = 'raw_stdout'
TC_STDOUT = 'tc_stdout'
TC_STDERR = 'tc_stderr'
STEP_STDOUT = 'step_stdout'


def terminal_size():
    try:
        h, w, hp, wp = struct.unpack('HHHH',
                                     fcntl.ioctl(
                                         0,
                                         termios.TIOCGWINSZ,
                                         struct.pack('HHHH', 0, 0, 0, 0)
                                     ))
    except:
        w = 80
        h = 24

    return w, h


class RawStdOutStream(OutputStream):
    def __init__(self):
        super(RawStdOutStream, self).__init__(sys.__stdout__)


class TcStdOutStream(OutputStream):
    def __init__(self):
        super(TcStdOutStream, self).__init__(sys.__stdout__)
        self.__line_start = self._remove_tabs("\t\t| ")
        self.new_section()
        self.__chars_in_line = 0

    def _remove_tabs(self, s):
        return s.replace('\t', '    ')

    def write(self, s):
        # lines = str.split('\n')

        # self.get_stream().write("\t\t| %s" % str)
        # self.__written += len(str)
        string = self._remove_tabs(s)

        t_width, t_height = terminal_size()

        for char in string:
            s = '\n%s' % self.__line_start

            if self._new_section:
                self.get_stream().write(s)
                self.__chars_in_line = len(s)

            if char == '\n' or char == '\r':
                self.get_stream().write(s)
                self.__chars_in_line += 1
            else:
                self.get_stream().write(char)
                self.__chars_in_line += 1

            if 'PYCHARM_HOSTED' not in os.environ or os.environ['PYCHARM_HOSTED'] == '0':
                if self.__chars_in_line >= t_width:
                    self.get_stream().write(s)
                    self.__chars_in_line = len(s)

            self.section_output_started()


class TcStdErrStream(OutputStream):
    def __init__(self):
        super(TcStdErrStream, self).__init__(sys.__stdout__)
        self.__line_start = self._remove_tabs("\t\t> ")
        # self.__line_start = self._remove_tabs("\t\t")
        self.new_section()
        self.__chars_in_line = 0

    def _remove_tabs(self, s):
        return s.replace('\t', '    ')

    def write(self, s):
        # lines = str.split('\n')

        # self.get_stream().write("\t\t| %s" % str)
        # self.__written += len(str)
        string = self._remove_tabs(s)

        t_width, t_height = terminal_size()

        self.get_stream().write("\033[0;31m")

        for char in string:
            s = '\n%s' % self.__line_start

            if self._new_section:
                self.get_stream().write(s)
                self.__chars_in_line = len(s)

            if char == '\n':
                self.get_stream().write(s)
                self.__chars_in_line += 1
            else:
                self.get_stream().write(char)
                self.__chars_in_line += 1

            if 'PYCHARM_HOSTED' not in os.environ or os.environ['PYCHARM_HOSTED'] == '0':
                if self.__chars_in_line >= t_width:
                    self.get_stream().write(s)
                    self.__chars_in_line = len(s)

            self.section_output_started()

        self.get_stream().write("\033[0m")


class StepPassStream(TcStdOutStream):
    def __init__(self):
        super(StepPassStream, self).__init__()
        self.__line_start = self._remove_tabs("\t\t@ ")
        self.new_section()
        self.__chars_in_line = 0


    def write(self, s):
        # lines = str.split('\n')

        # self.get_stream().write("\t\t| %s" % str)
        # self.__written += len(str)
        string = self._remove_tabs(s)

        t_width, t_height = terminal_size()

        for char in string:
            s = '\n%s' % self.__line_start

            if self._new_section:
                self.get_stream().write(s)
                self.__chars_in_line = len(s)

            if char == '\n' or char == '\r':
                self.get_stream().write(s)
                self.__chars_in_line += 1
            else:
                self.get_stream().write(char)
                self.__chars_in_line += 1

            if 'PYCHARM_HOSTED' not in os.environ or os.environ['PYCHARM_HOSTED'] == '0':
                if self.__chars_in_line >= t_width:
                    self.get_stream().write(s)
                    self.__chars_in_line = len(s)

            self.section_output_started()

RAW_STDOUT_STREAM = RawStdOutStream()
TC_STDOUT_STREAM = TcStdOutStream()
TC_STDERR_STREAM = TcStdErrStream()
STEP_STDOUT_STREAM = StepPassStream()

def register_streams():
    output_manager.register(RAW_STDOUT, RAW_STDOUT_STREAM)
    output_manager.register(TC_STDOUT, TC_STDOUT_STREAM)
    output_manager.register(TC_STDERR, TC_STDERR_STREAM)
    output_manager.register(STEP_STDOUT, STEP_STDOUT_STREAM)
    # output_manager.register(STEP_STDOUT, StepFailStream())


def print_raw_stdout(str):
    print(str, file=output_manager[RAW_STDOUT])


def print_tc_stdout(str):
    print(str, file=output_manager[TC_STDOUT])


if __name__ == "__main__":
    register_streams()
    print_raw_stdout("Hello from RAW!!!!")
    print_tc_stdout("Hello from inside a testcase!!!")
