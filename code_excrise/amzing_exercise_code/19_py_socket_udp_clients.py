# Echo client
import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Connect the socket to the port where the server is listening.
server_name = sys.argv[1]   # 外部参数传入服务器名称 , 允许哪个地方访问
# server_address = ('localhost', 10001)   # 默认服务器名称
server_address = (server_name, 10003)

print('send udp to {} port {}'.format(*server_address))
# sock.connect(server_address)

try:
    # send data
    message = b'This is the message. It will be repeated.'
    print('sending {!r}'.format(message))
    # sock.sendall(message) # tcp
    sent = sock.sendto(message, server_address)

    # Look for the response.
    amount_received = 0
    amount_expected = len(message)
    datas = b''
    while amount_received < amount_expected:
        data, server = sock.recvfrom(4096)  # 每次接受4096字节 UDP数据
        amount_received += len(data)
        print('received {!r}  from service:{}'.format(data, server))
        datas += data
    print(f'receive data:{type(datas), datas}')
finally:
    print('closing udp socket')

    sock.close()
