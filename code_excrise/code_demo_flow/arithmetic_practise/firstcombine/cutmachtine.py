# 切割法 合并两个有序队列
import time
t0 = time.time()
set1 = [1,2,4,5,7,9]
set2 = [3,5,6,8,10,11]
s1c = set1.copy()
s2c = set2.copy()
set3 = []

# while set1:
#     s1 = set1.pop(0)
for s1 in set1:
    print(f"now len set1:{len(set1)} and set2:{len(set2)}")
    while set2:
        s2 = set2[0]
        if s1 < s2:
            set3.append(s1)
            break
        else:
            set3.append(s2)
            set2.remove(s2)
    else:
        set3.extend(set1)
    print(f"now set3:{set3}")
else:
    set3.extend(set2)

cost1 = time.time() - t0
print(f"finally set3:{set3}, cost time:{cost1}")

time.sleep(1)
#################################内建排序方法#########################################
t1 = time.time()
s4 = sorted(s1c + s2c)
cost2 = time.time() - t1
print(f"sorted cost time:{cost2}, finally:{s4}")
