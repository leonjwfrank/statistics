
class Stack(object):
    """自定义数据类型，栈的py实现"""
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, value):
        self.items.append(value)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[len(self.items)-1]  # 返回最上层数据
    def size(self):
        return len(self.items)

def infixToPostfix(infixexpr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = list(infixexpr) # .split()    # 解析表达式到单词列表
    print('tokenList:{}'.format(tokenList))
    words = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = "0123456789"
    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  or token in "0123456789":
            postfixList.append(token)        # 操作数
            print('num postfixList:{}'.format(postfixList))
        elif token == "(":
            opStack.push(token)
            print(' ( postfixList:{}'.format(postfixList))
        elif token == ")":
            topToken = opStack.pop()
            while topToken != "(":
                postfixList.append(topToken)
                topToken = opStack.pop()
                print(' ) postfixList:{}'.format(postfixList))
        else:     # 操作符
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
                print('peek postfixList:{}'.format(postfixList))
            opStack.push(token)
        print('sign postfixList:{}'.format(postfixList))
    while not opStack.isEmpty():
        postfixList.append(opStack.pop())    # 操作符
    print('last postfixList:{}'.format(postfixList))
    return " ".join(postfixList)   # 合成后缀表达式字符

if __name__ == '__main__':
    print(infixToPostfix('A+B*C'))