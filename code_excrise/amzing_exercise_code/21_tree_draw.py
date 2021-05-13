import turtle

def tree(branch_len):
    t = turtle.Turtle()
    """向右画分形树"""
    t.pendown()
    t.forward(branch_len)
    t.penup()
    if branch_len > 5:
        t.left(20)
        tree(branch_len - 5)  # 45 35 25 15 5
        t.right(40)
        tree(branch_len - 5)  # 40 30  20  10
        t.left(20)
    t.backward(branch_len)

def solve(f, x1, x2):
    global x
    x = x + 1
    print('call num:{}'.format(x))
    mid = (x1 + x2) / 2
    if f(mid) == 0 or abs(x1 - x2) < 1e-8:
        print('call A num:{}'.format(x))
        return  mid# <A>
    elif f(mid) * f(x1) > 0:
        print('call B num:{}'.format(x))
        return solve(f, mid, x2) # <B>
    else:
        # return solve(f, x1, mid)# <C>
        print('call C num:{}'.format(x))
        # return mid
        return solve(f, x1, mid)  # <C>
if __name__ == '__main__':
    """
    # 分形树绘制
    # tree(50)
    # turtle.done()
    """
    x = 0
    def f(a,b=None):
        if not b:
            b = 0
        return (a + b)/2
    print(solve(f, -10, 12))
