# -*- coding: utf-8 -*-

############################################################

#    Utilities for reading/writing/parsing NeuroML 2 files

############################################################

from c302 import print_

class ConnectionInfo:

    def __init__(self,
                 pre_cell,
                 post_cell,
                 number,
                 syntype,
                 synclass):

        self.pre_cell = pre_cell
        self.post_cell = post_cell
        self.number = number
        self.syntype = syntype
        self.synclass = synclass


    def __str__(self):
        return "Connection from %s to %s (%i times, type: %s, neurotransmitter: %s)"%(self.pre_cell, self.post_cell, self.number, self.syntype, self.synclass)

    def short(self):
        return "Connection from %s to %s (%s)"%(self.pre_cell, self.post_cell, self.syntype)
    
    def __eq__(self, other):
        return other.pre_cell == self.pre_cell and other.post_cell == self.post_cell and  other.number == self.number and other.syntype == self.syntype and other.synclass == self.synclass 
        
    def __lt__(self, other):
        if other.pre_cell+other.post_cell > self.pre_cell+self.post_cell:
            return True
        else: 
            return False
    
    def __repr__(self):
        return self.__str__()



def getSegmentIds(cell):
    seg_ids = []
    for segment in cell.morphology.segments:
        seg_ids.append(segment.id)

    return seg_ids

def get3DPosition(cell, segment_index, fraction_along):
    seg = cell.morphology.segments[segment_index]
 
    end = seg.distal

    start = seg.proximal
    if start is None:
        segs = getSegmentIds(cell)
        seg_index_parent = segs.index(seg.parent.segments)
        start = cell.morphology.segments[seg_index_parent].distal

    fx = fract(start.x, end.x, fraction_along)
    fy = fract(start.y, end.y, fraction_along)
    fz = fract(start.z, end.z, fraction_along)

    #print "(%f, %f, %f) is %f between (%f, %f, %f) and (%f, %f, %f)"%(fx,fy,fz,fraction_along,start.x,start.y,start.z,end.x,end.y,end.z)

    return fx, fy, fz

def fract(a, b, f):
    return a+(b-a)*f


def analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns):

    print_("Found %s cells: %s\n"%(len(cells),sorted(cells)))
    #assert(len(cells) == 302)
    #print_("Expected number of cells correct if include_nonconnected_cells=True")


    print_("Found %s connections..."%(len(neuron_conns)))
    for c in neuron_conns[:5]: print_("   %s"%c)

    print_("   ...\n")
    nts = {}
    nts_tot = {}
    for c in neuron_conns:
        nt = c.synclass
        if not nt in nts:
            nts[nt] = 0
            nts_tot[nt] = 0
        nts[nt]+=1
        nts_tot[nt]+=c.number
    
    for nt in sorted(nts.keys()):
        print_("   %s present in %s connections, %s synapses total (avg %.3f syns per conn)"%(nt, nts[nt], nts_tot[nt], nts_tot[nt]/nts[nt]))

    print_("")
    print_("   ---  Muscles  ---")
    print_("")


    print_("Found %i neurons connected to muscles: %s\n"%(len(neurons2muscles), sorted(neurons2muscles)))
    print_("Found %i muscles connected to neurons: %s\n"%(len(muscles), sorted(muscles)))
    print_("Found %i connections between neurons and muscles, e.g. %s\n"%(len(muscle_conns), muscle_conns[0]))

    nts = {}
    nts_tot = {}
    for c in muscle_conns:
        nt = c.synclass
        if not nt in nts:
            nts[nt] = 0
            nts_tot[nt] = 0
        nts[nt]+=1
        nts_tot[nt]+=c.number
    
    for nt in nts:
        print_("  %s present in %s connections, %s synapses total (avg %.3f syns per conn)"%(nt, nts[nt], nts_tot[nt], nts_tot[nt]/nts[nt]))

    print_("")