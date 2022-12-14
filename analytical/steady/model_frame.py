import sys
import os
import configparser
import numpy as np

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../../'))

from input import Props, Parameters


class ModelFrame:
    def __init__(s, config_file, polynomial_degree):
        s.parameters = Parameters(config_file)
        s.parameters.process_steady()

        s.__config = configparser.ConfigParser()
        s.__config.read(config_file)

        s.polynomial_degree = int(polynomial_degree)
        s.n_time_points = len(s.parameters.steady.index)

        s.props = Props(config_file)

        s.G_fact = np.array(s.parameters.steady['Qoutlet, st. m3/s']).copy()
        s.G_fact *= s.props.a_dens * 1.E+5 + s.props.b_dens
        s.G_calc = None
        s.G_rel_err = None

        s.G_theta_der = None
        s.A_leastsq = None
        s.F_leastsq = None

        s.theta = None
        s.theta_path = list()

        s.theta_perm_file = current_path + '/../../' + s.__config.get('Matching', 'theta_perm_file')

    def __str__(s):
        out_str = 'polynomial_degree ' + str(s.polynomial_degree)
        out_str += '\nn_time_points ' + str(s.n_time_points)
        out_str += '\n' + str(s.props)
        out_str += '\nperm_file ' + str(s.theta_perm_file)
        return out_str


if __name__ == '__main__':
    model_frame = ModelFrame(config_file=sys.argv[1], polynomial_degree=3)
    print(model_frame)
