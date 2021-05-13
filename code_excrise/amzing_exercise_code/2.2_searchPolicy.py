"""
~~~ 查找策略
    顺序（无序，有序）
    二分查找(有序)，迭代和非迭代实现
    二叉查找树
    二叉平衡树
"""


def binarySearch(alist, item):
    """二分查找的非递归实现"""
    first = 0
    last = len(alist) - 1
    found = False
    iter_t = 0
    while first <= last and not found:
        iter_t += 1

        midpoint = (first + last) // 2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1
    print(f'search times:{iter_t}')
    return found


def recursionSearch(alist, item, rec_t=0):
    """二分查找的递归实现"""
    rec_t += 1
    if len(alist) == 0:
        return False  # 结束条件
    else:
        midpoint = len(alist) // 2
        if alist[midpoint] == item:
            return True
        else:
            if item < alist[midpoint]:  # 缩小规模
                print('now search rec_t:{}'.format(rec_t))
                return recursionSearch(alist[:midpoint], item)  # 调用自身
            else:
                print('now search rec_t:{}'.format(rec_t))
                return recursionSearch(alist[midpoint + 1:], item)  # 调用自身


def bubbleSort(alist, x=0):
    """冒泡排序"""
    exchange = True  # 用于检测冒泡排序是否发生交换
    for passnum in range(len(alist) - 1, 0, -1):
        if exchange:
            exchange = False
            for i in range(passnum):  # n-1 趟
                x += 1
                if alist[i] > alist[i + 1]:
                    exchange = True
                    print(f'是否发生交换:{exchange}')
                    """
                    # 序错，交换开始
                    temp = alist[i]
                    alist[i] = alist[i+1]
                    alist[i+1] = temp
                    # 序错，交换结束
                    """
                    alist[i], alist[i + 1] = alist[i + 1], alist[i]
    print('sort times:{}'.format(x))
    return alist


def shortBubbleSort(alist, n=0):
    """冒泡性能改进
    """
    exchanges = True
    passnum = len(alist) - 1
    while passnum > 0 and exchanges:
        exchanges = False

        for i in range(passnum):
            if alist[i] > alist[i + 1]:
                n += 1  # 排序多少次
                exchanges = True
                # temp = alist[i]
                alist[i], alist[i + 1] = alist[i + 1], alist[i]
        passnum = passnum - 1
    print(f'共排序{n}次')
    return alist


def selectionSorting(alist, n=0):
    """选择排序"""
    for fill in range(len(alist) - 1, 0, -1):
        positionOfMax = 0
        for local in range(1, fill + 1):

            if alist[local] > alist[positionOfMax]:
                n += 1
                positionOfMax = local

        # 选择排序是在每一次内存循环完成后才进行的
        alist[fill], alist[positionOfMax] = alist[positionOfMax], alist[fill]  # 交换位置
    print(f'select sort n:{n}')
    return alist


def insertionSort(alist, n=0):
    """插入排序
    移动操作仅包含一次赋值，是交换操作的1/3，所以插入排序性能会好一些"""
    for index in range(1, len(alist)):
        currentvalue = alist[index]  # 新项/插入项
        position = index
        while position > 0 and alist[position - 1] > currentvalue:  # 如果大于当前项进入循环
            n += 1
            alist[position] = alist[position - 1]  # 对比，移动
            position = position - 1

        alist[position] = currentvalue  # 插入新项
    print('插入排序比对次数{}'.format(n))
    return alist


def shellSort(alist):
    """谢尔排序, gap 取值1，3，5，7，9... 2k-1
    O(N**(3/2))"""
    sublistcount = len(alist) // 2  # 间隔设定
    while sublistcount > 0:
        for startposition in range(sublistcount):  # 子列表排序
            gapInsertionSort(alist, startposition, sublistcount)
        print("After increment of size:{}, \n The list:{} ".format(sublistcount, alist))

        sublistcount = sublistcount // 2  # 间隔缩小

    return alist


def gapInsertionSort(alist, start, gap):
    """间隔插入排序"""
    for i in range(start + gap, len(alist), gap):
        currentvalue = alist[i]
        position = 1

        while position >= gap and alist[position - gap] > currentvalue:
            alist[position] = alist[position - gap]
            position = position - gap
    pass


def mergeSort(alist, n=0):
    """归并排序"""
    print('split:{}'.format(alist))
    if len(alist) > 1:
        mid = len(alist) // 2  # 基本结束条件
        lefthalf = alist[:mid]
        rightalf = alist[mid:]

        mergeSort(lefthalf)  # 递归调用左半部分,排序左部分
        mergeSort(rightalf)  # 递归调用右半部分，排序右部分
        print(f'left{lefthalf}')
        print(f'right{rightalf}')

        i = j = k = 0
        while i < len(lefthalf) and j > len(rightalf):

            if lefthalf[i] < rightalf[j]:
                # 交错把左右半部从小到大归并到结果列表中
                alist[k] = lefthalf[i]
                i += 1
                print(f"merga times:i{i},j{j},k{k}, alist:{alist}")
            else:
                alist[k] = rightalf[j]
                j += 1
                print(f"merga times:i{i},j{j},k{k}, alist:{alist}")
            k += 1

        while i < len(lefthalf):
            # 归并左半部
            alist[k] = lefthalf[i]
            i += 1
            k += 1
            print(f"merga times:i{i},j{j},k{k}, alist:{alist}")
        while j < len(rightalf):
            # 归并右半部
            alist[k] = rightalf[j]
            j += 1
            k += 1
            print(f"merga times:i{i},j{j},k{k}, alist:{alist}")
        # return alist


def merge_sort(lst, n=0):
    """pythonic 的归并排序"""
    if len(lst) <= 1:
        return lst
    # 分解问题，递归调用解决
    midd = len(lst) // 2
    left = merge_sort(lst[:midd])  # 左部排好序
    right = merge_sort(lst[midd:])  # 右部排好序

    # 合并左右半部，完成排序
    merged = []
    while left and right:
        n += 1
        if left[0] <= right[0]:
            merged.append(left.pop(0))
        else:
            merged.append(right.pop(0))
    merged.extend(right if right else left)
    print(f'pythonic 归并排序{n}次:{merged}')
    return merged


class QuickSort(object):

    @staticmethod
    def quickSort(alist):
        QuickSort.quickSortHelper(alist, 0, len(alist) - 1)
        return alist

    @staticmethod
    def quickSortHelper(alist, first, last, n=0):
        if first < last:  # 基本结束条件，如果first 还大于等于last，则继续分裂
            n += 1
            splitpoint = QuickSort.partition(alist, first, last)  # 分裂

            QuickSort.quickSortHelper(alist, first, splitpoint - 1)  # 递归调用快速排序
            QuickSort.quickSortHelper(alist, splitpoint + 1, last)

            print(f"快速排序{n}次，{alist}")
        return alist

    @staticmethod
    def partition(alist, first, last):
        """快速排序的分裂函数"""
        pivotvalue = alist[first]  # 选择中值
        leftmark = first + 1
        rightmark = last  # 左右标初值

        done = False
        while not done:
            while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
                # 左标向右移
                leftmark = leftmark + 1
            while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
                # 右标向左移
                rightmark = rightmark - 1
            if rightmark < leftmark:
                # 左右标相错则结束
                done = True
            else:

                # # 左右标值交换
                alist[leftmark], alist[rightmark] = alist[rightmark], alist[leftmark]
                """
                #或者经典写法:
                temp = alist[leftmark]
                alist[leftmark] = alist[rightmark]
                alist[rightmark] = temp
                #"""
        # 中值就位
        temp = alist[first]
        alist[first] = alist[rightmark]
        alist[rightmark] = temp

        return rightmark  # 返回中值点，分裂点


class BinarySearchTree(object):
    """二叉搜索树是红黑树的基础
    红黑树（R-B TREE，全称：Red-Black Tree），本身是一棵二叉查找树，在其基础上附加了两个要求：
    树中的每个结点增加了一个用于存储颜色的标志域；
    树中没有一条路径比其他任何路径长出两倍，整棵树要接近于“平衡”的状态。
    """
    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def __iter__(self):
        """迭代器,用于实现for的循环"""
        return self.root.__iter__()

    def _put(self, key, val, currentNode):  # currentNode root节点
        if key < currentNode.key:  # 如果参数key 比 当前节点的key小，进入树的左子树进行 递归插入
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)  # 递归左子树
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)  # 树的节点
                # self.updateBalance(currentNode.leftChild)  # 调整因子
        else:  # 如果key 等于大于 当前节点key，进入树的右子树进行递归插入
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.rightChild)  # 递归右子树
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)
                # self.updateBalance(currentNode.rightChild)  # 调整因子

    def put(self, key, val):
        """BST高度 log_2 N ,如果key列表随机分布，大于小于根节点key的键值大致相等。性能在于二叉树的高度(最大层次),高度也受数据项key插入顺序影响
        算法分析，最差O(log_2 N)"""
        if self.root:  # 有root根节点
            self._put(key, val, self.root)
        else:  # 没有root，则构造单个节点的二叉查找树
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def __setitem__(self, key, value):
        self.put(key, value)

    def get(self, key):
        """只要是平衡树，get的时间复杂度可以保持在O(logN)"""
        if self.root:
            res = self._get(key, self.root)  # 递归函数
            if res:
                return res.payload  # 找到节点
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        """

        :param key:
        :param currentNode: 当前节点，即要插入的二叉查找树 子树的根，为当前节点
        :return:
        """
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, item):
        """实现val=myZipTree['PK']"""
        return self.get(item)

    def __contains__(self, item):
        """实现'PK' in myZipTree的归属判断运算符 in

         mytree[3]='red'
         mytree[6]='yellow'
          print(3 in mytree)
          print(mhytree[6])"""
        if self._get(item, self.root):
            return True
        else:
            return False

    def remove(self, currentNode):
        """delete 的具体实现, 要求仍然保持BST性质，分3种情况，
        1，节点无子节点； 2，节点有1个子节点； 3，节点有2个子节点"""
        if currentNode.isLeaf():  # leaf，叶节点，没有子节点，属于 场景1，无子节点，直接删除
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
        elif currentNode.hasBothChildren():  # inrterior, 有两个子节点
            succ = currentNode.findSuccessor()  # 找到当前需要删除的节点的后继节点，
            succ.spliceOut()
            currentNode.key = succ.key  # 替换key
            currentNode.payload = succ.payload  # 替换payload，节点的数据项值

        else:  # this node have one child，有一个子节点
            if currentNode.hasLeftChild():
                if currentNode.isLeftChild():
                    # 左子节点删除
                    currentNode.leftChild.parent = currentNode.parent  # 修改指针，当前节点的左子节点的父节点 修改为节点的父节点
                    currentNode.parent.leftChild = currentNode.leftChild  # 修改指针，当前节点的父节点的左子节点 修改为当前节点的左子节点
                elif currentNode.isRightChild():
                    # 右子节点删除
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                else:
                    # 根节点删除
                    currentNode.replaceNodeData(currentNode.leftChild.key,
                                                currentNode.leftChild.payload,
                                                currentNode.leftChild.leftChild,
                                                currentNode.leftChild.rightChild)
            else:
                if currentNode.isLeftChild():
                    # 左子节点删除
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                elif currentNode.isRightChild():
                    # 右子节点删除
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                else:
                    # 根节点删除
                    currentNode.replaceNodeData(currentNode.rightChild.key,
                                                currentNode.rightChild.payload,
                                                currentNode.rightChild.leftChild,
                                                currentNode.rightChild.rightChild)

    def delete(self, key):
        """删除树中某个节点，子节点来替换当前节点.具体是调用remove方法"""
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')

    def __delitem__(self, key):
        """实现 del MyTree['PK']这样的方法"""
        self.delete(key)

    def updateBalance(self, node):
        """更新平衡树"""
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)  # 重新平衡
            return
        if node.parent != None:  # 查看当前节点是否有父节点，如果没有，说明已经是根节点，不需要再传播了。
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1
            if node.parent.balanceFactor != 0:  # 如果父节点平衡因子不为0，进行父节点平衡因子的调整
                self.updateBalance(node.parent)  # 调整父节点因子

    def rebalance(self, node):
        """节点子树再平衡，左或右旋转"""
        if node.balanceFactor < 0:  # 右重需要旋转
            if node.rightChild.balanceFactor > 0:
                # Do an LR Rotation
                self.rotateRight(node.rightChild)  # 右子节点左重，先右旋
                self.rotateLeft(node)
            else:
                # single left
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:  # 左重需要右旋
                # Do an RL Rotation
                self.rotateLeft(node.leftChild)  # 左子节点右重先左旋
                self.rotateRight(node)
            else:
                # single right
                self.rotateRight(node)

    def rotateLeft(self, rotRoot):
        """旋转左子树，选择调整左子树平衡性"""
        newRoot = rotRoot.rightChild
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild != None:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        # 仅有两个节点需要调整因子
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)

    def rotateRight(self, rotRoot):
        """旋转右子树，选择调整右子树平衡性"""
        newRoot = rotRoot.leftChild
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild != None:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isRightChild():
                rotRoot.parent.rightChild = newRoot
            else:
                rotRoot.parent.leftChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        # 仅有两个节点需要调整因子
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)


class TreeNode(object):
    """二叉搜索树节点"""
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key  # 键值
        self.payload = val  # 数据项
        self.leftChild = left  # 左子节点
        self.rightChild = right  # 右子节点
        self.parent = parent  # 父节点
        self.balanceFactor = 0  # 平衡因子

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):  # 是否根节点
        return not self.parent

    def isLeaf(self):  # 是否叶节点
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def __iter__(self):
        """迭代器函数用来for函数，实际上递归函数yield是对每次迭代的返回值，
        中序遍历的迭代
        BST类中的 __iter__方法直接调用了TreeNode中同名方法"""
        if self:   # 根不为空，基本结束条件
            if self.hasLeftChild():  # 左子树不为空
                for elem in self.leftChild:  # 遍历左子树
                    yield elem      # 生成器，返回左子树一个元素
            yield self.key          # 生成器，返回根
            if self.hasRightChild():    # 右子树不为空
                for elem in self.rightChild:  # 遍历右子树
                    yield elem      # 生成器，返回右子树一个元素

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftchild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def spliceOut(self):
        """摘出节点"""
        if self.isLeaf():  # 挑出叶子节点
            if self.isLeftChild():
                self.parent.leftChild = None
            else:
                self.parent.rightChild = None  # 同时有两个左右子树，有左下角的情况，不会执行该代码
        elif self.hasAnyChildren():
            if self.hasLeftChild():  # 挑出左子节点
                if self.isLeftChild():  # 这一块if-else,在同时有两个左右子树，有左下角的情况，不会执行该代码
                    self.parent.leftChild = self.leftChild
                else:
                    self.parent.rightChild = self.leftChild
            else:  # 挑出带右子节点的节点
                if self.isLeftChild():
                    self.parent.leftChild = self.rightChild
                else:
                    self.parent.rightChild = self.rightChild  # 摘出带右子节点的节点
                self.rightChild.parent = self.parent

    def findSuccessor(self):
        """寻找后继节点"""
        succ = None
        if self.hasRightChild():
            succ = self.rightChild.findMin()
        else:
            if self.parent:  # 教材中的代码，处理的是情况是，该节点没有右子树，需要去其他地方找后继，但是在本例中，前提就是当前节点同时有左右子树
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ

    def findMin(self):
        """当前节点的右子节点，左子树的最左下角的值"""
        current = self
        while current.hasLeftChild():  # 直到找到最左下角的值，就是直接后继
            current = current.leftChild
        return current

################################TESTCASE#########################################################
import unittest
import time

class TreeTestCase(unittest.TestCase):


    def setUp(self):
        self.bst = BinarySearchTree()
        self.t0 = time.time()

    def tearDown(self):
        print(f'case cost time:{time.time() - self.t0}')

    def test_deep3_tree_put_get(self):
        """
        {50:'a', 10:'b', 75:'c', 25:'d', 9:'e', 10:'f', 61:'g', 80:'h', 0:'i'}
               a
           b      c
         e  d   g   h
       i    f
        :return:
        """
        self.bst.put(50, 'a')
        self.bst.put(10, 'b')
        self.bst.put(75, 'c')
        self.bst.put(25, 'd')
        self.bst.put(9, 'e')
        self.bst.put(10, 'f')
        self.bst.put(61, 'g')
        self.bst.put(80, 'h')
        self.bst.put(0, 'i')
        print(f'bst root:{self.bst.root}')

        assert self.bst.root.payload == 'a'
        assert self.bst.root.key == 50
        assert self.bst.get(50) == 'a'
        assert self.bst.get(10) == 'b'  # 只记得第一个值
        assert self.bst.get(75) == 'c'
        assert self.bst.get(25) == 'd'
        assert self.bst.get(9) == 'e'

        assert self.bst.get(61) == 'g'
        assert self.bst.get(80) == 'h'
        assert self.bst.get(0) == 'i'
        assert self.bst.root.leftChild.key == 10
        assert self.bst.root.leftChild.payload == 'b'
        assert self.bst.root.leftChild.rightChild.key == 25
        assert self.bst.root.leftChild.rightChild.payload == 'd'
        assert self.bst.root.leftChild.rightChild.hasAnyChildren is not None
        assert self.bst.root.leftChild.rightChild.rightChild is None
        assert self.bst.root.leftChild.rightChild.leftChild is not None
        assert self.bst.root.leftChild.rightChild.leftChild.key == 10
        assert self.bst.root.leftChild.rightChild.leftChild.payload == 'f'

        assert self.bst.root.rightChild.key == 75
        assert self.bst.root.rightChild.payload == 'c'

    def testDoulbePut10(self):
        self.bst.put(30, 'rx')
        assert self.bst.get(30) == 'rx'
        assert self.bst.root.key == 30
        assert self.bst.root.payload == 'rx'
        assert self.bst.root.leftChild is None
        assert self.bst.root.rightChild is None
        assert self.bst.root.hasAnyChildren() == None

        print(f'bsr1 root:{self.bst.get(30), self.bst.root, self.bst.root.key, self.bst.root.payload, self.bst.length()}')
        print(f'root not have child: {self.bst.root.hasAnyChildren()}')
        self.bst.put(10, 'ax')
        assert self.bst.root.leftChild.key == 10
        assert self.bst.root.leftChild.payload == 'ax'
        assert self.bst.root.rightChild is None
        assert self.bst.root.hasAnyChildren() is not False

        print(f'bsr1 root and left:{self.bst.get(10), self.bst.root.leftChild.key, self.bst.root.leftChild.payload, self.bst.length()}')
        print(f'root left child have non-child: {self.bst.root.leftChild.hasAnyChildren()}')
        self.bst.put(10, 'bx')
        assert self.bst.root.leftChild.rightChild.key == 10
        assert self.bst.root.leftChild.rightChild.payload == 'bx'
        assert self.bst.root.leftChild.leftChild is None
        assert self.bst.root.rightChild is None
        assert self.bst.root.leftChild.hasAnyChildren() is not None
        assert self.bst.root.leftChild.rightChild is not None

        print(f'bsr1 root and left:{self.bst.get(10), self.bst.root.leftChild.key, self.bst.root.leftChild.payload, self.bst.length()}')
        print(f'root left child have non-child: {self.bst.root.leftChild.hasAnyChildren()}')



if __name__ == '__main__':
    import time

    lis1 = [1, 12, 3, 32, 14, 21, 35, 21, 12, 123, 42, 21, 32, 42]
    bst1 = BinarySearchTree()

    # print(f'bsr1 root root-left-right:{bst1.get(10), bst1.root.leftChild.rightChild.key, bst1.root.leftChild.rightChild.payload, bst1.length()}')
    #
    # print(f'root左侧为None:{bst1.root.leftChild}, 第二个10应该在 右侧: {bst1.root.rightChild.key, bst1.root.rightChild.payload}')

    # unittest.main()
    x = BinaryTree('a')
    insertLeft(x, 'b')
    insertRight(x, 'c')
    insertRight(getRightChild(x), 'd')
    insertLeft(getRightChild(getRightChild(x)), 'e')


    """
    testlist = [0,1,2,3,7,8,13,25,258,1992,]
    t0 = time.clock()
    print(binarySearch(testlist, 258))
    print('timeit:{}'.format(time.clock() - t0))

    t1 = time.clock()
    print(binarySearch(testlist, 125))
    print('timeit2:{}'.format(time.clock() - t1))

    t2 = time.clock()
    print(recursionSearch(testlist, 258))
    print('timeit3:{}'.format(time.clock() - t2))
     
    t3 = time.clock()
    alist = [1, 3, 45, 3, 43434, 3, 2, 3, 43, 23, 534]
    print(bubbleSort([1, 3, 45, 3, 43434, 3, 2, 3, 43, 23, 534]))
    print('timeit3:{}'.format(time.clock() - t3))

    t4 = time.clock()
    print(shortBubbleSort(alist))
    print('timeit4:{}'.format(time.clock() - t3))

    t5 = time.clock()
    print(selectionSorting(alist))
    print('timeit5:{}'.format(time.clock() - t5))

    t6 = time.clock()
    print(f"插入排序:{insertionSort(alist)}")
    print('timeit6:{}'.format(time.clock() - t6))

    t7 = time.clock()
    print(f"shellSort: {shellSort(alist)}")
    print('timeit7:{}'.format(time.clock() - t7))


    t8 = time.time()
    alist = [1, 3, 45, 3, 43434, 3, 2, 3, 43, 23, 534]
    print(f'归并排序:{merge_sort(alist)}')
    print('timeit8:{}'.format(time.clock() - t8))


    t9=time.time()
    alist = [54,26,93,17,77,31,44,55,20]
    print(f'快速排序:{QuickSort.quickSort(alist)}')
    print('timeit9:{}'.format(time.clock() - t9))
    """
