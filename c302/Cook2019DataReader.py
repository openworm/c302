# -*- coding: utf-8 -*-

############################################################

#    A simple script to read the values in herm_full_edgelist.csv.

#    This is on of a number of interchangeable "Readers" which can 
#    be used to get connection data for c302

############################################################

import csv

from c302.ConnectomeReader import ConnectionInfo
from c302.ConnectomeReader import analyse_connections
from c302.ConnectomeReader import convert_to_preferred_muscle_name
from c302.ConnectomeReader import is_neuron
from c302.ConnectomeReader import is_body_wall_muscle

from openpyxl import load_workbook

import os
import numpy as np

from c302 import print_

spreadsheet_location = os.path.dirname(os.path.abspath(__file__))+"/data/"
filename = "%sSI 5 Connectome adjacency matrices.xlsx" % spreadsheet_location

SHEET_HERM_CHEM = 'hermaphrodite chemical'

class Cook2019DataReaderReader():

    def __init__(self):

        wb = load_workbook(filename)
        print_("Opened the Excel file: " + filename)   
        sheet = wb.get_sheet_by_name(SHEET_HERM_CHEM)
        print('Looking at sheet: %s'%SHEET_HERM_CHEM)
        self.pre_cells = []
        for i in range(4,304):
            self.pre_cells.append(sheet['C%i'%i].value)

        print('Pre cells (%i): %s'%(len(self.pre_cells),self.pre_cells))

        self.post_cells = []
        for i in range(4,457):
            self.post_cells.append(sheet.cell(row=3, column=i).value)

        print('Post cells (%i): %s'%(len(self.post_cells),self.post_cells))

        self.conns = np.zeros([len(self.pre_cells),len(self.post_cells)], dtype=int)

        print(self.conns)

        for i in range(len(self.pre_cells)):
            for j in range(len(self.post_cells)):
                val = sheet.cell(row=4+i, column=4+j).value
                #print('Cell (%i,%i) = %s)'%(i,j,val))
                if val is not None:
                    self.conns[i,j] = int(val)

        print(self.conns)



    def read_data(self, include_nonconnected_cells=False):
        """
        Args:
            include_nonconnected_cells (bool): Also append neurons without known connections to other neurons to the 'cells' list. True if they should get appended, False otherwise.
        Returns:
            cells (:obj:`list` of :obj:`str`): List of neurons
            conns (:obj:`list` of :obj:`ConnectionInfo`): List of connections from neuron to neuron
        """

        if not include_nonconnected_cells:
            raise Exception('Option include_nonconnected_cells=False not supported')

        conns = []
        cells = []

        for pre_index in range(len(self.pre_cells)):
            for post_index in range(len(self.post_cells)):

                pre = self.pre_cells[pre_index]
                post = self.post_cells[post_index]

                if not is_neuron(pre) or not is_neuron(post):
                    continue  # pre or post is not a neuron

                num = self.conns[pre_index,post_index]
                if num>0:
                    syntype = '???'
                    synclass = '???'

                    conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
                    #print ConnectionInfo(pre, post, num, syntype, synclass)
                    if pre not in cells:
                        cells.append(pre)
                    if post not in cells:
                        cells.append(post)

        return cells, conns


    def read_muscle_data(self):
        """
        Returns:
            neurons (:obj:`list` of :obj:`str`): List of motor neurons. Each neuron has at least one connection with a post-synaptic muscle cell.
            muscles (:obj:`list` of :obj:`str`): List of muscle cells.
            conns (:obj:`list` of :obj:`ConnectionInfo`): List of neuron-muscle connections.
        """

        neurons = []
        muscles = []
        conns = []

        '''
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            print_("Opened file: " + filename)

            for row in reader:
                pre, post, num, syntype, synclass = parse_row(row)

                if not (is_neuron(pre) or is_body_wall_muscle(pre)) or not is_body_wall_muscle(post):
                    continue

                if is_neuron(pre):
                    pre = remove_leading_index_zero(pre)
                else:
                    pre = get_old_muscle_name(pre)
                post = get_old_muscle_name(post)

                conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
                if is_neuron(pre) and pre not in neurons:
                    neurons.append(pre)
                elif is_body_wall_muscle(pre) and pre not in muscles:
                    muscles.append(pre)
                if post not in muscles:
                    muscles.append(post)'''

        return neurons, muscles, conns


def main():

    cdr = Cook2019DataReaderReader()
    read_data = cdr.read_data
    read_muscle_data = cdr.read_muscle_data
    
    cells, neuron_conns = read_data(include_nonconnected_cells=True)
    neurons2muscles, muscles, muscle_conns = read_muscle_data()

    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)

if __name__ == '__main__':
    main()
