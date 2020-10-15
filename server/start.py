# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import hmac
import os
import urllib.parse
import urllib.request
import urllib
import time
import logging as logger
# from logger import *
import ssl

listeners, names, tokens, names_obj = {}, {}, {}, {}

class DistributeHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, params):
       print(f"receive ws request:{self.request.remote_ip}, params info:{params}, protocol:{self.get_websocket_protocol().__dict__}")
       self.deal_func(params)
    def deal_func(self, params):
        group, token, name = params.split('/')
        print(f"recive group:{group}, token:{token}, name:{name}")
        self.group = group or 'default'
        self.token = token or 'none'
        self.name = name or 'anonymous'

        logger.info(self.group)

        logger.info(self.token)

        logger.info(self.name)

        # only authorized parties can join
        if DistributeHandler.tokens:
            if not self.token in tokens or not token[self.token] is None:
                self.close()
            else:
                tokens[self.token] = self
        if not self.group in listeners:
            logger.info("new group build")
            listeners[self.group] = []
        # notify clients that a member has joined the groups
        establish_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        logger.info(listeners.get(self.group, []))
        if len(listeners.get(self.group, [])) < 1:
            logger.info("the first in the group")
            names_obj[self.name] = self
            listeners[self.group].append(self)
            self.write_message('%s\tCurrent users in the group: %s' % (establish_time, ",".join(names_obj.keys())))
            self.write_message(
                "%s\tCurrnet group user number : %s" % (establish_time, str(len(listeners.get(self.group, [])))))
            # add new user to the group list

        else:
            if self.name not in names_obj:
                # inform new connection user
                logger.info("add name")
                names_obj[self.name] = self
                listeners[self.group].append(self)
                # inform online users
                for client in listeners.get(self.group, []):
                    logger.info("selfname :")
                    logger.info(self.name)
                    client.write_message(
                        '%s\tCurrent users in all accounts: %s' % (establish_time, ",".join(names_obj.keys())))
                    client.write_message("%s\tCurrnet account user number : %s" % (
                        establish_time, str(len(listeners.get(self.group, [])))))
                    client.write_message(f"protocol ws now is:{client.get_websocket_protocol()}")
                    # client send
                    # client.send()
            else:
                logger.info("name existed")
                self.write_message('%s\tUser already logged in!' % establish_time)
                names_obj[self.name].write_message(
                    '%s\tAnother client is trying to login with your id!' % establish_time)

        logger.info(listeners.get(self.group, []))
        logger.info(names_obj)
        logger.info('%s:CONNECT to %s' % (time.time(), self.group))

    def on_message(self, message):
        logger.info(message)

    def on_close(self):
        if self.group in listeners:
            listeners[self.group].remove(self)
        del names_obj[self.name]
        # notify clients that a member has left the groups
        # WEBSOCKET_SERVER_URL = 'https://127.0.0.1:%s' % WEBSOCKET_PORT
        current_account_user_num = str(len(listeners.get(self.group, [])))
        disconnect_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for client in listeners.get(self.group, []):
            client.write_message('%s\tConnection established by %s disconnected' % (disconnect_time, self.name))
            client.write_message("'%s\tCurrnet account user number : %s" % (disconnect_time, current_account_user_num))
        logger.info('%s:DISCONNECT from %s' % (time.time(), self.group))


if __name__ == "__main__":
    """
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)   #   PROTOCOL_TLS_SERVER
    # localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
    localhost_pem = os.path.join(os.path.abspath('.'), "private", "localhost.pem")
    ssl_context.load_cert_chain(localhost_pem)
    """
    usage = __doc__
    version = ""
    active_port = 80
    config_dict = {
                    "certfile": os.path.join(os.path.abspath('../'), "private", "localhost.pem"),
                   # "keyfile": os.path.join(os.path.abspath('../'), "private", "keys.pem"),
                   "port": active_port,
                   "address": "127.0.0.1",
                   "hmac_key": False,
                   "tokens": False}
    urls = [
        (r'/realtime/(.*)', DistributeHandler)]  # /(.*)
    application = tornado.web.Application(urls, auto_reload=True)
    ssl_options = dict(certfile=config_dict["certfile"])  # , keyfile=config_dict["keyfile"]
    http_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_options)   # , ssl_options=ssl_options
    http_server.listen(int(config_dict["port"]), address=config_dict["address"])
    DistributeHandler.tokens = config_dict["hmac_key"]
    print(f"wss server start at:{active_port}")
    tornado.ioloop.IOLoop.instance().start()
