"""
    基于corntab实现定时调度
"""
import functools
import math
from concurrent.futures.thread import ThreadPoolExecutor

from crontab import CronTab
from tornado.concurrent import run_on_executor
from tornado.gen import coroutine
from tornado.ioloop import PeriodicCallback
from tornado.options import options
from src.tornado_complete import run_unitil_all_complete


class CronTabCallback(PeriodicCallback):
    """基于Crontab的周期性回调"""
    executor = ThreadPoolExecutor(options.zmq_thread_max_worker, 'crontab_worker')
    def __init__(self, callback, schedule):
        """

        :param callback:
        :param schedule: 定时任务参数
        """
        self._callback = callback
        self._crontab = CronTab(schedule)

        if options.crontab_thread_enabled:
            super(CronTabCallback, self).__init__(self.worker_run, self._calc_callbacktime())
        else:
            super(CronTabCallback, self).__init__(self.coroutine_run, self._calc_callbacktime())
    def _calc_callbacktime(self, now=None):
        """计算出最近一次的执行时间"""
        return math.ceil(self._crontab.next(now, default_utc=False)) * 1000.0

    @run_on_executor
    def worker_run(self):
        """通过开启线程，执行回调"""
        run_unitil_all_complete(self._callback)

    @coroutine
    def coroutine_run(self):
        """通过协程执行回调"""
        yield self._callback()

    def _schedule_next(self) -> None:
        """覆盖基类，通过corntab计算下次执行时间"""
        self.callback_time = self._calc_callbacktime()
        super(CronTabCallback, self)._schedule_next()

def crontab(schedule):
    """装饰该函数后变成调度启动器，原始函数作为调度执行的目标函数
    :param schedule: crontab定时参数"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            CronTabCallback(functools.partial(func, *args, **kwargs), schedule).start()
        return wrapper
    return decorator