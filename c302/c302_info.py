import c302


def generate_c302_info(nml_doc, verbose=False):
    net = nml_doc.networks[0]

    cc_exc_conns = {}
    cc_inh_conns = {}
    all_cells = []

    for cp in net.continuous_projections:
        if cp.presynaptic_population not in cc_exc_conns.keys():
            cc_exc_conns[cp.presynaptic_population] = {}
        if cp.presynaptic_population not in cc_inh_conns.keys():
            cc_inh_conns[cp.presynaptic_population] = {}

        if cp.presynaptic_population not in all_cells:
            all_cells.append(cp.presynaptic_population)
        if cp.postsynaptic_population not in all_cells:
            all_cells.append(cp.postsynaptic_population)

        for c in cp.continuous_connection_instance_ws:
            if "inh" in c.post_component:
                cc_inh_conns[cp.presynaptic_population][cp.postsynaptic_population] = (
                    float(c.weight)
                )
            else:
                cc_exc_conns[cp.presynaptic_population][cp.postsynaptic_population] = (
                    float(c.weight)
                )

    gj_conns = {}
    for ep in net.electrical_projections:
        if ep.presynaptic_population not in gj_conns.keys():
            gj_conns[ep.presynaptic_population] = {}

        if ep.presynaptic_population not in all_cells:
            all_cells.append(ep.presynaptic_population)
        if ep.postsynaptic_population not in all_cells:
            all_cells.append(ep.postsynaptic_population)

        for e in ep.electrical_connection_instance_ws:
            gj_conns[ep.presynaptic_population][ep.postsynaptic_population] = float(
                e.weight
            )

    all_cells = sorted(all_cells)

    try:
        from PyOpenWorm import (
            connect as pyow_connect,
            __version__ as pyow_version,
        )

        pow_conn = pyow_connect("./pyopenworm.conf")
        all_neuron_info, all_muscle_info = c302._get_cell_info(pow_conn, all_cells)
        ver_info = "PyOpenWorm v%s" % pyow_version
    except Exception as e:
        c302.print_("Unable to connect to PyOpenWorm database: %s" % e)
        from owmeta_core.bundle import Bundle

        from owmeta_core import __version__ as owc_version
        from owmeta import __version__ as owmeta_version

        ver_info = "owmeta v%s (owmeta core v%s)" % (owmeta_version, owc_version)

        with Bundle("openworm/owmeta-data", version=6) as bnd:
            all_neuron_info, all_muscle_info = c302._get_cell_info(bnd, all_cells)

    all_neurons = []
    all_muscles = []
    for c in all_cells:
        if c302.is_muscle(c):
            all_muscles.append(c)
        else:
            all_neurons.append(c)

    info = "# Information on neuron and muscles\n"
    info += "## Generated using %s\n" % ver_info

    info += "### Neurons (%i)\n" % (len(all_neuron_info))
    info += "<table>\n"
    for n in all_neuron_info:
        info += "<tr>\n"
        ni = all_neuron_info[n]
        # print(ni)
        info += (
            "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Colour: %s</td>"
            % (n, _info_set(ni[1]), _info_set(ni[2]), _info_set(ni[3]), ni[4], ni[5])
        )
        info += "</tr>\n"
    info += "</table>\n"

    info += "### Muscles (%i)\n" % (len(all_muscle_info))
    info += "<table>\n"
    for n in all_muscle_info:
        info += "<tr>\n"
        ni = all_muscle_info[n]
        info += (
            "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Colour: %s</td>"
            % (n, _info_set(ni[1]), _info_set(ni[2]), _info_set(ni[3]), ni[4], ni[5])
        )
        info += "</tr>\n"
    info += "</table>\n"

    with open("examples/summary/summary.md", "w") as f2:
        # f2.write('<html><body>%s</body></html>'%info)
        f2.write("%s" % info)


def _info_set(s):
    s = sorted(s)
    return ", ".join(["%s" % i for i in s])


if __name__ == "__main__":
    from neuroml.loaders import read_neuroml2_file

    config = "c302_C0_Full.net.nml"

    nml_doc = read_neuroml2_file("examples/%s" % config)

    generate_c302_info(nml_doc)
