"""
select server
~~~~
Python的select（）函数是与底层操作系统实现的直接接口。它监视套接字，打开的文件和管道（任何使用fileno（）方法返回有效文件描述符的东西），直到它们变得可读或可写或发生通信错误为止。
select（）使同时监视多个连接变得容易，并且比使用套接字超时在Python中编写轮询循环更有效，因为监视发生在操作系统网络层，而不是解释器。

一般支持 UNIX 系列系统

通过使用select（），可以扩展套接字（第693页）部分中的echo服务器示例，以一次监视多个连接。通过创建一个非阻塞TCP / IP套接字并将其配置为侦听地址，可以开始新版本。

"""
import select
import socket
import sys
import queue

# Create a TCP/IP socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)   # 停止阻塞

# Bind the socket to the port.
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address),
           file=sys.stderr)
server.bind(server_address)

# Listen for incoming connections.
server.listen(5)
"""
select（）的参数是三个列表，其中包含要监视的通信通道。第一个是要检查要读取的传入数据的对象的列表，第二个包含当其缓冲区中有空间时将接收传出数据的对象，
第三个是可能有错误的对象（通常是一个组合）输入和输出通道对象的名称）。下一步是设置包含输入源和输出目的地，传递给select（）。


"""
# Sockets from which we expect to read
inputs = [server]

# Sockets to which we expect to write
outputs = []

"""
服务器主循环将连接添加到这些列表中或从这些列表中删除。由于此版本的服务器将在发送任何数据之前等待套接字变为可写状态（而不是立即发送答复），
因此每个输出连接都需要一个队列，以充当通过它发送的数据的缓冲区。
"""
# outgoing message queues (socket:queue)
message_queues = {}

"""服务器程序的主要部分循环，调用select（）来阻止并等待网络活动。"""
while inputs:
    # Wait for at least one of the sockets to be
    # ready for processing.
    print('waiting for the next event', file=sys.stderr)
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    """
    select（）返回三个新列表，其中包含传入的列表内容的子集。可读列表中的套接字对传入的数据进行了缓冲，可以读取；可写列表中的套接字在其缓冲区中具有可用空间，可以被写入；
    并且以特殊方式退还的插座发生了错误（“例外情况”的实际定义取决于平台）。
    “可读”套接字代表三种可能的情况。如果套接字是主“服务器”套接字（即用于侦听连接的套接字），则“可读”状态表示它已准备好接受另一个传入的连接。
    除了将新连接添加到要监视的输入列表之外，本节还将客户端套接字设置为不阻塞。
    """
    # Handle inputs.
    for s in readable:
        connection, client_address = s.accept()
        if s is server:
            # A "readable" socket is ready to accept a connection.

            print(' connection from', client_address,
               file=sys.stderr)

            connection.setblocking(0)
            inputs.append(connection)
            # Give the connection a queue for data
            # we want to send.
            message_queues[connection] = queue.Queue()

        else:
            data = s.recv(1024)
            if data:
                # A readable client socket has data
                print('  received {!r} from {}'.format(data, s.getpeername()), file=sys.stderr,)
                message_queues[s].put(data)
                # Add output channel for respone.
                if s not in outputs:
                    outputs.append(s)
            else:
                # Interpret empty result as closed connection.
                """不会读取来自recv（）的数据的可读套接字来自已断开连接的客户端，流已准备好关闭。"""
                print('  closing', client_address,
                      file=sys.stderr)
                # Stop listening for input on the connection.
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue.
                del message_queues[s]
    """可写连接的情况较少。如果队列中保存有用于连接的数据，则发送下一条消息。否则，将从输出连接列表中删除该连接，以便下次通过循环select（）时不表示套接字已准备好发送数据。"""
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            # No messages waiting, so stop checking
            # for writability.
            print('  ', s.getpeername(), 'queue empty',
                  file=sys.stderr)
            outputs.remove(s)
        else:
            print('  sending {!r} to {}'.format(next_msg,s.getpeername()),file=sys.stderr)
            s.send(next_msg)
    # 最后，例外列表中的套接字被关闭。
    # Handle "exceptional conditions."
    for s in exceptional:
        print('exception condition on', s.getpeername(), file=sys.stderr)
        # Stop listening for input on the connection.
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue.
        del message_queues[s]


