'''

    Parameters B:
        Cells:           Simple integrate and fire cells, custom component type, with an "activity" variable
        Chem Synapses:   Event based, ohmic; one rise & one decay constant
        Gap junctions:   Electrical connection; current linerly depends on difference in voltages 
        
    ASSESSMENT:
        Not very useful in longer term; same criticisms as parameters A


    We are very aware that:
    
        C elegans neurons do NOT behave like Integrate & Fire neurons
        Their synapses are NOT like double exponential, conductance based synapses
        Electrical synapses are very different from event triggered, conductance based synapses
        
    The values below are a FIRST APPROXIMATION of neurons for use in a network to 
    investigate the synaptic connectivity of C elegans
    

'''

from neuroml import ExpTwoSynapse
from neuroml import GapJunction

from parameters_A import ParameterisedModel as ParameterisedModel_A

class ParameterisedModel(ParameterisedModel_A):

    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "B"
        self.custom_component_types_definitions = 'cell_B.xml'
        
        self.set_default_bioparameters()

    def set_default_bioparameters(self):

        
        param_C = ParameterisedModel_A()
        param_C.set_default_bioparameters()
        for b in param_C.bioparameters:
            
            if 'iaf' in b.name or 'exc' in b.name or 'inh' in b.name or 'current' in b.name:
                self.add_bioparameter_obj(b)
            else:
                self.print_(" - Ignoring inherited param: %s"%b)
        
        self.add_bioparameter("neuron_iaf_tau1", "50ms", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_tau1", self.get_bioparameter("neuron_iaf_tau1").value, "BlindGuess", "0.1")

        
        self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0.01 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_elec_syn_gbase", "0.01 nS", "BlindGuess", "0.1")

        
        
    def create_generic_muscle_cell(self):
        self.generic_muscle_cell = IafActivityCell(id="generic_muscle_iaf_cell", 
                                C =                 self.get_bioparameter("muscle_iaf_C").value,
                                thresh =            self.get_bioparameter("muscle_iaf_thresh").value,
                                reset =             self.get_bioparameter("muscle_iaf_reset").value,
                                leak_conductance =  self.get_bioparameter("muscle_iaf_conductance").value,
                                leak_reversal =     self.get_bioparameter("muscle_iaf_leak_reversal").value,
                                tau1 =              self.get_bioparameter("muscle_iaf_tau1").value)   
   
   
    def create_generic_neuron_cell(self):
        self.generic_neuron_cell = IafActivityCell(id="generic_neuron_iaf_cell", 
                                C =                 self.get_bioparameter("neuron_iaf_C").value,
                                thresh =            self.get_bioparameter("neuron_iaf_thresh").value,
                                reset =             self.get_bioparameter("neuron_iaf_reset").value,
                                leak_conductance =  self.get_bioparameter("neuron_iaf_conductance").value,
                                leak_reversal =     self.get_bioparameter("neuron_iaf_leak_reversal").value,
                                tau1 =              self.get_bioparameter("neuron_iaf_tau1").value)  


    def create_neuron_to_neuron_syn(self):
        self.neuron_to_neuron_exc_syn = ExpTwoSynapse(id="neuron_to_neuron_exc_syn",
                                gbase =         self.get_bioparameter("neuron_to_neuron_chem_exc_syn_gbase").value,
                                erev =          self.get_bioparameter("chem_exc_syn_erev").value,
                                tau_decay =     self.get_bioparameter("chem_exc_syn_decay").value,
                                tau_rise =      self.get_bioparameter("chem_exc_syn_rise").value)


        self.neuron_to_neuron_inh_syn = ExpTwoSynapse(id="neuron_to_neuron_inh_syn",
                                gbase =         self.get_bioparameter("neuron_to_neuron_chem_inh_syn_gbase").value,
                                erev =          self.get_bioparameter("chem_inh_syn_erev").value,
                                tau_decay =     self.get_bioparameter("chem_inh_syn_decay").value,
                                tau_rise =      self.get_bioparameter("chem_inh_syn_rise").value)
                      
                                
        self.neuron_to_neuron_elec_syn = GapJunction(id="neuron_to_neuron_elec_syn",
                                conductance =    self.get_bioparameter("neuron_to_neuron_elec_syn_gbase").value)


    def create_neuron_to_muscle_syn(self):
        self.neuron_to_muscle_exc_syn = ExpTwoSynapse(id="neuron_to_muscle_exc_syn",
                                gbase =         self.get_bioparameter("neuron_to_muscle_chem_exc_syn_gbase").value,
                                erev =          self.get_bioparameter("chem_exc_syn_erev").value,
                                tau_decay =     self.get_bioparameter("chem_exc_syn_decay").value,
                                tau_rise =      self.get_bioparameter("chem_exc_syn_rise").value)


        self.neuron_to_muscle_inh_syn = ExpTwoSynapse(id="neuron_to_muscle_inh_syn",
                                gbase =         self.get_bioparameter("neuron_to_muscle_chem_inh_syn_gbase").value,
                                erev =          self.get_bioparameter("chem_inh_syn_erev").value,
                                tau_decay =     self.get_bioparameter("chem_inh_syn_decay").value,
                                tau_rise =      self.get_bioparameter("chem_inh_syn_rise").value)
                      
                                
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
        elif type == 'muscle_to_muscle':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'muscle_to_muscle_elec_syn_%s', 'gbase')
            conn_id = 'muscle_to_muscle_elec_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_elec_syn' % (pre_cell, post_cell)

        return GapJunction(id=conn_id, conductance=gbase)



class IafActivityCell():
    
    def __init__(self, id, C, thresh, reset, leak_conductance, leak_reversal, tau1):
        self.id = id
        self.C = C
        self.thresh = thresh
        self.reset = reset
        self.leak_conductance = leak_conductance
        self.leak_reversal = leak_reversal
        self.tau1 = tau1
        
        
    
    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write('    '*level + '<iafCell type="iafActivityCell" id="%s" C="%s" thresh="%s" reset="%s" leakConductance="%s" leakReversal="%s" tau1="%s"/>\n'%(self.id, self.C, self.thresh, self.reset, self.leak_conductance, self.leak_reversal, self.tau1))

