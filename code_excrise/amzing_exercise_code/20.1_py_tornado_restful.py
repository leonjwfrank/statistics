"""
    基于tornado创建restful api
～～～～～～～～～～～～～～～
    @author:autocommsky@gmail.com

    Tornado Web框架使用Python编写RESTful API变得容易。
    Tornado是一个Python Web框架和异步网络库，由于其无阻塞的网络I/O而提供了出色的可伸缩性。它还极大地促进了快速构建RESTful API的便利。
    这些功能是Tornado的核心，因为它是友好的Web服务器的开源版本。
    这里展示如何使用最新的Tornado Web框架构建RESTful API，并说明如何利用其异步功能。
"""

"""
# 将URL模式映射到请求处理程序
要使用Tornado构建RESTful API，必须将URL模式映射到tornado.web.RequestHandler的子类，该子类会覆盖处理URL的HTTP请求的方法。
例如，如果要通过同步操作处理HTTP GET请求，则必须创建tornado.web.RequestHandler的新子类并定义get（）方法。然后，您在tornado.web.Application中映射URL模式。

1显示了一个非常简单的RESTful API，该API声明了tornado.web.RequestHandler的两个子类，这些子类定义了get方法：VersionHandler和GetGameByIdHandler
"""

# A simple RESTful API in Tornado
import tornado.gen
import tornado.httpclient
from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web

"""
该代码很容易理解。它创建一个名为application的tornado.web.Application实例，其中包含构成Web应用程序的请求处理程序的集合。
该代码将元组列表传递给Application构造函数。该列表由正则表达式（regexp）和tornado.web.RequestHandler子类（request_class）组成。 
application.listen方法使用在指定端口上定义的规则为应用程序构建HTTP服务器。在这种情况下，代码使用默认的8888端口。
然后，对tornado.ioloop.IOLoop.instance().start()的调用将启动使用application.listen创建的服务器。

当Web应用程序接收到请求时，Tornado遍历该列表并创建第一个tornado.web.RequestHandler子类的实例，该子类的关联正则表达式与请求路径匹配，
然后调用head(),get(),post(),delete(),patch(),put()或options()方法以及基于HTTP请求的新实例的相应参数。

"""


class VersionHandler(tornado.web.RequestHandler):
    """
    RequestHandler 子类1
    """

    def get(self):
        """
        最简单的情况是VersionHandler.get方法，该方法仅将self作为参数接收，因为URL模式不包含任何参数。
        该方法创建一个响应字典，然后使用response作为参数调用self.write方法。
        self.write方法将接收到的块写入输出缓冲区。因为块（响应）是一个字典，所以self.write将其写为JSON并将响应的Content-Type设置为application / json。
        以下几行显示了GET的示例响应
        :return:
        http://localhost:8889/version and the response headers:
        {"last_build": "2019-08-08", "version": "6.x"
        Date: Thu, 08 Aug 2019 19:45:04 GMT
        Etag: "d733ae69693feb59f735e29bc6b93770afe1684f"
        Content-Type: application/json; charset=UTF-8
        Server: TornadoServer/6.1
        Content-Length: 48</p>
        """
        response = {'version': '6.x', 'last_build': date.today().isoformat()}
        # application/json
        self.write(response)

        # text/plain
        """
        如果要发送具有不同Content-Type的数据，则可以使用“ Content-Type”作为响应头名称和所需的值来调用self.set_header。
        调用self.write之后必须调用self.set_header，如下所示。它在新版本的VersionHandler类中将Content-Type设置为text / plain，而不是默认的application / json。
        tornado将所有标头值编码为UTF-8。
        """
        # self.write("version: 6.x, last_build:" + date.today().isoformat())
        # self.set_header("Content-Type", "text/plain")
        """
        Server: TornadoServer/6.x
        Content-Type: text/plain
        Etag: "c305b564aa650a7d5ae34901e278664d2dc81f37"
        Content-Length: 38
        Date: Fri, 09 Aug 2013 02:50:48 GMT
        """


class GetGameByIdHandler(tornado.web.RequestHandler):
    """
    RequestHandler 子类2
    Overriding the initialize() method.
    """

    def initialize(self, common_string):
        self.common_string = common_string

    def get(self, id):
        """
        GetGameByIdHandler.get方法接收两个参数：self和id。该方法创建一个响应字典，其中包含为id参数接收的整数值，然后调用带有响应作为参数的self.write方法。
        该示例不包含对id参数的任何验证，以使代码尽可能简单，因为专注于get方法的工作方式。假设您已经知道如何在Python中执行验证。
        以下各行显示了GET http//localhost:8889/getgamebyid/600 的示例响应以及响应标头：
        :param id:
        :return:
        {"id": 600, "name": "Crazy Game", "release_date": "2019-12-27"}
        Content-Length: 63
        Server: TornadoServer/6.x
        Content-Type: application/json; charset=UTF-8
        Etag: "489191987742a29dd10c9c8e90c085bd07a22f0e"
        Date: Fri, 09 Aug 2019 03:17:34 GMT
        """
        response = {'id': int(id),
                    'name': 'Crazy Game',
                    'release_date': date.today().isoformat(),
                    'common_string': self.common_string}
        self.write(response)
        """
        如果需要设置其他请求参数，例如标头和正文数据，则可以通过self.request访问它们。
        此变量是tornado.httpserver.HTTPRequest实例，该实例提供有关HTTP请求的所有信息。
        HTTPRequest类在httpserver.py中定义。
        """


"""
例如，表1显示了一些与前面的代码中定义的正则表达式匹配的HTTP请求。
以上两个Api 类分类实现的功能如下
HTTP verb and request URL                       | Tuple(regexp, request_class)that matches the request path路径匹配      |  RequestHandler subclass and method that is called
GET http://localhost:8888/getgamebyid/500       |       (r"/getgamebyid/([0-9]+)", GetGameByIdHandler)                  | GetGameByIdHandler.get
GET http://localhost:8888/version               |       (r"/version", VersionHandler)                                   | VersionHandler.get

"""

"""
回调，阅读和理解拆分回调为不同方法的代码有多么困难。 Tornado提供了一个基于生成器的接口（tornado.gen），使您可以在单个生成器中的处理程序中编写异步代码。

您只需要在必需的方法中将@tornado.gen.coroutine装饰器用于异步生成器，而无需添加@tornado.web.asynchronous装饰器。
方法3显示了tornado.web.RequestHandler的新子类，并使用@tornado.gen.coroutine装饰器定义了get（）方法。
您需要添加两个导入，以将代码添加到上一个清单中：导入tornado.gen和导入tornado.httpclient。

因为我添加了RequestHandler的新子类，所以有必要在tornado.Web.Application中映射URL模式。清单4显示了将/getfullpage URL映射到GetFullPageAsyncHandler的新代码。
"""


class GetFullPageAsyncHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        """
            GetFullPageAsyncHandler.get方法创建一个tornado.httpclient.AsyncHTTPClient实例（http_client），该实例表示一个非阻塞HTTP客户端。
            然后，代码调用此实例的http_client.fetch方法以异步执行请求。 fetch方法返回一个Future，其结果是HTTPResponse，如果请求返回的响应代码不是200，则引发HTTPError。
            该代码使用yield关键字从fetch方法返回的Future中检索HTTPResponse。

            调用以异步执行方式从http://127.0.0.1:8889/version检索Web开发页面。当获取操作以等于200的成功响应代码完成执行时，
            http_response将是一个HTTPRequest实例，其中包含在http_response.body中检索到的HTML页面的内容。该方法在调用fetch之后的行中继续执行。
            使用@tornado.gen.coroutine装饰器在get方法中需要执行的所有代码，并且不必担心为on_fetch编写回调。
            下一行将响应正文解码为字符串，并将“最新的高级内容”替换为“最新的内容”。
            然后，代码调用self.write方法来写入修改后的字符串，并将响应的Content-Type设置为application / html。

        """
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_response = yield http_client.fetch("http://127.0.0.1:8889/version")
        response = http_response.body.decode().replace(
            "Most Recent Premium Content", "Most Recent Content")
        self.write(response)
        self.set_header("Content-Type", "text/html")
        # self.set_header("Content-Type", "application/json")

        """
        
        以下是等效的代码，它使用@tornado.web.asynchronous装饰器而不是@tornado.gen.coroutine。在这种情况下，有必要定义on_fetch方法作为http_client.fetch方法的回调。
        因此，代码被分为两种方法。
        当fetch方法完成对内容的检索时，它将执行on_fetch中的代码。由于get方法使用@ tornado.web.asynchronous，因此您有责任调用self.finish（）完成HTTP请求。
        因此，on_fetch方法在调用self.write和self.set_header之后，在最后一行调用self_finish。如您所见，使用@tornado.gen.coroutine装饰器要容易得多。
        @tornado.web.asynchronous
        def get(self):
            http_client = tornado.httpclient.AsyncHTTPClient()
            http_client.fetch("http://127.0.0.1:8889/version", callback=self.on_fetch)
 
        def on_fetch(self, http_response):
            if http_response.error: raise tornado.web.HTTPError(500)
            response = http_response.body.decode().replace("Most Recent Premium Content", "Most Recent Content")
            self.write(response)
            self.set_header("Content-Type", "text/html")
        """


class ErrorHandler(tornado.web.RequestHandler):
    """
    此类显示了ErrorHandler请求处理程序的代码，该代码演示了三种不同机制在处理程序方法中返回错误的最简单用法。
    同时需要添加此类的映射到 application中

    如果error_code等于1，则get方法将调用self.set_status，该方法将设置响应的状态码。也可以指定一个原因字符串作为第二个参数。
    如果error_code等于2，则get方法调用self.send_error，它将指定的HTTP错误代码发送到浏览器。
    其他任何error_code值都会使get方法引发带有500状态代码的tornado.web.HTTPError异常。

    三种返回错误的机制将返回默认错误页面，您可以通过覆盖RequestHandler子类中的write_error方法来更改默认页面。
    """

    def get(self, error_code):
        if error_code == 1:
            self.set_status(status_code=500, reason="Server Internal Error.")
        elif error_code == 2:
            self.send_error(500)
        else:
            raise tornado.web.HTTPError(500)


"""
了解Tornado如何与RequestHandler子类一起工作
RequestHandler类使用以下代码定义SUPPORTED_METHODS类变量。如果需要对不同方法的支持，则需要在RequestHandler子类中重写SUPPORTED_METHODS类变量：
SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
head()，get()，post()，delete()，patch()，put()和options()方法的默认代码是引发HTTPError的一行。6 以下显示了get方法的代码：

def get(self, *args, **kwargs):
    raise HTTPError(405)
    
只要Web应用程序收到请求并匹配URL模式，Tornado就会执行以下操作：
    1，它创建RequestHandler子类的新实例，该实例已映射到URL模式。
    2，它使用在应用程序配置中指定的关键字参数调用initialize方法。您可以覆盖initialize方法，以将参数保存到成员变量中。
    3，无论HTTP请求如何，Tornado都会调用prepare方法。如果调用finish或send_error，Tornado将不会调用任何其他方法。
        您可以覆盖prepare方法来执行任何HTTP请求所需的代码，然后将特定代码写入head（），get（），post（），delete（），patch（），put（）或options（ ） 方法。
    4，它根据HTTP请求调用该方法，并使用基于捕获了不同组的URL正则表达式的参数作为参数。如您所知，您必须重写您希望RequestHandler子类能够处理的方法。
        例如，如果存在HTTP GET请求，则Tornado将使用不同的参数调用get方法。
    5，如果处理程序是同步的，根据HTTP请求返回，Tornado将在调用前一个方法之后调用on_finish。
    但是，如果处理程序是异步的，则在代码调用完成后，Tornado将执行on_finish。前面的异步示例显示了finish的用法。您可以重写on_finish方法以执行清理或日志记录。
    请注意，Tornado在将响应发送到客户端之后调用on_finish。
    
如果客户端在异步处理程序中关闭连接，则Tornado会调用on_connection_close。在此特定方案中，您可以重写此方法以清理资源。但是，必须在on_finish方法中包含处理请求后的清除。

清单7显示了一个新版本的GetGameByIdHandler类，该类重写了initialize方法，以接收在应用程序配置中指定的字符串。
initialize方法只是将common_string保存到一个成员变量中，然后get方法在响应中使用该字符串：
"""
# Mapping a URL to a handler.
# 以下代码显示传递给tornado.web.Application构造函数的参数的更改，以在GetGameByIdHandler请求处理程序的字典中传递common_string的值:
# 在这个Case下，我使用了一个简单的字符串作为从应用程序传递的值。但是，最常见的用法是传递一个或多个公共对象(例如，数据库对象).
#
application = tornado.web.Application([
    (r"/getfullpage", GetFullPageAsyncHandler),
    (r"/getgamebyid/([0-9]+)", GetGameByIdHandler, dict(common_string='Value defined in Application')),
    (r"/version", VersionHandler),
    (r"/error/([0-9]+)", ErrorHandler),   # 映射 错误处理类
])

if __name__ == "__main__":
    port = 8889
    application.listen(port)
    print(f'web server start on port:{port}')
    tornado.ioloop.IOLoop.instance().start()
