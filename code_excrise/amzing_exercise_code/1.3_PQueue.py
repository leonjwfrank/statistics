# 二，队列 Queue
#
#  py实现代码示例
class PQueue(object):
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0, item)      # O(n)
    def dequeue(self):
        return self.items.pop()     # O(1)
    def size(self):
        return len(self.items)
    def get(self):
        return self.items