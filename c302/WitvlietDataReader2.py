# Temporary class to allow this to be used in comparison notebook. 
# Should be tidied up.

from c302.W_SpreadsheetDataReader import WitvlietDataReader2
from c302.NeuroMLUtilities import analyse_connections

read_data = WitvlietDataReader2.read_data
read_muscle_data = WitvlietDataReader2.read_muscle_data


def main2():

    cells, neuron_conns = read_data(include_nonconnected_cells=True)
    neurons2muscles, muscles, muscle_conns = read_muscle_data()

    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)


if __name__ == '__main__':
    main2()