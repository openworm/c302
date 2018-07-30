'''

    Parameters BC1:
        Cells:           Simple integrate and fire cells, custom component type, with an "activity" variable (same as B)
        Chem Synapses:   Analogue/graded synapses; continuous transmission (voltage dependent) (same as C1)
        Gap junctions:   Electrical connection; current linerly depends on difference in voltages 
        
    ASSESSMENT:
        Probably not very useful in longer term; same criticisms as parameters A; see C0

'''

from neuroml import Cell
from neuroml import Morphology
from neuroml import Point3DWithDiam
from neuroml import Segment
from neuroml import BiophysicalProperties
from neuroml import IntracellularProperties
from neuroml import Resistivity
from neuroml import Species
from neuroml import MembraneProperties
from neuroml import InitMembPotential
from neuroml import SpecificCapacitance
from neuroml import ChannelDensity
from neuroml import SpikeThresh

from neuroml import GradedSynapse
from neuroml import GapJunction
from neuroml import PulseGenerator

from bioparameters import c302ModelPrototype

from parameters_B import IafActivityCell


class ParameterisedModel(c302ModelPrototype):

    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "BC1"
        self.custom_component_types_definitions = 'cell_B.xml'
        
        self.set_default_bioparameters()

    def set_default_bioparameters(self):

        self.add_bioparameter("muscle_iaf_leak_reversal", "-50mV", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_reset", "-50mV", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_thresh", "-30mV", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_C", "3pF", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_conductance", "0.1nS", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_tau1", "50ms", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_iaf_leak_reversal", "-50mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_reset", "-50mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_thresh", "-30mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_C", "3pF", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_conductance", "0.1nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_tau1", "50ms", "BlindGuess", "0.1")


        self.add_bioparameter("neuron_to_neuron_exc_syn_conductance", "8 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_conductance", "8 nS", "BlindGuess", "0.1")

        self.add_bioparameter("exc_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_vth", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_erev", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_k", "0.025per_ms", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_neuron_inh_syn_conductance", "8 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_conductance", "8 nS", "BlindGuess", "0.1")

        self.add_bioparameter("inh_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_vth", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_erev", "-70 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_k", "0.025per_ms", "BlindGuess", "0.1")
        

        self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0.3 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_elec_syn_gbase", "0.3 nS", "BlindGuess", "0.1")

        self.add_bioparameter("unphysiological_offset_current", "0 nA", "KnownError", "0") # Can be activated later
        self.add_bioparameter("unphysiological_offset_current_del", "0 ms", "KnownError", "0")
        self.add_bioparameter("unphysiological_offset_current_dur", "2000 ms", "KnownError", "0")

    def create_generic_muscle_cell(self):
        self.generic_muscle_cell = IafActivityCell(id="generic_muscle_iaf_cell", 
                                C =                 self.get_bioparameter("muscle_iaf_C").value,
                                thresh =            self.get_bioparameter("muscle_iaf_thresh").value,
                                reset =             self.get_bioparameter("muscle_iaf_reset").value,
                                leak_conductance =  self.get_bioparameter("muscle_iaf_conductance").value,
                                leak_reversal =     self.get_bioparameter("muscle_iaf_leak_reversal").value)   
   
    def create_generic_neuron_cell(self):
        self.generic_neuron_cell = IafActivityCell(id="generic_neuron_iaf_cell", 
                                C =                 self.get_bioparameter("neuron_iaf_C").value,
                                thresh =            self.get_bioparameter("neuron_iaf_thresh").value,
                                reset =             self.get_bioparameter("neuron_iaf_reset").value,
                                leak_conductance =  self.get_bioparameter("neuron_iaf_conductance").value,
                                leak_reversal =     self.get_bioparameter("neuron_iaf_leak_reversal").value)  

    def create_offset(self):

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


    def create_models(self):
        self.create_generic_muscle_cell()
        self.create_generic_neuron_cell()
        self.create_offset()
        self.create_neuron_to_muscle_syn()
        self.create_neuron_to_neuron_syn()
