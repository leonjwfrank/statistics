# 元注解单例的实践
import os
import traceback
from configparser import ConfigParser
from enum import Enum, unique
import redis
import pickle
# 协程库 gen允许异步代码更直接，而不用链式回调
from tornado.gen import coroutine, Return
# AsyncHTTPClient 是HTTP客户端实现
from tornado.httpclient import AsyncHTTPClient
# 异步网络库IOLoop
from tornado.ioloop import IOLoop

from tornado.options import options
import logging
from setting import root
from py_design_model.py_1_singleton import SingletonMetaclass

rd = redis.Redis(host=options.redis_host, port=options.redis_port, password=options.redis_password, db=options.redis_db)
pipe = rd.pipeline()


class WebRequest(metaclass=SingletonMetaclass):
    retry = "web:retry"

    def __init__(self):
        self.domain_alloc = None
        self.domain_record = None
        self.web_conf_path = os.path.join(os.path.join(root, 'private'), 'app.conf.py')
        self.reload_domain()

    def reload_domain(self):
        """
                需要配置文件格式如
                [url]
                root = '192.168.0.1:8080/home.html'
        """
        conf_web = ConfigParser()
        conf_web.read(self.web_conf_path)

        self.domain_alloc = conf_web.get('url', 'root')
        # 直接读取模块配置
        # import app.conf
        # self.domain_alloc = app.conf.root
    @coroutine
    def retry(self):
        if rd.exists(self.retry):
            self.reload_domain()
            uri, body, domain = pickle.loads(rd.rpop(self.retry))
            flag = yield self.post(uri, body, domain)
            if flag and rd.llen(self.retry) > 0:
                q_size = rd.llen(self.retry)
                IOLoop.instance().call_later(1 * (q_size % (q_size // 5)), self.retry)
    def push(self, uri, body, domain):
        """"""
        rd.lpush(self.retry, pickle.dumps((uri, body, domain)))
    @coroutine
    def post(self, uri, body, domain=None):
        if domain:
            url = self.domain_record + uri
        else:
            url = self.domain_alloc + uri
        try:
            request = AsyncHTTPClient()
            # logging for tracker
            response = yield request.fetch(url, method='POST', body=body)
            logging.info(f'Success fetch url:{url},post_resp_code:{response.code}, response:{response}')
            self.retry()
            raise Return(True)   # tornado Return
        except Return:
            pass
        except Exception as err:
            logging.exception(f'request url:{url}, error info:{err}')
            self.push(uri, body, domain)
            self.reload_domain()
            raise Return(False)
    @coroutine
    def post_callback(self, uri, body, domain=None, call_back=None, error_back=None, retry_times=3):
        """"""
        if domain:
            url = self.domain_record + uri
        else:
            url = self.domain_alloc + uri

        try:
            request = AsyncHTTPClient()
            logging.info(f"post_callback:{url}, call_back {call_back}")
            response = yield request.fetch(url, method="POST", body=body)
            if call_back:
                back_resp = call_back(response)
                if isinstance(back_resp, bytes):
                    logging.info(f"back_resp_decode:{back_resp.decode('utf-8', 'replace')}")
        except Exception as e:
            traceback.print_exc()
            if retry_times > 0:
                retry_times -= 1
                IOLoop.instance().call_later(1, self.post_callback, uri, body ,domain, call_back, error_back, retry_times)
            else:
                logging.exception(f"url:{url} failed info:{e}")
                if error_back:
                    error_back()





