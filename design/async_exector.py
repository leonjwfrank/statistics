"""
    异步进程执行者  concurrent.futures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=1) as pp:
        future = pp.submit(pow, 323,1233)
        print(future.result())
"""

###########+++++++++++++1,ThreadPoolExecutor exector-object+++++++++++++++++++++#########################
# concurrent.futures.Executor
## submit  调用对象的可执行方式
import math
import asyncio
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def executor_submit(n=1):
    with ProcessPoolExecutor(max_workers=n) as pp:
        future = pp.submit(pow, 2, 4)
        print(future.result())


def executor_map():
    with ProcessPoolExecutor(2) as ex:
        inter = ex.map(math.sqrt, [1, 2, 3, 4, 5, 6])
        ex.shutdown()
        print(f"list:{list(inter)}")


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True


def process_prime():
    PRIMES = [
        112272535095293,
        112582705942171,
        112272535095293,
        115280095190773,
        115797848077099,
        1099726899285419]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))


def executor_thread():
    import shutil
    log_path = "../log/"
    with ThreadPoolExecutor(max_workers=4) as e:
        e.submit(shutil.copy, f'{log_path}src1.txt', f'{log_path}dest1.txt')
        e.submit(shutil.copy, f'{log_path}src2.txt', f'{log_path}dest2.txt')
        e.submit(shutil.copy, f'{log_path}src3.txt', f'{log_path}dest3.txt')
        e.submit(shutil.copy, f'{log_path}src4.txt', f'{log_path}dest4.txt')


def executor_thread_never_end():
    import time

    # @asyncio.coroutine
    def wait_on_b():
        time.sleep(5)
        print(b.result())  # b will never complete because it is waiting on a.
        return 5

    # @asyncio.coroutine
    def wait_on_a():
        time.sleep(5)
        print(a.result())  # a will never complete because it is waiting on b.
        return 6

    def wait_on_c():
        asyncio.sleep(3)
        print(f"asyncio sleep")
        return 3

    def wait_on_d():
        asyncio.sleep(4)
        print(f"asyncio sleep 4")
        return 4
    executor = ThreadPoolExecutor(max_workers=4)
    a = executor.submit(wait_on_a)
    b = executor.submit(wait_on_b)


def executor_thread_never_end_two():
    def wait_on_future():
        f = executor.submit(pow, 5, 2)
        # This will never complete because there is only one worker thread and
        # it is executing this function.
        print(f.result())

    executor = ThreadPoolExecutor(max_workers=2)
    executor.submit(wait_on_future)


def executor_thread_pools():
    """拉取列表中的网站，返回网站和页面字节数"""
    import concurrent.futures
    import urllib.request

    URLS = ['http://www.foxnews.com/',
            'http://www.cnn.com/',
            'http://europe.wsj.com/',
            'http://www.bbc.co.uk/',
            'http://some-made-up-domain.com/']

    # Retrieve a single page and report the URL and contents
    def load_url(url, timeout):
        with urllib.request.urlopen(url, timeout=timeout) as conn:
            return conn.read()

    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                print('%r page is %d bytes' % (url, len(data)))


########+++++++++++++++++++++2,ProcessPoolExecutor++++++++++++++++++#####################
# ProcessPoolExecutor 使用的过程池异步执行调用子类。 使用该模块，它可以避开全局解释器锁定，但也意味着只能执行和返回可拾取对象

if __name__ == '__main__':
    # executor_map()
    # executor_thread()
    # executor_thread_pools()
    # executor_thread_never_end()
    pass

    str = "hihihihihi"
    for i in range(0, 10):
        for j in range(0, i + 1):
            print(str[j], end=" ")
        print()



