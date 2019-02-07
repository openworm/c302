from NeuroMLUtilities import ConnectionInfo
import PyOpenWorm as P

from c302 import print_

############################################################

#   A simple script to read the values in PyOpenWorm
#   Originally written by Mark Watts (github.com/mwatts15)

############################################################



def get_cells_in_model(net):

    cell_names = []
    for n in set(net.neurons()):
        cell_names.append(str(n.name()))

    return sorted(cell_names)

def read_data(include_nonconnected_cells=False):

    print_("Initialising OpenWormReader")
    P.connect()
    net = P.Worm().get_neuron_network()
    all_connections = net.synapses()
    print_("Finished initialising OpenWormReader")

    conns = []
    cells = []

    cell_names = get_cells_in_model(net)

    for s in all_connections:
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
    
    cells, conns = read_data(include_nonconnected_cells=True)

    print_("%i cells found using OpenWormReader: %s..."%(len(cells),sorted(cells)[0:3]))

    print_("Found %s connections using OpenWormReader: %s..."%(len(conns),conns[0]))
    
    conn_map_OWR = {}
    for c in conns:
        conn_map_OWR[c.short()] = c
    
    from UpdatedSpreadsheetDataReader import read_data as read_data_usr
    #from SpreadsheetDataReader import read_data as read_data_usr
    
    cells2, conns2 = read_data_usr(include_nonconnected_cells=True)
    
    print_("%i cells found using UpdatedSpreadsheetDataReader: %s..."%(len(cells2),sorted(cells2)[0:3]))
    print_("Found %s connections using UpdatedSpreadsheetDataReader: %s..."%(len(conns2),conns2[0]))
    
    conn_map_USR = {}
    for c2 in conns2:
        conn_map_USR[c2.short()] = c2
    
    maxn = 30000
    
    refs_OWR = conn_map_OWR.keys()
    
    matching = 0
    
    for i in range(min(maxn, len(refs_OWR))):
        #print("\n-----  Connection in OWR: %s"%refs[i])
        #print cm[refs[i]]
        ref = refs_OWR[i]
        if ref in conn_map_USR:
            if conn_map_OWR[ref].number != conn_map_USR[ref].number:
                print_("Mismatch: %s != %s"%(conn_map_OWR[ref],conn_map_USR[ref]))
            else:
                matching+=1
        else:
            print_("Missing from UpdatedSpreadsheetDataReader: %s"%(conn_map_OWR[ref]))
            
    print_('Number matching: %i'%matching)
    
    matching = 0
            
    refs_USR = conn_map_USR.keys()
    
    for i in range(min(maxn, len(refs_USR))):
        #print("\n-----  Connection in USR: %s"%refs[i])
        #print cm2[refs[i]]
        ref = refs_USR[i]
        if ref in conn_map_OWR:
            if conn_map_OWR[ref].number != conn_map_USR[ref].number:
                print_("Mismatch: %s != %s"%(conn_map_OWR[ref],conn_map_USR[ref]))
            else:
                matching+=1
        else:
            print_("* Missing from OpenWormReader: %s"%conn_map_USR[ref])
            
    print_('Number matching: %i'%matching)
    
