# 6, 代理模式
"""
# 代理重视实现代理对象的接口
1, 需要一个更接近客户的虚拟资源的时候，它可以替代另一个网络中的实际资源，如远程代理
2，需要监控对资源的访问时，如网络代理和实例计数代理
3，需要保护资源或对象（保护代理），因为直接访问资源将导致安全问题或危机资源，例如反向代理服务
4，需要从开销大的计算或网络操作中优化对结果的访问，以便不必每次都指向计算，如缓存代理

"""

from abc import ABCMeta, abstractmethod

class Employee(metaclass=ABCMeta):
    """An Employee class"""
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    @abstractmethod
    def get_role(self):
        """"""
        print(f"abc class get role.")

    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}, {self.age} years old {self.gender}"

class Engineer(Employee):
    """An Engineer Employee"""
    def get_role(self):
        return "engineering"

class Admin(Employee):
    """An admin Employee"""
    def get_role(self):
        return "administrator"

class Accountant(Employee):
    """An Accountant Employee"""
    def get_role(self):
        return "accounting"


# agent class
class EmployeeProxy(object):
    """Counting proxy class for Employees 实现一个组合对象代理，包装目标对象"""
    # Count of employees
    count = 0

    def __new__(cls, *args, **kwargs):
        """Overloaded __new__"""
        # To keep track of counts
        instance = object.__new__(cls)
        cls.incr_count()  # 实例计数
        return instance

    def __init__(self, employee):
        self.employee = employee

    @classmethod
    def incr_count(cls):
        """Increment employee count"""
        print(f"{cls.__class__.__name__} + count")
        cls.count += 1

    @classmethod
    def decr_count(cls):
        """Get employee count"""
        print(f"{cls.__class__.__name__} 代理计数，- 引用的 类计数")
        cls.count -= 1

    @classmethod
    def get_count(cls):
        """Get employee count"""
        print(f"{cls.__class__.__name__}  代理计数，返回引用的类计数")
        return cls.count

    def __str__(self):
        return str(self.employee)

    def __getattr__(self, item):
        """Redirect attributes to employee instance 重定向对象访问权"""
        return getattr(self.employee, item)

    def __del__(self):
        """Overloaded __del__ method"""
        # Decrement employee count
        self.decr_count()  # 实例计数

class EmployeeProxyFactory(object):
    """An Employee factory class returning proxy objects"""
    @classmethod
    def create(cls, name, *args):
        """Factory method for creating an Employee instance"""
        name = name.lower().strip()
        if name == 'engineer':
            return EmployeeProxy(Engineer(*args))
        elif name =='accountant':
            return EmployeeProxy(Accountant(*args))
        elif name == 'admin':
            return EmployeeProxy(Admin(*args))


if __name__ == '__main__':
    engineer = EmployeeProxyFactory.create('engineer', 'jack', 19, 2)
    print(engineer.get_count())
    print(EmployeeProxy.get_count())
    del engineer
    print(EmployeeProxy.get_count())

    e_lis = {i:f"e-{i}" for i in range(5)}
    for i, v in e_lis.items():
        e_lis[i] = EmployeeProxyFactory.create('engineer', f'jack-{i}', 19 +i, 0+i)
        # engineer2 = EmployeeProxyFactory.create('engineer', f'jack-{2}', 19 +2, 0+2)
        # engineer3 = EmployeeProxyFactory.create('engineer', f'jack-{3}', 19 +3, 0+3)

    print(EmployeeProxy.get_count())
    print(e_lis)
    for it, v in e_lis.items():
        print(f"NO.{it}, its:{v}")
