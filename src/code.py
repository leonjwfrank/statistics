# test for python3 and gitlab CI/CD log
from enum import IntEnum, unique, Enum

@unique
class CloseCode(IntEnum):
    """scoket 关闭编码 tools.ietf.org/html/rfc6455#section-7.4"""
    CLOSE_BY_CHECK_PING = 4001  # hearbet
    CLOSE_BY_CHECK_ARGS = 4002   # login error
    CLOSE_BY_CHECK_VERSION = 4003  # update
    CLOSE_BY_CHECK_SEQUENCE = 4004  # request num
    CLOSE_BY_CHECK_DUPLICATE = 4005  # double connect
    CLOSE_BY_CHECK_TIMEOUT = 4006   # timeout to login
    CLOSE_BY_SERVER_SHUTDOWN = 4007  # server closed
    CLOSE_BY_LOGIN_TIMEOUT = 4008