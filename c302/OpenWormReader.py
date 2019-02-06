from NeuroMLUtilities import ConnectionInfo
import PyOpenWorm as P

from c302 import print_

############################################################

#   A simple script to read the values in PyOpenWorm
#   Originally written by Mark Watts (github.com/mwatts15)

############################################################


class OpenWormReader:
    
    def __init__(self):
        print_("Initialising OpenWormReader")
        P.connect()
        self.net = P.Worm().get_neuron_network()
        self.all_connections = self.net.synapses()
        print_("Finished initialising OpenWormReader")
        
    
    def get_cells_in_model(self):

        cell_names = []
        for n in set(self.net.neurons()):
            cell_names.append(n.name())
        
        return sorted(cell_names)

    def readData(self, include_nonconnected_cells=False):
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
                    
        print_("Total cells %i (%i with connections)" % (len(cell_names), len(cells)))
        print_("Total connections found %i " % len(conns)) 
        P.disconnect()
        
        if include_nonconnected_cells:
            return cell_names, conns
        else:
            return cells, conns
            

if __name__ == "__main__":
    
    owr = OpenWormReader()
    
    cells, conns = owr.readData(include_nonconnected_cells=True)

    print_("%i cells in OpenWormReader: %s..."%(len(cells),sorted(cells)[0:3]))

    
    print_("Found %s connections: %s..."%(len(conns),conns[0]))
    cm = {}
    for c in conns:
        cm[c.short()] = c
    
    from UpdatedSpreadsheetDataReader import readDataFromSpreadsheet
    
    cells2, conns2 = readDataFromSpreadsheet(include_nonconnected_cells=True)
    
    cm2 = {}
    for c2 in conns2:
        cm2[c2.short()] = c2
    
    maxn = 30000
    
    refs = cm.keys()
    
    for i in range(min(maxn, len(refs))):
        #print("\n-----  Connection in OWR: %s"%refs[i])
        #print cm[refs[i]]
        if refs[i] in cm2:
            if cm[refs[i]].number != cm2[refs[i]].number:
                print_("Mismatch: %s != %s"%(cm[refs[i]],cm2[refs[i]]))
        else:
            print_("Missing: %s"%cm[refs[i]])
            
    refs = cm2.keys()
    for i in range(min(maxn, len(refs))):
        #print("\n-----  Connection in USR: %s"%refs[i])
        #print cm2[refs[i]]
        if refs[i] in cm:
            if cm[refs[i]].number != cm2[refs[i]].number:
                print_("Mismatch: %s != %s"%(cm[refs[i]],cm2[refs[i]]))
        else:
            print_("* Missing: %s"%cm2[refs[i]])
            
    
