import logging as logger
import struct
from concurrent.futures.thread import ThreadPoolExecutor
from inspect import iscoroutine

from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.iostream import StreamClosedError
from tornado.options import options
from tornado.web import HTTPError
from tornado.websocket import WebSocketHandler

from src.define_code import CloseCode
from src.socket_session import SocketSession, SocketSessionMgr
from src.tornado_complete import run_unitil_all_complete

logger.basicConfig(level=logger.DEBUG,
                   format='[%(asctime)s] [%(filename)s:%(lineno)s] [%(levelname)s] [%(process)d] [%(funcName)s] [%(name)] %(message)s')

import os


class BasicSocketHandler(object):
    """Socket request deal base class"""
    executor = ThreadPoolExecutor(options.socket_thread_max_workers, 'socket_worker')

    def __init__(self):
        self.attrs = {}
        self.buffer = bytearray()
        self.uuid = None
        self.session = None
        self.send_id = 0
        self.recv_id = 0

    @property
    def socket_ip(self):
        """Socket ip address"""
        raise NotImplementedError()

    @property
    def socket_opened(self):
        """if Socket opened"""
        raise NotImplementedError()

    @property
    def socket_router(self):
        """Socket router"""
        raise NotImplementedError()

    @property
    def socket_session_listener(self):
        """Socket session listener"""
        raise NotImplementedError()

    def socket_write(self, data):
        """Socket send data"""
        logger.debug(f"socket_write:{data}, raise NotImplementedError")
        raise NotImplementedError()

    def socket_close(self, code=None, reason=None):
        """Socket closed"""
        raise NotImplementedError()

    def socket_login(self, uuid):
        """Socket login"""
        if uuid and not self.uuid:
            self.uuid = uuid
            self.create_session()

    def socket_on_close(self):
        if self.session:
            self.destroy_session()
        logger.debug("Socket %s closed", self.socket_ip)

    async def socket_on_message(self, buf=None):
        """Socket receive msg func"""
        if buf:
            self.buffer += buf
        buf_len = len(self.buffer)
        if buf_len > 4:
            msg_len, = struct.unpack('>i', self.buffer[0:4])
            if buf_len >= msg_len:
                if options.socket_thread_enabled:
                    await self.worker_execute(*self.unpack(self.buffer[4:msg_len]))
                else:
                    await self.execute(*self.unpack(self.buffer[4:msg_len]))
                self.buffer = self.buffer[msg_len:buf_len]
                await self.socket_on_message()

    @run_on_executor
    def worker_execute(self, gameid, cmd, message, *args):
        """execute callbacll cmd, thread deal"""
        return run_unitil_all_complete(self.execute, gameid, cmd, message)

    async def execute(self, gameid, cmd, message, *args):
        """exec cmd callback, threading"""
        try:
            if not self.cmd_filter(gameid, cmd, message, *args):
                rule, _ = self.socket_router.find_target(cmd)
                result = rule.target(self.session or self, gameid, cmd, message, *args)
                return (await result) if result and iscoroutine(result) else result
        except HTTPError as e:
            await self.write_err(e, gameid, cmd, message)
        except Exception:
            self.socket_session_listener.execute_exception_callback(self.session)

    def cmd_filter(self, gameid, cmd, message, *args):
        """command filter"""
        return False

    async def write_msg(self, gameid, cmd, message, **kwargs):
        """message return binary"""
        try:
            result = self.pack(gameid, cmd, message, **kwargs)
            return await self.socket_write(result)
        except Exception:
            self.socket_session_listener.execute_exception_callback(self.session)

    def write_proto(self, gameid, cmd, proto, **kwargs):
        """msg return protobuf"""
        logger.debug(f"proto_cmd:{cmd.value, cmd} proto_msg:{proto}")
        logger.debug(f"proto_cmd:{cmd.value, cmd} proto_msg:{type(proto), proto}")
        return self.write_msg(gameid, cmd.value, proto.SerializeToString(), **kwargs)

    def write_err(self, exception, gameid, cmd, message, *args):
        logger.debug(f"Socket error exception:{exception} with game:{gameid} at cmd:{cmd} ,msg:{message}")
        pass

    def create_session(self):
        """create session obj"""
        self.session = SocketSession(self, self.uuid)
        SocketSessionMgr.add(self.session)
        self.socket_session_listener.execute_open_callback(self.session)
        logger.debug(f"Session %s created.", self.session)
        logger.debug(f"online_counts:{SocketSessionMgr.online_counts}, Session:{SocketSessionMgr.SESSIONS}")
        self.online()
        for session in SocketSessionMgr.SESSIONS.values():
            logger.debug(f"session_player uuid:{session.id}, session_ip:{session.socket_ip}")

    def destroy_session(self):
        """rm session"""
        logger.debug(f"session {self.session} destroyed.")
        if self.session is SocketSessionMgr.get(self.session.id):
            self.offline()
            self.socket_session_listener.execute_close_callback(self.session)
            self.session = SocketSessionMgr.remove(self.session)

    def online(self):
        """online logic"""
        pass

    def offline(self):
        """offline logic"""

    def pack(self, gameid, cmd, message, **kwargs):
        """protocol pack"""
        length = len(message)
        result = struct.pack(f">iihh{length}s", length + 12, self.send_id, gameid, cmd, message)
        logger.debug(f"Pack[{self.socket_ip}], game_id[{gameid}], seq[{self.send_id}] cmd[{cmd}]")
        if cmd in [2010, 2019, 3009]:
            pass
        self.send_id += 1
        return result

    def unpack(self, data):
        seq, gameid, cmd, message = struct.unpack(f'>ihh{len(data) - 8}s', data)
        logger.debug('Unpack[%s] seq[%s], gameid[%s], cmd[%s]', self.socket_ip, seq, gameid, cmd)
        # seq check 序号检查
        if seq != self.recv_id:
            self.socket_close(CloseCode.CLOSE_BY_CHECK_SEQUENCE)
        self.recv_id += 1
        return gameid, cmd, message


class WebSocketRequestHandler(WebSocketHandler, BasicSocketHandler):
    """WebSocket request base class"""

    def __init__(self, application, request, **kwargs):
        super(WebSocketRequestHandler, self).__init__(application, request, **kwargs)

    @property
    def socket_ip(self):
        return self.request.remote_ip

    @property
    def socket_opened(self):
        """Socket if opened"""
        return bool(self.ws_connection)

    @property
    def socket_router(self):
        """socket router"""
        return self.application.socket_router

    @property
    def socket_session_listener(self):
        """Socket session listner"""
        return self.application.socket_session_listener

    def socket_close(self, code=None, reason=None):
        """Socket closed"""
        self.close(code, reason)

    async def socket_write(self, data):
        """Socket send data"""
        if self.socket_opened:
            await self.write_message(data, True)

    def check_origin(self, origin: str) -> bool:
        """默认允许跨域"""
        return True

    def open(self, *args, **kwargs):
        """Sockets connect deal func"""
        logger.debug(f"Socket {self.socket_ip}")
        self.socket_login(self.get_argument("uuid", None))

    def on_message(self, buf=None):
        """Socket接受消息处理函数"""
        return self.socket_on_message(buf)

    def on_close(self):
        """Socket 关闭处理函数"""
        self.socket_on_close()

    def ping(self, data=b''):
        """send ping cmd to client"""
        if self.uuid:
            super(WebSocketRequestHandler, self).ping(data)
        else:
            self.socket_close(CloseCode.CLOSE_BY_CHECK_TIMEOUT)


class SocketRequestHandler(BasicSocketHandler):
    """Socket request deal base class"""
    PING = 0x9
    PONG = 0xA
    CLOSE = 0x8

    def __init__(self, server, stream, address):
        super(SocketRequestHandler, self).__init__()
        self.last_ping = 0
        self.last_pong = 0
        self.ping_callback = None
        self._server = server
        self._stream = stream
        self._address = address

    @property
    def socket_ip(self):
        """Socket ip address"""
        return self._address

    @property
    def socket_opened(self):
        """Socket if opend?"""
        return not self._stream.closed()

    @property
    def socket_router(self):
        """Socket router"""
        return self._server.socket_router

    @property
    def socket_session_listener(self):
        """Socket session listner manager"""
        return self._server.socket_session_listener

    async def socket_open(self):
        """building Socket"""
        logger.debug(f"Socket {self.socket_ip}")
        self._stream.set_close_callback(self.socket_on_close)
        self.start_pinging()
        await self.socket_handle()

    def socket_close(self, code=None, reason=None):
        """close Socket send close reason first"""
        coroutine = self.write_msg(0, self.CLOSE, str(code).encode())
        task = IOLoop.current().asyncio_loop.create_task(coroutine)
        task.add_done_callback(self._stream.close)
        logger.debug(f"socket_close_code:{code, str(code).encode()}, reason:{reason}")

    async def socket_write(self, data):
        """Socket send data"""
        if self.socket_opened:
            await self._stream.write(data)

    async def socket_handle(self):
        """client connect deal"""
        while True:
            try:
                await self.socket_on_message(await self._stream.read_bytes(65535, partial=True))
            except StreamClosedError:
                break

    def cmd_filter(self, gameid, cmd, message, *args):
        """cmd filter"""
        # client send Ping cmd
        if cmd == self.PING:
            self.on_ping(message)
            return True

        # client answer Ping cmd
        if cmd == self.PONG:
            self.on_pong(message)
            return True
        return False

    @property
    def ping_interval(self):
        """Ping cmd call space time interval"""
        if 'websocket_ping_interval' in options:
            return options.websocket_ping_interva
        return 0

    @property
    def ping_timeout(self):
        """Ping cmd answer timeout time"""
        if 'websocket_ping_timeout' in options:
            return options.websocket_ping_timeout
        return max(3 * self.ping_interval, 30)

    def start_pinging(self):
        """start crontab send Ping cmd caller"""
        if self.ping_interval > 0:
            self.last_ping = self.last_pong = IOLoop.current().time()
            self.ping_callback = PeriodicCallback(self.periodic_ping, self.ping_interval * 1000)
            self.ping_callback.start()

    def periodic_ping(self):
        """call loop, send ping cmd"""
        if self._stream.closed() and self.ping_callback is not None:
            self.ping_callback.stop()
            return
        now = IOLoop.current().time()
        since_last_pong = now - self.last_pong
        since_last_ping = now - self.last_ping
        if since_last_ping < 2 * self.ping_interval and since_last_pong > self.ping_timeout:
            self.socket_close(CloseCode.CLOSE_BY_CHECK_TIMEOUT)
            return
        self.ping()
        self.last_ping = now

    def ping(self, data=b''):
        """send ping cmd to client"""
        if self.uuid:
            IOLoop.current().spawn_callback(self.write_msg, 0, self.PING, data)
        else:
            self.socket_close(CloseCode.CLOSE_BY_LOGIN_TIMEOUT)

    def on_ping(self, data):
        """receive Ping cmd func"""
        IOLoop.current().spawn_callback(self.write_msg, 0, self.PONG, data)

    def on_pong(self, data):
        """receive Pong cmd func"""
        self.last_pong = IOLoop.current().time()
