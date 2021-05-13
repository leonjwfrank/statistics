
import time
import json
import hmac
import urllib
import base64
import hashlib

import logger


class RequestError(Exception):
    pass


class RequestService(object):
    def __init__(self, url, path):
        self.url = url
        self.path = path

    def request(self, url, params, path='web', method='POST', version='1.0.0', request_id=None):
        """call service
        :return:
        """

        if not params:
            raise RequestError('params is none')

        now = int(round(time.time() * 1000))


        sys_params = {
            'Path': self.path,
            'url': url,
            'Version': version,
            'Times': now
        }

        params = sys_params
        params.update(params)
        params['Signature'] = RequestService.sign(params, method, self.path + '&')

        url = self.url + path.lower()

        logger.info("Request url: {}".format(url))
        logger.info("Request params: {}".format(params))
        return RequestService.post_request(url, params)

    @staticmethod
    def post_request(url, params):
        """

        :param url:
        :param params:
        :return:
        """
        try:
            headers = {'Content-Type': 'application/json'}
            request = urllib.Request(url=url, headers=headers, data=json.dumps(params))
            response = urllib.urlopen(request).read()
            return json.loads(response)
        except Exception as e:
            raise RequestError('call  api error: %s' % (str(e)))

    @staticmethod
    def sign(params, method, secret_key):
        """加密

        :return:
        """

        to_sign_string = RequestService.generate_to_sign_string(params, method)
        return base64.b64encode(hmac.new(key=secret_key.encode(), msg=to_sign_string, digestmod=hashlib.sha1).digest())

    @staticmethod
    def generate_to_sign_string(params, method):
        """构造待签名字符串

        :param method:
        :return:
        """
        to_sign_string = ''
        keys = params.keys()
        keys.sort()
        for key in keys:
            to_sign_string += '&' + RequestService.percent_encode(key) + '=' + RequestService.percent_encode(params[key])
        to_sign_string = to_sign_string[1:]

        return method.upper() + '&' + RequestService.percent_encode('/') + '&' + RequestService.percent_encode(to_sign_string)

    @staticmethod
    def percent_encode(value):
        """参数编码

        :param value: 参数值
        :return:
        """

        # Python的bool类型转换为标准的: 'true'|'false'
        if isinstance(value, bool):
            value = 'true' if value else 'false'
        if not isinstance(value, str):
            value = str(value)

        return urllib.quote(value, "utf-8").replace("+", "%20").replace("*", "%2A").replace("%7E", "~")


import sys
import os
import unittest
import datetime
class RefDict(object):
    def __init__(self, dict):
        for key, value in dict.items():
            if isinstance(value, (ListType, TupleType)):
                setattr(self, key, [RefDict(x) if isinstance(x, DictType) else x for x in value])
            else:
                setattr(self, key, RefDict(value) if isinstance(value, DictType) else value)

    def __repr__(self):
        return str(self.__dict__)

    def __getitem__(self, key):
        assert hasattr(self, key)
        return getattr(self, key)

    def put(self, key, value):
        if isinstance(value, (ListType, TupleType)):
            setattr(self, key, [RefDict(x) if isinstance(x, DictType) else x for x in value])
        else:
            setattr(self, key, RefDict(value) if isinstance(value, DictType) else value)

class ExecCase(unittest.TestCase):
    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)

        # read in global.conf
        f = open(lib.global_conf_path, 'r')
        conf = eval(f.read())
        f.close()
        self.conf = conf
        self.config = RefDict(conf)
        self.method_name = method_name

    def setUp(self):
        # get self.ip from env/ip.conf
        self.ip = os.getenv('ip')
        self.t_t0 = str(datetime.datetime.now())
        if not self.ip:
            # set self.ip according ip.conf
            ip_file = open(lib.ip_conf_path, 'r')
            ip_conf = eval(ip_file.read())
            ip_file.close()
            if not ip_conf.has_key(self.__class__.__name__):
                self.ip = self.config.cluster_nc
            else:
                self.ip = ip_conf[self.__class__.__name__]

        self.logger = Logger(self.__class__.__name__ + "." + self.config.test_mode, self.method_name).get_logger(self.ip)

    def tearDown(self):
        t0_t0 = str(datetime.datetime.now())
        used_time = datetime.datetime.strptime(t0_t0, '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(self.t_t0,
                                                                                                               '%Y-%m-%d %H:%M:%S.%f')

        try:
            self.logger.info(
                'Test Case {} api Done! case used_time {}, start: {}'.format(self.__class__.__name__, used_time,
                                                                             self.t_t0))
            self.logger.info("===== Teardown Section of %s =====" % self.__class__.__name__)
        except AttributeError as msg:
            print("===== Teardown Section of %s, msg %s=====" % (self.__class__.__name__, msg))


from concurrent.futures import ProcessPoolExecutor
import asyncio
import random
from subprocess import PIPE,Popen
page = "https://www.learning.gov.cn/leader.php?event=1"


async def tasks(op_port):
    tasks = [
        loop.run_in_executor(executor, start_browser, *(op_port, page)),
        # loop.run_in_executor(executor, start_ff_brow, *(op_port, page)),
        loop.run_in_executor(executor, product_page_start, op_port)
    ]
    await asyncio.gather(*tasks)

# @staticmethod
def renew_listen_port():
    """find a port to listen"""
    while True:
        rand_port = random.choice(range(1000, 10000))
        if win_platform():
            cmd_port = 'netstat -an | findstr {}'.format(rand_port)
        else:
            cmd_port = 'netstat -an | grep {}'.format(rand_port)
        pp = Popen(cmd_port, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        info, err = pp.communicate()
        if not info or info in ['', "b''", []]:
            pp.kill()
            return int(rand_port)
        else:
            pp.kill()
            continue


if __name__ == '__main__':
    print('Request service')

    p_url = 'http://127.0.0.1/web/'
    p_request_id = 'test'
    p_request_key = '0123456789ta4b6CLMcMYA=='

    p_path = 'load_banlance'
    p_params = {
        'uuid': '123456789'
    }

    request_service = RequestService(p_url, 'web')
    print(json.dumps(request_service.request(p_path, p_params)))

    # =====================================ansy
    op_port = note_operate_page.renew_listen_port()

    loop = asyncio.get_event_loop()
    executor = ProcessPoolExecutor(max_workers=2)
    # try:
    loop.run_until_complete(tasks(op_port))