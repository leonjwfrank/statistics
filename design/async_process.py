"""
    异步面临的问题
        现有的接口不兼容异步，
        I/O操作的非异步阻塞
        长时间运行的CPU密集型操作
            I/O执行时，很容易从协程释放控制
            文件系统或套接字写/读时，需要等待  使用 await
    CPU广泛的任务使用多进程， I/O操作使用多线程，如果不适合异步，可以将异步代码 修改为同步非阻塞协同
        futures 将异步代码同步化
	    concurrent.futures
		Executor     #并行处理工作项的资源池 类似于multiprocessing Pool 和 Dummy.Pool 但是有完全不同的接口和语义
			有一个虚基类，不可实例化，两个具体实现
			ThreadPoolExecutor    # 线程池
			ProcessPoolExecutor   # 进程池
			每个池执行者有三个方法
			submit(fn, *args, **kwarg)     # 将资源池上执行调度的函数返回Future对象，该对象表示可调用执行 ，返回 Future对象
				from concurrent.futures import TheadPoolExecutor
				with ThreadPoolExecutor(1) as executro:
				future = executor.submit(loudy_return)
				future.result()    #  立即查看结果
			map(func, *iterables, timeout=None, chunksize=1)    # 在一个迭代器上执行func函数，类似multiprocessing.Pool.map()用法
			shutdown(wait=True)    # 将关闭执行程序并释放所有资源
		futures
    ~~~~~~~~~~~~~~~~~~~~~~
    异步进程池
    import asyncio
    from concurrent.futures import ProcessPoolExecutor
    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor(max_workers=1)

    print('')
    loop.run_until_complete(tasks(2))
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

print(
    f"################+++++++++++++++++++++ asyncio process ++++++++++++++++++++++++++++++############################")
import asyncio
import time
import sys
import random
import asyncio
import logging
import tracemalloc

logging.getLogger('asyncio').setLevel(logging.INFO)
from asyncio import AbstractEventLoop
# AbstractEventLoop().set_debug(enabled=True)



async def waiter(name):
    total_time = 0
    for x in range(4):
        time_to_sleep = random.randint(1, 3) / 4
        total_time += time_to_sleep
        time.sleep(time_to_sleep)  # time.sleep是 阻塞，不释放控件到事件循环
        logging.info(f"{name}")
        print(f"{name} waited {time_to_sleep} seconds")
    logging.info(f"total_time:{total_time}")


async def await_waiter(name):
    total_time = 0
    for y in range(4):
        time_to_sleep = random.randint(1, 3) / 4
        total_time += time_to_sleep
        await asyncio.sleep(time_to_sleep)  # time.sleep的协程版本
        print(f"await {name} waited {time_to_sleep} seconds")
    logging.info(f"total await time:{total_time}")


async def main():
    logging.info(f"event loop:{'foo, bar'}")
    await asyncio.wait([waiter("foo"), waiter("bar")])  # foo, bar 两个事件循环协程


async def await_main():
    logging.info(f"await waiter:{'foooo', 'barrrr'}")
    await asyncio.wait([await_waiter('foooo'), await_waiter('barrrrr')])


async def get_run_loop():  # py37功能
    logging.info(f"sys.version_info.minor:{sys.version_info.minor}")
    if sys.version_info.minor >= 7:
        yield asyncio.get_running_loop()
    else:
        yield asyncio.get_event_loop()

###############++++++ 异步开发的一些坑 =========================
@asyncio.coroutine
def test(n):
    """如果要调用此函数，需要加入loop主事件循环"""
    print(f"test {n}")


@asyncio.coroutine
def bug():
    """py 一般使用sys.excepthook() 处理异常，如果Future.set_exception()被调用，但是没有触发异常，sys.excepthook()将不会被调用，当垃圾回收器删除future时，将有日志记录"""
    raise Exception("not consumed")

@asyncio.coroutine
def handle_exception():
    """有不同的选项可以解决此问题。第一种选择是将协程链接到另一个协程中，并使用经典的try / except："""
    try:
        yield from bug()
    except Exception as e:
        logging.warning(f"exception info:{e}")

###########+++++++++++++++++正确处理协程++++++++++++++++++++++
# 当协程调用其他协程时，必须显示链接，否则不能保证执行顺序
# yield from 带有错误示例 asyncio.sleep() 模式缓慢的操作
@asyncio.coroutine
def create():
    yield from asyncio.sleep(3.0)
    print("(1) create file")

@asyncio.coroutine
def write():
    yield from asyncio.sleep(1.0)
    print("(2) write into file")

@asyncio.coroutine
def close():
    print("(3) close file")

@asyncio.coroutine
def test_async():
    asyncio.ensure_future(create())       # 未显式指定 调用的协程
    asyncio.ensure_future(write())          # 未显式指定 调用的协程
    asyncio.ensure_future(close())      # 未显式指定 调用的协程
    yield from asyncio.sleep(2.0)       # 显式指定 调用的协程
    loop.stop()

@asyncio.coroutine
def disp_test_async():
    """显式指定调用的协程"""
    yield from asyncio.ensure_future(create())
    yield from asyncio.ensure_future(write())
    yield from asyncio.ensure_future(close())
    yield from asyncio.sleep(2.0)
    loop.stop()
@asyncio.coroutine
def non_disp_test():
    yield from create()
    yield from write()
    yield from close()
    yield from asyncio.sleep(2.0)
    # loop.stop()
def dif_non_async():
    """显式调用"""
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(non_disp_test())
    loop.run_forever()
    print("Pending tasks at exit: %s" % asyncio.Task.all_tasks(loop))
    # loop.close()
def dif_test_async():
    """显式调用"""
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(disp_test_async())
    loop.run_forever()
    print("Pending tasks at exit: %s" % asyncio.Task.all_tasks(loop))
    loop.close()
def async_loop():
    """
    (1) create file
    (2) write into file
    (3) close file
    Pending tasks at exit: set()
    协同程序的调用顺序 create()，write()，close()。
    """
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(test_async())
    loop.run_forever()
    print("Pending tasks at exit: %s" % asyncio.Task.all_tasks(loop))
    loop.close()

if __name__ == '__main__':
    loop1 = asyncio.get_event_loop()
    t0 = time.time()
    loop1.run_until_complete(main())
    t1 = time.time()
    print(f"cost time0:{t1 - t0}")
    print(f"get current event loops:{loop1.is_running()}")
    loop1.set_debug(enabled=True)

    loop1.run_until_complete(await_main())
    print(f"get current event loops:{loop1.is_running()}")
    print(f"await asyncio.sleep cost time:{time.time() - t1}")

    # loop1.close()
    import functools
    ##############++++++++++++++++++++++++++ 错误示例，
    # 不会执行的调用
    test(1)
    # 将会执行的调用
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(2))
    # loop.run_forever()
    # loop.close()
    loop.call_soon(functools.partial(print, 'Hello', flush=True))
    # print("Hello", flush=True)
    #坑2： 未处理的异常
    loop_err = asyncio.get_event_loop()
    asyncio.ensure_future(handle_exception())   # 如果直接填入bug()执行时将触发异常，使用 handler则可执行正常
    # loop_err.run_forever()   # 如果抛出错误，forever 将停止在这个地方

    tasks = asyncio.ensure_future(bug())
    try:
        loop_err.run_until_complete(tasks)
    except Exception as e1:
        print(f"exception consumed {e1}")
    # loop_err.close()

    #坑3： 显式调用其他协程的问题
    dif_non_async()     # 如果此函数关闭了事件主循环，下一步函数将不会完成
    dif_test_async()    # 如果上一步函数关闭了事件主循环，这里将报错，因为挂起的任务被销毁，则其包装的协程的执行不会完成。这可能是一个错误，因此会记录警告

    # async_loop()
    loop.close()
    """
    实际输出
    (3) close file
    WARNING:root:exception info:not consumed
    (2) write into file
    INFO:asyncio:poll 1000.000 ms took 1000.000 ms: timeout
    INFO:asyncio:poll 1000.000 ms took 1000.000 ms: timeout
    Pending tasks at exit: {<Task pending coro=<create() running at D:/workspace/gitlab_def/clients/async_process.py:115> wait_for=<Future pending cb=[<TaskWakeupMethWrapper object at 0x0000025A20DE3258>()] created at C:\Python36\lib\asyncio\base_events.py:295> created at D:/workspace/gitlab_def/clients/async_process.py:129>, <Task finished coro=<bug() done, defined at C:\Python36\lib\asyncio\coroutines.py:210> exception=Exception('not consumed',) created at D:/workspace/gitlab_def/clients/async_process.py:186>}
    ERROR:asyncio:Task was destroyed but it is pending!
    source_traceback: Object created at (most recent call last):
      File "D:/workspace/gitlab_def/clients/async_process.py", line 194, in <module>
        async_loop()
    """











