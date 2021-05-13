
"""
此处显示了同一服务器的精简版本，没有日志记录调用。
仅需要提供请求处理程序类中的handle（）方法。
"""

import socketserver

import random
from subprocess import Popen, PIPE
from py_socket_binary_data import win_platform, renew_listen_port

class EchoRequestHandler(socketserver.BaseRequestHandler):
         def handle(self):
             # Echo the data back to the client.
             data = self.request.recv(1024)
             self.request.send(data)
             return



if __name__ == '__main__':
    import socket
    import threading
    import pdb

    new_port = renew_listen_port()
    address = ('localhost', new_port)     # Let the kernel assign a port.

    server = socketserver.TCPServer(address, EchoRequestHandler)
    ip, port = server.server_address   # What port was assigned?
    print(f'server ip:{ip}, port:{port}')
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # Don't hang on exit. t.start()
    # Connect to the server.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Send the data.
    message = 'Hello, world'.encode()
    print('Sending : {!r}'.format(message))
    len_sent = s.send(message)
    print(f'len_sent:{len_sent}')
    # Receive a response.

    print(pdb.run(s.recv(len_sent)))
    # print('Received: {!r}'.format(response))
    # Clean up.
    server.shutdown()
    s.close()
    server.socket.close()

