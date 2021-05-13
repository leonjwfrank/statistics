

"""
redis 缓存服务器避免重复计算已知的结果
因为两个Handler都需要用到redis，所以我们将redis单独抽出来，通过参数传递进去。
另外Handler可以通过initialize函数传递参数，在注册路由的时候提供一个字典就可以传递任意参数了，字典的key要和参数名称对应。
一个普通的tornado web服务器通常由四大组件组成。

ioloop实例，它是全局的tornado事件循环，是服务器的引擎核心，示例中tornado.ioloop.IOLoop.current()就是默认的tornado ioloop实例。
app实例，它代表着一个完成的后端app，它会挂接一个服务端套接字端口对外提供服务。一个ioloop实例里面可以有多个app实例，示例中只有1个，实际上可以允许多个，不过一般几乎不会使用多个。
handler类，它代表着业务逻辑，我们进行服务端开发时就是编写一堆一堆的handler用来服务客户端请求。
路由表，它将指定的url规则和handler挂接起来，形成一个路由映射表。当请求到来时，根据请求的访问url查询路由映射表来找到相应的业务handler。
这四大组件的关系是，一个ioloop包含多个app(管理多个服务端口)，一个app包含一个路由表，一个路由表包含多个handler。
ioloop是服务的引擎核心，它是发动机，负责接收和响应客户端请求，负责驱动业务handler的运行，负责服务器内部定时任务的执行。

当一个请求到来时，ioloop读取这个请求解包成一个http请求对象，找到该套接字上对应app的路由表，通过请求对象的url查询路由表中挂接的handler，然后执行handler。
handler方法执行后一般会返回一个对象，ioloop负责将对象包装成http响应对象序列化发送给客户端。
"""
import json
import redis
import math
import tornado.ioloop
import tornado.web


class FactorialService(object):

    def __init__(self):
        self.cache = redis.StrictRedis("localhost", 6379)  # 缓存换成redis了
        self.key = "factorials"

    def calc(self, n):
        s = self.cache.hget(self.key, str(n))  # 用hash结构保存计算结果
        if s:
            return int(s), True
        s = 1
        for i in range(1, n):
            s *= i
        self.cache.hset(self.key, str(n), str(s))  # 保存结果
        return s, False


class FactorialHandler(tornado.web.RequestHandler):

    service = FactorialService()

    def get(self):
        n = int(self.get_argument("n") or 1)  # 参数默认值
        fact, cached = self.service.calc(n)
        result = {
            "n": n,
            "fact": fact,
            "cached": cached
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(result))


class PiService(object):

    def __init__(self, cache):
        self.cache = cache
        self.key = "pis"

    def calc(self, n):
        s = self.cache.hget(self.key, str(n))
        if s:
            return float(s), True
        s = 0.0
        for i in range(n):
            s += 1.0/(2*i+1)/(2*i+1)
        s = math.sqrt(s*8)
        self.cache.hset(self.key, str(n), str(s))
        return s, False

def make_app():
    return tornado.web.Application([
        (r"/fact", FactorialHandler),
    ])



"""
# pi.py
import json
import math
import redis
import tornado.ioloop
import tornado.web

class FactorialService(object):

    def __init__(self, cache):
        self.cache = cache
        self.key = "factorials"

    def calc(self, n):
        s = self.cache.hget(self.key, str(n))
        if s:
            return int(s), True
        s = 1
        for i in range(1, n):
            s *= i
        self.cache.hset(self.key, str(n), str(s))
        return s, False

class PiService(object):

    def __init__(self, cache):
        self.cache = cache
        self.key = "pis"

    def calc(self, n):
        s = self.cache.hget(self.key, str(n))
        if s:
            return float(s), True
        s = 0.0
        for i in range(n):
            s += 1.0/(2*i+1)/(2*i+1)
        s = math.sqrt(s*8)
        self.cache.hset(self.key, str(n), str(s))
        return s, False

class FactorialHandler(tornado.web.RequestHandler):

    def initialize(self, factorial):
        self.factorial = factorial

    def get(self):
        n = int(self.get_argument("n") or 1)
        fact, cached = self.factorial.calc(n)
        result = {
            "n": n,
            "fact": fact,
            "cached": cached
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(result))

class PiHandler(tornado.web.RequestHandler):

    def initialize(self, pi):
        self.pi = pi

    def get(self):
        n = int(self.get_argument("n") or 1)
        pi, cached = self.pi.calc(n)
        result = {
            "n": n,
            "pi": pi,
            "cached": cached
        }
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(result))

def make_app():
    cache = redis.StrictRedis("localhost", 6379)
    factorial = FactorialService(cache)
    pi = PiService(cache)
    return tornado.web.Application([
        (r"/fact", FactorialHandler, {"factorial": factorial}),
        (r"/pi", PiHandler, {"pi": pi}),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
"""

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
