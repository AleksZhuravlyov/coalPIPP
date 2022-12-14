import sys
import os
import pandas as pd
import numpy as np

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))


def optimized_df(props, time, press_in, press_out,
                 consumption_fact, consumption_calc,
                 consumption__rel_err):
    a_dens = props.a_dens
    b_dens = props.b_dens
    time_index = pd.Index(time, dtype=float)
    optimized_sample = pd.DataFrame(time_index, dtype=float)
    Q_fact = np.array(consumption_fact.copy()) / (a_dens * 1.E+5 + b_dens)
    optimized_sample['Qoutlet (fact), st. m3/s'] = Q_fact
    Q_calc = np.array(consumption_calc.copy()) / (a_dens * 1.E+5 + b_dens)
    optimized_sample['Qoutlet (calc), st. m3/s'] = Q_calc
    optimized_sample['Pinlet, Pa'] = press_in
    optimized_sample['Poutlet, Pa'] = press_out
    optimized_sample['Gerror'] = consumption__rel_err.copy()
    optimized_sample.index.name = 'time, s'
    return optimized_sample




