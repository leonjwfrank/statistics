import logging
from tornado.options import options
from tornado.web import Application
from application.socket import BasicSocketApplication
from src.define_code import CloseCode
# from http.http_router
from src.socket_session import SocketSessionMgr

# noinspection PyUnresolvedReferences
class WebApplication(BasicSocketApplication):
    """Tornado Web app base class"""
    def __init__(self):
        super(WebApplication, self).__init__()
        self.http_server=None
        self.web = Application(**{k:v for k,v in options.as_dict().items() if v is not None})
        self.web.http_router = HttpRouter()
        self.web.socket_router = self.socket_router
        self.web.socet_session_listener = self.socket_session_listener

    def http_handler(self, pattern):
        """Http dealer decorator"""
        def decorator(cls):
            self.add_http_handler(pattern, cls)
            return cls
        return decorator

    def add_http_handler(self, pattern, handler):
        """add rule dealer"""
        # 没开启http，不添加http处理程序
        if 'http_enabled' in options:
            from src.http_handler import WebRequestHandler
            if not options.http_enabled and issubclass(handler, WebRequestHandler):
                return
        # 没开启WebSocket, 不添加WebSocket处理器
        if 'websocket_enabled' in options:
            from src.socket_handler import BasicSocketHandler
            if not options.websocket_enabled and issubclass(handler, BasicSocketHandler):
                return
        self.web.default_router.rules[0].target.add_rules([pattern, handler])

    def url(self, url, method, cors=True, max_age=3600, origins=None, allowed_headers=None,
            exposed_headers=None, allow_credentials=True):
        """Http url mapping decorator
        :param cors 是否允许跨域
        :param max_age 跨域授权有效期
        :param origins 允许跨域主机
        :param allowed_headers: 允许跨域请求的头部信息
        :param exposed_headers 允许跨域响应的头部信息
        :param allow_credentials 是否允许保护认证信息"""
        origins = origins or {'*'}
        allowed_headers = allowed_headers or {'*'}
        exposed_headers = exposed_headers or set()

        def decorator(func):
            self.add_url_rule(str({'url':url}), url, method, func, cors, max_age, origins, allowed_headers, exposed_headers, allow_credentials)
            return func
        return decorator

    def add_url_rule(self, name, url, method, target, cors=True, max_age=3600, origins=None, allowed_headers=None, exposed_headers=None, allow_credentials=True):
        """add Http URL mapping
        :param name mapping rule name
        :param url URL 地址
        :param method 请求方式
        :param target mapping target func
        :param cors 是否允许跨域
        """
        origins = origins or {'*'}
        allowed_headers = allowed_headers or {'*'}
        exposed_headers = exposed_headers or set()
        self.web.http_router.add_rule(HttpRule(name, PathMatches(url), URLTarget(
            MethodTarget(method, target, cors, origins, max_age, allowed_headers, exposed_headers, allow_credentials)
        )))

    def init(self):
        """应用程序初始化"""
        super(WebApplication, self).init()
        if options.host_http_port and not self.http_server:
            for rule in self.web.default_router.rules:
                for r in rule.target.rules:
                    logging.debug(f'Http Lv1 router mapped [{r.matcher.regex.pattern}] on [{r.target}]')
            for rule in self.web.http_router.rules:
                logging.debug(f'Http Lv2 router mapped [{rule.name}] onto {rule.target}')
            if options.host_ssl:
                self.http_server = self.web.listen(options.host_http_port, xheaders=True, ssl_options={
                    'keyfile':options.host_ssl_key,
                    'certfile':options.host_ssl_cert
                })
            else:
                self.http_server = self.web.listen(options.host_http_port, xheaders=True)
            logging.info(f'Starting [{options.host_name}] http server listen on [{options.host_http_port}]')
    def close(self):
        """应用程序关闭, 第一阶段，关闭外部服务，可继续执行内部流程"""
        super(WebApplication, self).close()
        if self.http_server:
            SocketSessionMgr.close_all(CloseCode.CLOSE_BY_SERVER_SHUTDOWN)
            self.http_server.stop()
