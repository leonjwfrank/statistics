import pickle
import uuid
from src.redisdb import redis_db

class SessionMixin(object):
    @property
    def session(self):
        """get Session obj"""
        if not hasattr(self, '__session'):
            setattr(self, '__session', HttpSession(self, name=self.get_session_name(), expires=self.get_session_expires()))
        return getattr(self, '__session')

    def get_session_name(self):
        """default Session name"""
        return 'sessionid'

    def get_session_expires(self):
        """default Session timeout(half an hour)"""
        return 1800
class HttpSession(object):
    """base on Redis done achieve"""
    def __init__(self, handler, **settings):
        self._id = None
        self._key = None
        self._is_dirty = False
        self._is_exist = False
        self.handler = handler
        self.settings = settings

        self._session = {}
        self.__init_session()

    def __init_session(self, is_new=False):
        """init session, if is_new=True , create a new Session, otherwise session if exist, if exist restore"""
        prefix = self.settings.get('name', 'sessionid')
        if is_new:
            self.__generate_session_id(prefix)
        else:
            self._id = self.handler.get_argument(prefix, None)
            if not self._id:
                self._id = self.handler.request.headers.get(prefix)
            if not self._id:
                self._id = self.handler.get_cookie(prefix)
            if self._id:
                self._key = f'{prefix}: {self._id}'
                data = redis_db.get(self._key)
                if data:
                    self._is_exist = True
                    self._is_dirty = True
                    self._session = pickle.loads(data)
            else:
                self.__generate_session_id(prefix)
    def __generate_session_id(self, prefix):
        """Sessionid generate"""
        self._id = str(uuid.uuid4())
        self._key = f'{prefix}:{self._id}'
        self.handler.set_cookie(prefix, self._id)

    @property
    def id(self):
        """return SessionId"""
        return self._id

    def invalidate(self):
        """del session, create new session"""
        redis_db.delete(self._key)
        self.__init_session(True)

    def delete(self, oid):
        """delete session data from Redis"""
        redis_db.delete(f"{self.settings.get('name', 'sessionid')}:{oid}")

    def get(self, key, default=None):
        """get session data"""
        return self._session.get(key, default)

    def set(self, key, value):
        """save data to session"""
        self._is_dirty = True
        self._session[key] = value

    def pop(self, key, default=None):
        """delete Session data """
        if key in self._session:
            self._is_dirty = True
            return self._session.pop(key)
        return default

    def clear(self):
        """clear session data"""
        if self._session:
            self._is_dirty = True
            self._session = {}

    def keys(self):
        """return session all data keys"""
        return self._session.keys()

    def iterkeys(self):
        """return session keys iter"""
        return iter(self._session)

    def flush(self):
        """synchronize session data to Redis from session"""
        if self._is_dirty:
            expires = self.settings.get('expores', 1800)
            redis_db.set(self._key, pickle.dumps(self._session), ex=expires, xx=self._is_exist)
    __iter__ = iterkeys
    __delitem__ = pop

    def __contains__(self, key):
        return key in self._session

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        value = self.get(key)
        if value:
            return value
        raise KeyError(f"{key} not found")