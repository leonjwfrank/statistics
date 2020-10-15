# py 工厂模式实现, 通过一个入口创建多个类
from abc import ABCMeta, abstractmethod


# case one:
class Employee(metaclass=ABCMeta):
    """An employ class, base on abstract base class（抽象基类）"""

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    @abstractmethod
    def get_role(self):
        print(f"name:{self.name}, age:{self.age}, gender:{self.gender}")

    def __str__(self):
        return f"{self.__class__.__name__} - {self.name}, {self.age} years old {self.gender} gender"


class Engineer(Employee):
    """An Engineer Employee"""

    def get_role(self):
        return "engineering"


class SoftwareEngineer(Employee):
    """An Software Engineer"""

    def get_role(self):
        return 'SoftwareEngineer'


class Accountant(Employee):
    """An accountant employee"""

    def get_role(self):
        return "accountant"


class Admin(Employee):
    """An Admin Employee"""

    def get_role(self):
        return "administration"


# case two:
class EmployeeFactory(object):
    """An employee factory class
    工厂类通过一个入口创建多个类
    特征：通常使用一个工厂类关联整个类家族，类及子类的层次结构
    """

    @classmethod
    def create(cls, type_name, *args):
        """Factory method for creating an Employee instance
        特征: 工厂类的方法通常为 classmethod声明，这样可以通过类的命名空间直接调用，不用创建实例
        如EmployeeFactory.create('engineer', 'Sam', 25, 'M')
        """
        name = type_name.lower().strip()
        if name == 'engineer':
            return Engineer(*args)
        elif name == 'SoftwareEngineer':
            return SoftwareEngineer(*args)
        elif name == 'admin':
            return Admin(*args)
        elif name == 'accountant':
            return Accountant(*args)


if __name__ == '__main__':
    # case 1
    admin = Admin('jack', 18, 5)
    print(admin.get_role())
    print(admin)
    try:
        print(Employee('jack', 19, 6))   # 抽象基类禁止实例化
    except TypeError as te:
        print(te)
    print(Accountant('Lucy', 22, 4))   # 基于抽象基类的子类可以实例化
    # case 2
    print(EmployeeFactory().create('SoftwareEngineer', 'jack', 24, 'M'))
    print(EmployeeFactory.create('engineer', 'Sam', 25, 'F'))
