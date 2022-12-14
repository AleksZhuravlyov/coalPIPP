import sys
import os
import pandas as pd
import configparser

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))

from input import plot_parameters


class Parameters:
    def __init__(s, config_file):
        s.config = configparser.ConfigParser()
        s.config.read(config_file)

        s.parameters_file = current_path + '/../' + str(s.config.get('Main', 'parameters_file'))

        s.origin = None
        s.entire = None
        s.steady = None
        s.transient = None

    def __str__(s):
        out_str = 'parameters_file ' + str(s.parameters_file)
        return out_str

    def process_origin(s):
        s.origin = pd.read_csv(s.parameters_file, index_col='time',
                               parse_dates=True)
        s.origin.index.name = 'time'
        s.origin.columns.name = 'parameters'

    def process_entire(s):
        if s.origin is None:
            s.process_origin()
        s.entire = s.origin.copy()
        s.__data_to_seconds(s.entire)

    def process_steady(s):
        if s.origin is None:
            s.process_origin()
        s.steady = s.origin.copy()
        s.__data_to_seconds(s.steady)
        time_min = float(s.config.get('Steady', 'time_min'))
        time_max = float(s.config.get('Steady', 'time_max'))
        s.steady = s.steady[s.steady.index >= time_min]
        s.steady = s.steady[s.steady.index <= time_max]

    def process_transient(s):
        if s.origin is None:
            s.process_origin()
        s.transient = s.origin.copy()
        s.__data_to_seconds(s.transient)
        time_min = float(s.config.get('Transient', 'time_min'))
        time_max = float(s.config.get('Transient', 'time_max'))
        s.transient = s.transient[s.transient.index >= time_min]
        s.transient = s.transient[s.transient.index <= time_max]

    def __data_to_seconds(s, data_sample):
        time_series = pd.Series(s.origin.index - s.origin.index[0])
        data_sample.index = time_series.dt.total_seconds()
        data_sample.index.name = 'time, s'

    def plot(s, data_sample_type='origin',
             y_min=None, y_max=None, y2_min=None, y2_max=None,
             is_plot_saved=False):
        if data_sample_type == 'origin':
            if s.origin is None:
                s.process_origin()
            data_sample = s.origin
        elif data_sample_type == 'entire':
            if s.entire is None:
                s.process_entire()
            data_sample = s.entire
        elif data_sample_type == 'steady':
            if s.steady is None:
                s.process_steady()
            data_sample = s.steady
        elif data_sample_type == 'transient':
            if s.transient is None:
                s.process_transient()
            data_sample = s.transient

        plot_parameters(data_sample, data_sample_type,
                        y_min, y_max, y2_min, y2_max, is_plot_saved)

    def __str__(s):
        out_str = super().__str__()
        if s.origin is not None:
            out_str += '\norigin ' + '\n' + str(s.origin)
        if s.entire is not None:
            out_str += '\nentire ' + '\n' + str(s.entire)
        if s.steady is not None:
            out_str += '\nsteady ' + '\n' + str(s.steady)
        if s.transient is not None:
            out_str += '\ntransient ' + '\n' + str(s.transient)

        return out_str


if __name__ == '__main__':
    parameters = Parameters(config_file=sys.argv[1])
    parameters.process_entire()
    parameters.plot('entire', is_plot_saved=False)
    # parameters.process_steady()
    # parameters.plot('steady', is_plot_saved=True)
    # parameters.process_transient()
    # parameters.plot('transient', is_plot_saved=True)
