# Echo client
import socket
import sys
"""
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening.
server_name = sys.argv[1]   # 外部参数传入服务器名称 , 允许哪个地方访问
# server_address = ('localhost', 10001)   # 默认服务器名称
server_address = (server_name, 10001)

print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # send data
    message = b'This is the message. It will be repeated.'
    print('sending {!r}'.format(message))
    sock.sendall(message)

    # Look for the response.
    amount_received = 0
    amount_expected = len(message)
    datas = b''
    while amount_received < amount_expected:
        data = sock.recv(16)  # 每次接受16字节
        amount_received += len(data)
        print('received {!r}'.format(data))
        datas += data
    print(f'receive data:{type(datas), datas}')
finally:
    print('closing socket')

    sock.close()
"""

import pickle
import logging
import logging.handlers
import socketserver
import struct


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
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

class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = True

    def __init__(self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped(self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

class ServiceLog(object):
    def __init__(self, log_name):
        self.log_name = log_name

    def _logger_die(self, logger, msg):
        logger.error(msg)
        raise AssertionError(msg)

    def ret_log_file_path(self):
        return logPath + self.log_name

    def logger_writer(self, date):
        formatter = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)s][%(levelname)s][%(thread)d] %(message)s')
        DataLog = logging.getLogger(self.log_name)
        DataLog.handlers = []
        DataLog.setLevel(logging.DEBUG)
        DataLog.propagate = False

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)
        DataLog.addHandler(console)

        logfiledebug = logging.FileHandler(filename=logPath + self.log_name + '.' + date + '.debug.log', mode='a')
        logfiledebug.setFormatter(formatter)
        logfiledebug.setLevel(logging.DEBUG)
        DataLog.addHandler(logfiledebug)

        logfileinfo = logging.FileHandler(filename=logPath + self.log_name + '.' + date + '.info.log', mode='a')
        logfileinfo.setFormatter(formatter)
        logfileinfo.setLevel(logging.INFO)
        DataLog.addHandler(logfileinfo)
        DataLog.die = lambda msg: self._logger_die(DataLog, msg)
        return DataLog

def main():
    logging.basicConfig(
        format='%(relativeCreated)5d %(name)-15s %(levelname)-8s %(message)s')
    tcpserver = LogRecordSocketReceiver()
    print('About to start TCP server...')
    tcpserver.serve_until_stopped()

if __name__ == '__main__':
    main()



