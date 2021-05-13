import time

t0 = time.time()


def is_num_in(str1):
    num_all = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
    for n in list(str1):
        if n not in num_all:
            raise TypeError('input string is not suitable:{}, include:{}'.format(str1, n))
    return True


def nun_sec(str1):
    nums = []
    if str1 in [None, '', [], {}]:
        return nums
    is_num_in(str1)
    lis_n = list(str1.lower())
    # print('lis_n:{}'.format(lis_n))
    x = 0
    while len(lis_n) > 0:
        if 'z' in lis_n:
            nums.append('0' * lis_n.count('z'))
            for l_n in 'zero' * lis_n.count('z'):
                lis_n.remove(l_n)

        if 'g' in lis_n:
            nums.append('8' * lis_n.count('g'))
            for l_e in 'eight' * lis_n.count('g'):
                lis_n.remove(l_e)

        if 'x' in lis_n:
            nums.append('6' * lis_n.count('x'))
            for l_x in 'six' * lis_n.count('x'):
                lis_n.remove(l_x)

        if 'u' in lis_n:
            nums.append('4' * lis_n.count('u'))
            for l_u in 'four' * lis_n.count('u'):
                lis_n.remove(l_u)

        if 'w' in lis_n:
            nums.append('2' * lis_n.count('w'))
            for l_w in 'two' * lis_n.count('w'):
                lis_n.remove(l_w)

        # else:
        if 'f' in lis_n:
            nums.append('5' * lis_n.count('f'))
            for l_f in 'five' * lis_n.count('f'):
                lis_n.remove(l_f)

        if 't' in lis_n:
            nums.append('3' * lis_n.count('t'))
            for l_f in 'three' * lis_n.count('t'):
                lis_n.remove(l_f)
        if 's' in lis_n:
            nums.append('7' * lis_n.count('s'))
            for l_f in 'seven' * lis_n.count('s'):
                lis_n.remove(l_f)

        if 'o' in lis_n:
            nums.append('1' * lis_n.count('o'))
            for l_f in 'one' * lis_n.count('o'):
                lis_n.remove(l_f)

        if 'i' in lis_n:
            nums.append('9' * lis_n.count('i'))
            for l_f in 'nine' * lis_n.count('i'):
                lis_n.remove(l_f)

        if x > 100:
            break

    # print(nums)
    return nums


# def sort_num(nums):
#     import numpy as np
#     ty_np = np.array(list(nums))
#     # print(ty_np, type(ty_np), np.sort(ty_np))
#     ans_ite = ''
#     for ite in np.sort(ty_np):
#         ans_ite += ite
#     return ans_ite


def QuickSort(ls):
    def partition(lis, left, right):
        key = left
        while left < right:
            while left < right and lis[right] >= lis[key]:
                right -= 1
            while left < right and lis[left] <= lis[key]:
                left += 1
            (lis[left], lis[right]) = (lis[right], lis[left])
        (lis[left], lis[key]) = (lis[key], lis[left])
        return left

    def quicksort(lis, left, right):  # 递归调用
        if left >= right:
            return
        mid = partition(lis, left, right)
        quicksort(lis, left, mid - 1)
        quicksort(lis, mid + 1, right)

    # 主函数
    n = len(ls)
    if n <= 1:
        return ls
    quicksort(ls, 0, n - 1)
    return ls


if __name__ == '__main__':
    try:
        in_str = input('please input the encode string:')
        # is_num_in(in_str)
    except:
        str1 = 'NeNohuzirerooNNiNeteefersixeight'
    else:
        str1 = in_str
    t0 = time.time()
    nums = nun_sec(str1)

    arr = QuickSort(nums)
    print("after decode sucrity num：")
    for i in arr:
        print(i, end='')
    print('\nthe input str:{}'.format(str1))
    print('time cost:{}'.format(time.time() - t0))
