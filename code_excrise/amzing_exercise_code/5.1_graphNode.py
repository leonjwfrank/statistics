"""
    图的算法应用
    骑士周游

~~~~~~~~~~~~~~~~~~


"""
from Graph import Graph, Vertex


def orderByAvail(n):
    """按效益排序"""
    resList = []
    for v in n.getConnections():
        if v.getColor() == 'white':
            c = 0
            for w in v.getConnections():
                if w.getColor() == 'white':
                    c = c + 1
            resList.append((c, v))
    resList.sort(key=lambda x: x[0])
    return [y[1] for y in resList]


def posToNodeId(row, col, bdSize):
    return row * bdSize + col


def legalCoord(x, bdSize):
    if x >= 0 and x < bdSize:
        return True
    else:
        return False


def genLegalMoves(x, y, bdSize):
    newMoves = []
    moveOffsets = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
    for i in moveOffsets:
        newX = x + i[0]
        newY = y + i[1]
        if legalCoord(newX, bdSize) and legalCoord(newY, bdSize):
            newMoves.append((newX, newY))
    return newMoves


def knightGraph(bdSize):
    """按size生成棋盘大小"""
    ktGraph = Graph()
    for row in range(bdSize):
        for col in range(bdSize):
            nodeId = posToNodeId(row, col, bdSize)
            newPositions = genLegalMoves(row, col, bdSize)
            for e in newPositions:
                nid = posToNodeId(e[0], e[1], bdSize)
                ktGraph.addEdge(nodeId, nid)
    return ktGraph


def knightTour(n, path, u, limit):
    """采用先验的知识来改进算法性能的做法， 称作为“启发式规则heuristic” 启发式规则经常用于人工智能领域;
        可以有效地减小搜索范围、更快达到目标等等;
        如棋类程序算法，会预先存入棋谱、布阵口诀、
        高手习惯等“启发式规则”，能够在最短时间内
        从海量的棋局落子点搜索树中定位最佳落子。
        例如:黑白棋中的“金角银边”口诀，指导程序
        优先占边角位置等等

        其目的是建立一个没有分支的最深的深度优先树
        表现为一条线性的包含所有节点的退化树"""
    u.setColor('gray')
    path.append(u)
    if n < limit:
        nbrList = list(u.getConnections())
        i = 0
        done = False
        while i < len(nbrList) and not done:
            if nbrList[i].getColor() == 'white':
                done = knightTour(n + 1, path, nbrList[i], limit)  # 递归
            i = i + 1
        if not done:  # prepare to backtrack
            path.pop()
            u.setColor('white')
    else:
        done = True
    return done


def knightTourBetter(n, path, u, limit):  # use order by available function
    """
    依据人类的先验知识优化了骑士周游问题的复杂度，启发式规则heuristic，将u的合法移动目标棋盘格排序为:具有最少合 法移动目标的格子优先搜索
    同类的如 棋类程序算法，会预先存入棋谱、布阵口诀、高手习惯等“启发式规则”
    :param n:   层次
    :param path:  路径
    :param u:   当前顶点
    :param limit:  搜索总深度
    :return:

    """
    u.setColor('gray')
    path.append(u)  # 当前顶点加入路径
    if n < limit:
        nbrList = orderByAvail(u)
        # nbrList = u.connectedTo
        i = 0
        done = False
        while i < len(nbrList) and not done:
            if nbrList[i].getColor() == 'white':  # 选择白色未经过的顶点深入
                done = knightTour(n + 1, path, nbrList[i], limit)  # 层次加1，递归深入
            i = i + 1
        if not done:  # prepare to backtrack
            path.pop()  # 都无法完成总深度，回溯试本层下一个顶点
            u.setColor('white')
    else:
        done = True
    return done


if __name__ == '__main__':

    kg = knightGraph(5)  # five by five solution

    thepath = []
    start = kg.getVertex(4)
    knightTourBetter(0, thepath, start, 24)
    for v in thepath:
        print(v.getId())
