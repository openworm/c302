"""

Parameters X:
    Cells:           Single compartment, conductance based, passive cell
    Chem Synapses:   Analogue/graded synapses; continuous transmission (voltage dependent)
    Gap junctions:   Electrical connection; current linerly depends on difference in voltages

ASSESSMENT:
    TBC...

"""

from neuroml import Cell
from neuroml import Morphology
from neuroml import Point3DWithDiam
from neuroml import Segment
from neuroml import BiophysicalProperties
from neuroml import IntracellularProperties
from neuroml import Resistivity
from neuroml import MembraneProperties
from neuroml import InitMembPotential
from neuroml import SpecificCapacitance
from neuroml import ChannelDensity
from neuroml import SpikeThresh

from neuroml import GapJunction
from neuroml import PulseGenerator

from c302.bioparameters import c302ModelPrototype


class ParameterisedModel(c302ModelPrototype):
    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "X"
        self.custom_component_types_definitions = ["cell_X.xml", "custom_synapses.xml"]

        self.set_default_bioparameters()
        self.print_("Set default parameters for %s" % self.level)

    def set_default_bioparameters(self):
        self.add_bioparameter("cell_diameter", "5.641895835477563", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_length", "5.641895835477563", "BlindGuess", "0.1")

        self.add_bioparameter("initial_memb_pot", "-40 mV", "BlindGuess", "0.1")

        self.add_bioparameter(
            "specific_capacitance", "1 uF_per_cm2", "BlindGuess", "0.1"
        )

        self.add_bioparameter("muscle_spike_thresh", "-20 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_spike_thresh", "-20 mV", "BlindGuess", "0.1")

        self.add_bioparameter(
            "muscle_leak_cond_density", "0.01 mS_per_cm2", "BlindGuess", "0.1"
        )
        self.add_bioparameter(
            "neuron_leak_cond_density", "0.01 mS_per_cm2", "BlindGuess", "0.1"
        )

        self.add_bioparameter("leak_erev", "-35 mV", "BlindGuess", "0.1")

        self.add_bioparameter(
            "neuron_to_neuron_exc_syn_conductance", "100 pS", "BlindGuess", "0.1"
        )
        self.add_bioparameter(
            "neuron_to_muscle_exc_syn_conductance", "0.00 pS", "BlindGuess", "0.1"
        )

        self.add_bioparameter("exc_syn_ar", "1 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_ad", "5 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_beta", "0.125 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_vth", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_erev", "0 mV", "BlindGuess", "0.1")

        self.add_bioparameter(
            "neuron_to_neuron_inh_syn_conductance", "100 pS", "BlindGuess", "0.1"
        )
        self.add_bioparameter(
            "neuron_to_muscle_inh_syn_conductance", "0.00 nS", "BlindGuess", "0.1"
        )

        self.add_bioparameter("inh_syn_ar", "1 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_ad", "5 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_beta", "0.125 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_vth", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_erev", "-45 mV", "BlindGuess", "0.1")

        self.add_bioparameter(
            "neuron_to_neuron_elec_syn_gbase", "100 pS", "BlindGuess", "0.1"
        )
        self.add_bioparameter(
            "neuron_to_muscle_elec_syn_gbase", "100 pS", "BlindGuess", "0.1"
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
        self.generic_muscle_cell = Cell(id="GenericMuscleCell")

        morphology = Morphology()
        morphology.id = "morphology_" + self.generic_muscle_cell.id

        self.generic_muscle_cell.morphology = morphology

        prox_point = Point3DWithDiam(
            x="0", y="0", z="0", diameter=self.get_bioparameter("cell_diameter").value
        )
        dist_point = Point3DWithDiam(
            x="0",
            y=self.get_bioparameter("muscle_length").value,
            z="0",
            diameter=self.get_bioparameter("cell_diameter").value,
        )

        segment = Segment(id="0", name="soma", proximal=prox_point, distal=dist_point)

        morphology.segments.append(segment)

        self.generic_muscle_cell.biophysical_properties = BiophysicalProperties(
            id="biophys_" + self.generic_muscle_cell.id
        )

        mp = MembraneProperties()
        self.generic_muscle_cell.biophysical_properties.membrane_properties = mp

        mp.init_memb_potentials.append(
            InitMembPotential(value=self.get_bioparameter("initial_memb_pot").value)
        )

        mp.specific_capacitances.append(
            SpecificCapacitance(
                value=self.get_bioparameter("specific_capacitance").value
            )
        )

        mp.spike_threshes.append(
            SpikeThresh(value=self.get_bioparameter("muscle_spike_thresh").value)
        )

        mp.channel_densities.append(
            ChannelDensity(
                cond_density=self.get_bioparameter("muscle_leak_cond_density").value,
                id="Leak_all",
                ion_channel="Leak",
                erev=self.get_bioparameter("leak_erev").value,
                ion="non_specific",
            )
        )

        ip = IntracellularProperties()
        self.generic_muscle_cell.biophysical_properties.intracellular_properties = ip

        # NOTE: resistivity/axial resistance not used for single compartment cell models, so value irrelevant!
        ip.resistivities.append(Resistivity(value="0.1 kohm_cm"))

    def create_generic_neuron_cell(self):
        self.generic_neuron_cell = Cell(id="GenericNeuronCell")

        morphology = Morphology()
        morphology.id = "morphology_" + self.generic_neuron_cell.id

        self.generic_neuron_cell.morphology = morphology

        prox_point = Point3DWithDiam(
            x="0", y="0", z="0", diameter=self.get_bioparameter("cell_diameter").value
        )
        dist_point = Point3DWithDiam(
            x="0", y="0", z="0", diameter=self.get_bioparameter("cell_diameter").value
        )

        segment = Segment(id="0", name="soma", proximal=prox_point, distal=dist_point)

        morphology.segments.append(segment)

        self.generic_neuron_cell.biophysical_properties = BiophysicalProperties(
            id="biophys_" + self.generic_neuron_cell.id
        )

        mp = MembraneProperties()
        self.generic_neuron_cell.biophysical_properties.membrane_properties = mp

        mp.init_memb_potentials.append(
            InitMembPotential(value=self.get_bioparameter("initial_memb_pot").value)
        )

        mp.specific_capacitances.append(
            SpecificCapacitance(
                value=self.get_bioparameter("specific_capacitance").value
            )
        )

        mp.spike_threshes.append(
            SpikeThresh(value=self.get_bioparameter("neuron_spike_thresh").value)
        )

        mp.channel_densities.append(
            ChannelDensity(
                cond_density=self.get_bioparameter("neuron_leak_cond_density").value,
                id="Leak_all",
                ion_channel="Leak",
                erev=self.get_bioparameter("leak_erev").value,
                ion="non_specific",
            )
        )

        ip = IntracellularProperties()
        self.generic_neuron_cell.biophysical_properties.intracellular_properties = ip

        # NOTE: resistivity/axial resistance not used for single compartment cell models, so value irrelevant!
        ip.resistivities.append(Resistivity(value="0.1 kohm_cm"))

    def create_offsetcurrent(self):
        self.offset_current = PulseGenerator(
            id="offset_current",
            delay=self.get_bioparameter("unphysiological_offset_current_del").value,
            duration=self.get_bioparameter("unphysiological_offset_current_dur").value,
            amplitude=self.get_bioparameter("unphysiological_offset_current").value,
        )

    def create_neuron_to_neuron_syn(self):
        self.neuron_to_neuron_exc_syn = GradedSynapse2(
            id="neuron_to_neuron_exc_syn",
            conductance=self.get_bioparameter(
                "neuron_to_neuron_exc_syn_conductance"
            ).value,
            ar=self.get_bioparameter("exc_syn_ar").value,
            ad=self.get_bioparameter("exc_syn_ad").value,
            beta=self.get_bioparameter("exc_syn_beta").value,
            vth=self.get_bioparameter("exc_syn_vth").value,
            erev=self.get_bioparameter("exc_syn_erev").value,
        )

        self.neuron_to_neuron_inh_syn = GradedSynapse2(
            id="neuron_to_neuron_inh_syn",
            conductance=self.get_bioparameter(
                "neuron_to_neuron_inh_syn_conductance"
            ).value,
            ar=self.get_bioparameter("inh_syn_ar").value,
            ad=self.get_bioparameter("inh_syn_ad").value,
            beta=self.get_bioparameter("inh_syn_beta").value,
            vth=self.get_bioparameter("inh_syn_vth").value,
            erev=self.get_bioparameter("inh_syn_erev").value,
        )

        self.neuron_to_neuron_elec_syn = GapJunction(
            id="neuron_to_neuron_elec_syn",
            conductance=self.get_bioparameter("neuron_to_neuron_elec_syn_gbase").value,
        )

    def create_neuron_to_muscle_syn(self):
        self.neuron_to_muscle_exc_syn = GradedSynapse2(
            id="neuron_to_muscle_exc_syn",
            conductance=self.get_bioparameter(
                "neuron_to_muscle_exc_syn_conductance"
            ).value,
            ar=self.get_bioparameter("exc_syn_ar").value,
            ad=self.get_bioparameter("exc_syn_ad").value,
            beta=self.get_bioparameter("exc_syn_beta").value,
            vth=self.get_bioparameter("exc_syn_vth").value,
            erev=self.get_bioparameter("exc_syn_erev").value,
        )

        self.neuron_to_muscle_inh_syn = GradedSynapse2(
            id="neuron_to_muscle_inh_syn",
            conductance=self.get_bioparameter(
                "neuron_to_muscle_inh_syn_conductance"
            ).value,
            ar=self.get_bioparameter("inh_syn_ar").value,
            ad=self.get_bioparameter("inh_syn_ad").value,
            beta=self.get_bioparameter("inh_syn_beta").value,
            vth=self.get_bioparameter("inh_syn_vth").value,
            erev=self.get_bioparameter("inh_syn_erev").value,
        )

        self.neuron_to_muscle_elec_syn = GapJunction(
            id="neuron_to_muscle_elec_syn",
            conductance=self.get_bioparameter("neuron_to_muscle_elec_syn_gbase").value,
        )

    def get_elec_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False
        if type == "neuron_to_neuron":
            gbase = self.get_conn_param(
                pre_cell,
                post_cell,
                "%s_to_%s_elec_syn_%s",
                "neuron_to_neuron_elec_syn_%s",
                "gbase",
            )
            conn_id = "neuron_to_neuron_elec_syn"
        elif type == "neuron_to_muscle":
            gbase = self.get_conn_param(
                pre_cell,
                post_cell,
                "%s_to_%s_elec_syn_%s",
                "neuron_to_muscle_elec_syn_%s",
                "gbase",
            )
            conn_id = "neuron_to_muscle_elec_syn"

        if self.found_specific_param:
            conn_id = "%s_to_%s_elec_syn" % (pre_cell, post_cell)

        return GapJunction(id=conn_id, conductance=gbase)

    def get_exc_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False

        specific_param_template = "%s_to_%s_exc_syn_%s"
        if type == "neuron_to_neuron":
            conductance = self.get_conn_param(
                pre_cell,
                post_cell,
                specific_param_template,
                "neuron_to_neuron_exc_syn_%s",
                "conductance",
            )
            erev = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "erev"
            )
            ar = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "ar"
            )
            ad = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "ad"
            )
            beta = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "beta"
            )
            vth = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "vth"
            )

            conn_id = "neuron_to_neuron_exc_syn"

        elif type == "neuron_to_muscle":
            conductance = self.get_conn_param(
                pre_cell,
                post_cell,
                specific_param_template,
                "neuron_to_muscle_exc_syn_%s",
                "conductance",
            )
            erev = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "erev"
            )
            ar = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "ar"
            )
            ad = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "ad"
            )
            beta = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "beta"
            )
            vth = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "exc_syn_%s", "vth"
            )
            conn_id = "neuron_to_muscle_exc_syn"

        if self.found_specific_param:
            conn_id = "%s_to_%s_exc_syn" % (pre_cell, post_cell)

        return GradedSynapse2(
            id=conn_id,
            conductance=conductance,
            ar=ar,
            ad=ad,
            beta=beta,
            vth=vth,
            erev=erev,
        )

    def get_inh_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False

        specific_param_template = "%s_to_%s_inh_syn_%s"
        if type == "neuron_to_neuron":
            conductance = self.get_conn_param(
                pre_cell,
                post_cell,
                specific_param_template,
                "neuron_to_neuron_inh_syn_%s",
                "conductance",
            )
            erev = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "erev"
            )
            ar = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "ar"
            )
            ad = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "ad"
            )
            beta = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "beta"
            )
            vth = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "vth"
            )

            conn_id = "neuron_to_neuron_inh_syn"

        elif type == "neuron_to_muscle":
            conductance = self.get_conn_param(
                pre_cell,
                post_cell,
                specific_param_template,
                "neuron_to_muscle_inh_syn_%s",
                "conductance",
            )
            erev = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "erev"
            )
            ar = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "ar"
            )
            ad = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "ad"
            )
            beta = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "beta"
            )
            vth = self.get_conn_param(
                pre_cell, post_cell, specific_param_template, "inh_syn_%s", "vth"
            )

            conn_id = "neuron_to_muscle_inh_syn"

        if self.found_specific_param:
            conn_id = "%s_to_%s_inh_syn" % (pre_cell, post_cell)

        return GradedSynapse2(
            id=conn_id,
            conductance=conductance,
            ar=ar,
            ad=ad,
            beta=beta,
            vth=vth,
            erev=erev,
        )

    def create_n_connection_synapse(self, prototype_syn, n, nml_doc, existing_synapses):
        if prototype_syn.id in existing_synapses:
            return existing_synapses[prototype_syn.id]

        if isinstance(prototype_syn, GradedSynapse2):
            existing_synapses[prototype_syn.id] = prototype_syn
            nml_doc.graded_synapses.append(prototype_syn)
            return prototype_syn
        else:
            return super(ParameterisedModel, self).create_n_connection_synapse(
                prototype_syn, n, nml_doc, existing_synapses
            )

    def is_analog_conn(self, syn):
        return super(ParameterisedModel, self).is_analog_conn(syn) or isinstance(
            syn, GradedSynapse2
        )


class GradedSynapse2:
    def __init__(self, id, conductance, ar, ad, beta, vth, erev):
        self.id = id
        self.conductance = conductance
        self.ar = ar
        self.ad = ad
        self.beta = beta
        self.vth = vth
        self.erev = erev

    def export(self, outfile, level, namespace, name_, pretty_print=True, **kwargs_):
        outfile.write(
            "    " * level
            + '<gradedSynapse2 id="%s" conductance="%s" ar="%s" ad="%s" beta="%s" vth="%s" erev="%s"/>\n'
            % (
                self.id,
                self.conductance,
                self.ar,
                self.ad,
                self.beta,
                self.vth,
                self.erev,
            )
        )
