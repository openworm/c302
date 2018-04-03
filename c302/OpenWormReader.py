from NeuroMLUtilities import ConnectionInfo
import PyOpenWorm as P

import logging

############################################################

#   A simple script to read the values in PyOpenWorm
#   Originally written by Mark Watts (github.com/mwatts15)

############################################################

logger = logging.getLogger("OpenWormReader")

class OpenWormReader:
    def __init__(self):
        logger.info("Initialising OpenWormReader")
        P.connect()
        self.net = P.Worm().get_neuron_network()
        self.all_connections = self.net.synapses()
        logger.info("Finished initialising OpenWormReader")
        
    def get_cells_in_model(self):

        from os import listdir
        cell_names = [f[:-9] for f in listdir('../../../CElegans/morphologies/' ) if
                      f.endswith('.java.xml')]

        cell_names.remove('MDL08')  # muscle
        
        return sorted(cell_names)

    def read(self):
        conns = []
        cells = []
        
        cell_names = owr.get_cells_in_model()
    
        for s in self.all_connections:
            pre = str(s.pre_cell().name())
            post = str(s.post_cell().name())
            
            if isinstance(s.post_cell(), P.Neuron) and pre in cell_names and post in cell_names:  
                syntype = str(s.syntype())
                syntype = syntype[0].upper()+syntype[1:]
                num = int(s.number())
                synclass = str(s.synclass())
                ci = ConnectionInfo(pre, post, num, syntype, synclass)
                conns.append(ci)
                if pre not in cells:
                    cells.append(pre)
                if post not in cells:
                    cells.append(post)
                    
        logger.info("Total cells read " + str(len(cells)))
        logger.info("Total connections read " + str(len(conns)))
        P.disconnect()
        return cells, conns

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(name)s - %(levelname)s: %(message)s')
    owr = OpenWormReader()
    
    cells, conns = owr.read()

    print("%i cells in OpenWormReader: %s..."%(len(cells),sorted(cells)[0:3]))

    cell_names = owr.get_cells_in_model()

    s_c = sorted(cell_names)
    print("%i cells known in model: %s..."%(len(cell_names),s_c[0:3]))

    cell_names2 = list(cell_names)
    for c in cells: 
        if c in cell_names2:
            cell_names2.remove(c)

    print("Difference 1: %s"%cell_names2)
    
    cells2 = list(cells)
    for c in cell_names: 
        if c in cells2:
            cells2.remove(c)

    print("Difference 2: %s"%cells2)
    
    
    print("Found %s connections: %s..."%(len(conns),conns[0]))
    cm = {}
    for c in conns:
        cm[c.short()] = c
    
    from UpdatedSpreadsheetDataReader import readDataFromSpreadsheet
    
    cells2, conns2 = readDataFromSpreadsheet(include_nonconnected_cells=True)
    
    cm2 = {}
    for c2 in conns2:
        cm2[c2.short()] = c2
    
    
    maxn = 3000
    
    refs = cm.keys()
    
    for i in range(min(maxn, len(refs))):
        #print("\n-----  Connection in OWR: %s"%refs[i])
        #print cm[refs[i]]
        if refs[i] in cm2:
            if cm[refs[i]].number != cm2[refs[i]].number:
                print("Mismatch: %s != %s"%(cm[refs[i]],cm2[refs[i]]))
        else:
            print("Missing: %s"%cm[refs[i]])
            
    refs = cm2.keys()
    for i in range(min(maxn, len(refs))):
        #print("\n-----  Connection in USR: %s"%refs[i])
        #print cm2[refs[i]]
        if refs[i] in cm:
            if cm[refs[i]].number != cm2[refs[i]].number:
                print("Mismatch: %s != %s"%(cm[refs[i]],cm2[refs[i]]))
        else:
            print("* Missing: %s"%cm2[refs[i]])
            
    
