import logging
import random
import struct
from src.socket_session import SocketSessionMgr
from abc import ABCMeta
from urllib import parse
from tornado.ioloop import IOLoop
from tornado.websocket import websocket_connect

from src.define_code import CloseCode


class SocketClient(object):
    """Socket client base class"""
    __metaclass__ = ABCMeta

    def __init__(self, uuid):
        self.uuid = uuid

    @property
    def id(self):
        """"""
        return self.uuid

    def send_msg(self, gameid, cmd, message, **kwargs):
        """send msg to server, binarry"""
        raise NotImplementedError()

    def send_proto(self, gameid, cmd, proto, **kwargs):
        """send data to server, protobuf"""
        raise NotImplementedError()

    def clode(self, code=None, reason=None):
        """disconnect with server"""
        raise NotImplementedError()

    def __eq__(self, other):
        return self.uuid == other.uuid


class WebSocketClient(SocketClient):
    """
    WebSocket client base class, auto connect when need
    """

    def __init__(self, uuid, url, query=None, on_message_callback=None):
        super(WebSocketClient, self).__init__(uuid)
        self.url = url
        self.query = query
        self._send_id = 0
        self._recv_id = 0

        self._buffer = bytearray()
        self._ws_connect = None
        self._on_message_callback = on_message_callback

    @property
    def connected(self):
        """return if the session connected"""
        return self._ws_connect is not None

    async def connect(self):
        """build server connect"""
        if not self.connected:
            if self.query:
                url = f'{self.url}?uuid={self.uuid}&{parse.urlencode(self.query)}'
            else:
                url = f'{self.url}?uuid={self.uuid}'
            self._ws_connect = await websocket_connect(url, on_message_callback=self._on_message)
            return self.connected
        return True

    def pack(self, gameid, cmd, message, *args, **kwargs):
        """pack protocol, length(4 bytes), number(2 bytes) Gameid(2 bytes) command(2 bytes), data(none standard)"""
        length = len(message)
        result = struct.pack(f'>iihh{length}s', length + 12, self._send_id, gameid, cmd, message)
        logging.debug('Pack seq[%s], gameid[%s], cmd[%s]', self._send_id, gameid, cmd)

        self._send_id += 1
        return result

    def unpack(self, data):
        """pack protocol, length(4 bytes) number(2 bytes) Gameid(2 bytes) commands(2 bytes) data(not standard)"""
        seq, gameid, cmd, message = struct.unpack(f'>ihh{len(data) - 8}s', data)
        logging.debug('Unpack seq[%s], gameid[%s], cmd[%s]', seq, gameid, cmd)

        if seq != self._recv_id:
            self.close(CloseCode.CLOSE_BY_CHECK_SEQUENCE)
        self._recv_id += 1
        return gameid, cmd, message

    async def send_msg(self, gameid, cmd, message, **kwargs):
        """send data to server, data barri"""
        data = self.pack(gameid, cmd, message, **kwargs)
        if self.connected:
            return await self._ws_connect.write_message(data, binary=True)
        else:
            if await self.connect():
                return await self._ws_connect.write_message(data, binary=True)

    def send_proto(self, gameid, cmd, proto, **kwargs):
        """send data to server, protobuf"""
        return self.send_msg(gameid, cmd.value, proto.SerializeToString(), **kwargs)

    def close(self, code=None, reason=None):
        """disconnect from server"""
        if self.connected:
            self._ws_connect.closed(code, reason)

    def on_message(self, msg=None):
        """receive msg from server, length(4 bytes) GameId(2 bytes) commands(2 bytes) data
        """
        if msg:
            self._buffer += msg
        buf_len = len(self._buffer)
        if buf_len > 4:
            msg_len, = struct.unpack('>i', self._buffer[0:4])
            if buf_len >= msg_len:
                data = self.unpack(self._buffer[4:msg_len])
                if self._on_message_callback:
                    self._on_message_callback(*data)
                self._buffer = self._buffer[msg_len:]
                self.on_message()

    def on_close(self):
        """callback when disconnect from server"""
        self._buffer.clear()
        self._ws_connect = None

    def _on_message(self, msg):
        """callback when receive msg"""
        if msg is None:
            self.on_close()
        else:
            self.on_message(msg)

    def __str__(self):
        return f'Client [uuid={self.uuid}, url={self.url}, query={self.query}]'


class GameWebSocketClient(WebSocketClient):
    """GameServer WebSocket cloent"""

    def __init__(self, uuid, url, query=None):
        super(GameWebSocketClient, self).__init__(uuid, url, query, self.dispatch)

    def pack(self, gameid, cmd, message, *args, **kwargs):
        """protocol pack, length(4 types) GameId(2bytes) data(non standard) playerid(22bytes)"""
        length = len(message)
        player = kwargs.get('player')
        logging.debug('Pack gameid[%s], cmd[%s], player[%s]', gameid, cmd, player)
        return struct.pack(f'>ihh{length}s22s', length + 30, gameid, cmd, message, player.encode())

    def unpack(self, data):
        """pack protocol, length(4bytes), GameId(2bytes), commands(2bytes), data(non standard) playerid(22bytes)"""
        gameid, cmd, message, player = struct.unpack(f'>hh{len(data) - 26}s22s', data)
        player = player.decode()
        logging.debug('Unpack gameid[%s], cmd[%s], player[%s]', gameid, cmd, player)
        return gameid, cmd, message, player

    @staticmethod
    def dispatch(gameid, cmd, message, player):
        """receive msg"""
        SocketSessionMgr.write_msg(gameid, cmd, message, player)


class WebSocketClientPool(SocketClient):
    """WebSocket client pools(Fixed size)"""

    def __init__(self, uuid, clientid, url, query=None, size=5, client_cls=GameWebSocketClient):
        super(WebSocketClientPool, self).__init__(uuid)
        self.size = size
        self.client_cls = client_cls
        self.clients = [client_cls(clientid, url, query) for _ in range(size)]

    def send_msg(self, gameid, cmd, message, **kwargs):
        """send msg to server ,data binary"""
        return random.choice(self.clients).send_msg(gameid, cmd, message, **kwargs)

    def send_proto(self, gameid, cmd, proto, **kwargs):
        """send msg to server, data protobuf"""
        return random.choice(self.clients).send_proto(gameid, cmd, proto, **kwargs)

    def close(self, code=None, reason=None):
        """disconnect from server"""
        for client in self.clients:
            client.close(code, reason)

    def __str__(self):
        return f"ClientPool [uuid={self.uuid}, size={self.size}, client_cls={self.client_cls}]"


class SocketClientMgr(object):
    """Socket client mgr"""
    CLIENTS = {}

    @staticmethod
    def get(uuid):
        """get client for specific ID"""
        return SocketClientMgr.CLIENTS.get(uuid)

    @staticmethod
    def is_exists(uuid):
        """judgement if client is exist"""
        return uuid in SocketClientMgr.CLIENTS

    @staticmethod
    def add(client):
        """add new clients"""
        SocketClientMgr.remove(client)
        SocketClientMgr.CLIENTS[client.id] = client

    @staticmethod
    def remove(client, code=None, reason=None):
        """remove client"""
        if client in SocketClientMgr.CLIENTS.values():
            client = SocketClientMgr.CLIENTS.pop(client.id)
            if client:
                client.close(code, reason)

    @staticmethod
    def send_msg(gameid, cmd, message, *ids, **kwargs):
        """send msg to server, data binary"""
        for uuid in ids:
            client = SocketClientMgr.CLIENTS.get(uuid)
            if client:
                IOLoop.current().spawn_callback(client.send_msg, gameid, cmd, message, **kwargs)

    @staticmethod
    def send_proto(gameid, cmd, proto, *ids, **kwargs):
        """send msg to server ,data protobuf"""
        for uuid in ids:
            client = SocketClientMgr.CLIENTS.get(uuid)
            if client:
                IOLoop.current().spawn_callback(client.send_proto, gameid, cmd, proto, **kwargs)

    @staticmethod
    def close(code=None, reason=None):
        """close all clients"""
        for client in SocketClientMgr.CLIENTS.values():
            client.close(code, reason)
