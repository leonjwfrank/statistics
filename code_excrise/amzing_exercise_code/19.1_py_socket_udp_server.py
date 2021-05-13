# socket 的 TCP/IP 客户端和服务端
# 回显服务器  Echo Server
import socket
import sys
import datetime

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_name = sys.argv[1]   # 外部参数传入服务器名称
server_address = (server_name, 10003)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)  # 绑定服务器地址

# Listen for incoming connections.
# sock.listen(1) # UDP 不需要监听？
while True:
    # Wait for a connection.
    print('waiting for recevice message')
    # connection, client_address = sock.accept()
    data, address = sock.recvfrom(4096)
    try:
        # print('connection from:{}'.format(client_address))
        print('receive {} bytes from {}, data:{}'.format(len(data), address, data))
        # Receive the data in small chunks and retransmit it.

        if data:
            print('sending data back to the client')
            # connection.sendall(data)
            send = sock.sendto(data, address)
            print('sent {} bytes back to {}'.format(send, address))
        else:
            print('no data from', address)
            break
    finally:
        # Clean up the connection.
        # 保证关闭连接This example uses a try:finally block to ensure that close() is always called, even in the event of an error.
        print('done receive:{}, data:{}'.format(address, datetime.datetime.now()))


