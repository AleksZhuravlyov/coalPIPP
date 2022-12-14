import sys
import os
import numpy as np
from scipy import optimize

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../../'))

from analytical.steady import Model
from output import plot_optimized_sample


class AnalyticalScipy(Model):
    def __init__(s, config_file, polynomial_degree, theta_ini):
        super().__init__(config_file, polynomial_degree)

        s.theta_ini = theta_ini

    def calculate(s):
        optimization = optimize.minimize(s.empirical_risk, s.theta_ini,
                                         method="Nelder-Mead")
        s.theta = optimization.x
        s.save_theta()
        s.calculate_G_using_theta()
        s.calculate_G_rel_err()

    def plot(s):
        data_sample = s.return_optimized_case()
        plot_optimized_sample(data_sample, s.theta, s.props,
                              'Analytical Steady State SciPy Optimisation')

    def __str__(s):
        out_str = super().__str__()
        out_str += '\ntheta_ini ' + str(s.theta_ini)
        return out_str


if __name__ == '__main__':
    degree = 1
    ini = np.zeros(degree + 1, dtype=float)
    ini[0] = 1.e-14

    analytical_scipy = AnalyticalScipy(config_file=sys.argv[1],
                                       polynomial_degree=degree,
                                       theta_ini=ini)
    print(analytical_scipy)
    analytical_scipy.calculate()
    analytical_scipy.plot()
