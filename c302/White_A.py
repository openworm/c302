# Temporary class to allow this to be used in comparison notebook.
# Should be tidied up.

from c302.WhiteDataReader import White_A

from c302.ConnectomeReader import analyse_connections

read_data = White_A.read_data
read_muscle_data = White_A.read_muscle_data


def main1():
    cells, neuron_conns = read_data(include_nonconnected_cells=True)
    neurons2muscles, muscles, muscle_conns = read_muscle_data()
    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)


if __name__ == "__main__":
    main1()
