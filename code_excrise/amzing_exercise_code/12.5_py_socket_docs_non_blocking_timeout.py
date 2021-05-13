"""
默认情况下，将套接字配置为发送或接收数据块，这意味着它将停止程序执行，直到套接字就绪为止。调用send（）等待缓冲区空间可用于传出数据，
而调用recv（）等待其他程序发送可以读取的数据。这种形式的I / O操作很容易理解，但是如果两个程序最终都在等待另一个程序发送或接收数据，则可能导致低效的操作甚至死锁。
有几种方法可以解决这种情况。
一种方法是使用单独的线程与每个套接字通信。但是，这可能导致线程之间的通信带来其他复杂性。
另一种选择是将套接字更改为完全不阻塞，如果尚未准备好处理该操作，则立即返回。使用setblocking（）方法可以更改套接字的阻止标志。默认值为1，表示阻止；默认值为1。值为0将关闭阻止。
如果套接字已关闭阻塞并且尚未准备好执行该操作，则会引发socket.error。
一种折衷的解决方案是为套接字操作设置超时值。使用settimeout（）将套接字的超时更改为浮点值，该值表示在确定套接字尚未准备好进行操作之前要阻塞的秒数。超时到期时，将引发超时异常。
"""

"""
扩展阅读
Related Reading
• Standard library documentation for socket.10
• Python 2 to 3 porting notes for socket (page 1362).
• select (page 728): Testing a socket to see if it is ready for reading or writing for non-blocking I/O.
• SocketServer: Framework for creating network servers.
• asyncio (page 617): Asynchronous I/O and concurrency tools.
• urllib and urllib2: Most network clients should use the more convenient libraries for accessing remote resources through a URL.
• Socket Programming HOWTO11: An instructional guide by Gordon McMillan, included in the
standard library documentation.
• Foundations of Python Network Programming, Third Edition, by Brandon Rhodes and John Goerzen. Apress, 2014. ISBN-10: 1430258543.
• Unix Network Programming, Volume 1: The Sockets Networking API, Third Edition, by W. Richard Stevens, Bill Fenner, 
    and Andrew M. Rudoff. Addison-Wesley, 2004. ISBN-10: 0131411551.
"""


