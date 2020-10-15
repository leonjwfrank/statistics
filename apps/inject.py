import importlib
import logging as logger
import os
import sys
from argparse import ArgumentError
from types import FunctionType

from injector import Injector
from application.base import BaseApplication
import os

class InjectApplication(BaseApplication):
    """support inject application"""
    def __init__(self):
        super(InjectApplication, self).__init__()
        self.injector = Injector()

    def install(self, module):
        self.injector.binder.install(module)
        logger.debug(f"inject.install_module:{module}, self_dict:{self.__dict__}")
        return module

    def bind(self, interface=None, scope=None):
        """binding decorator"""
        def decorator(target):
            if isinstance(target, FunctionType):
                if interface:
                    self.injector.binder.bind(interface, self.injector.call_with_injection(target), scope)
                else:
                    logger.warning(f"The bind target object is the function return value, the interface must specify")
            else:
                self.injector.binder.bind(interface or target, target, scope)
            return target
        logger.debug(f"inject:{self.injector} bind_interface:{interface}, scope:{scope}")
        return decorator

    def bind_map(self, interface, key=None, scope=None):
        if not isinstance(interface, dict):
            raise ArgumentError(interface, 'Interface type must be a subtype of dict')
        def decorator(target):
            if isinstance(target,FunctionType):
                if key:
                    self.injector.binder.multibind(interface, {key:self.injector.call_with_injection(target)}, scope)
                else:
                    logger.warning(f"The bind target object is the function return value, key must be specify")
            return target
        logger.debug(f"Inject.bind_map:interface:{interface}, key:{key}, scope:{scope}")
        return decorator
    def bind_list(self, interface, scope=None):
        """bind decorator"""
        if not isinstance(interface, list):
            raise ArgumentError(interface, "Interface type must be a subtype of list")

        def decorator(target):
            if isinstance(target, FunctionType):
                self.injector.binder.multibind(interface, [self.injector.call_with_injection(target)],scope)
            else:
                self.injector.binder.multibind(interface, [target], scope)
            return target
        logger.debug(f"inject bind_list:interface:{interface}, scope:{scope}")
        return decorator

    def bind_inherit(self, interface):
        """bind decorator dynamic inherit(继承). bind again after dynamic inherit"""
        def decorator(cls):
            inherit_cls = type(cls.__name__, (cls, self.injector.get(interface).__class__), {})
            self.bind(interface)(inherit_cls)
            return inherit_cls
        logger.debug(f"inject.bind_inherit.interface:{interface}")
        return decorator
    def call_start_callbacks(self):
        """execute callback func after start"""
        for callback in self._start_callbacks:
            self.injector.call_with_injection(callback.callback)
        logger.debug(f"inject.callback.after.start:{self._start_callbacks}")

    def call_shutdown_callbacks(self):
        """execute callback func before closed"""
        for callback in self._shutdown_callbacks:
            self.injector.call_with_injection(callback.callback)
        logger.debug(f"inject.callback.before.close:{self._shutdown_callbacks}")

    @staticmethod
    def import_modules(module_path, filterdir=(), filterfile=()):
        """load module file"""
        logger.debug(f"inject.import.module.path:{module_path}")
        _import_m = []
        for path, subdir, files in os.walk(module_path):
            logger.debug(f"module_path:{module_path}, iter path:{path}, subdir:{subdir}, file:{files}")
            skip = False
            curdir = os.path.normcase(path)
            for checkdir in filterdir:
                skip = True
                break
            if skip:
                continue
            for filename in files:
                if filename.endswith(('.py', 'pyc')) and not filename.startswith(tuple(filterfile)):
                    m = os.path.normcase(os.path.splitext(os.path.join(path, filename))[0]).replace(os.path.sep, '.')
                    logger.debug(f'not in sys_modules:{len(sys.modules)} load injector module file:{importlib.import_module(m)}')
                    _import_m.append(m)
            logger.debug(f"had imported:{_import_m} from path:{module_path}")




