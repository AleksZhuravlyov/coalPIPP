import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))

from numerical import Steady, Transient
from input import Props, Parameters

props = Props(config_file=sys.argv[1])
props_array = props.get_props_array()
theta_files_array = props.get_theta_files_array()

parameters = Parameters(config_file=sys.argv[1])

# parameters.process_steady()
# time = parameters.steady.index.to_numpy()
# press_in = parameters.steady['Pinlet, Pa'].to_numpy()
# press_out = parameters.steady['Poutlet, Pa'].to_numpy()
# consumption = parameters.steady['Qoutlet, st. m3/s'].copy().to_numpy()
# consumption *= props.a_dens * 1.E+5 + props.b_dens
# steady = Steady(props_array, theta_files_array,
#                 time, press_in, press_out, consumption)
#
# # theta_perm = np.loadtxt(props.theta_perm_file, dtype=float)
# # empirical_risk = steady.calculate_empirical_risk(theta_perm)
#
# steady.load_theta_perm()
# steady.calculate_consumptions()
# pd.DataFrame({'consumption_fact': steady.consumption_fact,
#               'consumption_calc': steady.consumption_calc}).plot()

parameters.process_transient()
time = parameters.transient.index.to_numpy()
press_in = parameters.transient['Pinlet, Pa'].to_numpy()
press_out = parameters.transient['Poutlet, Pa'].to_numpy()
consumption = parameters.transient['Qoutlet, st. m3/s'].copy().to_numpy()
consumption *= props.a_dens * 1.E+5 + props.b_dens
transient = Transient(props_array, theta_files_array,
                      time, press_in, press_out, consumption)
transient.load_theta_perm()

# theta_poro = np.loadtxt(props.theta_poro_file, dtype=float)
# empirical_risk = transient.calculate_empirical_risk(theta_poro)

transient.load_theta_poro()
transient.calculate_consumptions()
pd.DataFrame({'consumption_fact': transient.consumption_fact,
              'consumption_calc': transient.consumption_calc}).plot()

plt.show()
