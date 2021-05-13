import sys
sys.path.append('.')
#from BaseProd import Electron, Food, DailyPro, Alcohol

class ClassItem(object):
    numbers = 1

    def __init__(self, unq_id, name, price, numbers):
        self.unq_id = unq_id
        self.product_name = name
        self.price = '{:.2f}'.format(price)
        self.numbers = numbers


class Electron(ClassItem):
    def __init__(self):
        """datetime """
        ClassItem.__init__(self, unq_id='1_1_1', name=None, price=1000, numbers=1)
        self.numbers = ClassItem.numbers

    @property
    def set_prices(self):
        return self.price

    @set_prices.setter
    def set_prices(self, value):
        self.price = value

    @property
    def number(self):
        return self.numbers

    @number.setter
    def number(self, numbers):
        self.numbers = numbers

    @property
    def price_sign_total(self):
        return "{:.2f}".format(self.number * self.set_prices)


class Food(Electron):
    def __init__(self):
        """datetime """
        ClassItem.__init__(self, unq_id='1_1_1', name=None, price=1000, numbers=1)
        self.numbers = ClassItem.numbers


class DailyPro(Electron):
    def __init__(self):
        """datetime """
        ClassItem.__init__(self, unq_id='1_1_1', name=None, price=1000, numbers=1)
        self.numbers = ClassItem.numbers


class Alcohol(Electron):
    def __init__(self):
        """datetime """
        ClassItem.__init__(self, unq_id='1_1_1', name=None, price=1000, numbers=1)
        self.numbers = ClassItem.numbers



class Ipad(Electron):

    @property
    def ipad_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '1_1_2012', 'product_name': 'ipad_2012', 'price': 2399})
        return pro_info

    @property
    def cn_name(self):
        return u'名称: 苹果平板电脑 型号: ipad_2012'


class Iphone(Electron):

    @property
    def iphone_2019_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '1_2_2012', 'product_name': 'iphone_2019', 'price': 5012})
        return pro_info

    @property
    def cn_name(self):
        return u'苹果手机 型号: iphone_2019'


class Displayer(Electron):

    @property
    def displayer_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '1_3_2012', 'product_name': 'displayer_2019', 'price': 1799})
        return pro_info

    @property
    def cn_name(self):
        return u'显示器 型号: displayer_2019'


class Laptop(Electron):

    @property
    def laptop_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '1_4_2012', 'product_name': 'laptop_2019', 'price': 6500})
        return pro_info

    @property
    def cn_name(self):
        return u'笔记本计算机 型号: laptop_2019'

class Keyboard(Electron):

    @property
    def keyboard_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '1_5_2012', 'product_name': 'keyboard_2019', 'price': 65})
        return pro_info

    @property
    def cn_name(self):
        return u'键盘 型号: keyboard_2019'

class Bread(Food):

    @property
    def bread_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '2_1_2019', 'product_name': 'bread_0722', 'price': 9})
        return pro_info

    @property
    def cn_name(self):
        return u'面包 型号: bread_0722'

class Cookie(Food):

    @property
    def cookie_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '2_2_2019', 'product_name': 'cookie_0722', 'price': 10})
        return pro_info

    @property
    def cn_name(self):
        return u'饼干 型号: cookie_0722'

class Cake(Food):

    @property
    def cake_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '2_3_2019', 'product_name': 'cake_0722', 'price': 12})
        return pro_info

    @property
    def cn_name(self):
        return u'蛋糕 型号: cake_0722'

class Beef(Food):

    @property
    def beef_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '2_4_2019', 'product_name': 'beef_0722', 'price': 25})
        return pro_info

    @property
    def cn_name(self):
        return u'牛肉 型号: beef_0722'

class Fish(Food):

    @property
    def fish_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '2_5_2019', 'product_name': 'fish_0722', 'price': 20})
        return pro_info

    @property
    def cn_name(self):
        return u'鱼 型号: fish_0722'

class Vegetable(Food):

    @property
    def vegetable_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '2_6_2019', 'product_name': 'vegetable_0722', 'price': 5.98})
        return pro_info

    @property
    def cn_name(self):
        return u'蔬菜 型号: vegetable_0722'

class Napkin(DailyPro):

    @property
    def napkin_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '3_1_2019', 'product_name': 'napkin_0722', 'price': 3.2})
        return pro_info

    @property
    def cn_name(self):
        return u'餐巾纸 型号: napkin_0722'

class StorageBox(DailyPro):

    @property
    def storage_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '3_2_2019', 'product_name': 'Storage_0722', 'price': 8})
        return pro_info

    @property
    def cn_name(self):
        return u'储物箱 型号: Storage_0722'


class CoffeeCup(DailyPro):

    @property
    def coffee_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '3_3_2019', 'product_name': 'Coffee_info_0722', 'price': 13})
        return pro_info

    @property
    def cn_name(self):
        return u'咖啡杯 型号: Coffee_info_0722'

class Umbrella(DailyPro):

    @property
    def umbrella_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '3_4_2019', 'product_name': 'umbrella_0722', 'price': 20})
        return pro_info

    @property
    def cn_name(self):
        return u'雨伞 型号: umbrella_0722'

class Beer(Alcohol):

    @property
    def beer_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '4_1_2019', 'product_name': 'Beer_0722', 'price': 25})
        return pro_info

    @property
    def cn_name(self):
        return u'啤酒 型号: Beer_0722'

class Wine(Alcohol):

    # @property
    def __str__(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '4_2_2019', 'product_name': 'wine_0722', 'price': 90})
        return pro_info

    @property
    def cn_name(self):
        return u'白酒 型号: wine_0722'

class Vodka(Alcohol):

    @property
    def vodka_info(self):
        pro_info = self.__dict__
        pro_info.update({'unq_id': '4_3_2019', 'product_name': 'vodka_0722', 'price': 70})
        return pro_info

    @property
    def cn_name(self):
        return u'伏特加 型号: vodka_0722'


if __name__ == '__main__':
    ipad = Ipad()
    ipad_info = ipad.ipad_info
    print('ipad_2012', ipad, ipad_info)
    ipad.number = 2
    ipad.price = 2312
    print('ipad_2012 after', ipad, ipad_info, ipad.price_sign_total)

    iphone = Iphone()
    iphone_info = iphone.iphone_2019_info
    print('iphone_2012', ipad, iphone_info)
    iphone.number = 1
    iphone.price = 5010


    print('iphone_2012 after', iphone, iphone_info, iphone.price_sign_total)