"""

该示例客户端程序使用两个套接字来演示带有select（）的服务器如何同时管理多个连接。客户端首先将每个TCP / IP套接字连接到服务器。
"""
import socket
import sys

messages = ['This is the message.','It will be sent ',
         'in parts.',]
server_address = ('localhost', 10000)

# Create a TCP/IP socket list.
socks = [
socket.socket(socket.AF_INET, socket.SOCK_STREAM),
socket.socket(socket.AF_INET, socket.SOCK_STREAM), ]

# Connect the socket to the port where the server is listening.
print('connecting to {} port {}'.format(*server_address), file=sys.stderr)
for s in socks:
    s.connect(server_address)

"""
接下来，它通过每个套接字一次发送一条消息，并在写入新数据后读取所有可用的响应。
"""

for message in messages:
    outgoing_data = message.encode()

    # Send messages on both sockets.
    for s in socks:
        print('{}: sending {!r}'.format(s.getsockname(), outgoing_data), file=sys.stderr)
        s.send(outgoing_data)

    # Read responses on both sockets.
    for s in socks:
        data = s.recv(1024)
        print('{}: received {!r}'.format(s.getsockname(), data), file=sys.stderr)

        if not data:
            print('closing socket', s.getsockname(), file=sys.stderr)
            s.close()




