"""
套接字传输字节流。如前面的示例一样，这些字节可以包含编码为字节的文本消息，也可以由二进制数据组成，
这些二进制数据已被打包到带有struct（第117页）的缓冲区中，以准备进行传输。
该客户端程序将一个整数，两个字符的字符串和一个浮点值编码为一系列字节，这些字节可以传递给套接字进行传输。
"""
import binascii
import socket
import struct
import sys
import random
import platform
from subprocess import Popen, PIPE

try:
    ip_server = sys.argv[1]
except:
    ip_server = 'localhost'


def win_platform():
    """check if pc or mac"""
    if 'Window' in str(platform.platform()):
        return True
    else:
        return False


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


def binary_client(values, op_port):
    """注意发送和接受的values顺序"""
    # create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip_server, op_port)
    sock.connect(server_address)

    #  values 序列中的值的类型需要一一对应， I 表示 int 类型， 2s 表示两位 bytes， f 表示 float

    packer = struct.Struct('I 2s d')   # 使用双精度 double  浮点数的精度损失更小。

    packed_data = packer.pack(*values)  #

    print('client send values =', values)

    try:
        # send data
        print('client is sending {!r}'.format(binascii.hexlify(packed_data)))
        sock.sendall(packed_data)
    finally:
        print('client closing socket')
        sock.close()


def binary_server(port):
    """
    在两个系统之间发送多字节二进制数据时，重要的是要确保连接的双方都知道字节处于哪个顺序，
    以及如何将它们重新组合为本地体系结构的正确顺序。服务器程序使用相同的Struct说明符解压缩接收到的字节，以便以正确的顺序解释它们。
    :return:
    """
    # Create a TCP/IP socket.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip_server, port)
    sock.bind(server_address)  # 绑定
    sock.listen(1)  # 监听

    unpacker = struct.Struct('I 2s d')
    # struct.unpack(str, )

    while True:
        print(f'\n server is waiting for a connection :{op_port}')
        connection, client_address = sock.accept()
        try:
            data = connection.recv(unpacker.size)
            print('server received {!r}'.format(binascii.hexlify(data)))

            unpacker_data = unpacker.unpack(data)
            print('server unpacked:', unpacker_data)
        finally:
            connection.close()


import asyncio
from concurrent.futures import ProcessPoolExecutor


async def tasks(values, op_port):
    tasks_lis = [
        loop.run_in_executor(executor, binary_server, int(op_port)),
        # loop.run_in_executor(executor, start_ff_brow, *(op_port, page)),
        loop.run_in_executor(executor, binary_client, *(values, int(op_port)))
    ]
    await asyncio.gather(*tasks_lis)


if __name__ == '__main__':
    """
    浮点值在打包和解包时会失去一些精度，但否则会按预期方式传输数据。要记住的一件事是，根据整数的值，将其转换为文本然后传输该数据而不是使用struct可能更有效。
    整数1在表示为字符串时使用1个字节，但在打包到结构中时使用4个字节。
    """
    op_port = renew_listen_port()

    values = (1, b'ab', 2.7)

    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor(max_workers=2)
    # try:
    # loop.run_until_complete(tasks(values, op_port))

    print('')
    str_values = []
    for x in range(len(values)):
        x_val = values[x]
        if type(x_val) in [int, float]:
            print(f'str_values:{str_values}, values:{values}, {x, x_val} type x val:{type(x_val)}')
            str_values.insert(x, x_val)
        else:
            str_values.insert(x, x_val)
    print(f'str_values:{str_values}')
    # [values[x]=str(values[x]) for x in range(len(values)) if type(values[x])==int]
    print(f'values:{values}, str_values:{str_values}')
    loop.run_until_complete(tasks(str_values, op_port))
    # binary_server()
    # binary_client()
