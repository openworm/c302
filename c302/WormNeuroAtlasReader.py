import logging

from c302.ConnectomeReader import ConnectionInfo
from c302.ConnectomeReader import analyse_connections
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
        syn_sign = wa.SynapseSign()

        self.dom_glu = syn_sign.get_neurons_producing("Glu", mode="dominant")
        self.dom_ach = syn_sign.get_neurons_producing("ACh", mode="dominant")
        self.dom_gaba = syn_sign.get_neurons_producing("GABA", mode="dominant")

        self.alt_glu = syn_sign.get_neurons_producing("Glu", mode="alternative")
        self.alt_ach = syn_sign.get_neurons_producing("ACh", mode="alternative")
        self.alt_gaba = syn_sign.get_neurons_producing("GABA", mode="alternative")

        self.all_cells = self.atlas.neuron_ids
        for i in range(len(self.all_cells)):
            if self.all_cells[i] == "AWCOFF":
                self.all_cells[i] = "AWCL"
            if self.all_cells[i] == "AWCON":
                self.all_cells[i] = "AWCR"

    def determine_nt(self, neuron):
        if neuron in self.dom_glu:
            return "Glutamate"
        elif neuron in self.dom_ach:
            return "Acetylcholine"
        elif neuron in self.dom_gaba:
            return "GABA"
        else:
            nt = "Generic_CS"
            if neuron in self.alt_glu:
                nt += "_Glutamate"
            if neuron in self.alt_ach:
                nt += "_Acetylcholine"
            if neuron in self.dom_gaba:
                nt += "_GABA"

            return nt

    def read_data(self, include_nonconnected_cells=False):
        print_("Initialising WormNeuroAtlasReader")

        conns = []
        gj = self.atlas.get_gap_junctions()
        cs = self.atlas.get_chemical_synapses()

        connected_cells = []

        for pre in self.all_cells:
            apre = self.atlas.ids_to_ai([pre])
            for post in self.all_cells:
                apost = self.atlas.ids_to_ai([post])

                connection = False

                gji = gj[apost, apre]
                num = gji[0]
                if num > 0:
                    # print("Gap junc (%s (%i) -> %s (%i): %s"%(pre, apre, post, apost, gji))
                    synclass = "Generic_GJ"
                    syntype = "GapJunction"
                    conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
                    connection = True

                csi = cs[apost, apre]
                num = csi[0]
                if num > 0:
                    # print("Chem syn (%s (%i) -> %s (%i): %s"%(pre, apre, post, apost, gji))
                    synclass = self.determine_nt(pre)
                    syntype = "Chemical"
                    conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
                    connection = True

                if connection:
                    if pre not in connected_cells:
                        connected_cells.append(pre)
                    if post not in connected_cells:
                        connected_cells.append(post)

        if include_nonconnected_cells:
            return self.all_cells, conns
        else:
            return connected_cells, conns

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
