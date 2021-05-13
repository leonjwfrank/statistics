# 客户端连接 Easy Client Connections
import socket
import sys

def get_constants(prefix):
    """Create a dictionary mapping socket module
         constants to their names.
         """
    return {
             getattr(socket, n): n
             for n in dir(socket)
             if n.startswith(prefix)
    }
families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO_')

# Create a TCP/IP socket.
sock = socket.create_connection(('localhost', 10001))
print('Family  :', families[sock.family])
print('Type    :', types[sock.type])
print('Protocol:', protocols[sock.proto])
print()

try:
        # Send data.
        message = b'This is the message. It will be repeated.'
        print('sending {!r}'.format(message)) 
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        datas = b''
        while amount_received < amount_expected:
            data = sock.recv(16)  # 每次接受16字节
            amount_received += len(data)
            print('received {!r}'.format(data))
            datas += data
        print(f'receive data:{type(datas), datas}')
finally:
    print('closing socket')

    sock.close()