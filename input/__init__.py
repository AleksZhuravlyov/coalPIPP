import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_path, '../'))

from input.props import Props
from input.parameters import Parameters
from input.plot_parameters import plot_parameters
