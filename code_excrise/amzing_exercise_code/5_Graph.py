""""""

import sys
import os
import unittest


class Graph:
    """Graph():创建一个空的图;
        addVertex(vert):将顶点vert加入图中 addEdge(fromVert, toVert):添加有向边
        addEdge(fromVert, toVert, weight):添加 带权的有向边
        getVertex(vKey):查找名称为vKey的顶点 getVertices():返回图中所有顶点列表
        in:按照vert in graph的语句形式，返回顶点 是否存在图中True/False"""

    def __init__(self):
        self.vertices = {}      # 顶点信息
        self.numVertices = 0   # 顶点总数
        self.numEdge = 0       # 边总数

    def addVertex(self, key):
        """添加顶点"""
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex     # 设置新的顶点信息
        return newVertex

    def getVertex(self, n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertices

    def addEdge(self, f, t, cost=0):
        """
        :param f:  出发顶点
        :param t:  结束顶点
        :param cost:  边的权重
        :return:
        """
        if f not in self.vertices:
            nv = self.addVertex(f)
        if t not in self.vertices:
            nv = self.addVertex(t)
        self.vertices[f].addNeighbor(self.vertices[t], cost)    # 使用顶点类的方法，添加邻接边
        self.numEdge += 1

    def getVertices(self):
        """获取顶点列表"""
        return list(self.vertices.keys())

    def __iter__(self):
        return iter(self.vertices.values())


class Vertex:
    """顶点，Vertex包含了顶点信息，以及顶点连接边"""

    def __init__(self, num):
        self.id = num
        self.connectedTo = {}
        self.color = 'white'
        self.dist = sys.maxsize
        self.pred = None
        self.disc = 0
        self.fin = 0

    # def __lt__(self,o):
    #     return self.id < o.id

    def addNeighbor(self, nbr, weight=0):
        """

        :param nbr:   顶点对象一个字典的key
        :param weight:
        :return:
        """
        self.connectedTo[nbr] = weight      # 设置边和 边的权重信息

    def delNeighbor(self, nbr):
        """移除该顶点的一个邻接点"""
        del self.connectedTo[nbr]

    def setColor(self, color):
        self.color = color

    def setDistance(self, d):
        """"""
        self.dist = d

    def setPred(self, p):
        self.pred = p

    def setDiscovery(self, dtime):
        self.disc = dtime

    def setFinish(self, ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + ":color " + self.color + ":disc " + str(self.disc) + ":fin " + str(
            self.fin) + ":dist " + str(self.dist) + ":connect and weight info" + str(self.connectedTo) + ":pred \n\t[" + str(self.pred) + "]\n"

    def getId(self):
        return self.id


class adjGraphTests(unittest.TestCase):
    def setUp(self):
        self.tGraph = Graph()

    def testMakeGraph(self):
        gFile = open("test.dat")
        for line in gFile:
            fVertex, tVertex = line.split('|')
            fVertex = int(fVertex)
            tVertex = int(tVertex)
            self.tGraph.addEdge(fVertex, tVertex)
        for i in self.tGraph:
            adj = i.getAdj()
            for k in adj:
                print(i, k)


if __name__ == '__main__':
    # unittest.main()
    g=Graph()
    g.addVertex(1)
    g.addVertex(2)
    g.vertices[1].setDistance(2)
    print(g.vertices[1].getConnections())
    print(g.vertices[2].getConnections())
    g.addEdge(1,2,1)
    g.addEdge(1, 2, 1)
    g.addEdge(1,3,2)
    g.addEdge(1,4,1)
    g.addEdge(2,3,2)
    g.addEdge(2,4,3)
    g.addEdge(3,4,4)
    g.addEdge(2,1,2)
    g.vertices[3].setDistance(4)
    g.vertices[2].setDistance(3)
    print(f'顶点总数:{g.numVertices}, 边总数:{g.numEdge} 顶点1的信息:', g.getVertex(1))
    print(f'vertice connection keys:{[(1,k.id) for k in g.vertices[1].getConnections()]}')
    # for k, w in g.vertices[1].connectedTo.items():
    #     print(f'id 1 connect info 起始点{1}, 连接点{k.id}, 路径权重{w}')

    del_cont = None
    for k in g.vertices.keys():  # 打印图中所有点的连接信息
        for j, w in g.vertices[k].connectedTo.items():
            print(f'id connect info 起始点{k}, 连接点{j.id}, 路径权重{w}')
            if k==1 and j.id == 4:
                del_cont = j
    g.vertices[1].delNeighbor(del_cont)

    def recursion_vert(g):
        for j, w in g.vertices.items():
            print(f'g info connect info{j}, 路径{w}')
        if g.vertices:  # 退出条件
            pop_it = g.vertices.popitem()  # 缩小规模
            print(f'pop_it :{pop_it}')
            return recursion_vert(g)

    print(f'vert recursion: {recursion_vert(g)}')



