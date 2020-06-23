# -*- coding: utf-8 -*-

############################################################

#    A simple script to read the values in CElegansNeuronTables.xls.

#    Note: this file will be replaced with a call to PyOpenWorm
#    when that package is updated to read all of this data from the
#    spreadseet

############################################################


from c302.NeuroMLUtilities import ConnectionInfo

from xlrd import open_workbook
import os

spreadsheet_location = os.path.dirname(os.path.abspath(__file__))+"/data/"

from c302 import print_


def read_data(include_nonconnected_cells=False, neuron_connect=False):
    # reading the NeuronConnect.xls file if neuron_connect = True
    if neuron_connect:
        conns = []
        cells = []
        filename = "%sNeuronConnectFormatted.xlsx"%spreadsheet_location
        rb = open_workbook(filename)
        print_("Opened Excel file: " + filename)

        for row in range(1,rb.sheet_by_index(0).nrows):
            pre = str(rb.sheet_by_index(0).cell(row,0).value)
            post = str(rb.sheet_by_index(0).cell(row,1).value)
            syntype = rb.sheet_by_index(0).cell(row,2).value
            num = int(rb.sheet_by_index(0).cell(row,3).value)
            synclass = 'Generic_GJ' if 'EJ' in syntype else 'Chemical_Synapse'

            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
            if pre not in cells:
                cells.append(pre)
            if post not in cells:
                cells.append(post)

        return cells, conns

    else:
        conns = []
        cells = []
        filename = "%sCElegansNeuronTables.xls"%spreadsheet_location
        rb = open_workbook(filename)

        print_("Opened Excel file: " + filename)

        known_nonconnected_cells = ['CANL', 'CANR', 'VC6']


        for row in range(1,rb.sheet_by_index(0).nrows):
            pre = str(rb.sheet_by_index(0).cell(row,0).value)
            post = str(rb.sheet_by_index(0).cell(row,1).value)
            syntype = rb.sheet_by_index(0).cell(row,2).value
            num = int(rb.sheet_by_index(0).cell(row,3).value)
            synclass = rb.sheet_by_index(0).cell(row,4).value

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

    filename = "%sCElegansNeuronTables.xls"%spreadsheet_location
    rb = open_workbook(filename)

    print_("Opened Excel file: "+ filename)

    sheet = rb.sheet_by_index(1)

    for row in range(1,sheet.nrows):
        pre = str(sheet.cell(row,0).value)
        post = str(sheet.cell(row,1).value)
        syntype = 'Send'
        num = int(sheet.cell(row,2).value)
        synclass = sheet.cell(row,3).value.replace(',', 'plus').replace(' ', '_')

        conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
        if pre not in neurons:
            neurons.append(pre)
        if post not in muscles:
            muscles.append(post)


    return neurons, muscles, conns


def main():

    cells, conns = read_data(include_nonconnected_cells=True)

    assert(len(cells) == 302)

    print_("Lengths are equal if include_nonconnected_cells=True")

    print_("Found %s cells: %s..."%(len(cells),cells))
    print_("Found %s connections: %s..."%(len(conns),conns[0]))

    neurons, muscles, conns = read_muscle_data()

    print_("Found %i neurons connected to muscles: %s"%(len(neurons), sorted(neurons)))
    print_("Found %i muscles connected to neurons: %s"%(len(muscles), sorted(muscles)))
    print_("Found %i connections between neurons and muscles, e.g. %s"%(len(conns), conns[0]))

if __name__ == '__main__':

    main()
