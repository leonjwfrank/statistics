"""
queue 的 py 的应用
  ~~~~~
    应用示例
    1, 热土豆(击鼓传花)问题
    2, 打印任务(队列)  先到先服务的队列策略
        决策支持问题
        抽象对象特征: 提交时间，打印页数
        队列属性: 具有FIFO性质的打印任务队列
        打印机属性: 打印速度，是否繁忙
"""
from PQueue import PQueue


def hotPotato(name_list, num):
    simqueue = PQueue()
    for n in name_list:
        simqueue.enqueue(n)

    while simqueue.size() > 1:  # 直到只剩下一个人
        for i in range(num):  #
            simqueue.enqueue(simqueue.dequeue())  # 一次传递

        simqueue.dequeue()
    return simqueue.dequeue()


class Printer(object):
    # 打印机对象
    def __init__(self, ppm):
        self.pagerate = ppm         # 打印速度
        self.currentTask = None     # 打印任务
        self.timeRemaining = 0      # 任务倒计时

    def tick(self):
        # 打印1秒
        if self.currentTask != None:
            self.timeRemaining = self.timeRemaining - 1
            if self.timeRemaining <= 0:
                self.currentTask = None

    def busy(self):
        # 打印是否繁忙
        if self.currentTask != None:
            return True
        else:
            return False

    def startNext(self, newTask):
        # 打印新作业
        self.currentTask = newTask
        self.timeRemaining = (newTask.getPages() * 60) / self.pagerate

import random
class Task(object):

    # 任务对象
    def __init__(self, time):
        self.timestamp = time                   # 生成时间戳
        self.pages = random.randrange(1, 21)    # 打印页数

    def getStamp(self):
        return self.timestamp
    def getPages(self):
        return self.pages
    def waittime(self, currenttime):
        return currenttime - self.timestamp     # 等待时间


def newPrintTask():
    num = random.randrange(1, 181)     # 1/180 概率生成作业
    if num == 180:
        return True
    else:
        return False


def simulation(numSeconds, pagesPerMinute):
    """

    :param numSeconds:
    :param pagesPerMinute: 模拟
    :return:
    """
    labprinter = Printer(pagesPerMinute)    # 生成一个打印对象
    printQueue = PQueue()                    # 生成打印队列
    waitingtimes = []                       # 等待时间
    averageWaitList = []
    for curtentSecond in range(numSeconds):
        # 迭代循环，时间进行中...
        if newPrintTask():
            task = Task(curtentSecond)
            printQueue.enqueue(task)  # 新生成对象，加入任务队列
        if (not labprinter.busy()) and (not printQueue.isEmpty()):
            nexttask = printQueue.dequeue()   # 取出队列任务，队尾
            waitingtimes.append(curtentSecond) # nexttask.waitTime 下一个任务等待时长
            labprinter.startNext(nexttask)
        labprinter.tick()   # 打印1s
        try:
            averageWait = sum(waitingtimes) / len(waitingtimes)
            print("Avg time: {:6.2f} s, secs:{:3d} tasks remaining. list:{}".format(averageWait, printQueue.size(), printQueue.get()))
            averageWaitList.append(averageWait)
        except (Exception, ZeroDivisionError) as e:
            print('some random wait happend, wait for next round:{}'.format(e))
    return sum(averageWaitList) / len(averageWaitList)

if __name__ == '__main__':
    # 热土豆问题，最后显示谁
    print(hotPotato(['Bill', 'Jack', 'Sam', 'Jane', 'Kent', 'Bob'], 7))
    #
    # 模拟打印 10次，每分钟打印5页，标准模式(快速模式，打印质量会下降)
    import time
    print_avg_time = []
    for i in range(5):
        cost_time = simulation(3600, 5)
        print('num:{}, cost avg time:{:6.3f} s'.format(i, cost_time))
        print_avg_time.append(cost_time)
        time.sleep(3)
    print('all avg:{}, all list cost_time:{}'.format(sum(print_avg_time)/ len(print_avg_time), print_avg_time))
