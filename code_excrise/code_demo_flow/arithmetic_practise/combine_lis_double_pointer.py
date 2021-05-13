"""
    合并列表 及测试用例
ordered list combine example  O(N), simple  sorted， list sort
    ~~~~~

    A micr combine list program based on python36 example.
    and follows best practice patterns.

    :copyright: ©ydxue
    :author: ydxue
    :contact: autocommsky@gmail.com

for example
    a=[1, 4, 4, 8, 64]
    b=[0, 2, 5, 6, 16, 21, 21, 24, 30]
    print(extent_lis(a, b))
        [0, 1, 2, 4, 4, 5, 6, 8, 16, 21, 21, 24, 30, 64]
This example showcases the order list combine.

```python36 base
"""

import unittest
import time
import random
import sys
import functools


def def_extent_lis(ext_a, ext_b):
    """使用python自带的方法进行合并和排序"""
    c = []
    c.extend(ext_a)
    c.extend(ext_b)
    c.sort()
    return c


def def_sorted(ext_a,ext_b):
    """sorted 两个列表相加,返回排序列表"""
    return sorted(ext_a + ext_b)


def extent_lis(ext_a, ext_b, def_ordered=True):
    """两个列表元素相互比较，并按升序添加到返回列表，算法复杂度最差 O(N), N为两个列表的长度之和
    扩展:如果有多个列表，调用此方法迭代求值。"""
    k, h = 0, 0   # k表示存入了第几个a列表元素，h表示存入第几个b列表元素
    c = []
    if not def_ordered:
        assert AssertionError('need two list is ordered！！')
    # 处理有空列表的场景
    if not ext_a and not ext_b:
        return c
    if not ext_a and ext_b:
        return ext_b
    if not ext_b and ext_a:
        return ext_a

    a = ext_a.copy()
    b = ext_b.copy()
    print(f'get two ordered list a:{a}, b:{b}')

    # 两个列表元素对比有三种情况，a列表元素大于b列表对于元素
    for i in range(len(a)):

        for j in range(h, len(b)):
            # print(f'1 now ai:{k, i, a[i]}, bj:{h, j, b[j]}, rst c: {c}')
            if a[i] < b[j]:
                c.append(a[i])   # b[j] 如果恰好是最后一个且是所有中最大的，可能会被遗漏无法添加到返回列表，在主循环体外进行处理
                k += 1
                break  # a列表指针 k移动
            if a[i] == b[j]:
                k += 1
                h += 1
                c.append(a[i])
                c.append(b[j])
                break  # a，b列表指针同时移动

            if a[i] > b[j]:
                c.append(b[j])
                # b.remove(b[j])  # 不能通过删除元素处理，这样会导致b列表数据遗漏
                h += 1
                continue  # b列表指针移动

        # 某个列表遍历完成，直接处理另一个列表
        if h == len(ext_b) and k == len(ext_a):
            print(f'终止ab循环添加，ext_b 已添加:{h} ext_a 已添加:{k}')
            break  # a,b 同时添加完成
        if h == len(ext_b):   # 如果b列表已经添加完成，但是a列表仍没 添加完成
            print(f'终止b添加，ext_b 已添加:{h} ext_a 已添加 {k}, 还剩:{a[k:]}')
            if a[k:]:  # 如果列表b已经遍历对比完成，但是a列表还有元素，因为a列表为有序列表，所以直接从a列表当前位置k切片，添加到返回列表即可
                c.extend(a[k:])
            break  # b列表添加完成
        elif k == len(ext_a):  # 如果a列表已经添加完成
            print(f'终止a添加，ext_a 已添加:{k} ext_b 已添加{h}, 还剩:{b[h:]}')
            if b[h:]:  # 如果列表a已经遍历对比完成，但是b列表还有元素，因为b列表为有序列表，所以直接从b列表当前位置h切片，添加到返回列表即可
                c.extend(b[h:])
            print(f'break c:{c} break b:{b}')
            break   # a列表添加完成
        else:
            continue  # a列表未完成遍历，继续移动指针执行遍历

    print(f'combine ai:{len(a), a}, bj:{len(b), b}, return list c: {c},len c:{len(c)}, assert len a+b=c:{len(a)+len(b)==len(c)}')

    return c


class ExtListTest(unittest.TestCase):
    """将函数转换为类方法。
    
            类方法将类作为隐式第一个参数接收，
             就像实例方法接收实例一样。
                要声明类方法，请使用以下惯用法：
    
                C级：
                 @classmethod
                 def f（cls，arg1，arg2，...）：
                     ...
    
            可以在类（例如C.f（））或实例上调用它
            （例如C（）。f（））。该实例除其类外均被忽略。
              如果为派生类调用类方法，则派生类
             对象作为隐式第一个参数传递。"""

    a_length=5
    b_length=8

    @classmethod
    def setUpClass(cls):
        cls.class_t0 = time.time()
        print('start test case' + '=='*20)

    @classmethod
    def tearDownClass(cls):
        cls.class_end = time.time()
        print('end test case' + '==' * 20)
        print('all case cost:{:15f}'.format(cls.class_end - cls.class_t0))

    def setUp(self):

        self.case_t0 = time.time()

    def tearDown(self):
        case_end = time.time()
        print('this case cost:{:15f}'.format(case_end - self.case_t0))

    @staticmethod
    def ret_really_random_lis(length=a_length, isFloat=True):
        """# 根据参数产生对应长度的 随机列表，列表元素大小限定在指定参数的2倍内"""
        if isFloat:
            random_lis = list(map(lambda x: x, [(random.randrange(10)+x/2) for x in range(10)]))
        else:
            random_lis = list(map(lambda x: x, [random.randrange(length) + x for x in range(length)]))
        return random_lis

    @staticmethod
    def ret_ordered_random_lis(length=a_length, isFloat=True):
        """有序地在 给定长度 length * length倍范围内，按随机间隔取 length 个数， 随机间隔长度 1～ length
        产生一个递增序列
        """
        ret_lis = []
        item_list = 0
        for i in range(length):
            item_list += random.randrange(length)
            ret_lis.append(item_list)
        # [random.randrange(length) for i in range(length)]
        return ret_lis

    def test_lists_length_equal(self):
        """相等长度的两个有序列表合并"""
        equal_lis_one1 = self.ret_ordered_random_lis(self.a_length)
        equal_lis_two2 = self.ret_ordered_random_lis(self.a_length)
        combine_lis = extent_lis(equal_lis_one1, equal_lis_two2)
        self.assertEqual(len(equal_lis_one1)+len(equal_lis_two2), len(combine_lis), msg="length check.")
        self.assertIsNot(combine_lis, [], msg=f"Check equal list is ok.equal_lis_one:{equal_lis_one1} \n, "
        f"equal_lis_two:{equal_lis_one1}, combine_lis:{combine_lis}")

    def test_lists_value_equal(self):
        """相等长度的两个有序列表合并"""
        equal_value_lis_one = self.ret_ordered_random_lis(self.a_length)
        equal_value_lis_two = equal_value_lis_one.copy()
        combine_lis = extent_lis(equal_value_lis_one, equal_value_lis_two)
        self.assertEqual(len(equal_value_lis_one)+len(equal_value_lis_two), len(combine_lis), msg="length check.")
        self.assertIsNot(combine_lis, [], msg=f"Check equal list is ok.equal_value_lis_one:{equal_value_lis_one} \n, "
        f"equal_lis_two:{equal_value_lis_one}, combine_lis:{combine_lis}")

    def test_lists_length_bigger_one(self):
        """第一个列表更长"""
        bigger_lis_one = self.ret_ordered_random_lis(self.b_length)
        bigger_lis_two = self.ret_ordered_random_lis(self.a_length)
        combine_bigger_one_lis = extent_lis(bigger_lis_one, bigger_lis_two)
        self.assertIsNot(combine_bigger_one_lis, [], msg="Check bigger one list is ok.")

    def test_lists_value_bigger_one(self):
        """第一个列表数据范围更大，覆盖第二列表"""
        bigger_lis_one = self.ret_ordered_random_lis(self.a_length)
        bigger_lis_one[1] = 0
        bigger_lis_one[-1] = self.a_length*self.a_length
        bigger_lis_two = self.ret_ordered_random_lis(self.a_length)
        combine_bigger_one_lis = extent_lis(bigger_lis_one, bigger_lis_two)
        self.assertIsNot(combine_bigger_one_lis, [], msg="Check bigger one list is ok.")

    def test_lists_bigger_two(self):
        """第二个列表更长"""
        bigger_two_one = self.ret_ordered_random_lis(self.a_length)
        bigger_two_two = self.ret_ordered_random_lis(self.b_length)
        combine_bigger_two_lis = extent_lis(bigger_two_one, bigger_two_two)
        self.assertIsNot(combine_bigger_two_lis, [], msg="Check bigger two list is ok.")

    def test_lists_bigger_two_same_end_value(self):
        """第二个列表更长,最后一个元素值相等"""
        bigger_two_one = self.ret_ordered_random_lis(self.a_length)
        bigger_two_two = self.ret_ordered_random_lis(self.b_length)
        bigger_two_one[-1] = bigger_two_two[-1]
        combine_bigger_two_lis = extent_lis(bigger_two_one, bigger_two_two)
        self.assertIsNot(combine_bigger_two_lis, [], msg="Check bigger two list is ok.")
        self.assertEqual(len(combine_bigger_two_lis), len(bigger_two_one)+len(bigger_two_two), msg="Check two list lenght is ok.")

    def test_lists_bigger_two_same_start_value(self):
        """第二个列表更长,起始和最后一个元素值相等"""
        bigger_two_one = self.ret_ordered_random_lis(self.a_length)
        bigger_two_two = self.ret_ordered_random_lis(self.b_length)
        bigger_two_one[-1] = bigger_two_two[-1]
        bigger_two_one[0] = bigger_two_two[0]
        combine_bigger_two_lis = extent_lis(bigger_two_one, bigger_two_two)
        self.assertIsNot(combine_bigger_two_lis, [], msg="Check bigger two list is ok.")
        self.assertEqual(len(combine_bigger_two_lis), len(bigger_two_one) + len(bigger_two_two),
                         msg="Check two list lenght is ok.")

    def test_lists_bigger_one_same_start_value(self):
        """第一个列表更长,起始和最后一个元素值相等"""
        bigger_two_one = self.ret_ordered_random_lis(self.a_length)
        bigger_two_two = self.ret_ordered_random_lis(self.b_length+self.a_length)
        bigger_two_one[-1] = bigger_two_two[-1]
        bigger_two_one[0] = bigger_two_two[0]
        bigger_two_two.extend([bigger_two_two[-1]] * 3)
        combine_bigger_two_lis = extent_lis(bigger_two_two, bigger_two_one)
        self.assertIsNot(combine_bigger_two_lis, [], msg="Check bigger two list is ok.")
        self.assertEqual(len(combine_bigger_two_lis), len(bigger_two_one) + len(bigger_two_two),
                         msg="Check two list lenght.")

    def test_lists_bigger_one_same_start_end_value(self):
        """第一个列表更长,起始和最后一个元素值相等"""
        bigger_two_one = self.ret_ordered_random_lis(self.a_length)
        bigger_two_two = self.ret_ordered_random_lis(self.b_length+self.a_length)
        bigger_two_one[-1] = bigger_two_two[-1]
        bigger_two_one[0] = bigger_two_two[0]
        bigger_two_two.extend([bigger_two_two[-1]] * 3)
        lis_two = [bigger_two_one[0]] * 4
        lis_two.extend(bigger_two_two)
        combine_bigger_two_lis = extent_lis(lis_two, bigger_two_one)
        self.assertIsNot(combine_bigger_two_lis, [], msg="Check bigger two list is ok.")
        self.assertEqual(len(combine_bigger_two_lis), len(bigger_two_one) + len(lis_two),
                         msg="Check two list lenght.")

    def test_lists_value_bigger_two(self):
        """第二个列表数据范围更大，覆盖第一个列表"""
        bigger_two_one = self.ret_ordered_random_lis(self.a_length)
        bigger_two_two = self.ret_ordered_random_lis(self.a_length)
        bigger_two_two[0] = 0
        bigger_two_two[-1] = self.a_length*self.a_length
        combine_bigger_two_lis = extent_lis(bigger_two_one, bigger_two_two)
        self.assertIsNot(combine_bigger_two_lis, [], msg="Check bigger two list is ok.")

    def test_lists_all_bigger_two(self):
        """第二个列表数据范围更大,长度更长，覆盖第一个列表"""
        bigger_two_one = self.ret_ordered_random_lis(self.a_length)
        bigger_two_two = self.ret_ordered_random_lis(self.b_length + self.a_length)
        bigger_two_two[0] = 0
        bigger_two_two[-1] = self.a_length*self.b_length
        combine_bigger_two_lis = extent_lis(bigger_two_one, bigger_two_two)
        self.assertIsNot(combine_bigger_two_lis, [], msg="Check bigger two list is ok.")

    def test_lists_length_bigger_two_value_bigger_one(self):
        """第一个列表数据范围更大,长度更长，覆盖第二个列表"""
        bigger_two_one = self.ret_ordered_random_lis(self.a_length)
        bigger_two_one[0] = 0
        bigger_two_one[-1] = self.b_length * self.b_length
        bigger_two_two = self.ret_ordered_random_lis(self.b_length)

        combine_bigger_two_lis = extent_lis(bigger_two_one, bigger_two_two)
        self.assertIsNot(combine_bigger_two_lis, [], msg="Check bigger two list is ok.")

    def test_lists_only_one(self):
        """仅有一个有序列表"""
        only_one = self.ret_ordered_random_lis(self.a_length)
        combine_only_one_lis = extent_lis(only_one, [])
        self.assertIsNot(combine_only_one_lis, [], msg="Check only one list is ok.")

    def test_two_empty_lists(self):
        """合并两个空列表"""
        combine_only_one_lis = extent_lis([], [])
        self.assertIsNot(combine_only_one_lis, [], msg="Check only one list is ok.")

    def combine_ordered_more_lists(self, more_list):
        """有三个有序列表需要合并"""
        if not more_list:
            raise AssertionError(f'length error:{len(more_list), more_list}')
        if len(more_list) == 1:
            return more_list[0]
        if len(more_list) >= 2:
            # print(f'now more list:{more_list}')
            bigger_three_one = more_list.pop(0)  # 无放回取出第一个
            bigger_three_two = more_list.pop(0)  # 无放回弹出第一个
            # bigger_three_two = self.ret_ordered_random_lis(self.b_length)
            bigger_three_two[0] = 0
            bigger_three_two[-1] = self.a_length * self.b_length
            combine_only_one_lis = extent_lis(bigger_three_one, bigger_three_two)

            more_list.insert(0, combine_only_one_lis)  # [0] =
            combine_only_one_lis = self.combine_ordered_more_lists(more_list)  # 递归直到 待递归列表为1

            return combine_only_one_lis

    def test_combine_three_ordered_lists(self):
        bigger_three_one = self.ret_ordered_random_lis(self.a_length)
        bigger_three_two = self.ret_ordered_random_lis(self.b_length)
        bigger_three_three = self.ret_ordered_random_lis(self.a_length + self.b_length)
        three_list = [bigger_three_one, bigger_three_two, bigger_three_three]
        combine_only_lis = self.combine_ordered_more_lists(three_list)
        self.assertIsNot(combine_only_lis, [], msg="Check only one list is ok.")

    def test_lists_martix(self):
        """三个以上有序数组合并，矩阵合并, 同 test_combine_three_ordered_lists"""

        gen_lists = [self.ret_ordered_random_lis(self.b_length) for i in range(self.a_length)]
        combine_gen_lis = self.combine_ordered_more_lists(gen_lists)
        # self.assertIsNot(combine_gen_lis, [], msg=f"the case {sys._getframe().f_code.co_name} Check list not empty ok.")

        self.assertEqual(len(combine_gen_lis), sum([len(x) for x in gen_lists]), msg=f"the case {sys._getframe().f_code.co_name} Check list length is ok.")
        print(f'case:{sys._getframe().f_code.co_name} completed')


if __name__ == '__main__':
    """
    a = [1, 4, 4, 8, 64]
    b = [0, 2, 5, 6, 16, 21, 21, 24, 30]

    t0 = time.time()
    print(extent_lis(a, b))
    t00 = time.time()
    print('new method times:{:15f}'.format(float(float(t00) - float(t0))))

    t1 = time.time()
    print(def_extent_lis(a, b))
    t2 = time.time()
    print('def method times:{:15f}'.format(float(float(t2) - float(t1))))

    t3 = time.time()
    print(def_sorted(a, b))
    t4 = time.time()
    print('def sorted times:{:15f}'.format(float(float(t4) - float(t3))))
    
    a=[0, 0, 0, 5, 5, 6, 7, 9, 9, 12, 12, 13, 15, 15, 16, 16, 16, 16, 16, 17, 17, 19, 20, 20, 22, 24, 25, 26, 31, 40, 40, 40, 40]
    b=[0, 11, 13, 17, 19, 21, 22, 40]
    print(extent_lis(a, b))
    """
    unittest.main()
