# 一，py 实现一个栈类, 栈抽象数据的py实现
# 栈的基本操作包括，压入，弹出，判断空，大小判断等
class Stack(object):
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, value):
        self.items.append(value)      # 此时性能O(1) 比 insert(0, value)  O(n)高
    def pop(self):
        return self.items.pop()      # 默认弹出栈顶，性能高于 pop(n)
    def peek(self):
        return self.items[len(self.items)-1]  # 返回最上层数据
    def size(self):
        return len(self.items)


# 8，散列实现
class HashTable(object):
    """散列在最好的情况下，可以提供O(1)常数级 时间复杂度的查找性能由于散列冲突的存在，查找比较次数就没有这么简单
        如果λ较小，散列冲突的几率就小，数据项通常会保 存在其所属的散列槽中
        如果λ较大，意味着散列表填充较满，冲突会越来越 多，冲突解决也越复杂，也就需要更多的比较来找到 空槽;如果采用数据链的话，
        意味着每条链上的数据 项增多
        1,如果采用线性探测的开放定址法来解决冲 突(λ在0~1之间)
        成功的查找，平均需要比对次数为: 1/2(1+1/(1-𝛌))
        不成功的查找，平均比对次数为:1/2(1+1/(1-𝛌)^2)
        2,如果采用数据链来解决冲突(λ可大于1)
        成功的查找，平均需要比对次数为:1+λ/2
         不成功的查找，平均比对次数为:λ
        """

    def __init__(self):
        self.size = 11
        self.slots = [None] * self.size     # 散列插槽,其中一个slot列表用于保存key
        self.data = [None] * self.size      # 数据,平行的data列表用于保存数据项

    def hashfunciton(self, key):
        """hashfunction方法采用了简单求余方法来实现散列函数，而冲突解决则采用 线性探测“加1”再散列函数"""
        return key % self.size

    def rehash(self, oldhash):
        return (oldhash + 1) % self.size

    def put(self, key, data):
        hashvalue = self.hashfunciton(key)
        if self.slots[hashvalue] == None:  # key不存在，未发生冲突
            self.slots[hashvalue] = key
            self.data[hashvalue] = data
        else:
            if self.slots[hashvalue] == key:  # key已存在，替换val
                self.data[hashvalue] = data  # replace
            else:
                nextslot = self.rehash(hashvalue)
                # while 处理 散列冲突。同过再散列的方式，直到找到空槽或key
                while self.slots[nextslot] != None and self.slots[nextslot] != key:
                    nextslot = self.rehash(nextslot)
                if self.slots[nextslot] == None:
                    self.slots[nextslot] = key
                    self.data[nextslot] = data
                else:
                    self.data[nextslot] = data  # replace

    def get(self, key):
        startslot = self.hashfunciton(key)  # 标记散列值为查找起点

        data = None
        stop = False
        found = False
        position = startslot
        while self.slots[position] != None and not found and not stop:  # 找key，直到空槽或回到起点
            if self.slots[position] == key:
                found = True
                data = self.data[position]
            else:
                position = self.rehash(position)  # 未找到key，散列继续找
                if position == startslot:
                    stop = True  # 回到起点，停
        return data

    def get_base_info(self):
        print(f'散列插槽数{self.size}, 散列插槽值{self.slots}, 散列数据{self.data}')
        print(f'散列ks:{self.slots}')
        print(f'散列vs:{self.data}')

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, data):
        self.put(key, data)


if __name__ == '__main__':
    st = Stack()
    st.push(8)
    print(st.items)
    print(st.peek())
    print(st.size())
    data = [1, 35, 6, 5, 7, 9, 11]
    ht = HashTable()
    ht[1] = "c"
    ht[2] = "b"
    ht[3] = "a"
    print(f'散列信息{ht.get_base_info()}')
    ht.put(1, 121)

    print(f'散列信息{ht.get_base_info()}')
    print(f'散列put:{ht.put(35, 121)}')
    print(f'散列位置:{ht.get(1)}')
    ht.put(1, 1331)
    print(f'散列位置:{ht.get(121)}')
    print(f'散列信息1 {ht.get_base_info()}')
    ht[1] = 1332
    print(f'散列信息2 {ht.get_base_info()}')


    def func(str1):
        s = Stack()
        for char in str1:
            s.push(char)
        str2 = ''
        while not s.isEmpty():
            str2 += s.pop()
        return str2
    print(func('abcdefg'))

