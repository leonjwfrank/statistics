
def syncMakeChange(coinValueList, change, minCoins, coinsUsed):
    """
    找零钱问题的 动态规划解法，比递归更有条理，依赖于更少钱数的最优解
    问题最优解 包含了 更小规模 子问题的最优解，这时一个最优化问题苟能用动态规划策略解决的 必要条件
    :param coinValueList, 币值体系列表, 该币种有几种面值的币
    :param change, 需要找零的总额
    :param  minCoins, 已知的兑换方法，是需要找零的总数长度的列表，序列下标表示序号
    :param coinsUsed, 对应位置的零钱数，使用的硬币币值 组合
    :return:
    """
    # 从1分开始到change逐个计算最少硬币数
    for cents in range(1, change+1):  # 左闭右开
        # 1, 初始化一个最大值
        coinCount = cents
        newCoin = 1 # 初始化新加硬币
        # 2, 减去每个硬币，向后查最少硬币数，同时记录总的最少数
        less_list = [c for c in coinValueList if c <= cents]  # 小于cents的 币值体系列表
        print(f'小于待兑换总额{cents}的币值体系的列表:{less_list}')
        for j in less_list:   # 遍历币值体系列表
            print('minCoins[cents - j]:{}, coinCount:{},cents:{},  minCoins:{}'.format(minCoins[cents - j], coinCount,cents, minCoins))
            if minCoins[cents - j] + 1 < coinCount:
                print(f'合适的硬币数:{coinCount}, 当前cents:{cents} 信息:{minCoins}')
                coinCount = minCoins[cents - j] + 1
                newCoin = j
            print(f"newCoin:{newCoin}")

        # 3, 得到当前最少硬币数，记录到表中
        minCoins[cents] = coinCount
        coinsUsed[cents] = newCoin
    # 返回最后结果
    print(f'coinsUsed{coinsUsed}, minCoins:{minCoins}')
    return minCoins[change]

def printCoins(coinsUsed, change):
    coin = change
    while coin > 0:
        # 当前使用的硬币，在使用硬币表中查询，当前总额数量的金额，该列表记录的是最后使用的硬币面值
        thisCoin = coinsUsed[coin]
        print(f'当前选择的硬币:{thisCoin}')
        coin = coin - thisCoin   # 减去当前使用面值的硬币，剩余的额度继续循环


def rec_mc(coinValueList, change, knownResults):
    """
    找零钱递归解法
    :param coinValueList, 币值列表, 该币种有几种面值的币
    :param change, 需要找零的总额
    :param  knownResults, 已知的兑换方法，是需要找零的总数长度的列表，序列下标表示序号
    :return: 总额最后需要的最小组合
    """
    minCoins = change
    coin_value = []
    if change in coinValueList:   # 最小规模，返回, 结束条件
        knownResults[change]=1  # 记录最优解
        return 1
    elif knownResults[change] > 0:  # 查询是否在表中已有，如果有，则直接返回值
        return knownResults[change]
    else:
        for i in [c for c in coinValueList if c <= change]:
            print(f'i:{i}, change:{change}')
            numCoins = 1 + rec_mc(coinValueList, change-i, knownResults)  # 调用自身，递归，减小规模，每次减去一种硬币面值，挑选最小数量
            if numCoins < minCoins:
                minCoins = numCoins
                # 找到最优解，记录到表
                knownResults[change] = minCoins
    print(f'min_rst:{minCoins}, knownResults:{knownResults}')
    return minCoins


if __name__ == '__main__':
    import time

    coinValueList = [1, 2, 5, 10, 25]
    change = 63

    coinsUsed = [0] * 64
    """
    coinCount = [0] * 64
    run_lis = [c for c in coinValueList if c <= change]
    print(f'run_lis:{run_lis}')
    t0 = time.time()
    # 递归解法
    min_rst = rec_mc(coinValueList, change, coinCount)
    print('start time:{}, min rst:{}'.format(t0, min_rst))
    print(f'recursion cost time:{time.time() - t0}')
    """
    # 动态规划解法
    import timeit

    coinCount = [0] * 64
    # coinsUsed = [0] * 64
    t2 = time.clock()
    print('sync rst:{}'.format(syncMakeChange(coinValueList, change, coinCount, coinsUsed)))
    print(printCoins(coinsUsed, change))
    print(f'cost time:{time.clock() - t2}')


