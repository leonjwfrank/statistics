import unittest
import sys
import time
from datetime import datetime
import cart as zy_cart
from base_log import ServiceLog

log_oper = ServiceLog(log_name='test_log_{}_{}_{}.log'.format(datetime.now().year, datetime.now().month,
                                                     datetime.now().day))
log_write = log_oper.logger_writer('{}'.format(datetime.now().day))


class CartCaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        log_write.info('start for test cart')
        pass

    def setUp(self):
        log_write.info('start for case')
        self.cart = zy_cart.Cart()
        time.sleep(1)
        self.t0 = time.time()

    def test_cart_add(self):
        """test define cart_sum_num("""
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))
        # is empty add before
        self.assertEqual(self.cart.content, {})
        vodka = zy_cart.Products.Vodka()

        # after add is not empty
        self.cart.update(vodka)
        self.assertNotEqual(self.cart.content, {})
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))

    def test_cart_sum_num(self):
        """test define cart_sum_num("""
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))

        displays = zy_cart.Products.Displayer()
        displays.numbers = 1
        disp_info = displays.displayer_info
        log_write.debug('display:{}, {}'.format(displays, disp_info))
        log_write.info('{} * {}  {:.2f}'.format(displays.numbers, displays.cn_name, displays.price))

        # add things to cart
        self.cart.update(displays)

        # cart add succ
        self.assertEqual(float(self.cart.get_num_items()), 1.00)
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))
        pass

    def test_cart_sum_price(self):
        """test define cart_sum_price"""
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))

        displays = zy_cart.Products.Displayer()
        displays.numbers = 1
        disp_info = displays.displayer_info
        log_write.debug('display:{}, {}'.format(displays, disp_info))
        log_write.info('{} * {}  {:.2f}'.format(displays.numbers, displays.cn_name, displays.price))

        # add things to cart
        self.cart.update(displays)

        # cart add succ
        self.assertEqual(float(self.cart.get_total()), 1799.00)
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))
        pass

    def test_cart_del(self):
        """test define cart remove func"""
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))

        displays = zy_cart.Products.Displayer()
        displays.numbers = 1
        disp_info = displays.displayer_info
        log_write.debug('display:{}, {}'.format(displays, disp_info))
        log_write.info('{} * {}  {:.2f}'.format(displays.numbers, displays.cn_name, displays.price))

        # add things to cart
        self.cart.update(displays)

        # cart add succ
        self.assertNotEqual(float(self.cart.get_total()), 0.00)

        # clear cart
        self.cart.remove_item(displays.unq_id)

        # cart clear succ
        self.assertEqual(float(self.cart.get_total()), 0.00)
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))
        pass

    def test_cart_clear(self):
        """test cart clear func """
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))

        displays = zy_cart.Products.Displayer()
        displays.numbers = 1
        disp_info = displays.displayer_info
        log_write.debug('display:{}, {}'.format(displays, disp_info))
        log_write.info('{} * {}  {:.2f}'.format(displays.numbers, displays.cn_name, displays.price))

        # add things to cart
        self.cart.update(displays)

        # cart add succ
        self.assertNotEqual(float(self.cart.get_total()), 0.00)

        # clear cart
        self.cart.clear_all()

        # cart clear succ
        self.assertEqual(float(self.cart.get_total()), 0.00)
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))

    def test_coupon_availe(self):
        """test define time available coupon"""
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))
        # define coupon available
        cp1000_ava = zy_cart.CouponTotal(date='2021-01-28 12:28:23')

        # choose products
        displays = zy_cart.Products.Displayer()
        displays.numbers = 1
        disp_info = displays.displayer_info
        log_write.debug('display:{}, {}'.format(displays, disp_info))
        log_write.info('{} * {}  {:.2f}'.format(displays.numbers, displays.cn_name, displays.price))

        # add products
        self.cart.update(displays)

        # use coupon before price
        self.assertEqual(float(self.cart.get_total()), 1799.00)

        sr1_va = zy_cart.summary_result(cart=self.cart, coupon=cp1000_ava)
        reduce_price = sr1_va.ret_sum_product_price()

        # use coupon after price not change
        self.assertEqual(float(reduce_price), 1599.00)
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))

    def test_coupon_invaild(self):
        """test define invaild timeout coupon"""
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))
        cp1000_inv = zy_cart.CouponTotal(date='2011-01-28 12:28:23')
        displays = zy_cart.Products.Displayer()
        displays.numbers = 1
        disp_info = displays.displayer_info
        log_write.debug('display:{}, {}'.format(displays, disp_info))
        log_write.info('{} * {}  {:.2f}'.format(displays.numbers, displays.cn_name, displays.price))
        self.cart.update(displays)

        # use coupon before price
        self.assertEqual(float(self.cart.get_total()), 1799.00)

        sr1_va = zy_cart.summary_result(cart=self.cart, coupon=cp1000_inv)
        reduce_price = sr1_va.ret_sum_product_price()

        # use coupon after price not change
        self.assertEqual(float(reduce_price), 1799.00)
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))

    def test_cart_with_ava_coupon(self):
        """test cart and summary with available coupon"""
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))
        ipads = zy_cart.Products.Ipad()
        ipads.numbers = 1
        ipads_info = ipads.ipad_info
        log_write.debug('ipads:{}, {}'.format(ipads, ipads_info))
        log_write.info('{} * {}  {:.2f}'.format(ipads.numbers, ipads.cn_name, ipads.price))

        displays = zy_cart.Products.Displayer()
        displays.numbers = 1
        disp_info = displays.displayer_info
        log_write.debug('display:{}, {}'.format(displays, disp_info))
        log_write.info('{} * {}  {:.2f}'.format(displays.numbers, displays.cn_name, displays.price))

        Beers = zy_cart.Products.Beer()
        Beers.numbers = 12
        Beers_info = Beers.beer_info
        log_write.debug('Beers:{}, {}'.format(Beers, Beers_info))
        log_write.info('{} * {}  {:.2f}'.format(Beers.numbers, Beers.cn_name, Beers.price))

        Breads = zy_cart.Products.Bread()
        Breads.numbers = 5
        Breads_info = Breads.bread_info
        log_write.debug('Beers:{}, {}'.format(Breads, Breads_info))
        log_write.info('{} * {}  {:.2f}'.format(Breads.numbers, Breads.cn_name, Breads.price))
        log_write.info('cart total price1: {}'.format(self.cart.get_total()))
        self.cart.update(ipads)
        self.cart.update(displays)
        self.cart.update(Beers)
        self.cart.update(Breads)
        log_write.debug('cart:{},{},{}'.format(self.cart.content, self.cart.ret_things, self.cart.get_num_items()))
        log_write.info('cart total price: {}'.format(self.cart.get_total()))

        # assert used coupon before
        self.assertEqual(float(self.cart.get_total()), 4543.00)

        cp1000 = zy_cart.CouponTotal(date='2019-08-28 12:28:23')
        sr1 = zy_cart.summary_result(cart=self.cart, coupon=cp1000)

        reduce_price = sr1.ret_sum_product_price()
        log_write.info("购物车包含{} 个物品，总共价格 {} 元, 使用优惠券后{}元".format(self.cart.get_num_items(), self.cart.get_total(), reduce_price))
        # assert used the coupon after
        self.assertEqual(float(reduce_price), 4343.00)
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))

    def test_cart_with_invaild_coupon(self):
        """"test cart with invaild coupon"""
        log_write.info('Start test Case: {}'.format(sys._getframe().f_code.co_name))
        vag = zy_cart.Products.Vegetable()
        vag.numbers = 3
        vag_info = vag.vegetable_info
        log_write.debug('Beers:{}, {}'.format(vag, vag_info))
        log_write.info('{} * {}  {:.2f}'.format(vag.numbers, vag.cn_name, vag.price))

        napkin = zy_cart.Products.Napkin()
        napkin.numbers = 8
        napkin_info = napkin.napkin_info
        log_write.debug('Beers:{}, {}'.format(napkin, napkin_info))
        log_write.info('{} * {}  {:.2f}'.format(napkin.numbers, napkin.cn_name, napkin.price))

        # 定义过期券
        cp1000_invaild = zy_cart.CouponTotal(date='2014-01-28 12:28:23')

        self.cart.update(vag)
        self.cart.update(napkin)
        sr2 = zy_cart.summary_result(cart=self.cart, coupon=cp1000_invaild)
        sr2.ret_sum_product_price()
        log_write.info('completed test {} success'.format(sys._getframe().f_code.co_name))

    def tearDown(self):
        log_write.info('test end for case, cost time:{}'.format(time.time() - self.t0))
        self.cart.clear_all()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        log_write.info('completed test for cart')
        pass


if __name__ == '__main__':
    unittest.main()