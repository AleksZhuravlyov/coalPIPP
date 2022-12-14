import sys
import os
import numpy as np
from scipy import optimize
import configparser

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../../'))

from output import plot_optimized_sample, optimized_df
from input import Props, Parameters
from numerical import Transient


class NumericalScipy:
    def __init__(s, config_file, polynomial_degree, theta_ini):
        s.__config = configparser.ConfigParser()
        s.__config.read(config_file)

        s.polynomial_degree = polynomial_degree

        s.props = Props(config_file)
        props_array = s.props.get_props_array()
        theta_files_array = s.props.get_theta_files_array()

        s.theta_ini = theta_ini
        s.theta = None
        s.theta_file = current_path + '/../../' + s.__config.get('Matching', 'theta_poro_file')

        s.parameters = Parameters(config_file)
        s.parameters.process_transient()
        time = s.parameters.transient.index.to_numpy()
        press_in = s.parameters.transient['Pinlet, Pa'].to_numpy()
        press_out = s.parameters.transient['Poutlet, Pa'].to_numpy()
        consumption = s.parameters.transient['Qoutlet, st. m3/s'].to_numpy()
        consumption *= s.props.a_dens * 1.E+5 + s.props.b_dens
        s.transient = Transient(props_array, theta_files_array,
                                time, press_in, press_out, consumption)
        s.transient.load_theta_perm()

    def save_theta(s):
        np.savetxt(s.theta_file, s.theta)

    def calculate(s):
        optimization = optimize.minimize(s.transient.calculate_empirical_risk,
                                         s.theta_ini, method="Nelder-Mead")
        s.theta = optimization.x
        s.save_theta()

    def plot(s, is_plot_saved=False):
        s.transient.load_theta_poro()
        s.transient.calculate_consumptions()

        data_sample = optimized_df(s.props, s.transient.time,
                                   s.transient.press_in, s.transient.press_out,
                                   s.transient.consumption_fact,
                                   s.transient.consumption_calc,
                                   s.transient.consumption_rel_err)

        plot_optimized_sample(data_sample, s.theta, s.props,
                              'Numerical Transient State SciPy Optimisation',
                              theta_type='poro', is_plot_saved=is_plot_saved)

    def __str__(s):
        out_str = '\ntheta_ini ' + str(s.theta_ini)
        return out_str


if __name__ == '__main__':
    degree = 1
    ini = np.zeros(degree + 1, dtype=float)
    ini[0] = 0.01

    numerical_scipy = NumericalScipy(config_file=sys.argv[1],
                                     polynomial_degree=degree,
                                     theta_ini=ini)
    numerical_scipy.calculate()
    numerical_scipy.plot(is_plot_saved=True)
