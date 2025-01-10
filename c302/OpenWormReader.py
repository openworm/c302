import logging
import re

from c302.ConnectomeReader import ConnectionInfo
from c302.ConnectomeReader import analyse_connections
from c302 import print_, MUSCLE_RE

try:
    from owmeta_core.bundle import Bundle
    from owmeta_core.context import Context
    from owmeta.neuron import Neuron
    from owmeta.muscle import BodyWallMuscle
    from owmeta.worm import Worm
except Exception:
    print("owmeta not installed! Cannot run OpenWormReader")
    exit()

############################################################

#   A simple script to read the values in owmeta
#   Originally written by Mark Watts (github.com/mwatts15)

############################################################

LOGGER = logging.getLogger(__name__)


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

        try:
            cell_names, pre, post, conns = self._read_connections("neuron")
        except Exception:
            print(
                "\nProblem loading connections via owmeta! The package is installed however. You may need to try running:"
                + "\n\n    owm bundle remote --user add ow 'https://raw.githubusercontent.com/openworm/owmeta-bundles/master/index.json'\n"
            )

            exit()

        if include_nonconnected_cells:
            return cell_names, conns
        else:
            return pre + post, conns

    def read_muscle_data(self):
        cell_names, neurons, muscles, conns = self._read_connections("muscle")
        return neurons, muscles, conns

    def _read_connections(self, termination=None):
        if not self.cached:
            with Bundle("openworm/owmeta-data", version=6) as bnd:
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

        if termination == "neuron":
            term_type = set([Neuron.rdf_type])
        elif termination == "muscle":
            term_type = set([BodyWallMuscle.rdf_type])
        else:
            term_type = set([Neuron.rdf_type, BodyWallMuscle.rdf_type])

        conns = []
        pre_cell_names = set()
        post_cell_names = set()
        for conn in self.connlist:
            if Neuron.rdf_type in conn.pre_cell.rdf_type and term_type & set(
                conn.post_cell.rdf_type
            ):
                num = conn.number
                syntype = conn.syntype or ""
                synclass = conn.synclass or ""
                pre_name = conn.pre_cell.name
                post_name = conn.post_cell.name
                if BodyWallMuscle.rdf_type in conn.post_cell.rdf_type:
                    post_name = format_muscle_name(post_name)

                if not synclass:
                    # Hack/guess
                    if syntype and syntype.lower() == "gapjunction":
                        synclass = "Generic_GJ"
                    else:
                        if pre_name.startswith("DD") or pre_name.startswith("VD"):
                            synclass = "GABA"
                        synclass = "Acetylcholine"
                conns.append(
                    ConnectionInfo(pre_name, post_name, num, syntype, synclass)
                )

                pre_cell_names.add(pre_name)
                post_cell_names.add(post_name)

        print_(
            "Total cells %i (%i with connections)"
            % (
                len(self.cell_names | pre_cell_names | post_cell_names),
                len(pre_cell_names | post_cell_names),
            )
        )
        print_("Total connections found %i " % len(conns))

        return list(self.cell_names), pre_cell_names, post_cell_names, conns


def format_muscle_name(muscle_name):
    md = MUSCLE_RE.fullmatch(muscle_name)
    if md:
        return muscle_name
    else:
        md = re.fullmatch(r"([VD][LR])(\d+)", muscle_name)
        if md:
            return "M{0}{1:02d}".format(md.group(1), int(md.group(2)))
        else:
            LOGGER.debug("Unrecognized muscle name format in %s", muscle_name)
            return muscle_name


READER = OpenWormReader()

read_data = READER.read_data
read_muscle_data = READER.read_muscle_data

if __name__ == "__main__":
    cells, neuron_conns = read_data(include_nonconnected_cells=True)
    neurons2muscles, muscles, muscle_conns = read_muscle_data()

    analyse_connections(cells, neuron_conns, neurons2muscles, muscles, muscle_conns)

    exit()

    conn_map_OWR = {}
    for c in neuron_conns:
        conn_map_OWR[c.short().lower()] = c

    from c302.UpdatedSpreadsheetDataReader import read_data as read_data_usr

    # from c302.SpreadsheetDataReader import read_data as read_data_usr

    cells2, conns2 = read_data_usr(include_nonconnected_cells=True)

    print_(
        "%i cells found using UpdatedSpreadsheetDataReader2: %s..."
        % (len(cells2), sorted(cells2)[0:3])
    )
    print_(
        "Found %s connections using UpdatedSpreadsheetDataReader2, First few: "
        % (len(conns2),)
    )
    for c in sorted(conns2)[: min(len(conns2), 5)]:
        print_("  %s" % c)

    conn_map_USR = {}
    for c2 in conns2:
        conn_map_USR[c2.short().lower()] = c2

    maxn = 3

    refs_OWR = list(conn_map_OWR.keys())

    matching = 0

    for i in range(min(maxn, len(refs_OWR))):
        ref = refs_OWR[i]
        if ref in conn_map_USR:
            if conn_map_OWR[ref].number != conn_map_USR[ref].number:
                print_("Mismatch: %s != %s" % (conn_map_OWR[ref], conn_map_USR[ref]))
            else:
                matching += 1
        else:
            print_(
                "Missing from UpdatedSpreadsheetDataReader: %s" % (conn_map_OWR[ref])
            )

    print_("Number matching: %i" % matching)

    matching = 0

    refs_USR = list(conn_map_USR.keys())

    for i in range(min(maxn, len(refs_USR))):
        # print("\n-----  Connection in USR: %s"%refs[i])
        # print cm2[refs[i]]
        ref = refs_USR[i]
        if ref in conn_map_OWR:
            if conn_map_OWR[ref].number != conn_map_USR[ref].number:
                print_("Mismatch: %s != %s" % (conn_map_OWR[ref], conn_map_USR[ref]))
            else:
                matching += 1
        else:
            print_("* Missing from OpenWormReader: %s" % conn_map_USR[ref])

    print_("Number matching: %i" % matching)
