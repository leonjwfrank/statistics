import weakref
from abc import ABCMeta
from tornado.ioloop import IOLoop
from src.define_code import CloseCode


class Session(object):
    """session base class"""
    __metaclass__ = ABCMeta

    def __init__(self, uuid):
        self.uuid = uuid

    @property
    def id(self):
        """session id
        """
        return self.uuid

    def write_msg(self, gameid, cmd, message, **kwargs):
        """send data, binarry"""
        raise NotImplementedError()

    def write_proto(self, gameid, cmd, proto, **kwargs):
        """send data, protobuf"""
        raise NotImplementedError()

    def close(self, code=None, rease=None):
        """close connect"""
        raise NotImplementedError()

    def __eq__(self, other):
        """

        """
        return self.uuid == other.uuid


class SocketSession(Session):
    """socket session object"""

    def __init__(self, socket, uuid):
        super(SocketSession, self).__init__(uuid)
        self.socket = weakref.proxy(socket)

    @property
    def socket_ip(self):
        """connect ip, torbado.web.request.remote_ip"""
        return self.socket.socket_ip

    @property
    def attrs(self):
        """connect attr"""
        return self.socket.attrs

    @property
    def opened(self):
        """if connection is opend?"""
        return self.socket and self.socket.socket_opened

    async def write_msg(self, gameid, cmd, message, **kwargs):
        """send msg, binnary"""
        if self.opened:
            return await self.socket.write_msg(gameid, cmd, message, **kwargs)

    async def write_proto(self, gameid, cmd, proto, **kwargs):
        """send msg, protobuf"""
        if self.opened:
            return await self.socket.write_proto(gameid, cmd, proto, **kwargs)

    def close(self, code=None, reason=None):
        """close connect"""
        if self.opened:
            self.socket.socket_close(code, reason)

    def __str__(self):
        return f"Session [uuid={self.uuid}, ip={self.socket_ip}, attrs={self.attrs}]"


class SocketSessionGroup(Session):
    """Socket session group object"""

    def __init__(self, uuid):
        super(SocketSessionGroup, self).__init__(uuid)
        self.sessions = []

    @property
    def counts(self):
        """session numbers"""
        return len(self.sessions)

    def add_session(self, session):
        """new session object"""
        self.sessions.append(session)

    def remove_session(self, session):
        """rm session object"""
        self.sessions.remove(session)

    async def write_msg(self, gameid, cmd, message, **kwargs):
        """send data, binarry"""
        for session in self.sessions:
            if session.opened:
                return await session.write_msg(gameid, cmd, message, **kwargs)

    async def write_proto(self, gameid, cmd, proto, **kwargs):
        """send msg, protobuf"""
        for session in self.sessions:
            if session.opened:
                return await session.write_proto(gameid, cmd, proto, **kwargs)

    def close(self, code=None, reason=None):
        """close connect"""
        for session in self.sessions:
            session.close(code, reason)
        self.sessions.clear()

    def __str__(self):
        """"""
        return f"SessionGroup [uuid={self.uuid}, sessions={self.counts}]"


class SocketSessionListener(object):
    """Socket session listener"""

    def __init__(self):
        self._open_callbacks = []
        self._close_callbacks = []
        self._exception_callbacks = []

    def add_open_callback(self, callback, key, reverse):
        """add Socket session callback func"""
        self._open_callbacks.append(callback)
        self._open_callbacks.sort(key=key, reverse=reverse)

    def execute_open_callback(self, session):
        """exec Socket session callback func"""
        for callback in self._open_callbacks:
            callback.callback(session)

    def add_close_callback(self, callback, key, reverse):
        """add the callback func when Socket session closed"""
        self._close_callbacks.append(callback)
        self._close_callbacks.sort(key=key, reverse=reverse)

    def execute_close_callback(self, session):
        """execute Socket session callback func when session closed"""
        for callback in self._close_callbacks:
            callback.callback(session)

    def add_exception_callback(self, callback, key, reverse):
        """add the callback func when Socket session error"""
        self._exception_callbacks.append(callback)
        self._exception_callbacks.sort(key=key, reverse=reverse)

    def execute_exception_callback(self, session):
        """execute socket session callback func when session error"""
        for callback in self._exception_callbacks:
            callback.callback(session)


class SocketSessionMgr(object):
    """Session manager"""
    SESSIONS = {}

    @staticmethod
    def get(uuid):
        """get the session ID"""
        return SocketSessionMgr.SESSIONS.get(uuid)

    @staticmethod
    def is_online(uuid):
        """judgement if online"""
        return uuid in SocketSessionMgr.SESSIONS

    @staticmethod
    def online_counts():
        """count total person online"""
        return len(SocketSessionMgr.SESSIONS)

    @staticmethod
    def add(session):
        """new session"""
        SocketSessionMgr.close(session.id.CloseCode.CLOSE_BY_CHECK_DUPLICATE)
        SocketSessionMgr.SESSIONS[session.id] = session

    @staticmethod
    def remove(session):
        """remove session"""
        if session in SocketSessionMgr.SESSIONS.values():
            existed = SocketSessionMgr.SESSIONS.get(session.id)
            if existed is session:
                SocketSessionMgr.SESSIONS.pop(session.id)

    @staticmethod
    def write_msg(gameid, cmd, message, *ids, **kwargs):
        for uuid in ids:
            session = SocketSessionMgr.SESSIONS.get(uuid)
            if session:
                IOLoop.current().spawn_callback(session.write_msg, gameid, cmd, message, **kwargs)

    @staticmethod
    def write_proto(gameid, cmd, proto, *ids, **kwargs):
        """send msg by group"""
        for uuid in ids:
            session = SocketSessionMgr.SESSIONS.get(uuid)
            if session:
                IOLoop.current().spawn_callback(session.write_proto, gameid, cmd, proto, **kwargs)

    @staticmethod
    def wirte_msg_all(gameid, cmd, message, **kwargs):
        """send msg by group"""
        for session in SocketSessionMgr.SESSIONS.values():
            IOLoop.current().spawn_callback(session.write_msg, gameid, cmd, message, **kwargs)

    @staticmethod
    def write_proto_all(gameid, cmd, proto, **kwargs):
        """send msg by proto group"""
        for session in SocketSessionMgr.SESSIONS.values():
            IOLoop.current().spawn_callback(session.write_proto, gameid, cmd, proto, **kwargs)

    @staticmethod
    def close(sessionid, code=None, reason=None):
        """close session"""
        if sessionid in SocketSessionMgr.SESSIONS:
            session = SocketSessionMgr.SESSIONS.pop(sessionid)
            if session:
                session.close(code, reason)

    @staticmethod
    def close_all(code=None, reason=None):
        """close all session(disconnect)"""
        for session in SocketSessionMgr.SESSIONS.values():
            session.close(code, reason)
        SocketSessionMgr.SESSIONS.clear()
