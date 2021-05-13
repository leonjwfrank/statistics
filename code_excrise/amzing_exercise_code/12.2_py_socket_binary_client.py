import binascii
import socket
import struct
import sys
# import random
# import platform

# 打包和解包固定长度字符串
a = struct.pack("I2s3s", 1, b'ab', b'2.9')
b = struct.unpack("I2s3s", a)

print(f'a{a} b:{ b}')


# 打包和解包 变长字符串
s1 = [3, 1, 2]
s = bytes(s1)
data = struct.pack("I%ds" % (len(s),), len(s), s)

# 解包变长字符时首先解包内容的长度，在根据内容的长度解包数据
int_size = struct.calcsize("I")
(i,), data = struct.unpack("I", data[:int_size]), data[int_size:]
print(f'i:{i} ,data:{data}')

