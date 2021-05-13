"""
~~~
    博物馆大盗问题的动态规划解决

"""

# 宝物重量和价值
bw = [None, {'w':2,'v':3}, {'w':3, 'v':4}, {'w':4, 'v':8}, {'w':5,'v':8}, {'w':9, 'v':10}]
bwr = [(2, 3), (3, 4), (4, 8), (5, 8), (9, 10)]

# 最大承重
max_w = 20

# 初始化二维表m[(i,w)]
# 表示前i个宝物中，最大重量w的组合，所得的最大价值
# 当i什么都不取，或w上限为0，价值均为0

m = {(i, w): 0 for i in range(len(bw))
                for w in range(max_w + 1)}
me = {}  # 初始化一个空的


def sum_weight():
    # 逐个填写二维表
    for i in range(1, len(bw)):
        for w in range(1, max_w + 1):
            if bw[i]['w'] > w:  # 装不下第i个宝物
                m[(i, w)] = m[(i-1, w)] # 不装第i个宝物
            else:
                # 不要第i个宝物 与要第 i 个宝物，两个情况下最大价值
                m[(i,w)]=max(m[(i-1, w)], m[(i-1, w-bw[i]['w'])] + bw[i]['v'])
    return m[(len(bw)-1, max_w)]


def sum_weight_real(bwr, w):
    print(f'bwr:{bwr}, me:{me}, w:{w}')
    if bwr == set() or w == 0:
        me[(tuple(bwr), w)] = 0  # tuple 是key的要求
        return 0
    elif (tuple(bwr)) in me:
        return m[(tuple(bwr), w)]
    else:
        vmax = 0
        for t in bwr:
            if t[0] <= w:
                # 逐个从集合去掉某个宝物，递归调用
                # 选出所有价值最大值
                print(f'bwr:{bwr}, t:{t}')
                v = sum_weight_real(set(bwr) - {t}, w-t[0]) + t[1]   # 递归调用
                vmax = max(vmax, v)
        m[tuple(bwr), w] = vmax
        return vmax

def queen(A, cur=0):
    """八皇后问题"""

    if cur == len(A):
        print(A)
        return 0
    for col in range(len(A)):
        A[cur], flag = col, True
        for row in range(cur):
            if A[row] == col or abs(col - A[row]) == cur - row:
                flag = False
                break
        if flag:
            queen(A, cur + 1)  # 递归调用
    return A

if __name__ == '__main__':
    """
    print(sum_weight())
    print(sum_weight_real(bwr, max_w))
    lis1 = [0,12,'#',4]
    # sorted(lis1, reverse=True)
    """
    print(queen([None] * 8))