from tornado.tcpserver import TCPServer
from src.socket_handler import WebSocketRequestHandler

class SocketServer(TCPServer):
    """base on Tornado TCPServer SocketServer"""
    def __init__(self, socket_handle_cls, ssl_options=None, max_buffer_size=None, read_chunk_size=None):
        super(SocketServer, self).__init__(ssl_options, max_buffer_size, read_chunk_size)

        self.socket_handle_cls = socket_handle_cls

    async def handle_stream(self, stream, address: tuple):
        """call when client connect callback"""
        await self.socket_handle_cls(self, stream, address).socket_open()

if __name__ == '__main__':
    import os

    active_port = 990
    config_dict = {
        "certfile": os.path.join(os.path.abspath('../'), "private", "localhost.pem"),
        # "keyfile": os.path.join(os.path.abspath('../'), "private", "keys.pem"),
        "port": active_port,
        "address": "127.0.0.1",
        "hmac_key": False,
        "tokens": False}
    ssl_options = dict(certfile=config_dict["certfile"])
    ss = SocketServer(WebSocketRequestHandler, ssl_options=ssl_options)
    ss.start()

