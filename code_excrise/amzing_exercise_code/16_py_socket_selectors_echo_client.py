
"""
selectors Multiplexing Abstractions
选择器模块在select中特定于平台的I / O监视功能(platform-specific I/O monitoring functions)的上方提供独立于平台的抽象层（第728页）。

选择器中的API基于事件，类似于select中的poll（）。存在几种实现，该模块自动设置别名DefaultSelector来引用当前系统配置中最高效的别名。
选择器对象提供用于指定要在套接字上查找哪些事件的方法，然后让调用者以与平台无关的方式等待事件。注册事件中的兴趣将创建一个SelectorKey，
该SelectorKey包含套接字，有关兴趣事件的信息以及可选的应用程序数据。
选择器的所有者调用其select（）方法来了解事件。返回值是一系列键对象和一个位掩码，指示发生了哪些事件。使用选择器的程序应重复调用select（），然后适当地处理事件。
"""

'''
Echo Clients
~~~~~~~~~~
下面的echo客户示例将处理主循环中的所有I / O事件，而不是使用回调。它设置选择器以报告套接字上的读取事件，并报告套接字准备好发送数据的时间。
因为它查看两种类型的事件，所以客户端必须通过检查掩码值来检查发生了哪些事件。发送所有传出数据后，它将选择器配置更改为仅在有要读取的数据时才报告。
'''

import selectors
import socket

mysel = selectors.DefaultSelector()
keep_running = True

outgoing = [b'It will be repeated.', b'This is  the message.',]
bytes_sent = 0
bytes_received = 0

# Connecting is a blocking operation, so call setblocking()
# 连接一个独占 阻塞操作，所以需要调用setblocking()
# after it returns
server_address = ('localhost', 10003)
print('connecting to {} print {}'.format(*server_address))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.setblocking(False)    # 非阻塞，完全不阻塞，同时发送接收可能报错

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
            keep_running = not(
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



