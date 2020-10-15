# A simple RESTFul API in Tornado
import tornado.gen
import tornado.httpclient
from datetime import date
import tornado.ioloop
import tornado.web

class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version':'6.x', 'last_build':date.today().isoformat()}
        # application/json default
        self.write(response)

        # diff Content-Type data
        # self.write('version:6.x, last_build:' + date.today().isoformat())
        # self.set_header('Content-Type', 'text/plain')
        """
        Server:TornadoServer/6.xs
        Content-Type:text/plain
        """



class GetGameByIdHandler(tornado.web.RequestHandler):
    def initialize(self, common_string):
        self.common_string = common_string
    def get(self, id):
        response = {'id': int(id),
                    'name': 'Crazy Game',
                    'release_data': date.today().isoformat(),
                    'common_string':self.common_string}
        self.write(response)

class GetFullPageAsyncHandler(tornado.web.RequestHandler):
    def initialize(self, port):
        self.port = port

    @tornado.gen.coroutine
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_response = yield  http_client.fetch("http://127.0.0.1:{}/version".format(self.port))
        response = http_response.body.decode().replace('6.x', 'Version 6.01')
        self.write(response)
        self.set_header("Content-Type", 'application/json')

class ErrorHandler(tornado.web.RequestHandler):
    def get(self, error_code):
        if error_code == 1:
            self.set_status(status_code=500, reason='Server Internal Error.')
        elif error_code == 2:
            self.send_error(500)
        else:
            raise tornado.web.HTTPError(500)



def define_url(port):
    active_port = port
    application = tornado.web.Application([
        (r"/getfullpage", GetFullPageAsyncHandler, dict(active_port=active_port)),
        (r"/getgamebyid/[0-9]+", GetGameByIdHandler, dict(common_string='Value defined in Applicaiton')),
        (r"/version", VersionHandler),
        (r"/error/([0-9]+)", ErrorHandler),   # 映射错误类处理

    ])
    application.listen(active_port)


if __name__ == '__main__':
    define_url(8009)
    tornado.ioloop.IOLoop.instance().start()



