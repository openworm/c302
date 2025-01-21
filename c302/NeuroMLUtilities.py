# -*- coding: utf-8 -*-

############################################################

#    Utilities for reading/writing/parsing NeuroML 2 files

############################################################


from c302.ConnectomeReader import analyse_connections


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

    # print "(%f, %f, %f) is %f between (%f, %f, %f) and (%f, %f, %f)"%(fx,fy,fz,fraction_along,start.x,start.y,start.z,end.x,end.y,end.z)

    return fx, fy, fz


def fract(a, b, f):
    return a + (b - a) * f


if __name__ == "__main__":
    # from SpreadsheetDataReader import read_data, read_muscle_data
    from WormNeuroAtlasReader import read_data, read_muscle_data

    cells, neuron_conns = read_data(include_nonconnected_cells=True)
    neurons2muscles, muscles, muscle_conns = read_muscle_data()

    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)
