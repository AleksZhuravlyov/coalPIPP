import sys
import os
import configparser
import numpy as np

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))


class Props:
    def __init__(s, config_file):
        s.__config = configparser.ConfigParser()
        s.__config.read(config_file)
        get = s.__config.get

        s.a_dens = float(get('Properties', 'a_dens'))
        s.b_dens = float(get('Properties', 'b_dens'))
        s.visc = float(get('Properties', 'visc'))
        s.length = float(get('Properties', 'length'))
        s.area = float(get('Properties', 'area'))
        s.grid_block_n = float(get('Properties', 'grid_block_n'))
        s.delta_volume = s.length * s.area / s.grid_block_n
        s.delta_length = s.length / s.grid_block_n
        s.iterative_accuracy = float(get('Properties', 'iterative_accuracy'))

        s.theta_perm_file = current_path + '/../' + str(get('Matching', 'theta_perm_file'))
        s.theta_poro_file = current_path + '/../' + str(get('Matching', 'theta_poro_file'))

    def get_props_array(s):
        props_list = list()
        props_list.append(s.a_dens)
        props_list.append(s.b_dens)
        props_list.append(s.visc)
        props_list.append(s.length)
        props_list.append(s.area)
        props_list.append(s.grid_block_n)
        props_list.append(s.delta_volume)
        props_list.append(s.delta_length)
        props_list.append(s.iterative_accuracy)
        return np.array(props_list, dtype=float)

    def get_theta_files_array(s):
        theta_files_list = list()
        theta_files_list.append(s.theta_perm_file)
        theta_files_list.append(s.theta_poro_file)
        return np.array(theta_files_list, dtype=str)

    def __str__(s):
        out_str = 'a_dens ' + str(s.a_dens)
        out_str += '\nb_dens ' + str(s.b_dens)
        out_str += '\nvisc ' + str(s.visc)
        out_str += '\nlength ' + str(s.length)
        out_str += '\narea ' + str(s.area)
        out_str += '\ngrid_block_n ' + str(s.grid_block_n)
        out_str += '\ndelta_volume ' + str(s.delta_volume)
        out_str += '\ndelta_length ' + str(s.delta_length)
        out_str += '\niterative_accuracy ' + str(s.iterative_accuracy)
        out_str += '\ntheta_perm_file ' + s.theta_perm_file
        out_str += '\ntheta_poro_file ' + s.theta_poro_file

        return out_str


if __name__ == '__main__':
    props = Props(config_file=sys.argv[1])
    print(props)

