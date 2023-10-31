import sys

sys.setrecursionlimit(10 ** 7)

result = 0

def f(n):
    if n == 1:
        return 1
    else:
        return n + f(n - 1)

for i in range(1, 101):
    if f(2023)//f(i) % 2 == 0:
        result += 1

print(result)