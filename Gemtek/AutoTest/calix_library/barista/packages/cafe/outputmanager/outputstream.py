import sys
import os

__author__ = "akhanov"


class OutputStream(object):
    def __init__(self, output_stream=sys.stdout):
        self.__ostream = output_stream

        self.closed = self.__ostream.closed

        try:
            self.encoding = self.__ostream.encoding
        except AttributeError:
            # self.encoding = None
            pass

        try:
            self.errors = self.__ostream.errors
        except AttributeError:
            # self.errors = None
            pass

        try:
            self.mode = self.__ostream.mode
        except AttributeError:
            pass

        try:
            self.name = self.__ostream.name
        except AttributeError:
            pass

        try:
            self.newlines = self.__ostream.newlines
        except AttributeError:
            pass

        try:
            self.softspace = self.__ostream.softspace
        except AttributeError:
            pass

        self._new_section = True
        # self.__written = 0

    def __iter__(self):
        return self.__ostream.__iter__()

    # Special, non-File-interface methods here

    # def add_written(self, num_chars):
    #     self.__written += num_chars
    #
    # def get_written(self):
    #     return self.__written
    def new_section(self):
        self._new_section = True

    def section_output_started(self):
        self._new_section = False

    # End; Here follow implementations of standard File Object interface

    def get_stream(self):
        return self.__ostream

    def close(self):
        self.__ostream.close()
        self.closed = self.__ostream.closed

    def flush(self):
        self.__ostream.flush()

    def fileno(self):
        return self.__ostream.fileno()

    def isatty(self):
        return self.__ostream.isatty()

    def next(self):
        return self.__ostream.next()

    def read(self, size=-1):
        return self.__ostream.read(size)

    def readline(self, size=-1):
        return self.__ostream.readline(size)

    def readlines(self, sizehint=-1):
        return self.__ostream.readlines(sizehint)

    def seek(self, offset, whence=os.SEEK_SET):
        return self.__ostream.seek(offset, whence)

    def tell(self):
        return self.__ostream.tell()

    def truncate(self, size=None):
        return self.__ostream.truncate(size)

    def write(self, str):
        return self.__ostream.write(str)

    def writelines(self, sequence):
        return self.__ostream.writelines(sequence)
