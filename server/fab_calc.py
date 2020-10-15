# restful server
import tornado.websocket
import tornado.gen
import tornado.httpclient
from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import redis
import json
import time

from functools import lru_cache


import tornado.httpserver
import ssl
import os
import tornado.netutil
import tornado.process


class FactorialRedis(object):
    def __init__(self):
        self.cache = redis.StrictRedis("localhost", 6379)  # 缓存换为redis


class CalcFibonacci(object):
    """计算斐波那契数列 fibonacci """
    t = []

    @lru_cache(None)
    def calc_fib(self, n):
        if n < 2:
            return 1
        else:
            return self.calc_fib(n - 1) + self.calc_fib(n - 2)

    @staticmethod
    def calc_fib_no_cache(n):
        if n < 2:
            return 1
        else:
            return CalcFibonacci.calc_fib_no_cache(n - 1) + CalcFibonacci.calc_fib_no_cache(n - 2)

    @staticmethod
    def calc_fib_math(x):
        a, b = 0, 1
        while a < x:
            CalcFibonacci.t.append(a)
            print(a, end=" ")
            a, b = b, a+b
        return CalcFibonacci.t


class FactoricalService(object):
    """计算阶乘主服务函数"""

    def __init__(self, recalc=None):
        self.cache = FactorialRedis().cache
        self.key = "factorials"
        self.recalc = True if recalc is None else recalc
        assert type(self.recalc) is bool

    def calc(self, n):
        if self.recalc is False:  # 指定取缓存值
            s = self.cache.hget(self.key, str(n))  # 用hash结构计算保存结果
            if s:
                return int(s), True
            else:
                raise ValueError(f'this not save in redis cache!')
        else:
            s = 1
            for i in range(1, n + 1):  # 再次计算阶乘
                s *= i
            self.cache.hset(self.key, str(n), str(s))  # 保存结果
            return s, False  # False 表示它是计算得来。不是redis缓存取的


class FactorialRestFul(tornado.web.RequestHandler):
    """计算阶乘服务，RestFul接口， 同时接收两个参数，"""

    def initialize(self, service):
        self.service = service

    def get(self, re, n):
        """
        Args:
            re: 是否重新计算
            n:  计算哪个值的阶乘
        Returns:
        """
        print(f"receive url path re:{re}, n:{n}")
        # 接收处理参数
        try:
            self.service.recalc = True if int(re) is not 0 else False  # 0表示不重新计算，非0整数表示重新计算。
        except:
            self.service.recalc = False
        # 接收处理参数
        try:
            n = int(n) if n else 1  # 如果为真强制转换为 int 类型
        except:  # 如果n不可以强制转换为 int类型，赋值为 1
            n = 1
        rst, cache = self.service.calc(n)
        result = {
            "n": n,
            "factorial": rst,
            "cached": cache
        }
        print(f"return calc result:{result}")
        self.write(json.dumps(result))


class FactorialHandler(tornado.web.RequestHandler):
    def initialize(self, service):
        """recalc 指定是否重新计算，参数的bool值决定
        0 不重新计算， 读取redis的 cache值
        非0， 重新计算，此时即使redis中有值也重新计算
        :return:
        """
        try:
            re_calc = bool(int(self.get_argument("recalc")))  # get模式, 从encode字符串接受参数，并转义为python 的bool类型
        except Exception as earg:
            print(f"get argument error:{earg}")
            re_calc = False
        service.recalc = re_calc
        self.service = service

    def get_arg(self):
        """

        Returns:

        """
        return int(self.get_argument('ng') or 1)

    def ret_result(self, **kwargs):
        """
        :param kwargs
        Args:
            **kwargs:

        Returns:

        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        try:
            n = kwargs['ng']  # 尝试获取n的值，否重参数默认值 http://127.0.0.1:8888/factorial?recalc=0&ng=6
        except:
            n = 1
        factorial = kwargs['factorial']
        cached = kwargs['cached']
        result = {
            "n": n,
            "factorial": factorial,
            "cached": cached
        }
        self.write(json.dumps(result))

    def service_math(self):
        """

        Returns:
        """
        n_num = self.get_arg()
        # if n_num == 1 and n:   # 从用户get请求输入获取需要计算的n值
        #     n_num = n
        factorial, cached = self.service.calc(n_num)
        self.ret_result(**{'ng': n_num, 'factorial': factorial, 'cached': cached})
        return n_num, factorial, cached

    def get(self):
        """

        Returns:

        """
        n_num, factorical, cached = self.service_math()

    def post(self, n):
        """

        Returns:

        """
        n_num, factorical, cached = self.service_math()


class VersionHandler(tornado.web.RequestHandler):
    """RequestHandler 子类"""

    def get(self):
        response = {'version': '6.x', 'last_build': date.today().isoformat()}
        self.write(response)


class GetGameByIdHandler(tornado.web.RequestHandler):
    def initialize(self, common_string):
        self.common_string = common_string

    def get(self, id):
        response = {'id': int(id),
                    'name': 'Crazy_Game',
                    'release_date': date.today().isoformat(),
                    'common_string': self.common_string}
        self.write(response)


class GetFullPageAsyncHandler(tornado.web.RequestHandler):
    def initialize(self, active_port):
        self.active_port = active_port

    @tornado.gen.coroutine
    def get(self):
        """非阻塞HTTP客户端"""
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_response = yield http_client.fetch("http://127.0.0.1:{}/version".format(self.active_port))
        response = http_response.body.decode().replace('6.x', 'Version 6.0.1')
        self.write(response)
        self.set_header('Content-Type', 'application/json')


class WSHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, name=None):
        self.name = name
        self.t0 = None

    @property
    def ret_dater(self):
        import datetime
        return str(datetime.datetime.now())

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self):
        """

        Returns:

        """
        self.t0 = time.clock()
        print(f"received request body:{self.request.body}, remote ip:{self.request.remote_ip} at time {self.ret_dater}")
        print(f"WebSocker Opend!  self.t0:{self.t0}")

    def get(self, msg=None):
        """

        Returns:

        """
        resp_msg = str(self.request.body) + str(self.ret_dater)
        print(f"get message:{msg}")
        self.write("get response message:{}".format(resp_msg))

    def post(self):
        """

        Returns:

        """
        resp_bytes = str(self.ret_dater) + str(self.request.body) + str(self.request.remote_ip)
        self.write_message("post reponse message#:{}".format(resp_bytes.encode()), True)

    async def on_message(self, message):
        """

        Args:
            message:

        Returns:

        """
        print(
            f"debug message one client arrived at time :@{self.ret_dater}, request method:{self.request.method}, client request_time:{self.request.request_time()}")
        await self.write_message(u"@time:{} You said:{}".format(self.ret_dater, message), True)
        print(f"cost time on message:{time.clock() - self.t0}")

    def on_close(self) -> None:
        """

        Returns:

        """
        print(f"cost time：{time.clock() - self.t0}， closed time:{time.clock()}")
        print(f"WebSocket closed!")


class ErrorHandler(tornado.web.RequestHandler):
    """错误处理类ErrorHandler请求处理程序代码，演示了三个不同机制在处理程序方法中返回错误的最简单方法
    同时需要添加此类映射到application中，如果error_code=1, get方法调用self.set_status
    如果error_code=2, get方法调用self.send_error,它将指定的HTTP错误代码发送到浏览器
    其他任何error_code都使get方法引发带有500状态码的tornado.web.HTTPError异常
    通过覆盖RequestHandler子类的write_error方法更改默认页面。"""

    def get(self, error_code):
        if error_code == 1:
            self.set_status(status_code=500, reason='Server Internal Error, Detail:{}'.format(error_code))
        elif error_code == 2:
            self.send_error(500, reason='Internal Error with code:{}'.format(error_code))
        else:
            raise tornado.web.HTTPError(500, reason='HttpError:{}'.format(error_code))


class TipsHandler(tornado.web.RequestHandler):
    def get(self):
        pass
        import os
        from filter_words import buddha
        self.write(f"filter_words:{buddha.__dict__}")


class PassHandler(object):

    @staticmethod
    def listener(port, service_calc):
        application = tornado.web.Application([
            (r"/getfullpage", GetFullPageAsyncHandler, dict(active_port=port)),
            (r"/getgamebyid/([0-9]+)", GetGameByIdHandler, dict(common_string='Value defined in application')),
            (r"/version", VersionHandler),
            (r"/error/([0-9]+)", ErrorHandler),  # 映射，错误处理类
            (r"/factorial", FactorialHandler, dict({'service': service_calc})),
            (r"/factor/([0-9]+)/([0-9]+)", FactorialRestFul, dict({'service': service_calc})),
            (r"/wsecho", WSHandler),
            (r"/tips", TipsHandler),
        ], )

        application.listen(port)


def listener(port, service_calc):
    config_dict = {"certfile": os.path.join(os.path.abspath('..'), "minica.pem"),  # "private", "cacert.pem"
                   "keyfile": os.path.join(os.path.abspath('..'), "minica-key.pem"),  # "private", "prvtkey.pem"
                   "port": active_port,
                   "address": "0.0.0.0",
                   "hmac_key": False,
                   "tokens": False}
    urls = [
        (r'/realtime', service_calc),
        (r'/echo', WSHandler)
    ]
    application = tornado.web.Application(urls, auto_reload=True)
    ssl_options = dict(certfile=config_dict["certfile"], keyfile=config_dict["keyfile"])
    http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_options)
    http_server = tornado.httpserver.HTTPServer(application)
 

    # ssl crt
    ca_path = "."
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain(os.path.join(ca_path, "ca1.crt"),
                            os.path.join(ca_path, "ca1.key"))
    server = tornado.web.HTTPServer(application, ssl_options=ssl_ctx)
    http_server.bind(port)
    # http_server.start(0)  # forks multiple sub-processes
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    # 服务端口
    active_port = 8011
    # 初始化  计算类服务]
    print(f"web server start on port:{active_port}")
    """
    factor_calc = FactoricalService()

    # 绑定接口和服务
    
    PassHandler.listener(active_port, factor_calc)
    
    
    tornado.ioloop.IOLoop.instance().start()
    """
    # hs = EchoWebSocket()
    # application = tornado.web.Application([
    #      (r"/wsecho", WSHandler),
    # ], )
    #
    # application.listen(active_port)
    # tornado.ioloop.IOLoop.instance().start()

    # PassHandler.listener(active_port, WSHandler)
    n = 35
    t0 = time.time()
    fb_list = CalcFibonacci().calc_fib(n)
    print(f"Cached 40 fib list cost time:{time.time() - t0}, {fb_list}")

    t1 = time.time()
    no_cached_list = CalcFibonacci.calc_fib_no_cache(n)
    print(f"No cached 40 fib list cost time:{time.time() - t1}, {no_cached_list}")
