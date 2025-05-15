"""

Parameters W2D:
    Cells:           Simple cell with just bias and gain from Worm2D
    Chem Synapses:   Continuous transmission of output of one cell to next
    Gap junctions:   Electrical connection; current linearly depends on difference in voltages

ASSESSMENT:
    Useful as tested in a number of 2D worm body models & very few parameters

"""

from neuroml import PulseGenerator

from neuroml import GapJunction

from c302.bioparameters import c302ModelPrototype


class ParameterisedModel(c302ModelPrototype):
    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "W2D"
        self.custom_component_types_definitions = [
            "cell_W2D.xml",
            "custom_synapses.xml",
        ]

        self.set_default_bioparameters()
        self.print_("Set default parameters for %s" % self.level)

    def set_default_bioparameters(self):
        self.add_bioparameter("initial_memb_pot", "-45 mV", "BlindGuess", "0.1")

        self.add_bioparameter(
            "neuron_to_neuron_elec_syn_gbase", "1 nS", "BlindGuess", "0.1"
        )
        self.add_bioparameter(
            "neuron_to_muscle_elec_syn_gbase", "1 nS", "BlindGuess", "0.1"
        )

        self.add_bioparameter(
            "unphysiological_offset_current", "0 pA", "KnownError", "0"
        )  # Can be activated later
        self.add_bioparameter(
            "unphysiological_offset_current_del", "0 ms", "KnownError", "0"
        )
        self.add_bioparameter(
            "unphysiological_offset_current_dur", "2000 ms", "KnownError", "0"
        )

    def create_models(self):
        self.create_generic_muscle_cell()
        self.create_generic_neuron_cell()
        self.create_offsetcurrent()
        self.create_neuron_to_neuron_syn()
        self.create_neuron_to_muscle_syn()

    def create_generic_muscle_cell(self):
        self.generic_muscle_cell = CellW2D(id="GenericMuscleCell")

    def create_generic_neuron_cell(self):
        self.generic_neuron_cell = CellW2D(id="GenericNeuronCell")

    def create_offsetcurrent(self):
        self.offset_current = PulseGenerator(
            id="offset_current",
            delay=self.get_bioparameter("unphysiological_offset_current_del").value,
            duration=self.get_bioparameter("unphysiological_offset_current_dur").value,
            amplitude=self.get_bioparameter("unphysiological_offset_current").value,
        )

    def create_neuron_to_neuron_syn(self):
        self.neuron_to_neuron_exc_syn = OutputSynapse(id="neuron_to_neuron_w2d")

        self.neuron_to_neuron_elec_syn = GapJunction(
            id="neuron_to_neuron_elec_syn",
            conductance=self.get_bioparameter("neuron_to_neuron_elec_syn_gbase").value,
        )

    def create_neuron_to_muscle_syn(self):
        self.neuron_to_muscle_exc_syn = OutputSynapse(id="neuron_to_muscle_w2d")

        self.neuron_to_muscle_elec_syn = GapJunction(
            id="neuron_to_muscle_elec_syn",
            conductance=self.get_bioparameter("neuron_to_muscle_elec_syn_gbase").value,
        )

    def get_elec_syn(self, pre_cell, post_cell, type):
        if type == "neuron_to_neuron":
            gbase = self.get_bioparameter("neuron_to_neuron_elec_syn_gbase").value
            conn_id = "neuron_to_neuron_elec_syn"

        elif type == "neuron_to_muscle":
            gbase = self.get_bioparameter("neuron_to_muscle_elec_syn_gbase").value
            conn_id = "neuron_to_muscle_elec_syn"

        return GapJunction(id=conn_id, conductance=gbase)

    def get_exc_syn(self, pre_cell, post_cell, type):
        return self.neuron_to_neuron_exc_syn

    def get_inh_syn(self, pre_cell, post_cell, type):
        return self.neuron_to_neuron_exc_syn


from c302.bioparameters import NonNeuroMLCustomType


class CellW2D(NonNeuroMLCustomType):
    def __init__(self, id):
        self.id = id


class OutputSynapse(NonNeuroMLCustomType):
    def __init__(self, id):
        self.id = id
