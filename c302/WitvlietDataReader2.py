# Temporary class to allow this to be used in comparison notebook.
# Should be tidied up.

from c302.W_SpreadsheetDataReader import WitvlietDataReader
from c302.ConnectomeReader import analyse_connections

wdr = WitvlietDataReader("witvliet_2020_8.xlsx")

read_data = wdr.read_data
read_muscle_data = wdr.read_muscle_data


def main2():
    cells, neuron_conns = read_data()
    neurons2muscles, muscles, muscle_conns = read_muscle_data()

    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)


if __name__ == "__main__":
    main2()
