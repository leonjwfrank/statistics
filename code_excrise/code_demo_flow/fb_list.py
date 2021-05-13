import functools
import profile

@functools.lru_cache(maxsize=None)
def fbnc(n):
	a, b = 0, 1
	if n in [1, 2]:
		yield 1
	while True:
		x = a + b
		a = b
		b = x
		yield x


#  递归， 默认最多1000层
@functools.lru_cache(maxsize=None)
def fb(n):
	if n <= 2:
		return 1
	else:
		return fb(n-1) + fb(n-2)


if __name__ == '__main__':
	f9 = fbnc(9)
	for s in range(5, 10):
		print('s', next(fbnc(s)))
		profile.run('print("value", next(f9))')
	for i in range(10):
		print('ind:', i)
		profile.run("print('value', fb(i));print()")