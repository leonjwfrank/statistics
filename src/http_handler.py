import logging
import random
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from inspect import iscoroutine

from tornado.concurrent import run_on_executor
from tornado.escape import utf8, json_decode
from tornado.log import gen_log
from tornado.options import options
from tornado.web import RequestHandler, HTTPError

from src.http_router import HttpMethod
from src.http_session import SessionMixin
from src import json_extend as json
from src.tornado_complete import run_unitil_all_complete

class WebRequestHandler(RequestHandler, SessionMixin):
    """Http requestor, every request mapping one instance"""
    executor = ThreadPoolExecutor(options.http_thread_max_workers, 'http_worker')
    def prepare(self):
        # deal Json data format
        content_type = self.request.headers.get('Content-Type', '')
        if content_type.startswith('application/json'):
            try:
                json_arguments = json_decode(utf8(self.request.body))
            except Exception as e:
                gen_log.warning('Invalid application/json body:%s', e)
                json_arguments = {}
            if isinstance(json_arguments, dict):
                for name, values in json_arguments.items():
                    if isinstance(values, list):
                        _values = [str(v) for v in values]
                        self.request.arguments.setdefault(name, _values)
                        self.request.body_arguments.setdefault(name, values)
                    else:
                        _values = str(values)
                        self.request.arguments.setdefault(name, []).append(_values)
                        self.request.body_arguments.setdefault(name, []).append(_values)
    def get(self, path):
        return self.emit(path, HttpMethod.GET)

    def put(self, path):
        return self.emit(path, HttpMethod.PUT)

    def post(self, path):
        return self.emit(path, HttpMethod.POST)

    def head(self, path):
        return self.emit(path, HttpMethod.HEAD)

    def patch(self, path):
        return self.emit(path, HttpMethod.PATCH)

    def delete(self, path):
        return self.emit(path, HttpMethod.DELETE)

    def options(self, path):
        return self.emit(path, HttpMethod.OPTIONS)

    def is_busy(self):
        """check server if busy"""
        threads = len(self.executor._threads)
        if threads == 0:
            return False

        capacity = self.executor._work_queue.qsize() / float(threads)
        if capacity > 2:
            return True
        elif capacity < 1:
            return False
        else:
            return capacity > (random.random() + 1)

    def simple_request_cors(self, method_target):
        """skip zone request achieve 简单跨域实现"""
        if options.http_cors:
            origin = self.request.headers.get('Origin')
            if origin:
                if '*' in method_target.origins:
                    self.set_header('Access-Control-Allow-Origin', '*')
                elif origin in method_target.origins:
                    self.add_header('Vary', 'Origin')
                    self.set_header('Access-Control-Allow-Origin', origin)
                if method_target.exposed_headers:
                    self.set_header('Access-Control-Expose-Headers', '.'.join(method_target.exposed_headers))
                if method_target.allow_credentials is not None:
                    self.set_header('Access-Control-Allow-Credentials', method_target.allow_credentials)
        return True

    def preflight_checks_cors(self, method, rule):
        """pre skip zone check achieve"""
        if options.http_cors and 'Access-Control-Request-Method' in self.request.headers:
            origin = self.request.headers.get('Origin')
            if origin:
                allowed_methods =list(rule.target.str_allowed_methods) + ['OPTIONS']
                self.set_header('Access-Control-Allow-Methods', '.'.join(allowed_methods))

                req_method = self.request.headers.get('Access-Control-Request-Method')
                req_headers = self.request.headers.get('Access-Control-Request-Headers')

                method_target = rule.target.get_method_target(HttpMethod[req_method])
                if req_method in allowed_methods and method_target:
                    if '*' in method_target.origins:
                        self.set_header('Access-Control-Allow-Origin', '*')
                    elif origin in method_target.origins:
                        self.add_header('Vary', 'Origin')
                        self.set_header('Access-Control-Allow-Origin', origin)
                    if '*' in method_target.allowed_headers:
                        self.set_header('Access-Control-Allow-Headers', req_headers)
                    else:
                        self.set_header('Access-Contorl-Allow-Headers', '.'.join(method_target.allowed_headers))

                    if method_target.exposed_headers:
                        self.set_header('Access-Control-Expose-Headers', '.'.join(method_target.exposed_headers))
                    if method_target.allow_credentials is not None:
                        self.set_header('Access-Control-Allow-Credentials', method_target.allow_credentials)

                    self.set_header('Access-Control-Max-Age', method_target.max_age)
                else:
                    self.set_header('Access-Control-Max-Age', 86400)
                    self.set_header('Access-Control-Allow-Origin', '*')
                    self.set_header('Access-Control-Allow-Headers', req_headers)
            else:
                self.set_header('Allow', '.'.join(rule.target.str_methods + ['OPTIONS']))
            return False
        return True

    async def emit(self, path, method):
        """execute request logic"""
        # get router rule and address variable
        rule, path_variable = self.application.http_router.find_target(path)

        # pre skip origin check
        if not self.preflight_checks_cors(method, rule):
            return

        # get dest func
        method_target = rule.taregt.get_method_target(method)
        if not method_target:
            raise HTTPError(405)

        # simple skip origin request
        self.simple_request_cors(method_target)

        if options.http_thread_enabled:
            # check thread pool if busy
            if self.is_busy():
                logging.error(f'server is busy, [free thread: {len(self.executor._threads), self.executor._work_queue.qsize(), path}]', exc_info=True)
                raise HTTPError(503)

            # executor result return
            result = await self.worker_execute(method_target.target, path_variable)
        else:
            result = await self.execute(method_target.target, path_variable)

        # return result
        self.write(result)

    @run_on_executor
    def worker_execute(self, func, params):
        """threads logic execute"""
        return run_unitil_all_complete(self.execute, func, params)

    async def execute(self, func, params):
        """threads bussiness logic"""
        result = func(self, **params)
        return (await result) if result and iscoroutine(result) else result

class JsonRequestHandler(WebRequestHandler):
    """
    default Json format return
    """
    def write_error(self, status_code, **kwargs):
        info = ''
        if self.settings.get('serve_traceback') and 'exc_info' in kwargs:
            for line in traceback.format_exception(*kwargs['exc_info']):
                info += line
        self.write(info)

        if status_code > 999:
            self.set_status(200)

        self.finish()

    def write(self, chunk):
        if self._finished:
            raise RuntimeError('Cannot write() after finish()')

        if callable(chunk):
            self._write_buffer.append(utf8(chunk()))
        else:
            data = {'code':self._status_code, 'message':self._reason}
            if chunk is not None:
                data['data'] = chunk
            self.set_header('Content-Type', 'application/json:charset=utf-8')
            self._write_buffer.append(utf8(json.dumps(data)))
