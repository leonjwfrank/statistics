# py 实现无序表 -- 单链表

class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        """
        tep = Node(90)
        tep.getData
        90
        :return:
        """
        return self.data

    def getNext(self):
        return self.next

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext

    # def pop(self):
    #     return self.


class UnorderedList(object):
    """
    表头设置，数据项加入后，无序表head始终指向链条第一个节点
    通过head 是否None 检测是否 非空链表
    单链表，只有指向下一个节点的
    mylis = UnorderedList()
    print(mylis.head)
    None
    """

    def __init__(self):
        self.head = None

    def add(self, item):
        """链接次序很重要"""
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def size(self):

        current = self.head
        count = 0
        while current != None:
            count += 1
            current = current.getNext()    # O(N), 链式的操作时间复杂度为 O(n), 如果是顺序结构，可以最后一个地址 - 首地址 除以 长度
        return count

    def search(self, item):
        current = self.head
        found = False
        while current != None and not found:    # 最坏情况下 O(n), 最好O(1)
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()
        return found

    def remove(self, item):
        """找到节点，维护前一个节点，previous 指向 后一个节点位置，然后删除 current"""
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()
        if previous == None:   # 如果 previous 是 None，删除的是第一个节点
            self.head = current.getNext()
        else:
            previous.serNext(current.getNext())




