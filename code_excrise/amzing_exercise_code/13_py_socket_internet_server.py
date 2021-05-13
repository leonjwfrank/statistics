"""


socketserver模块是用于创建网络服务器的框架。它定义了用于在TCP，UDP，Unix流和Unix数据报上处理同步网络请求的类（服务器请求处理程序将阻塞直到请求完成）。
它还提供了混合类（ mix-in classes），可以轻松地将服务器转换为对每个请求使用单独的线程或进程。
处理请求的责任在服务器类和请求处理程序类之间划分。
服务器处理通信问题，
例如侦听套接字并接受连接，而请求处理程序处理“协议”问题，
例如解释（interpreting）传入的数据，对其进行处理（processing）并将数据发送回客户端。
这种职责划分意味着许多应用程序可以使用现有服务器类之一而无需进行任何修改，并提供一个请求处理程序类以使其与自定义协议一起使用。

socketserver中定义了五个服务器类。
BaseServer定义了API，并且不能直接实例化和使用。
TCPServer使用TCP / IP套接字进行通信。
UDPServer使用数据报套接字。
UnixStreamServer和UnixDatagramServer使用Unix域套接字，并且仅在Unix平台上可用。
"""

'''
要构建服务器，请向其传递一个用于侦听请求的地址和一个请求处理程序类（不是实例）。地址格式取决于服务器类型和使用的套接字系列。有关详细信息，请参见插槽（第693页）模块文档。
实例化服务器对象后，请使用handle_request（）或serve_forever（）处理请求。 serve_forever（）方法在无限循环中调用handle_request()。
但是，如果应用程序需要将服务器与另一个事件循环集成在一起或使用select（）监视不同服务器的多个套接字，则可以直接调用handle_request（）。
'''

'''
创建服务器时，重用现有类之一并提供自定义请求处理程序类通常就足够了。对于其他情况，BaseServer包含可以在子类中重写的几种方法。
•verify_request（request，client_address）：返回True处理请求，或者返回False忽略请求。例如，服务器可以拒绝来自IP范围的请求，或者服务器是否过载(overloaded)。
•process_request（request，client_address）：调用finish_request（）来实际完成处理请求的工作。与混合类一样，此方法也可以创建单独的线程或进程。
•finish_request（request，client_address）：使用提供给服务器构造函数的类创建请求处理程序实例。在请求处理程序上调用handle（）来处理请求。
'''

'''
请求处理程序完成接收传入请求并确定要采取的操作的大部分工作。处理程序负责在套接字层（即HTTP，XML-RPC或AMQP）的顶部实施协议。
请求处理程序从传入的数据通道读取请求，进行处理，然后写回响应。可以重写三种方法。
•setup（）：为请求准备请求处理程序。在StreamRequestHandler中，setup（）方法创建类似于文件的对象，以从套接字读取和写入套接字。
•handle（）：真正处理请求。解析传入的请求，处理数据并发送响应。
•finish（）：清除在setup（）期间创建的所有内容。
只能使用handle（）方法来实现许多处理程序。
'''

# 此示例实现了一个简单的服务器/请求处理程序对，该对接受TCP连接并回显客户端发送的所有数据。它从请求处理程序开始。
import logging
import sys
import socketserver

logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(message)s',)

class EchoRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.logger = logging.getLogger('EchoRequestHandler')
        self.logger.debug('__init__')
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        self.logger.debug('setup')
        return socketserver.BaseRequestHandler.setup(self)

    def handle(self):
        self.logger.debug('handle')

        # Echo the data back to the client
        data = self.request.recv(1024)
        self.logger.debug('recv()->"%s"', data)

    def finish(self):
        self.logger.debug('finish')
        return socketserver.BaseRequestHandler.finish(self)



class EchoServer(socketserver.TCPServer):
    """
    实际需要实现的唯一方法是EchoRequestHandler .handle（），但此处包含了前面介绍的所有方法的版本，以说明进行调用的顺序。
    EchoServer类与TCPServer没有什么不同，除了在调用每个方法时记录日志。
    """
    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.logger = logging.getLogger('EchoServer')
        self.logger.debug('__init__')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        self.logger.debug('server_activate')
        socketserver.TCPServer.server_activate(self)
        return

    def server_forever(self, poll_interval=0.5):
        self.logger.debug('waiting for request')
        self.logger.info('Handling requests, press <Ctrl-C> to quit')
        socketserver.TCPServer.serve_forever(self,poll_interval)
        return

    def handle_request(self):
        self.logger.debug('handle_request')
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        self.logger.debug('verify_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.verify_request(self, request, client_address,)

    def process_request(self, request, client_address):
        self.logger.debug('process_request(%s,%s)', request, client_address)
        return socketserver.TCPServer.process_request(self, request, client_address,)

    def server_close(self):
        self.logger.debug('server_close')
        return socketserver.TCPServer.server_close(self)

    def finish_request(self, request, client_address):
        self.logger.debug('finish_request(%s, %s)',
                          request, client_address)
        return socketserver.TCPServer.finish_request(self, request, client_address,)

    def close_request(self, request_address):
        self.logger.debug('close_request(%s)', request_address)
        return socketserver.TCPServer.close_request(self, request_address,)

    def shutdown(self):
        self.logger.debug('shutdown()')
        return socketserver.TCPServer.shutdown(self)


import random
from subprocess import Popen, PIPE
from py_socket_binary_data import win_platform


def renew_listen_port():
    """find a port to listen"""
    while True:
        rand_port = random.choice(range(1000, 10000))
        if win_platform():
            cmd_port = 'netstat -an | findstr {}'.format(rand_port)
        else:
            cmd_port = 'netstat -an | grep {}'.format(rand_port)
        pp = Popen(cmd_port, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        info, err = pp.communicate()
        pp.kill()
        if not info or info in ['', "b''", []]:
            return int(rand_port)
        else:
            continue


if __name__ == '__main__':
    # 最后一步是添加一个主程序，该程序将服务器设置为在线程中运行，并向其发送数据以说明在回显数据时调用了哪些方法。
    pass
    import socket
    import threading

    new_port = renew_listen_port()
    address = ('localhost', new_port)  # Let the kernel assign a port.
    server = EchoServer(address, EchoRequestHandler)
    ip, port = server.server_address  # What port was assigned?

    # Start the server in a thread.
    t = threading.Thread(target=server.server_forever)
    t.setDaemon(True)
    t.start()

    logger = logging.getLogger('client')
    logger.info('Server on %s:%s', ip, port)

    # Connect to the server
    logger.debug('creating socket')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logger.debug('connecting to server')
    s.connect((ip, port))

    # Send the data
    message = 'Hello , world'.encode()
    logger.debug('sending data:%r', message)
    len_sent = s.send(message)

    # Receive a response
    logger.debug('waiting for response')
    response = s.recv(len_sent)
    logger.debug('response from server: %r', response)

    # Clean up
    server.shutdown()
    logger.debug('closing socket')
    s.close()
    logger.debug('Done')
    server.socket.close()
