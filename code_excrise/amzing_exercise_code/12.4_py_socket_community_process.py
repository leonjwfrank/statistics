# socket 父进程与子进程通信
import socket
import os


def pair_process():
    parent, child = socket.socketpair()  # 通信交互

    pid = os.fork()  # 创建子进程
    if pid:
        print('in parent, sending message pid:', pid)
        child.close()
        parent.sendall(b'ping')
        response = parent.recv(1024)
        print('1 response from child:', response)
        parent.close()
    else:
        print('in child, waiting for message')
        parent.close()
        message = child.recv(1024)
        print('2 message from parent:', message)
        child.sendall(b'pong')
        child.close()


if __name__ == '__main__':
    pair_process()
    pass

