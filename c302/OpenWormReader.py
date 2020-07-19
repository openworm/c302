from c302.NeuroMLUtilities import ConnectionInfo
from c302 import print_

from owmeta_core.bundle import Bundle
from owmeta_core.context import Context
from owmeta.neuron import Neuron
from owmeta.muscle import Muscle
from owmeta.worm import Worm

############################################################

#   A simple script to read the values in PyOpenWorm
#   Originally written by Mark Watts (github.com/mwatts15)

############################################################


class OpenWormReader(object):
    def __init__(self):
        self.cached = False

    def get_cells_in_model(self, net):

        cell_names = set()
        for n in net.neurons():
            cell_names.add(str(n.name()))

        return cell_names

    def read_data(self, include_nonconnected_cells=False):
        print_("Initialising OpenWormReader")

        cell_names, pre, post, conns = self._read_connections('neuron')

        if include_nonconnected_cells:
            return cell_names, conns
        else:
            return pre + post, conns

    def read_muscle_data(self):
        cell_names, neurons, muscles, conns = self._read_connections('muscle')
        return neurons, muscles, conns

    def _read_connections(self, termination):
        with Bundle('openworm/owmeta-data') as bnd:
            if not self.cached:
                ctx = bnd(Context)(ident="http://openworm.org/data").stored
                # Extract the network object from the worm object.
                net = ctx(Worm).query().neuron_network()

                syn = net.synapse.expr
                pre = syn.pre_cell
                post = syn.post_cell

                (pre | post).rdf_type(multiple=True)

                (pre | post).name()
                pre()
                post()
                syn.syntype()
                syn.synclass()
                syn.number()
                self.connlist = syn.to_objects()

                self.cell_names = self.get_cells_in_model(net)
                self.cached = True

        if termination == 'neuron':
            term_type = Neuron.rdf_type
        elif termination == 'muscle':
            term_type = Muscle.rdf_type
        else:
            raise Exception("Unrecognized termination {}".format(termination))

        conns = []
        pre_cell_names = set()
        post_cell_names = set()
        for conn in self.connlist:
            if (Neuron.rdf_type in conn.pre_cell.rdf_type and
                    term_type in conn.post_cell.rdf_type):
                num = conn.number
                syntype = conn.syntype or ''
                synclass = conn.synclass or ''
                pre_name = conn.pre_cell.name
                post_name = conn.post_cell.name

                conns.append(ConnectionInfo(pre_name, post_name, num, syntype, synclass))

                pre_cell_names.add(pre_name)
                post_cell_names.add(post_name)

        print_("Total cells %i (%i with connections)" % (
            len(self.cell_names),
            len(pre_cell_names | post_cell_names)))
        print_("Total connections found %i " % len(conns))

        return list(self.cell_names), pre_cell_names, post_cell_names, conns


READER = OpenWormReader()

read_data = READER.read_data
read_muscle_data = READER.read_muscle_data

if __name__ == "__main__":

    cells, conns = read_data(include_nonconnected_cells=True)

    print_("%i cells found using OpenWormReader: %s..." % (len(cells), sorted(cells)[0:3]))

    print_("Found %s connections using OpenWormReader: %s..." % (len(conns), conns[0]))

    conn_map_OWR = {}
    for c in conns:
        conn_map_OWR[c.short()] = c

    from UpdatedSpreadsheetDataReader import read_data as read_data_usr
    #from SpreadsheetDataReader import read_data as read_data_usr

    cells2, conns2 = read_data_usr(include_nonconnected_cells=True)

    print_("%i cells found using UpdatedSpreadsheetDataReader: %s..." % (len(cells2), sorted(cells2)[0:3]))
    print_("Found %s connections using UpdatedSpreadsheetDataReader: %s..." % (len(conns2), conns2[0]))

    conn_map_USR = {}
    for c2 in conns2:
        conn_map_USR[c2.short()] = c2

    maxn = 30000

    refs_OWR = list(conn_map_OWR.keys())

    matching = 0

    for i in range(min(maxn, len(refs_OWR))):
        #print("\n-----  Connection in OWR: %s"%refs[i])
        # print cm[refs[i]]
        ref = refs_OWR[i]
        if ref in conn_map_USR:
            if conn_map_OWR[ref].number != conn_map_USR[ref].number:
                print_("Mismatch: %s != %s" % (conn_map_OWR[ref], conn_map_USR[ref]))
            else:
                matching += 1
        else:
            print_("Missing from UpdatedSpreadsheetDataReader: %s" % (conn_map_OWR[ref]))

    print_('Number matching: %i' % matching)

    matching = 0

    refs_USR = list(conn_map_USR.keys())

    for i in range(min(maxn, len(refs_USR))):
        #print("\n-----  Connection in USR: %s"%refs[i])
        # print cm2[refs[i]]
        ref = refs_USR[i]
        if ref in conn_map_OWR:
            if conn_map_OWR[ref].number != conn_map_USR[ref].number:
                print_("Mismatch: %s != %s" % (conn_map_OWR[ref], conn_map_USR[ref]))
            else:
                matching += 1
        else:
            print_("* Missing from OpenWormReader: %s" % conn_map_USR[ref])

    print_('Number matching: %i' % matching)
