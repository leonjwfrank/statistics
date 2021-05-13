"""图的最小生成树"""

from Graph import Graph, Vertex
import sys


class PriorityQueue:
    """优先队列"""
    def __init__(self):
        self.heapArray = [(0, 0)]
        self.currentSize = 0

    def buildHeap(self, alist):
        self.currentSize = len(alist)
        self.heapArray = [(0, 0)]
        for i in alist:
            self.heapArray.append(i)
        i = len(alist) // 2
        while (i > 0):
            self.percDown(i)
            i = i - 1

    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapArray[i][0] > self.heapArray[mc][0]:
                tmp = self.heapArray[i]
                self.heapArray[i] = self.heapArray[mc]
                self.heapArray[mc] = tmp
            i = mc

    def minChild(self, i):
        if i * 2 > self.currentSize:
            return -1
        else:
            if i * 2 + 1 > self.currentSize:
                return i * 2
            else:
                if self.heapArray[i * 2][0] < self.heapArray[i * 2 + 1][0]:
                    return i * 2
                else:
                    return i * 2 + 1

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapArray[i][0] < self.heapArray[i // 2][0]:
                tmp = self.heapArray[i // 2]
                self.heapArray[i // 2] = self.heapArray[i]
                self.heapArray[i] = tmp
            i = i // 2

    def add(self, k):
        self.heapArray.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def delMin(self):
        retval = self.heapArray[1][1]
        self.heapArray[1] = self.heapArray[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapArray.pop()
        self.percDown(1)
        return retval

    def isEmpty(self):
        if self.currentSize == 0:
            return True
        else:
            return False

    def decreaseKey(self, val, amt):
        # this is a little wierd, but we need to find the heap thing to decrease by
        # looking at its value
        done = False
        i = 1
        myKey = 0
        while not done and i <= self.currentSize:
            if self.heapArray[i][1] == val:
                done = True
                myKey = i
            else:
                i = i + 1
        if myKey > 0:
            self.heapArray[myKey] = (amt, self.heapArray[myKey][1])
            self.percUp(myKey)

    def __contains__(self, vtx):
        for pair in self.heapArray:
            if pair[1] == vtx:
                return True
        return False


def prim(G, start):
    """
    最小生成树算法，用于解决信息传播过程中的广播风暴的问题，最小权重的生成树(minimum weight spanning tree)
        生成树:拥有图中所有的顶点和最少数量的边，以保持连通的子图。
    图G(V,E)的最小生成树T，定义为 包含所有顶点V，以及E的无圈子集，并且边权重 之和最小。

    解决最小生成树问题的Prim算法，属于 “贪心算法”，即每步都沿着最小权重的 边向前搜索
    构造最小生成树的思路很简单，如果T还 不是生成树，则反复做: 找到一条最小权重的可以安全添加的边，将边添 加到树T
    “可以安全添加”的边，定义为一端顶点 在树中，另一端不在树中的边，以便保持 树的无圈特性
    :param G:
    :param start:
    :return:
    """
    pq = PriorityQueue()
    for v in G:
        v.setDistance(sys.maxsize)
        v.setPred(None)
    start.setDistance(0)
    pq.buildHeap([(v.getDistance(), v) for v in G])
    while not pq.isEmpty():
        currentVert = pq.delMin()
        for nextVert in currentVert.getConnections():
            newCost = currentVert.getWeight(nextVert)
            if nextVert in pq and newCost < nextVert.getDistance():
                nextVert.setPred(currentVert)
                nextVert.setDistance(newCost)
                pq.decreaseKey(nextVert, newCost)


if __name__ == '__main__':
    theHeap = PriorityQueue()
    theHeap.add((2, 'x'))
    theHeap.add((3, 'y'))
    theHeap.add((5, 'z'))
    theHeap.add((6, 'a'))
    theHeap.add((4, 'd'))

    assert theHeap.currentSize == 5
    assert theHeap.delMin() == 'x'
    assert theHeap.delMin() == 'y'

    theHeap.decreaseKey('d', 1)
    assert theHeap.delMin() == 'd'

