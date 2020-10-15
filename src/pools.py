# 池化相关操作
class PooledObject(object):
    """可池化对象基类"""
    def init(self, *args, **kwargs):
        pass
    def activate(self, *args, **kwargs):
        """激活对象，对象被借出时调用"""
        pass

    def passivate(self,*args, **kwargs):
        """钝化对象，对象归还时调用"""
        pass
    def destroy(self, *args, **kwargs):
        """销毁对象"""
        pass

class ObjectPool(object):
    """对象池基类，提供所有对象的存取管理"""
    def __init__(self, provider, max_idle):
        """构造对象"""
        self._objects = []
        self._max_idle = max_idle
        self._provider = provider

    @property
    def max_idle(self):
        """最大空闲数，超过这个数量的对象归还时销毁"""
        return self._max_idle

    @property
    def provider(self):
        """对象池对象提供者"""
        return self._provider

    def borrow_object(self, *args, **kwargs):
        """对象池中借出"""
        if not self._objects:
            self.add_object()
        return self.provider.activate_object(self._objects.pop(), *args, **kwargs)

    def return_object(self, obj,*args, **kwargs):
        """对象归还到对象池"""
        if len(self._objects) < self.max_idle:
            self._objects.append(self.provider.passivate_object(obj, *args, **kwargs))
        else:
            self.provider.destroy_object(obj, *args, **kwargs)

    def add_object(self, *args, **kwargs):
        """创建一个新的对象到对象池"""
        self._objects.append(self.provider.make_object(*args, **kwargs))

class ObjectProvider(object):
    """对象提供者基类定义"""
    def make_object(self, *args, **kwargs):
        """创建对象"""
        pass

    def activate_object(self,obj,*args, **kwargs):
        """激活对象，借出时调用"""
        obj.activate(*args, **kwargs)
        return obj
    def passivate_object(self, obj, *args, **kwargs):
        obj.passivate(*args, **kwargs)
        return obj

    def destroy_object(self, obj, *args, **kwargs):
        """销毁对象，对象被销毁时调用"""
        obj.destroy(*args, **kwargs)
        del obj













