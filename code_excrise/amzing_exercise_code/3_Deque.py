# 三，双端队列
# py实现

class Deque(object):
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def addFront(self, item):
        self.items.append(item)     # 添加到队首

    def addRear(self, item):
        self.items.insert(0, item)  # 添加到队尾 O(n)

    def removeFront(self):
        return self.items.pop()     # O(1) 队首尾移除

    def removeRear(self):
        return self.items.pop(0)   # O(n) 队尾移除

    def size(self):
        return len(self.items)


