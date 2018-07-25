# -*- coding: utf-8 -*-

############################################################

#    A simple script to read the values in herm_full_edgelist.csv.

#    Note: this file will be replaced with a call to PyOpenWorm
#    when that package is updated to read all of this data from the 
#    spreadseet

############################################################

import csv

from NeuroMLUtilities import ConnectionInfo
import os

from c302 import print_

spreadsheet_location = os.path.dirname(os.path.abspath(__file__))+"/data/"
filename = "%sherm_full_edgelist.csv" % spreadsheet_location

def get_all_muscle_prefixes():
    return ["pm", "vm", "um", "dBWM", "vBWM"]


def get_body_wall_muscle_prefixes():
    return ["dBWM", "vBWM"]


def is_muscle(cell):
    known_muscle_prefixes = get_all_muscle_prefixes()
    return cell.startswith(tuple(known_muscle_prefixes))


def is_body_wall_muscle(cell):
    known_muscle_prefixes = get_body_wall_muscle_prefixes()
    return cell.startswith(tuple(known_muscle_prefixes))


def is_neuron(cell):
    return cell[0].isupper()


def remove_leading_index_zero(cell):
    """
    Returns neuron name with an index without leading zero. E.g. VB01 -> VB1.
    """
    if is_neuron(cell) and cell[-2:].startswith("0"):
        return "%s%s" % (cell[:-2], cell[-1:])
    return cell

def get_old_muscle_name(muscle):
    index = int(muscle[5:])
    if index < 10:
        index = "0%s" % index
    if muscle.startswith("vBWML"):
        return "MVL%s" % index
    elif muscle.startswith("vBWMR"):
        return "MVR%s" % index
    elif muscle.startswith("dBWML"):
        return "MDL%s" % index
    elif muscle.startswith("dBWMR"):
        return "MDR%s" % index

def get_syntype(syntype):
    if syntype == "electrical":
        return "GapJunction"
    elif syntype == "chemical":
        return "Send"
    else:
        raise NotImplementedError("Cannot parse syntype '%s'" % syntype)
    
def get_synclass(cell, syntype):
    #dirty hack
    if syntype == "GapJunction":
        return "Generic_GJ"
    else:
        if cell.startswith("DD") or cell.startswith("VD"):
            return "GABA"
        return "Acetylcholine"

def parse_row(row):
    pre = str.strip(row["Source"])
    post = str.strip(row["Target"])
    num = int(row["Weight"])
    syntype = get_syntype(str.strip(row["Type"]))
    synclass = get_synclass(pre, syntype)
    return pre, post, num, syntype, synclass

def readDataFromSpreadsheet(include_nonconnected_cells=False):
    """
    Args:
        include_nonconnected_cells (bool): Also append neurons without known connections to other neurons to the 'cells' list. True if they should get appended, False otherwise.
    Returns:
        cells (:obj:`list` of :obj:`str`): List of neurons
        conns (:obj:`list` of :obj:`ConnectionInfo`): List of connections from neuron to neuron
    """

    conns = []
    cells = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        print_("Opened file: " + filename)

        known_nonconnected_cells = ['CANL', 'CANR']

        for row in reader:
            pre, post, num, syntype, synclass = parse_row(row)

            if not is_neuron(pre) or not is_neuron(post):
                continue  # pre or post is not a neuron

            pre = remove_leading_index_zero(pre)
            post = remove_leading_index_zero(post)
            
            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
            #print ConnectionInfo(pre, post, num, syntype, synclass)
            if pre not in cells:
                cells.append(pre)
            if post not in cells:
                cells.append(post)

        if include_nonconnected_cells:
            for c in known_nonconnected_cells:
                if c not in cells:
                    cells.append(c)

    return cells, conns


def readMuscleDataFromSpreadsheet():
    """
    Returns:
        neurons (:obj:`list` of :obj:`str`): List of motor neurons. Each neuron has at least one connection with a post-synaptic muscle cell.
        muscles (:obj:`list` of :obj:`str`): List of muscle cells.
        conns (:obj:`list` of :obj:`ConnectionInfo`): List of neuron-muscle connections.
    """

    neurons = []
    muscles = []
    conns = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        print_("Opened file: " + filename)

        for row in reader:
            pre, post, num, syntype, synclass = parse_row(row)

            if (not is_neuron(pre) and not is_body_wall_muscle(pre)) or not is_body_wall_muscle(post):
                # Don't add connections unless pre=neuron and post=body_wall_muscle
                continue

            if is_neuron(pre):
                pre = remove_leading_index_zero(pre)
            else:
                pre = get_old_muscle_name(pre)
            post = get_old_muscle_name(post)

            conns.append(ConnectionInfo(pre, post, num, syntype, synclass))
            #print ConnectionInfo(pre, post, num, syntype, synclass)
            if is_neuron(pre) and pre not in neurons:
                neurons.append(pre)
            elif is_body_wall_muscle(pre) and pre not in muscles:
                muscles.append(pre)
            if post not in muscles:
                muscles.append(post)

    return neurons, muscles, conns


def main():
    
    cells, conns = readDataFromSpreadsheet()

    print_("%i cells in spreadsheet: %s..."%(len(cells),sorted(cells)[0:3]))

    from os import listdir
    cell_names = [f[:-9] for f in listdir('%s/CElegans/morphologies/' % spreadsheet_location) if
                  f.endswith('.java.xml')]

    cell_names.remove('MDL08')  # muscle

    s_c = sorted(cell_names)
    print_("%i cell morphologies found: %s..."%(len(cell_names),s_c[0:3]))

    for c in cells: cell_names.remove(c)

    print_("Difference: %s"%cell_names)

    cells2, conns2 = readDataFromSpreadsheet(include_nonconnected_cells=True)

    assert(len(cells2) == 302)

    print_("Lengths are equal if include_nonconnected_cells=True")
    
    
    print_("Found %s connections: %s..."%(len(conns2),conns2[0]))

    neurons, muscles, conns = readMuscleDataFromSpreadsheet()

    print_("Found %i neurons connected to muscles: %s\n" % (len(neurons), sorted(neurons)))
    print_("Found %i muscles connected to neurons: %s\n" % (len(muscles), sorted(muscles)))
    print_("Found %i connections between neurons and muscles, e.g. %s" % (len(conns), conns[0]))


if __name__ == '__main__':
    main()
