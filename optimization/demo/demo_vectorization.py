import numpy as np


def f(x):
    a = np.array([1, 2])
    return np.dot(a, x)


x0 = np.arange(3, 5)
x1 = np.arange(2)

# x_left = np.arange(7)
# x_right = np.arange(3, 10)
x_left, x_right = np.meshgrid(np.arange(6), np.arange(3, 10))
print(x_left)
print(x_right)

x = np.stack((x_left, x_right), axis=-1)

# print('x0', x0)
# print('f(x0)', f(x0))
# print()
# print('x1', x1)
# print('f(x1)', f(x1))
# print()
print('x', x)
print()
print(x.transpose(0, 2, 1))
print()
print('f(x)', f(x.transpose(0, 2, 1)))
