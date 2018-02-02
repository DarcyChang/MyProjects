__author__ = 'kelvin'
"""
Network logging server
code was getting from python 2.7 cookbook.
"""
import SocketServer
import cPickle as pickle
import struct
import logging
import logging.handlers
import threading

from cafe.core.decorators import SingletonClass


class LogRecordStreamHandler(SocketServer.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle(self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self, data):
        return pickle.loads(data)

    def handleLogRecord(self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)

@SingletonClass
# class LogRecordSocketReceiver(SocketServer.ThreadingTCPServer):
class LogRecordSocketReceiver(SocketServer.TCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = 1

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        # SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
        SocketServer.TCPServer.__init__(self, (host, port), handler)
        self.abort = threading.Event()
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        print('About to start Log server...')
        print(threading.currentThread().getName())
        import select
        self.abort.clear()
        while not self.abort.isSet():
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort
        print("log server stop")

    def stop(self):
        self.abort.set()


def get_log_server(host="localhost", port=logging.handlers.DEFAULT_TCP_LOGGING_PORT, handler=LogRecordStreamHandler):
    """
    create log server object
    example usage:
    server = get_log_server()
    t = threading.Thread(target=server.serve_until_stopped)
    t.daemon = True
    server.start()
    time.sleep(30)
    server.stop()

    :param host:host/ip of the log server
    :param port: tcp port of the log server
    :return: log server object
    """
    _server = LogRecordSocketReceiver(host=host, port=port, handler=handler)
    return _server

if __name__ == "__main__":
    logging.getLogger('')
    logging.basicConfig(level = logging.DEBUG,
                    format = "[%(asctime)s] - %(name)s - %(levelname)s: %(message)s",
                    datefmt = "%Y-%m-%d %H:%M:%S")
    import time
    from threading import Thread
    server = get_log_server()
    t = Thread(target=server.serve_until_stopped, name='ROBOT_LOG_THREAD')
    t.daemon = True
    t.start()
    time.sleep(10)
    server.stop()
    time.sleep(10)