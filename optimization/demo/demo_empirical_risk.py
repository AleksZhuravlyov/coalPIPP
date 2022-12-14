import sys
import os
import numpy as np
from scipy import optimize
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits import mplot3d

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../../'))

from analytical.steady import Model

# steady_base.calculate_leastsq_problem()
# steady_base.calculate_G_using_theta()
# print('theta', steady_base.theta)
# print('empirical_risk', steady_base.empirical_risk(steady_base.theta))

# theta [ 1.01981958e-17 -2.96625640e-23  3.77621746e-29 -1.52247176e-35]
# empirical_risk 0.010973483448981547
#
# theta [ 5.40782539e-18 -7.14761522e-24  4.85049676e-30]
# empirical_risk 0.006436372856344486
#
# theta [ 3.16876166e-18 -2.68279152e-25]
# empirical_risk 0.017919535639444453
#
# theta [2.98489933e-18]
# empirical_risk 0.04099687689351021
#


theta_origin = np.array(
    [4.155892311521897426e-15, -1.294967296317188997e-20,
     1.683918917425242538e-26, -6.975107574216326758e-33],
    dtype=float)
degree = 3
#
# theta_origin = np.array(
#     [5.40782539e-18, -7.14761522e-24, 4.85049676e-30],
#     dtype=float)
# degree = 2
#
# theta_origin = np.array(
#     [3.16876166e-18, -2.68279152e-25],
#     dtype=float)
# degree = 1

ini = theta_origin.copy()
ini[-1] = 0
model = Model(config_file=sys.argv[1], polynomial_degree=degree)

theta_n = 101
rate_min_max = 0.5

theta_min = np.where(theta_origin >= 0, theta_origin * (1 - rate_min_max),
                     theta_origin * (1 + rate_min_max))

theta_max = np.where(theta_origin >= 0, theta_origin * (1 + rate_min_max),
                     theta_origin * (1 - rate_min_max))

# optimization = optimize.minimize(steady_base.empirical_risk, ini,
#                                  method="Nelder-Mead")

# print('optimization', optimization)

x0_i = 0
x1_i = 1

axes = list()
empirical_risk_slice = list()
for i in range(len(theta_origin)):
    if i != x0_i and i != x1_i:
        axes.append(np.array([theta_origin[i]], dtype=float))
        empirical_risk_slice.append(i)
    else:
        axes.append(np.linspace(theta_min[i], theta_max[i], theta_n))
empirical_risk_slice = tuple(empirical_risk_slice)

x_mesh0, x_mesh1, x_mesh2, x_mesh3 = np.array(
    np.meshgrid(axes[1], axes[0], axes[2], axes[3]))
x_mesh = np.array([x_mesh1, x_mesh0, x_mesh2, x_mesh3])

theta = np.stack(x_mesh, axis=-1)

plot_mesh = np.array(np.meshgrid(*[axes[x0_i], axes[x1_i]]))

transp_mask = np.arange(len(theta.shape))
transp_mask[-1], transp_mask[-2] = transp_mask[-2], transp_mask[-1]
transp_mask = tuple(transp_mask)

empirical_risk_mesh = model.empirical_risk(theta.transpose(transp_mask))

empirical_risk_mesh = np.squeeze(empirical_risk_mesh, axis=empirical_risk_slice)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(plot_mesh[0], plot_mesh[1], empirical_risk_mesh,
                rstride=1, cstride=1, cmap=mpl.cm.RdYlGn, edgecolor='none')
ax.set_zlabel('empirical_risk')

# fig, ax = plt.subplots(1, 1)
# min_max = [theta_min[x0_i], theta_max[x0_i], theta_min[x1_i],
#            theta_max[x1_i]]
# plt.imshow(empirical_risk_mesh, cmap=mpl.cm.RdYlGn, extent=min_max,
#            origin='lower', aspect='auto')
# plt.colorbar()

fig.suptitle('empirical risk')
ax.set_xlabel('x' + str(x0_i))
ax.set_ylabel('x' + str(x1_i))

plt.show()
