from c302.NeuroMLUtilities import ConnectionInfo
from c302.NeuroMLUtilities import analyse_connections

from openpyxl import load_workbook
import os

spreadsheet_location = os.path.dirname(os.path.abspath(__file__))+"/data/"


from c302 import print_

def read_data(include_nonconnected_cells=False, neuron_connect=False):

    if neuron_connect:
        conns = []
        cells = []
        filename = "%switvliet_2020_8.xlsx"%spreadsheet_location
        wb = load_workbook(filename)
        sheet = wb.worksheets[0]
        print_("Opened the Excel file: " + filename)
        

        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming data starts from the second row
            pre = str(row[0])
            post = str(row[1])
            syntype = str(row[2])
            num = int(row[3])
            synclass = 'Generic_GJ' if 'electrical' in syntype else 'Chemical_Synapse'

            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
            if pre not in cells:
                cells.append(pre)
            if post not in cells:
                cells.append(post)

        return cells, conns

    else:
        conns = []
        cells = []
        filename = "%switvliet_2020_8.xlsx"%spreadsheet_location
        wb = load_workbook(filename)
        sheet = wb.worksheets[0]

        print_("Opened Excel file..: " + filename)

        known_nonconnected_cells = ['CANL', 'CANR', 'VC6']


        for row in sheet.iter_rows(min_row=2, values_only=True):
            pre = str(row[0])
            post = str(row[1])
            syntype = str(row[2])
            num = int(row[3])
            synclass = 'Generic_GJ' if 'electrical' in syntype else 'Chemical_Synapse'


            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
            if pre not in cells:
                cells.append(pre)
            if post not in cells:
                cells.append(post)

        if include_nonconnected_cells:
            for c in known_nonconnected_cells: cells.append(c)

        return cells, conns


def read_muscle_data():

    conns = []
    neurons = []
    muscles = []

    filename = "%switvliet_2020_8.xlsx"%spreadsheet_location
    wb = load_workbook(filename)
    sheet = wb.worksheets[0]

    print_("Opened Excel file: "+ filename)

    for row in sheet.iter_rows(min_row=2, values_only=True):
            pre = str(row[0])
            post = str(row[1])
            syntype = str(row[2])
            num = int(row[3])
            synclass = 'Generic_GJ' if 'electrical' in syntype else 'Chemical_Synapse'

    conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
    if pre not in neurons:
            neurons.append(pre)
    if post not in muscles:
            muscles.append(post)


    return neurons, muscles, conns



def main():

    cells, neuron_conns = read_data(include_nonconnected_cells=True)
    neurons2muscles, muscles, muscle_conns = read_muscle_data()

    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)

if __name__ == '__main__':

    main()
