import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../../'))

from output import plot_optimized_sample
from analytical.steady import Model


class AnalyticalAnalytical(Model):
    def __init__(s, config_file, polynomial_degree):
        super().__init__(config_file, polynomial_degree)

    def calculate(s):
        s.calculate_leastsq_problem()
        s.calculate_G_using_theta()
        s.save_theta()
        s.calculate_G_rel_err()

    def plot(s, is_plot_saved=False):
        data_sample = s.return_optimized_case()
        plot_optimized_sample(data_sample, s.theta, s.props,
                              'Analytical Steady State Analytical Optimisation',
                              is_plot_saved=is_plot_saved)


if __name__ == '__main__':
    analytical_analytical = AnalyticalAnalytical(config_file=sys.argv[1],
                                                 polynomial_degree=3)
    print(analytical_analytical)
    analytical_analytical.calculate()
    analytical_analytical.plot(is_plot_saved=False)
