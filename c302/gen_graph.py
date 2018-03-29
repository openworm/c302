#!/usr/bin/python
'''
Utility for converting NeuroML descriptions to graphs

Originally developed by David Lung: https://github.com/lungd/nml_to_graph
'''
import os
import sys
import xml.etree.ElementTree as ET

from glob import glob
from subprocess import call


def usage(script):
    print 'USAGE: python %s directory [r]' % (script)
    sys.exit(-1)


def is_muscle(cell):
    return cell.startswith('MV') or cell.startswith('MD')


def get_cells(root):
    cells = []
    #network = root.find('network')
    for cell in root.getiterator():
        if 'population' not in cell.tag:
            continue
        #if is_muscle(cell.attrib['id']):
        #    continue
        cells.append(cell.attrib['id'])
    return cells


def get_elec_conns(root):
    elec_conns = []
    for elec_conn in root.getiterator():
        if 'electricalProjection' not in elec_conn.tag:
            continue
        pre = elec_conn.attrib['presynapticPopulation']
        post = elec_conn.attrib['postsynapticPopulation']

        append = True
        for conn in elec_conns:
            if "%s -> %s" % (post, pre) in conn:
                append = False
        

        #if is_muscle(pre) or is_muscle(post):
        #    continue

        if append:
            elec_conns.append('%s -> %s [style="dashed" minlen=2 arrowhead="none"]' % (pre, post))
    return elec_conns    


def get_chem_conns(root):
    chem_conns = []
    for chem_conn in root.getiterator():
        if 'continuousProjection' not in chem_conn.tag:
            continue
        pre = chem_conn.attrib['presynapticPopulation']
        post = chem_conn.attrib['postsynapticPopulation']

        #if is_muscle(pre) or is_muscle(post):
        #    continue

        for child in chem_conn:
            if 'inh' in child.attrib['postComponent']:
                chem_conns.append('%s -> %s [minlen=2 color=red arrowhead="tee"]' % (pre, post))
            else:
                chem_conns.append('%s -> %s [minlen=2 color="black"]' % (pre, post))
    return chem_conns


def write_graph_file(filename, cells, elec_conns, chem_conns, layout="neato"):
    with open(filename, 'w') as graph:
        graph.write('digraph exp {\n')
        graph.write('graph [layout = %s];\n' % layout)

        graph.write('splines=true; ')
        #graph.write('concentrate=false; ')
        graph.write('sep="+25,25"; ')
        graph.write('overlap=false; ')
        graph.write('fontsize=12;\n')

        graph.write('node [fontsize=11;style=filled]; ')
        for cell in cells:
            graph.write('%s ' % cell)
            if is_muscle(cell):
                graph.write('[color="darkolivegreen3"]')
            elif cell.startswith('DA') or cell.startswith('DB') or cell.startswith('DD') \
              or cell.startswith('VA')  or cell.startswith('VB')  or cell.startswith('VD'):
                graph.write('[color="slategray1"]')
            else:
                graph.write('[color="thistle2"]')
                
            graph.write(';\n')
            
        graph.write('\n')

        for elec in elec_conns:
            graph.write('%s;\n' % elec)

        for chem in chem_conns:
            graph.write('%s;\n' % chem)

        
        graph.write('}')
        
    print("Written file: %s"%filename)


def find_nml_files(directory='.', recursive=False):
    files = []
    for file in os.listdir(directory):
        if file.endswith(".nml"):
            files.append(os.path.join(directory, file))

    if recursive:
        return [y for x in os.walk(directory) for y in glob(os.path.join(x[0], '*.nml'))]
    
    return files


def execute_graph_generator(graphviz_file, fig_file):
    with open(fig_file, 'w') as fig:
        call(['neato', '-Tpng', graphviz_file], stdout=fig)
    print("Converted file: %s using neato to %s"%(graphviz_file,graphviz_file.replace('gv','png')))
    os.system('dot -Gsplines=none %s | neato -Gsplines=true -Tpng -o%s' % (graphviz_file, fig_file))
    print("Converted file: %s using dot to %s"%(graphviz_file,graphviz_file.replace('gv','png')))
    
        


def main():

    if len(sys.argv) >= 3:
        filenames = find_nml_files(sys.argv[1], recursive=True)
    else:
        if os.path.isfile(sys.argv[1]):
            
            filenames = [sys.argv[1]]
        else:
            filenames = find_nml_files(sys.argv[1])

    for filename in sorted(filenames)[:5]:
        if filename.endswith('nml') and not filename.endswith('cell.nml'):
            print "=============================\nCreating graph for %s" % filename
            dirname = os.path.dirname(filename)
            tree = ET.parse(filename)
            root = tree.getroot()

            cells = get_cells(root)
            elec_conns = get_elec_conns(root)
            chem_conns = get_chem_conns(root)

            base = os.path.basename(filename)
            graphviz_file = os.path.splitext(base)[0]
            graphviz_file1 = graphviz_file + '_dot.gv'
            graphviz_file2 = graphviz_file + '_neato.gv'

            fig_file = os.path.splitext(base)[0]
            fig_file1 = fig_file + '_dot.png'
            fig_file2 = fig_file + '_neato.png'

            write_graph_file(os.path.join(dirname, graphviz_file1), cells, elec_conns, chem_conns, layout='dot')
            execute_graph_generator(os.path.join(dirname, graphviz_file1), os.path.join(dirname, fig_file1))

            write_graph_file(os.path.join(dirname, graphviz_file2), cells, elec_conns, chem_conns, layout='neato')
            execute_graph_generator(os.path.join(dirname, graphviz_file2), os.path.join(dirname, fig_file2))
    

if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage(sys.argv[0])

    main()
    

