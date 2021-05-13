"""
selectors Multiplexing Abstractions
选择器模块在select中特定于平台的I / O监视功能(platform-specific I/O monitoring functions)的上方提供独立于平台的抽象层（第728页）。

选择器中的API基于事件，类似于select中的poll（）。存在几种实现，该模块自动设置别名DefaultSelector来引用当前系统配置中最高效的别名。
选择器对象提供用于指定要在套接字上查找哪些事件的方法，然后让调用者以与平台无关的方式等待事件。注册事件中的兴趣将创建一个SelectorKey，
该SelectorKey包含套接字，有关兴趣事件的信息以及可选的应用程序数据。
选择器的所有者调用其select（）方法来了解事件。返回值是一系列键对象和一个位掩码，指示发生了哪些事件。使用选择器的程序应重复调用select（），然后适当地处理事件。
"""

'''
Echo Server
~~~~~~~~~~

此处提供的回显服务器示例使用SelectorKey中的应用程序数据注册要在新事件上调用的回调函数。主循环从键获取回调，并将套接字和事件掩码传递给它。服务器启动时，
它将在主服务器套接字上注册要为读取事件而调用的accept（）函数。接受连接会产生一个新的套接字，然后将其注册到read（）函数中，作为读取事件的回调。
'''

import selectors
import socket

mysel = selectors.DefaultSelector()
keep_running = True
server_address = ('localhost', 10003)


class selector_server(object):

    @staticmethod
    def read(connection, mask=None):
        """call back for read enents"""
        global keep_running
        client_address = connection.getpeername()  # 通过名称获取地址
        print(f'read({client_address})')
        data = connection.recv(1024)
        if data:
            # A readable client socket has data
            print(' received {!r}'.format(data))
            connection.sendall(data)
        else:
            # Interpret empty result as closed connection
            print(' closing')
            mysel.unregister(connection)
            connection.close()
            # Tell the main loop to stop
            keep_running = False


    # @staticmethod
    def accept(self, sock, mask=None):
        """callback for new connectors"""
        new_connection, addr = sock.accept()
        print('accept {}'.format(addr))
        new_connection.setblocking(False)
        mysel.register(new_connection, selectors.EVENT_READ, self.read)

    # @staticmethod
    def keep_running(self):

        print('starting up on {} port {}'.format(*server_address))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4 tcp/ip 套接字

        # 如果两个程序最终都在等待另一个程序发送或接收数据，则可能导致低效的操作甚至死锁。
        """将套接字更改为完全不阻塞，如果尚未准备好处理该操作，则立即返回。使用setblocking（）方法可以更改套接字的阻止标志。默认值为1，表示阻止；默认值为1。值为0将关闭阻止。
        如果套接字已关闭阻塞并且尚未准备好执行该操作，则会引发socket.error。"""
        server.setblocking(False)  # setblocking（）设置为 False 即为 0，表示关闭阻止，可能在为准备好执行通信，可能引发socket.error

        server.bind(server_address)
        server.listen(5)

        mysel.register(server, selectors.EVENT_READ, self.accept)

        while keep_running:
            print('waiting for I/O')
            for key, mask in mysel.select(timeout=1):
                callback = key.data
                callback(key.fileobj, mask)

        print('shutting down')
        mysel.close()
        """如果read（）没有从套接字接收任何数据，则它将read事件解释为连接的另一端正在关闭而不是发送数据。因此，它将插座从选择器上卸下并关闭。
        由于这只是一个示例程序，因此该服务器在与单个客户端完成通信后也将自行关闭。"""


# Connecting is a blocking operation, so call setblocking()
# 连接一个独占 阻塞操作，所以需要调用setblocking()
# after it returns
# server_address = ('localhost', 10003)
def client_keep_running():
    outgoing = [b'It will be repeated.', b'This is  the message.', ]
    bytes_sent = 0
    bytes_received = 0
    print('connecting to {} print {}'.format(*server_address))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    sock.setblocking(False)  # 非阻塞，完全不阻塞，同时发送接收可能报错

    # Set up the selector to watch for when the socket is ready
    # to send data as well as when there is data to read.
    mysel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)  # 读写操作都注册
    while keep_running:
        print('waiting for I/O')
        for key, mask in mysel.select(timeout=1):
            connection = key.fileobj
            client_address = connection.getpeername()
            print('client({})'.format(client_address))

            if mask & selectors.EVENT_READ:
                print(' ready to read')
                data = connection.recv(1024)
                if data:
                    # A readbale client socket has data
                    print('  received {!r}'.format(data))
                    bytes_received += len(data)

                # Interpret empty result as closed connection,
                # and also close when we have received a copy
                # of all of the data sent.
                keep_running = not (
                        data or
                        (bytes_received and
                         (bytes_received == bytes_sent))
                )
            if mask & selectors.EVENT_WRITE:
                print('  ready to write')
                if not outgoing:
                    # We are out of messages, so we no longer need to write anything. Change our registration to let
                    # us keep reading responses from the server.
                    print(' switching to read-only')
                    mysel.modify(sock, selectors.EVENT_READ)
                else:
                    # Send the next message
                    next_msg = outgoing.pop()
                    print('   sending {!r}'.format(next_msg))
                    sock.sendall(next_msg)
                    bytes_sent += len(next_msg)
        print('shutting down !')
        mysel.unregister(connection)  # 注销
        connection.close()
        mysel.close()

    """客户端既跟踪已发送的数据量，也跟踪已接收的数据量。当这些值匹配并且非零时，客户端退出处理循环，并通过从选择器中删除套接字并同时关闭套接字和选择器来完全关闭。"""




import asyncio
from concurrent.futures import ProcessPoolExecutor


async def tasks(values, op_port):
    tasks_lis = [
        loop.run_in_executor(executor, selector_server().accept, int(op_port)),
        # loop.run_in_executor(executor, start_ff_brow, *(op_port, page)),
        loop.run_in_executor(executor, client_keep_running, *(values, int(op_port)))
    ]
    await asyncio.gather(*tasks_lis)

if __name__ == '__main__':
    pass
    """
        浮点值在打包和解包时会失去一些精度，但否则会按预期方式传输数据。要记住的一件事是，根据整数的值，将其转换为文本然后传输该数据而不是使用struct可能更有效。
        整数1在表示为字符串时使用1个字节，但在打包到结构中时使用4个字节。
        """
    op_port = 20003

    values = (1, b'ab', 2.7)

    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor(max_workers=2)

    selector_server = selector_server()
    selector_server.keep_running()
