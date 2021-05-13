# 双端队列应用
# 回文词判定
from Deque import Deque


def palchecker(aString):
    chardeque = Deque()
    for ch in aString:
        chardeque.addRear(ch)
    stillEqual = True

    while chardeque.size() > 1 and stillEqual:
        first = chardeque.removeFront()
        last = chardeque.removeRear()
        if first != last:
            stillEqual = False
    return stillEqual


if __name__ == '__main__':
    # 判定字符串是否回文词
    print(palchecker('lasdsal'))
    print(palchecker('radar'))
