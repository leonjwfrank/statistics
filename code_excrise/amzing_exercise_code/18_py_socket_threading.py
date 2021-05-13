"""
要向服务器添加线程或分支支持，请在服务器的类层次结构中包括适当的混入。当准备好处理请求并在新的子代中完成工作时，混合类将覆盖process_request（）以启动新的线程或进程。
对于线程，请使用ThreadingMixIn。
"""
import threading
import socketserver
from py_socket_binary_data import win_platform, renew_listen_port


class ThreadedEchoRequestHandler(socketserver.BaseRequestHandler,):
    def handle(self):
        # Echo the data back to the client
        # 来自该线程服务器的响应包括处理请求的线程的标识符。
        data = self.request.recv(1024)
        cur_thread = threading.currentThread()
        response = b'%s:%s' % (cur_thread.getName().encode(), data)
        self.request.send(response)
        return


class ThreadedEchoServer(socketserver.ThreadingMixIn, socketserver.TCPServer,):
    pass


if __name__ == '__main__':
    import socket
    new_port = renew_listen_port()
    address = ('localhost', new_port)
    server = ThreadedEchoServer(address, ThreadedEchoRequestHandler)
    ip, port = server.server_address   # 取得注册的地址和端口
    t = threading.Thread(target=server.serve_forever)

    t.setDaemon(True)   # Don't hang on exit
    t.start()
    print('Server loop running in thread:', t.getName())

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp/ip 套接字连接
    s.connect((ip, port))

    # Send the data.
    message = b'Hello, world'
    print('Sending:{!r}'.format(message))
    len_sent = s.send(message)

    # Receive a response.
    response = s.recv(1024)
    print('Received:{!r}'.format(response))

    # Clean up
    server.shutdown()
    s.close()
    server.socket.close()

