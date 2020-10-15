import asyncio
import platform
import sys

from tornado.concurrent import is_future, future_set_exc_info, Future
from tornado.gen import convert_yielded
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.netutil import Resolver
from tornado.platform.asyncio import AnyThreadEventLoopPolicy

def tornado_init():
    """tornado init configure"""
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())

    if platform.system() != "Windows":
        Resolver.configure('tornado.playform.careresolver.CaresResolver')
        AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')

def run_unitil_all_complete(func, *args, **kwargs):
    """exec func until all task done(可能往Event Loop 添加心的回调或任何)"""
    future_cell = [None]

    # noinspection PyTypeChecker, PyBroadexception
    def run():
        """execute dest func"""
        try:
            result = func(*args, **kwargs)
            if result is not None:
                result = convert_yielded(result)
        except Exception:
            future_cell[0] = Future()
            future_set_exc_info(future_cell[0], sys.exc_info())
        else:
            if is_future(result):
                future_cell[0] = result
            else:
                future_cell[0] = Future()
                future_cell[0].set_result(result)
        IOLoop.current().add_future(future_cell[0], lambda  future:check_stop())

    def check_stop():
        """检查是否可能停止"""
        for task in asyncio.Task.all_tasks():
            if not (task.done() or task.cancelled()):
                IOLoop.current().add_callback(check_stop)
                return None
        IOLoop.current().stop()
    IOLoop.current().add_callback(run)
    IOLoop.current().start()
    return future_cell[0].result()