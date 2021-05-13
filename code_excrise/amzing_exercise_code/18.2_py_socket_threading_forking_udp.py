

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



class ForkingEchoServer(socketserver.ForkingMixIn, socketserver.UDPServer,):
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



