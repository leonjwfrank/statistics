"""
cart example
    ~~~~~

    A microcart based on python36 example.
    and follows best practice patterns.

    :copyright: ©ydxue
    :author: ydxue
    :contact: autocommsky@gmail.com

for example cart coupon

This example showcases the product add，remove.

```python36 base
"""

from datetime import datetime
from product import Products
from base_log import ServiceLog

log_oper = ServiceLog(log_name='{}_{}_{}.log'.format(datetime.now().year, datetime.now().month,
                                                     datetime.now().day))
log_write = log_oper.logger_writer('{}'.format(datetime.now().day))


class Coupon(object):
    def __init__(self, cp_id, reduct_total, reduct_num):
        self.cp_id = cp_id
        self.reduct_total = reduct_total
        self.reduct_num = reduct_num

    @staticmethod
    def total_reduce(total, reduct_total=None, reduct_num=None):
        """  :param reduct_total:
             :param reduction [1000 ,200]
             :param total 2301
             :return total after reduce if condition"""
        return (float(total) - float(reduct_num)) if float(total) >= float(reduct_total) else total


class TimeHander(object):
    @staticmethod
    def format_date_type(date_str=None):
        """if 2019-01-25 00:04:01.292 ret 2019-01-25 00:04:01.292000 :return"""
        if date_str is None:
            return str(datetime.now())
        date_str = str(date_str)
        if '.' not in date_str:
            date_str = date_str + '.'
        if len(date_str) > 26:
            return str(date_str)[26:]
        if len(date_str) < 26:
            n = 26 - len(date_str)
            date_str += '0' * (n - 1)
            date_str = str(date_str) + '0'
        assert isinstance(datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f'), datetime) is True
        return date_str

    @staticmethod
    def ret_pot_date(date_str=None):
        str_date = TimeHander.format_date_type(date_str)
        pot_date = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S.%f')
        return "{}.{}.{}".format(pot_date.year, pot_date.month, pot_date.day)


class CouponTotal(Coupon):
    """total 1000 reduce 200，timeout invaild"""
    def __init__(self, date):
        """datetime """
        Coupon.__init__(self, cp_id=1, reduct_total=1000, reduct_num=200)
        date = TimeHander.format_date_type(date)
        self._availab_date = date

    def coupon_availab(self):
        """ ret datetime.datetime t1 reduce t0
        :return  the coupon availabilty if time early than now"""
        return datetime.now() < datetime.strptime(self._availab_date, '%Y-%m-%d %H:%M:%S.%f')

    def total_reduce(self, total, **kwargs):
        if self.coupon_availab():
            return '{:.2f}'.format(Coupon.total_reduce(total, self.reduct_total, self.reduct_num))
        else:
            return '{:.2f}'.format(float(total))

    @property
    def coupon_info(self):
        return {"cp_id": self.cp_id,
                "reduct_total": self.reduct_total,
                "reduct_num": self.reduct_num,
                "availab": self.coupon_availab()}

    @property
    def compare_date(self):
        return self._availab_date

    @property
    def pot_date(self):
        pot_date = TimeHander.ret_pot_date(self._availab_date)
        return "{}".format(pot_date)

    @compare_date.setter
    def compare_date(self, datetstr):
        datestr = TimeHander.format_date_type(datetstr)
        self._availab_date = datestr


class Cart(object):
    """add remove product in cart"""
    def __init__(self):
        self.content = dict()

    @property
    def ret_things(self):
        return self.content

    def update(self, item):
        if item.unq_id not in self.content:
            self.content.update({item.unq_id: item})
            return
        for k, v in self.content.get(item.unq_id).items():
            if k == 'unq_id':
                continue
            elif k == 'numbers':
                total_nums = v.numbers + item.numbers
                if total_nums:
                    v.numbers = total_nums
                    continue
                self.remove_item(k)
            else:
                v[k] = item[k]

    def get_total(self):
        return "{:.2f}".format(sum([v.price * v.numbers for _, v in self.content.items()]))

    def get_num_items(self):
        return sum([v.numbers for _, v in self.content.items()])

    def remove_item(self, key):
        self.content.pop(key)

    def clear_all(self):
        self.content.clear()


class SummaryResult(object):
    """checkout counter"""

    def __init__(self, cart=None, coupon=None):
        """summary price in coupon
            :param product_lis list make up of product object
            :param coupon object"""
        self.coupon = coupon
        self._cart = cart

    def sum_product(self):
        return self._cart

    def ret_sum_product_nums(self):
        return self._cart.get_num_items()

    def ret_sum_product_price(self):
        """if coupon display info and use, display blank if not"""
        if self.coupon and self.coupon.coupon_availab():
            log_write.info("{}.{}.{}".format(datetime.now().year, datetime.now().month, datetime.now().day))
            log_write.info("{} {} {}".format(self.coupon.pot_date, self.coupon.reduct_total, self.coupon.reduct_num))
            total_price = self.coupon.total_reduce(self._cart.get_total())
            log_write.info("{}".format(total_price))
        else:
            log_write.info("{}.{}.{}".format(datetime.now().year, datetime.now().month, datetime.now().day))
            log_write.info('')
            total_price = self._cart.get_total()
            log_write.info("{}".format(total_price))
        return total_price


if __name__ == '__main__':

    ipads = Products.Ipad()
    ipads.numbers = 1
    ipads_info = ipads.ipad_info
    log_write.info('{} * {}  {:.2f}'.format(ipads.numbers, ipads.cn_name, ipads.price))

    Beers = Products.Beer()
    Beers.numbers = 5
    Beers_info = Beers.beer_info
    # print('Beer', Beers, Beers_info)
    log_write.info('{} * {}  {:.2f}'.format(Beers.numbers, Beers.cn_name, Beers.price))

    cart = Cart()
    cart.update(ipads)
    cart.update(Beers)
    log_write.info('cart total price: {}'.format(cart.get_total()))

    cp1000 = CouponTotal(date='2019-08-28 12:28:23')
    sr1 = SummaryResult(cart=cart, coupon=cp1000)

    cou_price = sr1.ret_sum_product_price()

    log_write.info("购物车包含{} 个物品，总共价格 {} 元, 使用优惠券后{}元".format(cart.get_num_items(), cart.get_total(), cou_price))
    cart.remove_item('1_1_2012')
    log_write.info("购物车包含{} 个物品，总共价格 {} 元".format(cart.get_num_items(), cart.get_total()))
