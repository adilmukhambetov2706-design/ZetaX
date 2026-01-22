def square(side):
    y = side ** 2
    return y

def multiply(x, y):
    ans = x * y
    return ans

def find_min(a):
    mn = a[0]
    for b in a:
        if mn > b:
            mn = b
    return mn

