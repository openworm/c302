'''

    Parameters X:
        Cells:           Single compartment, conductance based, passive cell
        Chem Synapses:   Analogue/graded synapses; continuous transmission (voltage dependent)
        Gap junctions:   Electrical connection; current linerly depends on difference in voltages 
        
    ASSESSMENT:
        TBC...

'''

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

from neuroml import GradedSynapse
from neuroml import GapJunction
from neuroml import PulseGenerator

from c302.bioparameters import c302ModelPrototype

class ParameterisedModel(c302ModelPrototype):

    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "X"
        self.custom_component_types_definitions = 'cell_X.xml'
        
        self.set_default_bioparameters()
        self.print_("Set default parameters for %s"%self.level)

    def set_default_bioparameters(self):

        self.add_bioparameter("cell_diameter", "5", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_length", "20", "BlindGuess", "0.1")

        self.add_bioparameter("initial_memb_pot", "-45 mV", "BlindGuess", "0.1")
        
        self.add_bioparameter("specific_capacitance", "1 uF_per_cm2", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_spike_thresh", "-20 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_spike_thresh", "-20 mV", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_leak_cond_density", "5e-7 S_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_leak_cond_density", "0.01 mS_per_cm2", "BlindGuess", "0.1")
        
        self.add_bioparameter("leak_erev", "-35 mV", "BlindGuess", "0.1")
        
        self.add_bioparameter("neuron_to_neuron_exc_syn_conductance", "0.00001 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_conductance", "0.000 nS", "BlindGuess", "0.1")
        
        self.add_bioparameter("exc_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_vth", "-25 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_erev", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_k", "0.025per_ms", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_neuron_inh_syn_conductance", "0.00 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_conductance", "0.00 nS", "BlindGuess", "0.1")
        
        self.add_bioparameter("inh_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_vth", "-25 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_erev", "-45 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_k", "0.025per_ms", "BlindGuess", "0.1")
        
        self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0.00052 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_elec_syn_gbase", "0.00052 nS", "BlindGuess", "0.1")


        self.add_bioparameter("unphysiological_offset_current", "0 pA", "KnownError", "0") # Can be activated later
        self.add_bioparameter("unphysiological_offset_current_del", "0 ms", "KnownError", "0")
        self.add_bioparameter("unphysiological_offset_current_dur", "2000 ms", "KnownError", "0")





    def create_models(self):
        self.create_generic_muscle_cell()
        self.create_generic_neuron_cell()
        self.create_offsetcurrent()
        self.create_neuron_to_neuron_syn()
        self.create_neuron_to_muscle_syn()


    def create_generic_muscle_cell(self):

        self.generic_muscle_cell = Cell(id = "GenericMuscleCell")

        morphology = Morphology()
        morphology.id = "morphology_"+self.generic_muscle_cell.id

        self.generic_muscle_cell.morphology = morphology

        prox_point = Point3DWithDiam(x="0", y="0", z="0", diameter=self.get_bioparameter("cell_diameter").value)
        dist_point = Point3DWithDiam(x="0", y=self.get_bioparameter("muscle_length").value, z="0", diameter=self.get_bioparameter("cell_diameter").value)

        segment = Segment(id="0",
                          name="soma",
                          proximal = prox_point, 
                          distal = dist_point)

        morphology.segments.append(segment)

        self.generic_muscle_cell.biophysical_properties = BiophysicalProperties(id="biophys_"+self.generic_muscle_cell.id)

        mp = MembraneProperties()
        self.generic_muscle_cell.biophysical_properties.membrane_properties = mp

        mp.init_memb_potentials.append(InitMembPotential(value=self.get_bioparameter("initial_memb_pot").value))

        mp.specific_capacitances.append(SpecificCapacitance(value=self.get_bioparameter("specific_capacitance").value))

        mp.spike_threshes.append(SpikeThresh(value=self.get_bioparameter("muscle_spike_thresh").value))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_leak_cond_density").value, 
                                                   id="Leak_all", 
                                                   ion_channel="Leak", 
                                                   erev=self.get_bioparameter("leak_erev").value,
                                                   ion="non_specific"))

        ip = IntracellularProperties()
        self.generic_muscle_cell.biophysical_properties.intracellular_properties = ip

        # NOTE: resistivity/axial resistance not used for single compartment cell models, so value irrelevant!
        ip.resistivities.append(Resistivity(value="0.1 kohm_cm"))



    def create_generic_neuron_cell(self):

        self.generic_neuron_cell = Cell(id = "GenericNeuronCell")

        morphology = Morphology()
        morphology.id = "morphology_"+self.generic_neuron_cell.id

        self.generic_neuron_cell.morphology = morphology

        prox_point = Point3DWithDiam(x="0", y="0", z="0", diameter=self.get_bioparameter("cell_diameter").value)
        dist_point = Point3DWithDiam(x="0", y="0", z="0", diameter=self.get_bioparameter("cell_diameter").value)

        segment = Segment(id="0",
                          name="soma",
                          proximal = prox_point, 
                          distal = dist_point)

        morphology.segments.append(segment)

        self.generic_neuron_cell.biophysical_properties = BiophysicalProperties(id="biophys_"+self.generic_neuron_cell.id)

        mp = MembraneProperties()
        self.generic_neuron_cell.biophysical_properties.membrane_properties = mp

        mp.init_memb_potentials.append(InitMembPotential(value=self.get_bioparameter("initial_memb_pot").value))

        mp.specific_capacitances.append(SpecificCapacitance(value=self.get_bioparameter("specific_capacitance").value))

        mp.spike_threshes.append(SpikeThresh(value=self.get_bioparameter("neuron_spike_thresh").value))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("neuron_leak_cond_density").value, 
                                                   id="Leak_all", 
                                                   ion_channel="Leak", 
                                                   erev=self.get_bioparameter("leak_erev").value,
                                                   ion="non_specific"))

        ip = IntracellularProperties()
        self.generic_neuron_cell.biophysical_properties.intracellular_properties = ip

        # NOTE: resistivity/axial resistance not used for single compartment cell models, so value irrelevant!
        ip.resistivities.append(Resistivity(value="0.1 kohm_cm"))


    def create_offsetcurrent(self):

        self.offset_current = PulseGenerator(id="offset_current",
                                delay=self.get_bioparameter("unphysiological_offset_current_del").value,
                                duration=self.get_bioparameter("unphysiological_offset_current_dur").value,
                                amplitude=self.get_bioparameter("unphysiological_offset_current").value)

    

    def create_neuron_to_neuron_syn(self):
        self.neuron_to_neuron_exc_syn = GradedSynapse(id="neuron_to_neuron_exc_syn",
                                conductance =        self.get_bioparameter("neuron_to_neuron_exc_syn_conductance").value,
                                delta =              self.get_bioparameter("exc_syn_delta").value,
                                Vth =                self.get_bioparameter("exc_syn_vth").value,
                                erev =               self.get_bioparameter("exc_syn_erev").value,
                                k =                  self.get_bioparameter("exc_syn_k").value)


        self.neuron_to_neuron_inh_syn = GradedSynapse(id="neuron_to_neuron_inh_syn",
                                conductance =        self.get_bioparameter("neuron_to_neuron_inh_syn_conductance").value,
                                delta =              self.get_bioparameter("inh_syn_delta").value,
                                Vth =                self.get_bioparameter("inh_syn_vth").value,
                                erev =               self.get_bioparameter("inh_syn_erev").value,
                                k =                  self.get_bioparameter("inh_syn_k").value)

        self.neuron_to_neuron_elec_syn = GapJunction(id="neuron_to_neuron_elec_syn",
                               conductance =    self.get_bioparameter("neuron_to_neuron_elec_syn_gbase").value)



    def create_neuron_to_muscle_syn(self):
        self.neuron_to_muscle_exc_syn = GradedSynapse(id="neuron_to_muscle_exc_syn",
                                conductance =        self.get_bioparameter("neuron_to_muscle_exc_syn_conductance").value,
                                delta =              self.get_bioparameter("exc_syn_delta").value,
                                Vth =                self.get_bioparameter("exc_syn_vth").value,
                                erev =               self.get_bioparameter("exc_syn_erev").value,
                                k =                  self.get_bioparameter("exc_syn_k").value)


        self.neuron_to_muscle_inh_syn = GradedSynapse(id="neuron_to_muscle_inh_syn",
                                conductance =        self.get_bioparameter("neuron_to_muscle_inh_syn_conductance").value,
                                delta =              self.get_bioparameter("inh_syn_delta").value,
                                Vth =                self.get_bioparameter("inh_syn_vth").value,
                                erev =               self.get_bioparameter("inh_syn_erev").value,
                                k =                  self.get_bioparameter("inh_syn_k").value)

        self.neuron_to_muscle_elec_syn = GapJunction(id="neuron_to_muscle_elec_syn",
                               conductance =    self.get_bioparameter("neuron_to_muscle_elec_syn_gbase").value)



    def get_elec_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False
        if type == 'neuron_to_neuron':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'neuron_to_neuron_elec_syn_%s', 'gbase')
            conn_id = 'neuron_to_neuron_elec_syn'
        elif type == 'neuron_to_muscle':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'neuron_to_muscle_elec_syn_%s', 'gbase')
            conn_id = 'neuron_to_muscle_elec_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_elec_syn' % (pre_cell, post_cell)

        return GapJunction(id=conn_id, conductance=gbase)



    def get_exc_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False

        specific_param_template = '%s_to_%s_exc_syn_%s'
        if type == 'neuron_to_neuron':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_neuron_exc_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                             'erev')
            delta = self.get_conn_param(pre_cell, post_cell, specific_param_template,'exc_syn_%s',
                                                              'delta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                            'vth')
            k = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                          'k')
            
            conn_id = 'neuron_to_neuron_exc_syn'

        elif type == 'neuron_to_muscle':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_muscle_exc_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                             'erev')
            delta = self.get_conn_param(pre_cell, post_cell, specific_param_template,'exc_syn_%s',
                                                              'delta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                            'vth')
            k = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                          'k')
            
            conn_id = 'neuron_to_muscle_exc_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_exc_syn' % (pre_cell, post_cell)

        return GradedSynapse(id=conn_id,
                             conductance=conductance,
                             delta=delta,
                             Vth=vth,
                             erev=erev,
                             k=k)

    def get_inh_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False

        specific_param_template = '%s_to_%s_inh_syn_%s'
        if type == 'neuron_to_neuron':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_neuron_inh_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                             'erev')
            delta = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'inh_syn_%s',
                                                              'delta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                            'vth')
            k = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                          'k')
            
            conn_id = 'neuron_to_neuron_inh_syn'

        elif type == 'neuron_to_muscle':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_muscle_inh_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                             'erev')
            delta = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                           'delta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                            'vth')
            k = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                            'k')
            
            conn_id = 'neuron_to_muscle_inh_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_inh_syn' % (pre_cell, post_cell)

        return GradedSynapse(id=conn_id,
                             conductance=conductance,
                             delta=delta,
                             Vth=vth,
                             erev=erev,
                             k=k)