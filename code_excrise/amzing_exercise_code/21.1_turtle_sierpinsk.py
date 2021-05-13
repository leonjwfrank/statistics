"""
# 乌龟作图绘制谢尔宾斯三角形
递归的三个应用解决一些问题
#  1，谢尔宾斯三角形
#  2，汉诺塔移动
#  3，走出迷宫
"""
import turtle
t = turtle.Turtle()

def drawTriangle(points, c):
    """绘制等边三角形"""
    t.fillcolor(c)
    # t.pencolor(c)
    t.penup()
    t.goto(points['top'])
    t.pendown()
    t.begin_fill()
    t.goto(points['left'])
    t.goto(points['right'])
    t.goto(points['top'])
    t.end_fill()
    # for i in range(3):  # 绘制一个等边三角形
    #     t.forward(300)  # 向前100
    #     t.right(120)  # 右转60度
    # turtle.done()


def getMid(f, s):
    """取两个点的中点"""
    return ((f[0]+s[0])/2, (f[1] + s[1])/2)


def sierpinski(degree, points):
    """
    :param degree:  整形，n阶 谢尔宾斯三角形
    :param points:  字典，三角形轮廓，左下角，右边
    :return:
    """
    colormap = ['blue', 'black', 'green', 'white', 'yellow', 'red', 'orange', 'cyan']
    drawTriangle(points, colormap[degree])
    if degree > 0: # degree 最小规模，退出
        # 调用自身，递归，左上右的次序
        # getMid 边长减半
        sierpinski(degree - 1,
                   {'left':points['left'],
                    'top':getMid(points['left'], points['top']),
                    'right':getMid(points['left'], points['right'])
                    })
        sierpinski(degree - 1,
                   {'left': getMid(points['left'], points['top']),
                    'top': points['top'],
                    'right': getMid(points['top'], points['right'])
                    })
        sierpinski(degree - 1,
                   {'left': getMid(points['left'], points['right']),
                    'top': getMid(points['top'], points['right']),
                    'right': points['right']
                    })
import time
def draw():

    start = 5
    if start and isinstance(start, int):
        time.sleep(start)
    points = {'left': (-300, -100),
              'top': (0, 300),
              'right': (300, -100)}
    # drawTriangle(points, 'red')
    sierpinski(3, points)  #
    turtle.done()


class MoveTower(object):
    """汉诺塔的移动方法， 如果对汉诺塔问题本身不清楚，请自行搜索资料"""
    @staticmethod
    def moveDisk(disk, fromPole, toPole):
        print(f"Moving disk[{disk}], fromPole{fromPole} toPole{toPole}")
        pass


    @staticmethod
    def moveTower(height, fromPole, withPole, toPole):
        if height >= 1:
            MoveTower.moveTower(height - 1, fromPole, toPole, withPole)
            MoveTower.moveDisk(height, fromPole,  toPole)
            MoveTower.moveTower(height - 1, withPole, fromPole, toPole)

class Maze(object):
    """走出迷宫"""
    def __init__(self, mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []
        mazeFile = open(mazeFileName, 'r')
        rowsInMaze = 0
        for line in mazeFile:   #
            rowList = []
            col = 0
            for ch in line[:-1]:
                rowList.append(ch)
                if ch == 'S':
                    self.startRow = rowsInMaze
                    self.startCol = col
                col = col + 1
            rowsInMaze += 1
            self.mazelist.append(rowList)    # 保持矩阵
            columnsInMaze = len(rowList)

    def drawMaze(self):
        """绘制迷宫图形，墙壁用实心方格绘制"""
        pass

    def updatePosition(self, row, col, val):
        """更新海龟位置，并标注"""
        pass

    def isExit(self, row, col):
        """判断是否 出口"""
        pass

    @staticmethod
    def searchFrom(maze, startRow, startColumn):
        # 1,碰到墙壁。返回失败
        OBSTACLE = 'OBSTACLE'   # 墙壁
        maze.updatePosition(startRow, startColumn)
        if maze[startRow][startColumn] == OBSTACLE:
            return False

        # 2,碰到面包屑。返回失败
        TRIED = 'TRIED'
        DEAD_END = 'DEAD_END'

        if maze[startRow][startColumn] == TRIED or maze[startRow][startColumn] == DEAD_END:
            return False

        # 3,碰到出口。返回成功
        PORT_OF_PATH = 'PORT_OF_PATH'
        if maze.isExit(startRow, startColumn):
            maze.updatePosition(startRow, startColumn, PORT_OF_PATH)
            return True

        # 4, 洒下面包屑，继续
        maze.updatePosition(startRow, startColumn, TRIED)

        # 向4个方向 东南西北继续探索，or操作符具有短路效应
        found = Maze.searchFrom(maze, startRow - 1, startColumn) or \
                Maze.searchFrom(maze, startRow + 1, startColumn) or \
                Maze.searchFrom(maze, startRow, startColumn - 1) or \
                Maze.searchFrom(maze, startRow, startColumn + 1)
        # 如果探索成功，标记当前点，失败则标记为"死胡同"
        if found:
            maze.updatePosition(startRow, startColumn, PORT_OF_PATH)
        else:
            maze.updatePosition(startRow, startColumn, DEAD_END)
        return found


if __name__ == '__main__':
    """
    # 谢尔斯宾三角形绘制
    # points 外轮廓三个顶点
    t0 = time.time()
    
    pass
    draw()
    print('cost time:{}'.format(time.time() - t0))
    """
    # 汉诺塔的移动问题
    MoveTower.moveTower(3, '#1', '#2', '#3')