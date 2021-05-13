"""
stack 的 py 的应用
  ~~~~~
    应用示例
    1, 括号配对应用
    2, 进制的转换应用
    3, 表达式的转换
    4, 后缀表达式的求值
    :copyright: ©ydxue
    :author: ydxue
    :contact: autocommsky@gmail.com

for example to find all sub list
```python36 base
"""

# 1.1，栈的应用，高级语言的基础算法，简单括号匹配
# 栈也可以用于 XML,HTML的成对的关键字匹配校验
# 括号一般用来指定表达式的运算优先级，多层括号的层级是否正确如，((()), ())))))
# 规则，按栈的方式取值，第一个左括号 匹配 第一个右括号
#  推广到 开闭校验，如 html
from Stack import Stack

def parChecker(symb_str):
    """括号成对匹配"""
    s = Stack()
    balanced = True  # 判断是否对称
    index = 0
    while index < len(symb_str) and balanced:
        symb = symb_str[index]
        if symb in "([{":
            s.push(symb)
        else:
            if s.isEmpty():
                balanced = False
            else:
                top = s.pop()
                if not matched(top, symb):  # 右括号是否与原 左括号匹配
                    balanced = False
        index = index + 1
    if balanced and s.isEmpty():
        return True
    else:
        return False


def matched(op, cs):
    opens = "([{"  #
    closers = ")]}"  # 与opens需要对应
    return opens.index(op) == closers.index(cs)


def  divideBy2(decNumber, n=None):
    """
    # 1.2，栈的应用，十进制转化为二进制
    # 人类常用的计算方法为 十进制，计算机计算方法为二进制
    # 高级语言算法 会经常对 十进制和二进制进行转换
    # 十进制转换为二进制，采用的是 除以2求余数的算法
    # 将整数不断除以2，每次得到的余数就是由低到高 的二进制
    # 35 / 2  = 17  余 1  -- k0    # 低位
    # 17 /2 = 8   余   1  -- k1
    # 8/2 = 4   余  0  -- k2
    # 4/2 = 2  余  0  -- k3
    # 2/2 = 1 余  0   -- k4
    # 1/2 = 0 余  1  --  k5     # 高位
    10进制转换为2进制，默认
    :params  decNumber 要转换的数字
    :params n 要转换为的进制，默认为2"""
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if not n:
        n = 2
    remstack = Stack()    # 栈来处理逆序算法
    while decNumber > 0:
        rem = decNumber % n       # 求余数
        remstack.push(rem)
        decNumber = decNumber // n    # 整数除
    binString = ''
    while not remstack.isEmpty():
        binString = binString + digits[remstack.pop()]   # 取相应进制组合成数字
    return binString


def infixToPostfix(infixexpr):
    """# 1.3，栈的应用，表达式转换
    # 中缀表达式。A*B 类似这样，操作符介于操作数 operabd 中间的表示法，称为 中缀 表示法
    # 有括号时，括号表示强制优先级，嵌套括号中，内层优先级更高
    # 以操作符相对于操作数的位置来定义，
    # 前缀表达式。+AB， A+B*C  的前缀表达式为   +A*BC
    # 后缀表达式。AB+,   A+B*C 的后缀表达式为   ABC*+
    # 中缀 转换为前缀或后缀表达式
    # 1，中缀表达式 转换为 全括号形式
    # 2，把运算符移到 左括号(前缀)  或 右括号(后缀)并替换，然后删除所有括号即可

    """
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
#     tokenList = infixexpr.split()    # 解析表达式到单词列表
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
    return "".join(postfixList)   # 合成后缀表达式字符


class fix_eval(object):
    """
    # 后缀表达式求值
    # 由于操作符在后缀表达式的后面，需要暂存操作数，在碰到操作符的时候，再将暂存的两个操作数进行实际的计算，
    # 利用栈的特点，操作符只作用于离它最近的两个操作数
    # 如后缀表达式 4 5 6 * +
    # 1，弹出两个操作数6，5，计算得到结果30， 先弹出的右操作数，后弹出的是左操作数，这对于 -/ 很重要
    # 2，将30 压入栈顶，继续扫描后面的符号
    # 3，所以操作符都处理完毕，栈中只留下1个操作数，这个数就是表达式的值

    # 代码步骤
    # 创建空栈operandStack 用于 暂存操作数
    # 将后缀表达式用split 方法解析为单词 token，从左到右扫描单词列表，如果单词是一个操作数，将单词转换为整数int，压入oparandStack 栈顶
    # 如果单词是一个操作符号 (*/+-), 就开始求值，从栈顶弹出2个操作数，先弹出的是右操作数，计算后重新压入栈顶
    # 单词扫描结束后，表达式的值就在栈顶
    # 弹出栈顶的值，返回
    """

    @staticmethod
    def doMath( op, op1, op2):
        if op == '*':
            return op1 * op2
        elif op == '/':
            return op1 / op2
        elif op == '+':
            return op1 + op2
        else:
            return op1 - op2

    @staticmethod
    def postfixEval(postfixExpr):
        operandStack = Stack()
        tokenList = list(postfixExpr)  # .split()
        #     tokenList = postfixExpr.split()
        print('tokenList:{}'.format(tokenList))
        for token in tokenList:
            #         if token in "0123456789":
            if isinstance(token, int):
                operandStack.push(int(token))  # 操作数
                print('operandStack:{}'.format(operandStack.items))
            else:
                operand2 = operandStack.pop()
                print('pop operand2:{}'.format(operand2))
                print('operandStack:{}'.format(operandStack.items))
                operand1 = operandStack.pop()
                print('pop operand1:{}'.format(operand1))
                print('operandStack:{}'.format(operandStack.items))
                result = fix_eval.doMath(token, operand1, operand2)  # 操作符
                operandStack.push(result)
                print('result operandStack:{}'.format(operandStack.items))
        rst = operandStack.pop()
        print('result:{}'.format(rst))
        del operandStack
        return rst

    @staticmethod
    def func1(str1):
        """按序列 中元素大小生成一个 可遍历对象，
        每一个元素大小组成的栈的长度 与前一个栈的大小相加，组成一个新的递增的序列

        """
        s1, s2 = Stack(), Stack()
        for char in str1:
            s1.push(char)
        print('s1:{}'.format(s1))
        lst2 = []
        while not s1.isEmpty():
            #         lst2.append(s1.peek())
            for i in range(s1.pop()):
                s2.push(i)
            lst2.append(s2.size())
        return lst2


if __name__ == '__main__':
    # 匹配括号
    print(parChecker('({{[[{]]}})'))
    print(parChecker('()'))

    # 进制转换
    print(divideBy2(42, 2))
    print(divideBy2(42, 8))
    print(divideBy2(42, 16))

    # 转换为后缀表达式
    print(infixToPostfix("A+(B*C)"))


    # 后缀表达式求值
    back_express = infixToPostfix("9-(7*2)")
    print('back_express:{}'.format(back_express))
    # print(postfixEval(back_express))
    # print(doMath("-", 10, 11))

    #
    print('rst:{}'.format(fix_eval.func1([1, 3, 5, 7, 9])))

