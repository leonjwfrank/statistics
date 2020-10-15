# py 迭代器设计模式实现
import itertools

class Prime(object):
    """迭代器遵循迭代器协议，在py中必须拥有 __iter__ & __next__ 方法"""
    def __init__(self, initial, final=0):
        """Initializer -accepts a number
        :params initial: 开始的数字
        :params final"""
        self.current = initial
        self.final = final

    def __iter__(self):
        """"""
        return self

    def __next__(self):
        """return next item in iteratro"""
        return self._compute()

    def _compute(self):
        """Compute the next prime number"""
        num = self.current
        while True:
            is_prime = True
            for x in range(2, int(pow(self.current, 0.5)+1)):
                if self.current%x==0:
                    is_prime = False
                    break
            num = self.current
            self.current += 1
            if is_prime:
                print(f"current:{self.current}")
                return num

            # If there is and end range, look for it
            if self.final > 0 and self.current > self.final:
                raise StopIteration


if __name__ == '__main__':
    # case 1
    print(f"2-50 之间的质数: {list(Prime(2, 50))}")
    # 前100个质数
    print(f"自然数中前100个质数:{list(itertools.islice(Prime(2), 100))}")
    # 前10个 以 1结束的质数
    print(f"自然数中前10个以1结束的质数:{list(itertools.islice(itertools.filterfalse(lambda x:x % 10 != 1, Prime(2)), 10))}")
    # 前10个回文质数 First 10 palindromic primes
    print(f"前十个回文质数:{list(itertools.islice(itertools.filterfalse(lambda x:str(x)!=str(x)[-1::-1], Prime(10)), 10))}")
    



