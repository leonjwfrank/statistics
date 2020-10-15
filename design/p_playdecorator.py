# 装饰器一般用于封装函数
## 1，装饰器，作为一个函数，返回包装原始函数调用的一个子函数

def tes_decro(fuc):
    x = 1

    def do_func(*args, **kwargs):
        res = fuc(*args, **kwargs)
        return res + x

    return do_func


@tes_decro
def sum_add(a, b):
    return a * b + 2


## 2，类 装饰器
### 如果装饰器需要复杂的参数化或依赖于特定状态，类装饰器
## 2.1 非参数化装饰器
class DecoratorAsClass:
    def __init__(self, function):
        self.func = function

    def __call__(self, *args, **kwargs):
        # 在调用原始函数前做的事情
        res = self.func(*args, **kwargs)
        # 调用原始函数后做的事情
        # ...
        # 返回结果
        return res


@DecoratorAsClass
def sum_class_decorator(a, b):
    return a * b * 3


## 2.2 参数化的装饰器，可在装饰器传入参数, 需要两层包装
def repeat(number=3):
    """
    返回最后一次原始函数运行 后的值作为结果
    :param number:重复次数,默认值3
    """

    def actual_decorator(function):
        """外层包装"""

        def wrapper(*args, **kwargs):
            """内层包装"""
            result = None
            for _ in range(number):
                result = function(*args, **kwargs)
                print(f"b result:{result}")
                if result:
                    result += _
                    print(f"result:{result}")
            return result

        return wrapper

    return actual_decorator


# @repeat
@repeat(2)  # 有参数的装饰器 如果没有传入参数，也没有使用默认参数将会报错
def add_num(a, b):
    """执行函数"""
    print(a + b)
    return a + b


##2.3, 保持内省的装饰器， 即可保存原始函数的元数据（主要是文档串和原始函数名）
## 保持内省的装饰器有利于函数的调试
from functools import wraps


def repeat_outer(number=2):
    """保留原始函数"""

    def repeat_inner(func):
        """外层包装"""

        @wraps(func)
        def inner_func(*args, **kwargs):
            """内层包装"""
            rest = None
            for xx in range(number):
                rest = func(*args, **kwargs)
            return rest

        return inner_func

    return repeat_inner


@repeat_outer()  # 必须要括号使用默认参数
def rep_add(a, b):
    """执行者，保留了原始函数"""
    return a * b


# 3, 装饰器用途，参数检查，缓存，代理，上下文提供者
## 3.1 参数检查，rpc 调用时的才是检查
rpc_info = {}


def xmlrpc(in_=(), out_=(type(None, ),)):
    """
     该装饰器函数 将 传入的函数注册到全局字典，并将其参数和返回值保存在一个类型列表中。
    """

    def _xmlrpc(function):
        # 注册签名
        func_name = function.__name__
        rpc_info[func_name] = (in_, out_)

        def _check_types(elements, types):
            """用于检查类型的子函数"""
            if len(elements) != len(types):
                raise TypeError('argument count is wrong.')
            typed = enumerate(zip(elements, types))  # zip打包并返回一个 enumerate枚举对象
            for index, couple in typed:
                arg, of_the_right_type = couple
                if isinstance(arg, of_the_right_type):
                    continue
                raise TypeError(f'arg {index} should be {of_the_right_type}')

        def __xmlrpc(*args):  # 包装过的函数，没有允许的关键词
            # 检查输入内容, 装饰器函数
            checkable_args = args[1:]  # 去掉self
            _check_types(checkable_args, in_)
            # 执行函数
            res = function(*args)
            #  检查输出内容
            if not type(res) in (tuple, list):
                checkable_res = (res,)
            else:
                checkable_res = res
            _check_types(checkable_res, out_)

            # 函数及其类型检查成功
            return res

        return __xmlrpc

    return _xmlrpc


class RPCView:
    @xmlrpc((int, int))  # int -> None
    def meth_one(self, a: int, b: int):
        print(f"received {a} and {b}")

    @xmlrpc((str,), (int,))  # string -> int
    def meth_two(self, phrase):
        print(f"received {phrase}")
        return 12


## 3.2 缓存装饰器
### 将输出和计算需要的参数放到一起，并在后续调用中直接返回， 函数式编程
import time
import hashlib
import pickle

cache = {}


def is_obsolete(entry, duration):
    return time.time() - entry['time'] > duration


def compute_key(function, args, kw):
    key = pickle.dumps((function.__name__, args, kw))  # 建立hash
    return hashlib.sha1(key).hexdigest()


def memoize(duration=10):  # 持续时间
    def _memoize(function):
        def __memoize(*args, **kw):
            key = compute_key(function, args, kw)
            # 是否已经拥有
            if (key in cache and not is_obsolete(cache[key], duration)):
                print('we got a winner')
                return cache[key]['value']
            # 计算
            result = function(*args, **kw)
            # 保存信息
            cache[key] = {'value': result, 'time': time.time()}
            return result

        return __memoize

    return _memoize


@memoize()  # 不加括号将报错
def very_complex_stuff(a, b):
    return a + b


@memoize(12)  # 1秒后失效
def very_very_complex_stuff(a, b):
    return a + b


## 3.3 代理 装饰器
### 代理装饰器使用全局机制标记和注册函数，如 根据用户来保护代码的安全层，可用使用集中式检测器和相关可调用的对象要求的权限来实现
class User(object):
    def __init__(self, roles):
        self.roles = roles


class Unauthorized(Exception):
    pass


def protect(role):
    """代理模型，可用于保护函数的 访问安全"""

    def _protect(function):
        def __protect(*args, **kwargs):
            user = globals().get('user')
            if user is None or role not in user.roles:
                raise Unauthorized('No accepted access.')
            return function(*args, **kwargs)

        return __protect

    return _protect


## 3.4 上下文提供器
### 3.4.1 作为一个类，与with上下文管理器共用，确保函数运行在正确的上下文中，或者函数前后运行一些代码。
#### 如当一个数据需要在多个线程之间共享时，需要用一个锁来保护它避免多次访问，锁可用在装饰器中编写
from threading import RLock

lock = RLock()


def synchronized(function):
    def _synchronized(*args, **kwargs):
        lock.acquire()
        try:
            return function(*args, **kwargs)
        finally:
            lock.release()

    return _synchronized


@synchronized
def thread_safe():  # 确保锁定资源
    print(f"locked info")


### with 嵌套和多个对象同时打开
def with_example():
    with open('./a.txt') as a, open('./b.txt') as b:
        # ...
        pass
    """
    或者 等价嵌套
    """
    with open('a.txt') as a:
        with open('b.txt') as b:
            # ...
            pass


## 实现自定义 with类，包含 __enter__(self), __exit__(self)
class ContextIllustration:
    def __enter__(self):
        print('enter with context')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('leaving with context')
        if exc_type is None:
            print('with no error')
        else:
            print(f'with an error:{exc_val}')  # with 语句子句报错时抛出此错误


### 3.4.2 作为一个函数 contextlib模块
from contextlib import contextmanager


@contextmanager
def context_illus():
    print('enter context')
    try:
        yield
    except Exception as e:
        print('leaving context')
        print('with an error', e)
        # 需要再次抛出异常
        raise
    else:
        print('leaved context.')
        print('with no error.')


if __name__ == '__main__':
    # xx = sum_add(2,3)
    # print(xx)

    # xc = sum_class_decorator(3, 4)
    # print(xc)
    #
    # print(f'add_num:{add_num.__doc__}')
    # total_res = add_num(3, 4)
    # print(f"total_res:{total_res}")
    #
    # print(f"keep:{rep_add.__doc__}")
    # rep_rest = rep_add(4,5)
    # print(f"rest:{rep_rest}")

    # 应用1，RPC请求参数检查
    # print(rpc_info)
    # mm = RPCView()
    # print(mm.meth_one(1,11))
    # print(mm.meth_two('staa'))
    #
    # # 应用2，缓存管理
    # print(f"before cache:{cache}")
    # very_complex_stuff(2,3)
    # print(f"after cache:{cache}")

    # very_very_complex_stuff(2,3)
    # print(f"very after cache {cache}")
    """
    ## 应用3， 代理，保护函数安全访问
    trek = User(('admin', 'user'))
    bill = User(('user',))


    class MySecrets(object):
        @protect('admin')
        def waffle_recipe(self):
            print('use tons of butter!')


    there_are = MySecrets()
    user = trek
    print(f"there_are waffle recipe:", there_are.waffle_recipe())
    # user = bill
    # there_are.waffle_recipe()

    ## 应用4， 上下文提供者
    thread_safe()
    """
    ct = ContextIllustration()

