import sys
import os
import numpy as np
import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../../'))

from analytical.steady.model_frame import ModelFrame
from output import optimized_df


class Model(ModelFrame):
    def __init__(s, config_file, polynomial_degree):
        super().__init__(config_file, polynomial_degree)

        s.calculate_G_theta_der()

    def calculate_G_theta_der(s):
        a_dens = s.props.a_dens
        b_dens = s.props.b_dens
        length = s.props.length
        visc = s.props.visc
        k1 = np.arange(s.polynomial_degree + 1) + 1
        k2 = np.arange(s.polynomial_degree + 1) + 2
        P_in = s.parameters.steady['Pinlet, Pa'].to_numpy()
        P_out = s.parameters.steady['Poutlet, Pa'].to_numpy()        

        diff_press_k1 = np.power.outer(P_in, k1) - np.power.outer(P_out, k1)
        s.G_theta_der = diff_press_k1 * b_dens / k1 / length / visc
        diff_press_k2 = np.power.outer(P_in, k2) - np.power.outer(P_out, k2)
        s.G_theta_der += diff_press_k2 * a_dens / k2 / length / visc
        s.G_theta_der *= s.props.area

    def calculate_leastsq_problem(s):
        s.F_leastsq = np.dot(s.G_fact, s.G_theta_der)
        s.A_leastsq = np.dot(s.G_theta_der.transpose(), s.G_theta_der)
        s.theta = np.linalg.solve(s.A_leastsq, s.F_leastsq)

    def calculate_G_using_theta(s):
        s.G_calc = np.dot(s.G_theta_der, s.theta)

    def save_theta(s):
        np.savetxt(s.theta_perm_file, s.theta)

    def calculate_G_rel_err(s):
        s.G_rel_err = np.absolute((s.G_calc.transpose() - s.G_fact) / s.G_fact)
        s.G_rel_err = s.G_rel_err.transpose()

    def clear_theta_path(s):
        s.theta_path.clear()

    def empirical_risk(s, theta):
        s.theta = theta
        s.calculate_G_using_theta()
        s.calculate_G_rel_err()
        s.theta_path.append(theta)
        return s.G_rel_err.mean(axis=0)

    def return_optimized_case(s):
        return optimized_df(s.props, s.parameters.steady.index,
                            np.array(s.parameters.steady['Pinlet, Pa']),
                            np.array(s.parameters.steady['Poutlet, Pa']),
                            s.G_fact, s.G_calc, s.G_rel_err)


if __name__ == '__main__':
    model = Model(config_file=sys.argv[1], polynomial_degree=3)
    print(model)
