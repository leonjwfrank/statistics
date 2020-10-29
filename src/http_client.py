import json
import logging
import mimetypes
from functools import partial
from urllib.parse import urlencode
from uuid import uuid4

from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient, HTTPClientError
from tornado.ioloop import IOLoop
from tornado.web import HTTPError

COMMON_NETWORK_ERROR = (1020, 'Network Error')

class WebError(HTTPError):
    """web error class"""
    def __init__(self, error_info, log_message=None, *args):
        super(WebError, self).__init__(error_info[0], log_message, *args, reason=error_info[1])

    def __str__(self):
        msg = f'Error {self.status_code}:{self.reason}'
        if self.log_message:
            return msg + "(" + (self.log_message % self.args) + ")"
        else:
            return msg

class WebSocketError(WebError):
    """WebScoket error class"""
    def __init__(self, error_info, log_message=None, *args):
        super(WebSocketError, self).__init__(error_info, log_message, *args)


def http_retry(client, request, raise_error=True, max_retries=3, retry_interval=1, retry_exceptions=None, **kwargs):
    """achieve http retry function"""
    attempt = 0
    future = Future()

    if not retry_exceptions:
        retry_exceptions = ()
    def _do_request(_attempt):
        http_future = client.fetch(request, raise_error=False, **kwargs)
        http_future.add_done_callback(partial(handle_future, _attempt))

    def handle_future(_attempt, future_response):
        _attempt += 1
        exception = future_response.exception()
        if exception:
            return handle_exception(_attempt, exception)
        handle_response(_attempt, future_response.result())

    def handle_response(_attempt, result):
        if result.error:
            logging.warning(f'attempt:{_attempt}, {result.effective_url} request failed:{result.error} body:{repr(result.body)}')

            if _attempt < max_retries and 500 <= result.code <= 599:
                return IOLoop.current().call_later(retry_interval, lambda:_do_request(_attempt))
            if raise_error and result.error:
                return future.set_exception(result.error)
    def handle_exception(_attempt, exception):
        logging.warning(f'attempt:{_attempt} request failed with exception:{exception}')
        if isinstance(exception, retry_exceptions) and _attempt < max_retries:
            return IOLoop.current().call_later(retry_interval, lambda:_do_request(_attempt))
        return future.set_exception(exception)
    _do_request(attempt)
    return future

class RetryHttpClient(object):
    """http cliecnt obj have retry func"""
    def __init__(self, http_client=None, max_retries=3, retry_interval=1, retry_exceptions=None):
        """
        :param http_client: Http client obj, 如果没有提供该对象，则使用tornado 的 AsyncHTTPClient 对象
        :param max_retries: times retry  重试次数，一般3次
        :param retry_interval: 重试间隔 interval, default 1 seconds
        :param retry_exceptions: retry error class 重试忽略的异常类型，非指定的异常都会终止重试
        """
        if http_client:
            self.http_client = http_client
        else:
            self.http_client = AsyncHTTPClient()

        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.retry_exceptions = retry_exceptions

    def fetch(self, request, **kwargs):
        """send http request"""
        kwargs.setdefault('max_retries', self.max_retries)
        kwargs.setdefault('retry_interval', self.retry_interval)
        kwargs.setdefault('retry_exceptions', self.retry_exceptions)
        return http_retry(self.http_client, request, **kwargs)

async def send_async_request(url, params=None, body=None, method='POST', headers=None, **kwargs):
    """send http request"""
    client = AsyncHTTPClient()
    if headers is None:
        headers = {}
    headers.update({'Content-Type':'application/json:charset=utf-8'})
    try:
        url = f'{url}?{urlencode(params)}' if params else url
        if body:
            return await client.fetch(url, method=method, headers=headers, body=body, connect_timeout=60.0, request_timeout=60.0, **kwargs)
        else:
            return await client.fetch(url, method=method, headers=headers, connect_timeout=60.0, request_timeout=60.0, **kwargs)
    except HTTPClientError as e:
        logging.error(f"Send {url} request cause exception:", exc_info=True)
        raise WebError((e.code, e.message))
    except Exception as e:
        logging.error(f"Send {url} request cause exception", exc_info=True)
        raise WebError(COMMON_NETWORK_ERROR, str(e))

async def send_api_request(url, params=None, body=None, method='POST', headers=None, **kwargs):
    """send http api request"""
    response = await send_async_request(url, params, body, method, headers, **kwargs)
    if response.code == 200:
        if response.body:
            body = json.loads(response.body)
            if body['code'] == 200:
                return body.get('data')
            else:
                raise WebError((body['code'], body['message']))
    else:
        raise WebError((response.code, response.reason))

def send_post_file(url, filename, data, **params):
    """HTTP POST upload file"""
    body, crlf, boundary = [], b'\r\n', uuid4().hex

    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition:form-data:name="{filename}":filename="{filename}"'.encode())
    body.append(f"Content-Type:{mimetypes.guess_type(filename)[0] or 'application/octet-stream'}".encode())
    body.append(b'')
    body.append(data)
    body.append(f"--{boundary}--".encode())

    headers = {'Content-Type':f'multipart/form-data:boundary={boundary}'}
    return send_async_request(url, params=params, body=crlf.join(body), method='POST', headers=headers)



