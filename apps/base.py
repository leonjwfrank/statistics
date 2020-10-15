import asyncio
import logging
import signal
import time
from collections import namedtuple

from tornado.ioloop import IOLoop
from tornado.options import options

app = None

def make_app(application):
    global app
    app = application()
    app.start()
    return app

Callback = namedtuple("Callback", ['callback', 'priority'])

class BaseApplication(object):
    """class for base applicaiton"""
    MAX_WAIT_SECONDE_BEFORE_SHUTDOWN = 5

    def __init__(self):
        self.running = False
        self._start_callbacks = []
        self._shutdown_callbacks = []

    def init(self):
        """app start init, then start callback func"""
        pass

    def close(self):
        """app close out service, can continue inside process"""
        pass

    def destory(self):
        """app stage, close process realease all resources"""
        pass

    def start(self):
        if not self.running:
            self.init()
            self.call_start_callbacks()
            self.running = True

            signal.signal(signal.SIGINT, self.shutdown_hook)
            signal.signal(signal.SIGTERM, self.shutdown_hook)

    def shutdown(self):
        """close application, two stage: Close, Destroy. app will close when wait for seconds"""
        if self.running:
            self.close()
            self.call_shotdown_callbacks()
            self.running = False

            logging.info(f'Shutdown [{options.host_name}], maximum wait to [{self.MAX_WAIT_SECONDE_BEFORE_SHUTDOWN}] seconds... ')
            def stop_io_loop(deadline):
                now = time.time()
                if now < deadline and asyncio.Task.all_tasks():
                    IOLoop.current().add_timeout(now+1, stop_io_loop, deadline)
                else:
                    self.destory()
                    IOLoop.current().stop()

                stop_io_loop(time.time() + self.MAX_WAIT_SECONDE_BEFORE_SHUTDOWN)
    def on_start(self, priority=0):
        """装饰器配置应用启动后的回调函数
        priority: 优先级越高越先调用，默认优先按配置先后顺序调用
        装饰器函数"""
        def decorator(func):
            self.add_start_callback(func, priority)

        return decorator
    def add_start_callback(self, func, priority=0):
        """new callback func after start
        func: callback func
        priority: 优先级越高越先调用，默认优先级按配置先后顺序调用"""
        self._start_callbacks.append(Callback(func, priority))
        self._start_callbacks.sort(key=lambda c:c.priority, reverse=True)

    def on_shutdown(self, priority=0):
        def decorator(func):
            self.add_shutdown_callback(func, priority)
        return decorator

    def add_shutdown_callback(self, func, priority=0):
        self._shutdown_callbacks.append(Callback(func, priority))
        self._shutdown_callbacks.sort(key=lambda c:c.priority, reverse=True)

    def call_start_callbacks(self):
        """execute callback func when start"""
        for callback in self._start_callbacks:
            callback.callback()

    def call_shutdown_callbacks(self):
        """"""
        for callback in self._start_callbacks:
            callback.callback()

    def shutdown_hook(self, signum, frame):
        logging.info('Caught shutdown signal:%s, frame:%s', signum, frame)
        IOLoop.current().add_callback_from_signal(self.shutdown)


