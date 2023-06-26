import logging
import re

from c302.NeuroMLUtilities import ConnectionInfo
from c302.NeuroMLUtilities import analyse_connections
from c302 import print_

import wormneuroatlas as wa


############################################################

#   A simple script to read the values in WormNeuroAtlas

#    This is on of a number of interchangeable "Readers" which can 
#    be used to get connection data for c302

############################################################

LOGGER = logging.getLogger(__name__)


class WormNeuroAtlasReader(object):

    def __init__(self):
        self.atlas = wa.NeuroAtlas()
        self.all_cells = self.atlas.neuron_ids


    def read_data(self, include_nonconnected_cells=False):
        print_("Initialising WormNeuroAtlasReader")

        cell_names = self.atlas.neuron_ids
        conns = []
        gj = self.atlas.get_gap_junctions()

        for pre in self.all_cells:
            apre = self.atlas.ids_to_ai([pre])
            for post in self.all_cells:
                apost = self.atlas.ids_to_ai([post]) 

                gji = gj[apre, apost]
                num = gji[0]
                if num>0:
                    #print("Gap junc (%s (%i) -> %s (%i): %s"%(pre, apre, post, apost, gji))
                    synclass = 'Generic_GJ'
                    syntype = "GapJunction"
                    conns.append(ConnectionInfo(pre, post, num, syntype, synclass))

        if include_nonconnected_cells:
            return cell_names, conns
        else:
            return pre + post, conns

    def read_muscle_data(self):
        neurons = []
        muscles = []
        conns = []
        return neurons, muscles, conns

READER = WormNeuroAtlasReader()

read_data = READER.read_data
read_muscle_data = READER.read_muscle_data

if __name__ == "__main__":

    cells, neuron_conns = read_data(include_nonconnected_cells=True)
    neurons2muscles, muscles, muscle_conns = read_muscle_data()

    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)
