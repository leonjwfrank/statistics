# http://code.activestate.com/recipes/577395-multiprocess-safe-logging-file-handler/
#
# Copyright (c) 2010 Jan Kaliszewski (zuo). Licensed under the PSF License.
#
# MultiprocessRLock acquire()/release() methods patterned, to some extent,
# after threading.RLock acquire()/release() of Python standard library.

"""
Multiprocess-safe logging and interprocess locking classes.

A Python 2.x/3.x-compatibile multiprocess-safe logging file-handler
(logging.FileHandler replacement, designed for logging to a single file from
multiple independent processes) together with a simple interprocess RLock.
在Python标准库的线程化之后，在一定程度上对MultiprocessRLockquiren（）/ release（）方法进行了模式化

The module contains:
* universal abstract classes:
  MultiprocessRLock, MultiprocessFileHandler, LockedFileHandler,
* Unix/Linux-only example implementation (with flock-based locking):
  FLockRLock and FLockFileHandler classes.
多进程安全日志记录和进程间锁定类。

一个Python 2.x / 3.x兼容的多进程安全日志文件处理程序（logging.FileHandler替换，旨在从多个独立的进程记录到单个文件）以及一个简单的进程间RLock。

该模块包含：
*通用抽象类：
  MultiprocessRLock，MultiprocessFileHandler，LockedFileHandler，
*仅限Unix / Linux的示例实现（具有基于flock的锁定）：FLockRLock和FLockFileHandler类。

已在Debian GNU / Linux下测试

Tested under Debian GNU/Linux, with Python 2.4, 2.5, 2.6 and 3.1.
"""

import logging
import os
import sys

#
# Unix or non-Unix platform? (supporting or not supporting the fcntl module)
try:
    # 仅限Unix/Linux
    import fcntl
    __all__ = (
        # abstract classes: 抽象类
        'MultiprocessRLock',
        'MultiprocessFileHandler',
        'LockedFileHandler',
        # fcntl.flock()-based implementation: 基于fcntl.flock()实现
        'FLockRLock',
        'FLockFileHandler',
    )
except ImportError:
    # non-Unix 非Unix
    fcntl = None
    __all__ = (
        # abstract classes only:  仅抽象类
        'MultiprocessRLock',
        'MultiprocessFileHandler',
        'LockedFileHandler',
    )

#
# Real or dummy threading? 实线程 还是虚拟线程？
try:
    import threading
except ImportError:
    import dummy_threading as threading

#
# Python 2.x or 3.x?
try:
    # 2.x (including < 2.6)  包括低版本的py
    try:
        from thread import get_ident as get_thread_ident
    except ImportError:
        from dummy_thread import get_ident as get_thread_ident
except ImportError:
    # 3.x  支持3.x
    def get_thread_ident(get_current_thread=threading.current_thread):
        return get_current_thread().ident



#
# Abstract classes  抽象类
#

class MultiprocessRLock(object):

    """Interprocess and interthread recursive lock (abstract class).
    进程间和线程间递归锁。抽象类"""

    def __init__(self):
        self._threading_lock = threading.Lock()     # 线程锁
        self._owner = None
        self._count = 0

    def __repr__(self):
        return '<%s owner=%s count=%d>' % (self.__class__.__name__,
                                           self._owner, self._count)

    def _interprocess_lock_acquire(self, blocking):  # abstract method 抽象方法
        # the implementing function should return: 实现函数应返回
        # * True on success 成功时为真
        # * False on failure (applies to non-blocking mode)  错误时为假(非阻塞式模式)
        raise NotImplementedError

    def _interprocess_lock_release(self):  # abstract method  抽象方法
        raise NotImplementedError

    @staticmethod
    def _get_me(getpid=os.getpid, get_thread_ident=get_thread_ident):
        return '%d:%d' % (getpid(), get_thread_ident())

    def acquire(self, blocking=1):
        me = self._get_me()
        if self._owner == me:
            self._count += 1
            return True
        if not self._threading_lock.acquire(blocking):
            return False
        acquired = False
        try:
            acquired = self._interprocess_lock_acquire(blocking)
        finally:
            if not acquired:
                # important to be placed within the finally-block 重要的是要放置在finally块
                self._threading_lock.release()
            else:
                self._owner = me
                self._count = 1
        return acquired

    __enter__ = acquire

    def release(self):
        if self._owner != self._get_me():
            raise RuntimeError("cannot release un-acquired lock")
        self._count -= 1
        if not self._count:
            self._owner = None
            self._interprocess_lock_release()
            self._threading_lock.release()

    def __exit__(self, *args, **kwargs):
        self.release()



class MultiprocessFileHandler(logging.FileHandler):

    """Multiprocess-safe logging.FileHandler replacement (abstract class).
    多进程安全日志记录，抽象类"""

    def createLock(self):  # abstract method
        "Create a lock for serializing access to the underlying I/O."
        raise NotImplementedError



class LockedFileHandler(MultiprocessFileHandler):

    """File-locking based logging.FileHandler replacement (abstract class).
    基于文件锁定的日志记录。FileHandler替换（抽象类）"""

    def __init__(self, filename, mode='a', encoding=None, delay=0):
        """Open the specified file and use it for logging and file locking.
        打开指定文件，并将其用于日志记录和文件锁定。"""
        if delay:
            """抛出错误，无法使用非零延迟来初始化LockedFileHandler实例"""
            raise ValueError('cannot initialize LockedFileHandler'
                             ' instance with non-zero delay')

        # base classe's __init__() calls createLock() method before setting
        # 在setting，创建实例类之前调用__init__
        # self.stream -- so we have to mask that method temporarily:
        # 在设置前调用createLock(), 因此我们必须暂时屏蔽该方法
        self.createLock = lambda: None
        MultiprocessFileHandler.__init__(self, filename, mode, encoding)
        del self.createLock  # now unmask...
        self.createLock()    # ...and call it



if fcntl is not None:

    #
    # Unix/Linux implementation。实现
    #

    class FLockRLock(MultiprocessRLock):

        """"flock-based MultiprocessRLock implementation (Unix/Linux only).
        基于多进程群 锁的实现

        FLockRLock也可以单独使用-类似于threading.Rlock，除了：
        锁定文件对象必须传递到构造函数中，（很重要！）您可以同步多个独立的进程，不仅是线程
        """

        def __init__(self, lockfile):
            MultiprocessRLock.__init__(self)
            self.lockfile = lockfile

        def _interprocess_lock_acquire(self, blocking,
                                       flock=fcntl.flock,
                                       flags=(fcntl.LOCK_EX | fcntl.LOCK_NB,
                                              fcntl.LOCK_EX),
                                       exc_info=sys.exc_info):
            try:
                flock(self.lockfile, flags[blocking])   # 阻断，锁文件
            except IOError:
                # Python 2.x & 3.x -compatibile way to get Python 2.x和3.x -compatibile获取异常对象的方法
                # the exception object: call sys.exc_info()
                if exc_info()[1].errno in (11, 13):
                    return False  # <- applies to non-blocking mode only
                raise
            else:
                return True

        def _interprocess_lock_release(self, flock=fcntl.flock,
                                       LOCK_UN=fcntl.LOCK_UN):
            flock(self.lockfile, LOCK_UN)



    class FLockFileHandler(LockedFileHandler):

        """LockedFileHandler implementation using FLockRLock (Unix/Linux only).
        使用FLockRLock的LockedFileHandler实现（仅Unix / Linux）。
        FLockFileHandler 与 logging.FileHandler一样，除了delay参数必须为零

        基于fcntl.flock（）的文件锁定似乎不会产生巨大的开销（在我的计算机上进行快速测试的结果是：
        12个进程*每个中有3个线程* 1000条日志记录== 36000条日志记录：
        logging.FileHandler-大约8秒，FLockFileHandler-大约11秒
        """

        def createLock(self):
            """Create a lock for serializing access to the underlying I/O. 创建一个锁，用于序列化对基础I / O的访问。"""
            self.lock = FLockRLock(self.stream)



######################test_module##############################################
#!/usr/bin/env python

# from multiprocessfilehandler import *

import logging
import os
import re
import sys
import threading

from itertools import islice, takewhile
from os.path import abspath
from random import randint

try:
    from itertools import filterfalse  # Py3.x
except ImportError:
    from itertools import ifilterfalse as filterfalse  # Py2.x

# try: irange = xrange
# except NameError:  # Py2's xrange() is range() in Py3.x
#     irange = range

try: inext = next
except NameError:
    inext = lambda i: i.next()

# constants

PY_VER = sys.version[:3]
DEFAULT_FILENAME = 'test.log'
LOG_FORMAT = '%(asctime)s %(message)s'
REC_BODY_PATTERN = 'proc:%(pid)d thread:%(thread_ident)d rec:%%s'

LOCK_DESCR = 'per-thread', 'thread-shared'
POSSIBLE_RESULTS = 'acquired', 'released', 'not acquired'
FILLER_AFTER_NOACK = 'so nothing to release :)'

RECORD_REGEX = re.compile(r'('
        r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} '  # time
        r'|'
        r'-{24}'  # written with stream.write()
    r')'
    r'%(py_ver)s'
    r' proc:\d+ thread:\d+ rec:'
    r'('
        r'\d+'  # record counter
        r'|'
        r'(%(msg_pattern)s)'
        r'|'
        r'%(filler_after_noack)s'
    r')$'% dict(
        py_ver=r'[\d\.]{%d}' % len(PY_VER),
        msg_pattern=r') ('.join((
            r'|'.join(map(re.escape, LOCK_DESCR)),
            r'<FLockRLock owner=\w+ count=\d+>',
            r'|'.join(map(re.escape, POSSIBLE_RESULTS)),
        )),
        filler_after_noack=re.escape(FILLER_AFTER_NOACK),
    )
)


def for_subthread(thread_shared_lock, thread_i, proc_i,logrecords, locktests, filename):

    # FLockFileHandler test
    logger = logging.getLogger()
    rec_pattern = ' '.join((PY_VER, REC_BODY_PATTERN
                                    % dict(pid=proc_i,
                                           thread_ident=thread_i)))
    for rec_i in range(logrecords):
        logger.info(rec_pattern % rec_i)

    # additional per-thread/thread-shared -files-based FLockRLock tests
    per_thread_lockfile = open(abspath(filename), 'a')
    try:
        per_thread_lock = FLockRLock(per_thread_lockfile)
        descr2locks = {'per-thread': per_thread_lock,
                       'thread-shared': thread_shared_lock}
        msg_pattern = rec_pattern % '%s %s %s'
        msg = dict((result,
                    dict((lock, msg_pattern % (descr, lock, result))
                         for descr, lock in descr2locks.items()))
                   for result in POSSIBLE_RESULTS)
        msg_acquired = msg['acquired']
        for lock, m in msg_acquired.items():
            # to be written directly to the file -- to avoid deadlock
            msg_acquired[lock] = ''.join((24 * '-', m, '\n'))
        filler_after_noack = rec_pattern % FILLER_AFTER_NOACK
        locks = list(descr2locks.values())  # Py3's .values() -> a view
        for i in range(locktests):
            if randint(0, 1):
                iterlocks = iter(locks)
            else:
                iterlocks = reversed(locks)
            for lock in iterlocks:
                if lock.acquire(blocking=randint(0, 1)):
                    try:
                        lock.lockfile.write(msg['acquired'][lock])
                        lock.lockfile.flush()
                    finally:
                        lock.release()
                        logger.info(msg['released'][lock])
                else:
                    logger.info(msg['not acquired'][lock])
                    logger.info(filler_after_noack)
    finally:
        per_thread_lockfile.close()


def for_subprocess(proc_i, subthreads, logrecords, locktests, filename):

    # setting up logging to test FLockFileHandler
    f = logging.Formatter(LOG_FORMAT)
    h = FLockFileHandler(filename)
    h.setFormatter(f)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(h)

    # (standalone FLockRLock instance also to be tested)
    thread_shared_lockfile = open(abspath(filename), 'a')
    try:
        thread_shared_lock = FLockRLock(thread_shared_lockfile)
        threads = [threading.Thread(target=for_subthread,
                                    args=(thread_shared_lock,
                                          thread_i, proc_i,
                                          logrecords, locktests,
                                          filename))
                   for thread_i in range(subthreads)]
        for t in threads: t.start()
        for t in threads: t.join()  # wait for subthreads
    finally:
        thread_shared_lockfile.close()


def check_records_only(filename):
    logfile = open(abspath(filename))
    try:
        try:
            badline = inext(filterfalse(RECORD_REGEX.match, logfile))
        except StopIteration:
            return "OK"
        else:
            sys.exit('Invalid record found: %s' % badline)
    finally:
        logfile.close()


def check_records_and_len(filename, expected_len):
    logfile = open(abspath(filename))
    try:
        # Py2.4-compatibile fast way to check file content and length
        file_ending = islice(takewhile(RECORD_REGEX.match, logfile),
                             expected_len - 1, expected_len + 1)
        try:
            inext(file_ending)
        except StopIteration:
            sys.exit('Too few valid lines found (%d expected)'
                     % expected_len)
        # at this point the file content should have been read entirely
        try:
            inext(file_ending)
        except StopIteration:
            return "OK"
        else:
            sys.exit('Too many valid (?) lines found (%d expected)'
                     % expected_len)
    finally:
        logfile.close()


def main(subprocs=3, subthreads=3, logrecords=5000,locktests=500, firstdelete=1, filename=DEFAULT_FILENAME):
    print(f'start loging {subprocs} * {subthreads} * {logrecords} = '
          f'{int(subprocs)*int(subthreads)*int(logrecords)}')
    # args may origin from command line, so we map it to int
    (subprocs, subthreads, logrecords, firstdelete, locktests
    ) = map(int, (subprocs, subthreads, logrecords, firstdelete, locktests))

    # expected number of generated log records
    expected_len = subprocs * subthreads * (logrecords + (4 * locktests))

    if firstdelete:
        try:
            os.remove(abspath(filename))
        except OSError:
            pass

    for proc_i in range(subprocs):
        if not os.fork():
            # we are in a subprocess
            for_subprocess(proc_i, subthreads, logrecords,
                           locktests, filename)
            break
    else:
        # we are in the parent process
        for i in range(subprocs):
            os.wait()  # wait for subprocesses

        # finally, check the resulting log file content
        if firstdelete:
            print(check_records_and_len(filename, expected_len))
        else:
            print(check_records_only(filename))

    print(f'end.')

# try running the script simultaneously using different Python versions :)
if __name__ == '__main__':
    import pdb
    pdb.run(main(*sys.argv[1:]))


