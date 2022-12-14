from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits import mplot3d
import numpy as np


def function_explicit_arg(x1, x2):
    return .5 * (1 - x1) ** 2 + (x2 - x1 ** 2) ** 2


x_min = 0.9
x_max = 1.1
# x_n = 101
y_min = 0.9
y_max = 1.1
# y_n = 101
#
# x_linspace = np.linspace(x_min, x_max, x_n, dtype=float)
# y_linspace = np.linspace(y_min, y_max, y_n, dtype=float)
# x_mesh, y_mesh = np.meshgrid(x_linspace, y_linspace)
# z_mesh = function(x_mesh, y_mesh)
#
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.plot_surface(x_mesh, y_mesh, z_mesh, rstride=1, cstride=1,
#                 cmap=mpl.cm.RdYlGn, edgecolor='none')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# plt.show()
#

# plt.imshow(z_mesh, interpolation='bilinear', cmap=mpl.cm.RdYlGn,
#            extent=[x_min, x_max, y_min, y_max])
# plt.show()

ini = np.array([2, -1], dtype=float)
ranges_var = ((x_min, x_max), (y_min, y_max))


def f(x):
    return function_explicit_arg(x[0], x[1])


def jacobi(x):
    return np.array((-2 * .5 * (1 - x[0]) - 4 * x[0] * (x[1] - x[0] ** 2),
                     2 * (x[1] - x[0] ** 2)))


def hessi(x):
    return np.array(
        ((1 - 4 * x[1] + 12 * x[0] ** 2, -4 * x[0]), (-4 * x[0], 2)))


# result = optimize.minimize(f, ini, method="CG")
# result = optimize.minimize(f, ini, method="CG", jac=jacobi)
# result = optimize.minimize(f, ini, method="Newton-CG", jac=jacobi)
# result = optimize.minimize(f, ini, method="Newton-CG", jac=jacobi, hess=hessi)
# result = optimize.minimize(f, ini, method="BFGS")
# result = optimize.minimize(f, ini, method="BFGS", jac=jacobi)
# result = optimize.minimize(f, ini, method="BFGS", jac=jacobi, hess=hessi)
# result = optimize.minimize(f, ini, method="L-BFGS-B")
# result = optimize.minimize(f, ini, method="L-BFGS-B", jac=jacobi)
# result = optimize.minimize(f, ini, method="Nelder-Mead")
# result = optimize.brute(f, ranges=ranges_var, Ns=100)
# result = optimize.minimize(f, ini, bounds=ranges_var, method="L-BFGS-B")
result = optimize.minimize(f, ini, bounds=ranges_var, method="SLSQP")

print(result)
