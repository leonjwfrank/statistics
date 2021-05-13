def change_place(lis1):
    """取得逆序 笨办法不用内建函数"""
    ls = len(lis1)
    reverse_lis = []
    for i in range(ls):
        reverse_lis.append(lis1[len(lis1) - (1 + i)])
    print(f'reverse_lis:{reverse_lis}')
    return reverse_lis


img_lis = []


def image_lis(lis1):
    """动态规划"""
    ls = len(lis1)
    if not len(img_lis) == ls:
        for i in range(ls // 2):
            start_index = (2 ** i) - 1
            end_index = (2 ** (i + 1)) - 1
            expend_lis = change_place(lis1[start_index:end_index])
            img_lis.extend(expend_lis)
            print(f'now img_lis:{img_lis}')
    return img_lis


import sys

if __name__ == "__main__":
    # 读取第一行的n
    # al=[]
    # for line in sys.stdin:
    a = sys.stdin.readline().strip()
    print(f'a:{a}')
    al = a.split()
    print(f'al:{al}')
    print(image_lis(al))
