"""
# 四，有序表的实现
# 有序表 数据相对位置取决于它们之间的 大小 比较
#    适用所有定义了 __gt__ (>)的方法
# next 链表实现

"""
from DisorderNode import Node

class OrderedList(object):
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.items == []

    def removeFront(self):
        return self.items.pop()  # O(1) 队首尾移除

    def removeRear(self):
        return self.items.pop(0)  # O(n) 队尾移除

    def size(self):
        return len(self.items)

    def add(self, item):
        """必须保证有序性，必须添加到合适位置，以维护整个链表的有序性"""
        current = self.head
        previous = None
        stop = False
        while current != None and not stop:
            if current.getData() > item:    # 发现插入位置
                stop = True
            else:
                previous = current
                current = current.getData()
        temp = Node(item)
        if previous == None:    # 插入表头
            temp.setNext(self.head)
            self.head = temp
        else:   # 插入表中
            temp.setNext(current)
            previous.setNext(temp)

    def search(self, item):
        """当遇到比item大的 元素时，直接返回False"""
        current = self.head
        found = False
        stop = False
        while current != None and not found and not stop:
            if current.getData() == item:
                found = True
            else:
                if current.getData() > item:    # 遇到大于当前item的元素，因为是有序表，停止搜索
                    stop = True
                else:
                    current = current.getNext()
        return found
