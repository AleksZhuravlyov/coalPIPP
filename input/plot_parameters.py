import sys
import os
import matplotlib.pyplot as plt

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))


def plot_parameters(data_sample, title='parameters', y_min=None, y_max=None,
                    y2_min=None, y2_max=None, is_plot_saved=False):
    ax1 = data_sample[data_sample.columns[
        data_sample.columns != 'Qoutlet, st. m3/s']].plot(legend=True,
                                                          marker='o',
                                                          markersize=1.2,
                                                          figsize=(8, 5))
    if y_min is not None and y_max is not None:
        ax1.set_ylim([float(y_min), float(y_max)])

    ax2 = data_sample['Qoutlet, st. m3/s'].plot(ax=ax1, secondary_y=True,
                                                legend=True, marker='o',
                                                markersize=1.2)
    if y2_min is not None and y2_max is not None:
        ax2.set_ylim([float(y2_min), float(y2_max)])

    ax1.set_title(title)

    ax1.set_ylabel('pressure, Pa')
    ax2.set_ylabel('consumption, m3/s')

    ax1.grid(True, which='major', axis='y')
    ax1.grid(True, which='major', axis='x')

    ax1.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

    if is_plot_saved:
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.savefig(title + '.eps', format='eps')

    plt.show()
