
"""

fork 线程， 新线程 id 在子进程中
扩展阅读
• Standard library documentation for socketserver.15
• socket (page 693): Low-level network communication.
• select (page 728): Low-level asynchronous I/O tools.
• asyncio (page 617): Asynchronous I/O, event loop, and concurrency tools.
• SimpleXMLRPCServer: XML-RPC server built using socketserver.
• Unix Network Programming, Volume 1: The Sockets Networking API, Third Edition, by W. Richard Stevens, Bill Fenner,
    and Andrew M. Rudoff. Addison-Wesley, 2004. ISBN-10: 0131411551.
• Foundations of Python Network Programming, Third Edition, by Brandon Rhodes and John Goerzen. Apress, 2014. ISBN-10: 1430258543.

"""
import os
import socketserver
from py_socket_binary_data import win_platform, renew_listen_port


class ForkingEchoRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Echo the data back to the client.
        data = self.request.recv(1024)
        cur_pid = os.getpid()
        response = b'%d: %s' % (cur_pid, data)
        self.request.send(response)

        return


class ForkingEchoServer(socketserver.ForkingMixIn, socketserver.TCPServer,):
    pass


if __name__ == '__main__':
    import socket
    import threading
    """
    此例中，线程id 包含在子进程中。
    In this case, the process ID of the child is included in the response from the server.
    """
    new_port = renew_listen_port()
    address = ('localhost', new_port)  # Let the kernel assign a port

    server = ForkingEchoServer(address, ForkingEchoRequestHandler)

    ip, port = server.server_address  # 取得注册的ip和端口
    print(f'address:{address}, ip-port:{ip, port}')

    t = threading.Thread(target=server.serve_forever)
    print(f'thread name :{t.getName()} os pid:{os.getpid()}')
    t.setDaemon(True)   # Don't hang on exit
    t.start()

    print('Server loop running in process:', os.getpid())

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Send the data
    message = 'Hello, world'.encode()
    print('Sending: {!r}'.format(message))
    len_sent = s.send(message)

    # Receive a response.
    response = s.recv(1024)
    print('Received: {!r}'.format(response))

    # Clean up
    server.shutdown()
    s.close()
    server.socket.close()

