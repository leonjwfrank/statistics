# socket 的 TCP/IP 客户端和服务端
# 回显服务器  Echo Server
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_name = sys.argv[1]   # 外部参数传入服务器名称
server_address = (server_name, 10001)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)  # 绑定服务器地址

# Listen for incoming connections.
sock.listen(1)
while True:
    # Wait for a connection.
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from:{}'.format(client_address))

        # Receive the data in small chunks and retransmit it.
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break
    finally:
        # Clean up the connection.
        # 保证关闭连接This example uses a try:finally block to ensure that close() is always called, even in the event of an error.
        connection.close()
