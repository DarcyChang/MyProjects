#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    # For readline input support
    import readline
except:
    pass

import sys
import os
import traceback
import codeop
import signal
import cStringIO
import cPickle
import tempfile

from cafe.core.logger import CLogger

__author__ = 'David Qian'

"""
Created on 06/16/2016
@author: David Qian

code from: http://code.activestate.com/recipes/576515/
"""

_module_logger = CLogger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info


def pipename(pid):
    """Return name of pipe to use"""
    return os.path.join(tempfile.gettempdir(), 'debug-%d' % pid)


class NamedPipe(object):
    def __init__(self, name, end=0, mode=0666):
        """Open a pair of pipes, name.in and name.out for communication
        with another process.  One process should pass 1 for end, and the
        other 0.  Data is marshalled with pickle."""
        self.in_name, self.out_name = name + '.in',  name + '.out',
        try:
            os.mkfifo(self.in_name, mode)
        except OSError:
            pass
        try:
            os.mkfifo(self.out_name, mode)
        except OSError:
            pass

        # NOTE: The order the ends are opened in is important - both ends
        # of pipe 1 must be opened before the second pipe can be opened.
        if end:
            self.inp = open(self.out_name, 'r')
            self.out = open(self.in_name, 'w')
        else:
            self.out = open(self.out_name, 'w')
            self.inp = open(self.in_name, 'r')
        self._open = True

    def is_open(self):
        return not (self.inp.closed or self.out.closed)

    def put(self, msg):
        if self.is_open():
            data = cPickle.dumps(msg, 1)
            self.out.write("%d\n" % len(data))
            self.out.write(data)
            self.out.flush()
        else:
            raise Exception("Pipe closed")

    def get(self):
        txt = self.inp.readline()
        if not txt:
            self.inp.close()
        else:
            l = int(txt)
            data = self.inp.read(l)
            if len(data) < l:
                self.inp.close()
            return cPickle.loads(data)  # Convert back to python object.

    def close(self):
        self.inp.close()
        self.out.close()
        try:
            os.remove(self.in_name)
        except OSError:
            pass
        try:
            os.remove(self.out_name)
        except OSError:
            pass

    def __del__(self):
        self.close()


def build_frame_selector(frame):
    _frame = frame

    def _select_frame(index):
        cur_frame = _frame
        while index > 0:
            if cur_frame is None:
                raise RuntimeError('Frame index is out of range')

            index -= 1
            cur_frame = cur_frame.f_back

        return cur_frame

    return _select_frame


def remote_debug(sig, frame):
    warn('Enter remote debug handler')
    warn('Stack trace: %s' % ''.join(traceback.format_stack(frame)))

    """Handler to allow process to be remotely debugged."""
    def _raise_ex(ex):
        """Raise specified exception in the remote process"""
        _raise_ex.ex = ex
    _raise_ex.ex = None

    try:
        # Provide some useful functions.
        locs = {
            '_raise_ex': _raise_ex,
            '_frame_selector': build_frame_selector(frame),
        }
        locs.update(frame.f_locals)  # Unless shadowed.
        globs = frame.f_globals

        pid = os.getpid()  # Use pipe name based on pid
        pipe = NamedPipe(pipename(pid))

        old_stdout, old_stderr = sys.stdout, sys.stderr
        txt = ''
        frame_list = traceback.format_stack(frame)
        frame_list_with_lineno = []
        index_list = range(len(frame_list))
        index_list.reverse()
        for index, line in zip(index_list, frame_list):
            frame_list_with_lineno.append('#%d    %s' % (index, line))

        msg = 'Interrupting process at following point:\n' + ''.join(frame_list_with_lineno) + '\n'
        usage = [
            'Usage:',
            'Type "_raise_ex(Exception)" to raise exception when detach from the Cafe process',
            'Type "_frame_selector(index)" to get the frame object by frame index',
        ]

        msg += '\n'.join(usage) + '\n' + '>>> '
        pipe.put(msg)

        try:
            while pipe.is_open() and _raise_ex.ex is None:
                line = pipe.get()
                if line is None:
                    # EOF
                    continue
                txt += line
                try:
                    code = codeop.compile_command(txt)
                    if code:
                        sys.stdout = cStringIO.StringIO()
                        sys.stderr = sys.stdout
                        exec code in globs, locs
                        txt = ''
                        pipe.put(sys.stdout.getvalue() + '>>> ')
                    else:
                        pipe.put('... ')
                except:
                    txt = '' # May be syntax err.
                    sys.stdout = cStringIO.StringIO()
                    sys.stderr = sys.stdout
                    traceback.print_exc()
                    pipe.put(sys.stdout.getvalue() + '>>> ')
        finally:
            sys.stdout = old_stdout # Restore redirected output.
            sys.stderr = old_stderr
            pipe.close()

    except:  # Don't allow debug exceptions to propogate to real program.
        traceback.print_exc()

    if _raise_ex.ex is not None:
        raise _raise_ex.ex


def debug_process(pid):
    """Interrupt a running process and debug it."""
    os.kill(pid, signal.SIGUSR1)  # Signal process.
    pipe = NamedPipe(pipename(pid), 1)
    try:
        while pipe.is_open():
            txt = raw_input(pipe.get()) + '\n'
            pipe.put(txt)
    except EOFError:
        # Exit.
        pass
    pipe.close()


def register_remote_debug_handler():
    # Register for remote debugging.
    signal.signal(signal.SIGUSR1, remote_debug)


