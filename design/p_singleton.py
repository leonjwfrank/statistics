# py 单例实现方法
class Singletion(object):
    """继承实现单例"""
    instances = {}

    # noinspection PyArgumentList
    def __new__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(Singletion, cls).__new__(cls, *args, **kwargs)
        return cls.instances[cls]


class SingletonMetaclass(type):
    """元注解实现单例"""

    def __init__(cls, name, bases=None, dic=None):
        super(SingletonMetaclass, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
        return cls.instance


def singleton(cls, *args, **kwargs):
    """类装饰器实现单例"""
    instances = {}

    def _get_instance():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _get_instance


if __name__ == '__main__':
    # @singleton
    class DemoSingle(Singletion):
        d = 'd1'
        def demo(self):
            print(f'demo:{self.d}')


    class_sing = DemoSingle()
    print(id(class_sing), print(class_sing.d))
    class_sing2 = DemoSingle()
    print(id(class_sing2), print(class_sing2.d))

    print(id(class_sing) == id(class_sing2))

    # type annotation
    import time
    class meta_class(metaclass=SingletonMetaclass):
        trys = 'ws_try'
        def __init__(self):
            self._meta = f"Meta - {time.time()}"
            # cls._meta = f'Meta-{time.time()}'
        @property
        def meta(self):
            return self._meta

        @meta.setter
        def meta(self, v):
            self._meta = v + str(time.time())

        def __str__(self):
            return f"<meta:{self._meta}, trys:{self.trys}>"


    mc = meta_class()
    mc.trys = 'Outs:Try'
    print(f"{id(mc)}, mc.meta:{mc.meta}")
    mc.meta = f"NewMeta" + str(time.time())
    print(f"{id(mc)}, mc.meta:{mc.meta}")

    mc2 = meta_class()
    print(mc.meta == mc2.meta)
    print(f"{id(mc2)}, mc2._meta:{mc2.meta}")
    mc2.meta = f"NewMeta2" + str(time.time())
    print(f"{id(mc2)}, _meta:{mc2.meta}")
    print(mc.meta == mc2.meta)


