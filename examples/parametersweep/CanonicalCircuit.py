from neuromllite import (
    Cell,
    Synapse,
    InputSource,
    Input,
    RandomLayout,
    Population,
    Simulation,
    Network,
    Projection,
    RandomConnectivity,
    RectangularRegion,
)
from neuromllite.NetworkGenerator import check_to_generate_or_run
import sys

sys.path.append("..")

INTERNEURON = "interneuron"
MOTORNEURON = "motorneuron"
MOTORNEURON_DORSAL = "motorneuronD"
MOTORNEURON_VENTRAL = "motorneuronV"
MUSCLE = "muscle"


neuron_id = "GenericNeuronCell"
neuron_nmllite = Cell(id=neuron_id, neuroml2_source_file="%s.cell.nml" % (neuron_id))

muscle_id = "GenericMuscleCell"
muscle_nmllite = Cell(id=muscle_id, neuroml2_source_file="%s.cell.nml" % (muscle_id))

interneuron_region = RectangularRegion(
    id="%ss" % INTERNEURON, x=0, y=0, z=0, width=100, height=100, depth=100
)
motorneurons_d_region = RectangularRegion(
    id="Dorsal %ss" % MOTORNEURON, x=200, y=0, z=0, width=100, height=100, depth=100
)
motorneurons_v_region = RectangularRegion(
    id="Ventral %ss" % MOTORNEURON, x=200, y=200, z=0, width=100, height=100, depth=100
)
muscles_region = RectangularRegion(
    id="%ss" % MUSCLE, x=300, y=0, z=0, width=1000, height=100, depth=1000
)

regions = {
    INTERNEURON: interneuron_region,
    MOTORNEURON_DORSAL: motorneurons_d_region,
    MOTORNEURON_VENTRAL: motorneurons_v_region,
    MUSCLE: muscles_region,
}

colors = {INTERNEURON: "1 0 .4", MOTORNEURON: ".5 .4 1", MUSCLE: "0 0.6 0"}

all_cell_pops = {}


def add_cell(net, name, type, region=None):
    region = regions[type] if region is None else regions[region]
    cell_pop = Population(
        id=name,
        size=1,
        component=neuron_nmllite.id,
        properties={"color": colors[type]},
        random_layout=RandomLayout(region=region.id),
    )

    all_cell_pops[name] = cell_pop
    net.populations.append(cell_pop)


def add_connection(net, pre, post, syn, weight):
    net.projections.append(
        Projection(
            id="proj_%s_%s" % (pre, post),
            presynaptic=pre,
            postsynaptic=post,
            synapse=syn.id,
            delay=0,
            weight=weight,
            type="continuousProjection",
            random_connectivity=RandomConnectivity(probability=1),
        )
    )


def add_elec_connection(net, pre, post, syn, weight):
    net.projections.append(
        Projection(
            id="elec_proj_%s_%s" % (pre, post),
            presynaptic=pre,
            postsynaptic=post,
            synapse=syn.id,
            type="electricalProjection",
            weight=weight,
            random_connectivity=RandomConnectivity(probability=1),
        )
    )


def generate(duration=1000, paramset="C"):
    global neuron_id
    global neuron_nmllite
    # reference = "%s_%s"%(config, cell)

    reference = "Canonical_%s" % paramset  # %(config, cell)

    net = Network(id=reference)
    net.parameters = {}

    cell_params = {"bias": 0, "gain": 1, "tau": "100ms"}

    if paramset == "W2D":
        neuron_id = "GenericNeuronCellW2D"

        neuron_nmllite = Cell(id=neuron_id, lems_source_file="../../c302/cell_W2D.xml")
        neuron_nmllite.parameters = {}

        for p in cell_params:
            neuron_nmllite.parameters[p] = p
            net.parameters[p] = cell_params[p]

        exc_syn = Synapse(
            id="neuron_to_neuron_exc_syn_w2d", neuroml2_source_file="test_syns.xml"
        )
        net.synapses.append(exc_syn)

        inh_syn = Synapse(
            id="neuron_to_neuron_inh_syn_w2d", neuroml2_source_file="test_syns.xml"
        )
        # net.synapses.append(inh_syn)

        elec_syn = Synapse(id="gapJunction0", neuroml2_source_file="test_syns2.xml")
        net.synapses.append(elec_syn)

    else:
        exc_syn = Synapse(
            id="neuron_to_neuron_exc_syn", neuroml2_source_file="test_syns.xml"
        )
        net.synapses.append(exc_syn)
        inh_syn = Synapse(
            id="neuron_to_neuron_inh_syn", neuroml2_source_file="test_syns.xml"
        )
        net.synapses.append(inh_syn)

    net.cells.append(neuron_nmllite)
    # net.cells.append(muscle_nmllite)

    net.regions.append(interneuron_region)
    net.regions.append(motorneurons_d_region)
    net.regions.append(motorneurons_v_region)
    net.regions.append(muscles_region)

    add_cell(net, "AVB", INTERNEURON)
    add_cell(net, "VB", MOTORNEURON, MOTORNEURON_VENTRAL)
    add_cell(net, "DB", MOTORNEURON, MOTORNEURON_DORSAL)
    add_cell(net, "VD", MOTORNEURON, MOTORNEURON_VENTRAL)

    add_cell(net, "DD", MOTORNEURON, MOTORNEURON_DORSAL)

    net.parameters["stim_duration"] = "2000ms"
    net.parameters["stim_amp"] = "3.5pA"
    net.parameters["weight_IN_MN"] = 3
    net.parameters["weight_MN_MN_Exc"] = 20
    net.parameters["weight_MN_MN_Inh"] = 40
    net.parameters["scaleDinout"] = 0.5

    if paramset == "W2D":
        net.parameters["stim_duration"] = "2000ms"
        net.parameters["stim_amp"] = "0.2pA"
        net.parameters["weight_IN_MN"] = 1
        net.parameters["weight_MN_MN_Exc"] = 1
        net.parameters["weight_MN_MN_Inh"] = -5
        net.parameters["scaleDinout"] = 0.5

    mode = "circ"

    if paramset == "W2D":
        mode = "iclamp"

    if mode == "circ":
        add_connection(net, "AVB", "VB", exc_syn, "weight_IN_MN")
        add_connection(net, "AVB", "DB", exc_syn, "weight_IN_MN * scaleDinout")
        add_connection(net, "DB", "VD", exc_syn, "weight_MN_MN_Exc")
        add_connection(net, "DB", "DD", exc_syn, "weight_MN_MN_Exc")
        add_connection(net, "VB", "VD", exc_syn, "weight_MN_MN_Exc")
        add_connection(net, "VB", "DD", exc_syn, "weight_MN_MN_Exc")

        add_connection(net, "VD", "VB", inh_syn, "weight_MN_MN_Inh")
        add_connection(net, "DD", "DB", inh_syn, "weight_MN_MN_Inh")

    if mode == "iclamp":
        add_elec_connection(net, "AVB", "VB", elec_syn, "weight_IN_MN")
        add_connection(net, "VB", "VD", exc_syn, "weight_MN_MN_Exc")
        #
        """add_connection(net, "AVB", "VB", exc_syn, 0)
        # add_connection(net, "VB", "DD", exc_syn, "weight_MN_MN_Exc")

        add_connection(net, "VD", "VB", inh_syn, "weight_MN_MN_Inh")"""

    if paramset == "W2D":
        input_source = InputSource(
            id="iclamp_0",
            neuroml2_input="PulseGenerator",
            parameters={
                "amplitude": "stim_amp",
                "delay": "500ms",
                "duration": "stim_duration",
            },
        )

    else:
        input_source = InputSource(
            id="iclamp_0",
            neuroml2_input="PulseGenerator",
            parameters={
                "amplitude": "stim_amp",
                "delay": "500ms",
                "duration": "stim_duration",
            },
        )

    net.input_sources.append(input_source)

    net.inputs.append(
        Input(id="stim", input_source=input_source.id, population="AVB", percentage=100)
    )

    print(net.to_json())
    new_file = net.to_json_file("%s.json" % net.id)

    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(
        id="Sim%s" % net.id,
        network=new_file,
        duration=duration,
        dt="0.1",
        record_traces={"all": "*"},
    )

    if paramset == "W2D":
        sim.record_traces = {}
        sim.record_variables = {
            "state": {"all": "*"},
            "output": {"all": "*"},
        }  # "V": {"all": "*"},
        """sim.plots2D = {
            "DB-VB": {
                "x_axis": "VD/0/%s/output" % neuron_id,
                "y_axis": "VB/0/%s/output" % neuron_id,
            }
        }"""

    sim.to_json_file()

    return sim, net


if __name__ == "__main__":
    if "-all" in sys.argv:
        for cell in colors:
            generate(cell, 3000, config="IClamp", parameters={"stim_amp": "1pA"})

    elif "-w2d" in sys.argv:
        sim, net = generate(duration=3000, paramset="W2D")

        check_to_generate_or_run(sys.argv, sim)

    elif "-d" in sys.argv:
        sim, net = generate(duration=3000, paramset="D")

        check_to_generate_or_run(sys.argv, sim)

    else:
        # sim, net = generate('cADpyr229_L23_PC_c292d67a2e_0_0', 3000, config="IClamp")

        sim, net = generate(duration=3000)

        check_to_generate_or_run(sys.argv, sim)
