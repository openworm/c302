'''

    Parameters A:
        Cells:           Simple integrate and fire cells
        Chem Synapses:   Event based, ohmic; one rise & one decay constant
        Gap junctions:   NOT REAL GJs: using event based synapses, generally set to zero conductance
        
    ASSESSMENT:
        Not very useful in longer term; tendency for cells to over excite; difficult to tune networks
        
        
    We are very aware that:
    
        C elegans neurons do NOT behave like Integrate & Fire neurons
        Their synapses are NOT like double exponential, conductance based synapses
        Electrical synapses are very different from event triggered, conductance based synapses
        
    The values below are a FIRST APPROXIMATION of neurons for use in a network to 
    investigate the synaptic connectivity of C elegans

'''

from neuroml import IafCell
from neuroml import ExpTwoSynapse
from neuroml import PulseGenerator

from bioparameters import c302ModelPrototype


class ParameterisedModel(c302ModelPrototype):

    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "A"
        self.custom_component_types_definitions = None
        self.set_default_bioparameters()

    def set_default_bioparameters(self):

        self.add_bioparameter("neuron_iaf_leak_reversal", "-50mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_reset", "-50mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_thresh", "-30mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_C", "3pF", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_iaf_conductance", "0.1nS", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_iaf_leak_reversal", self.get_bioparameter("neuron_iaf_leak_reversal").value, "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_reset", self.get_bioparameter("neuron_iaf_reset").value, "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_thresh", self.get_bioparameter("neuron_iaf_thresh").value, "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_C", self.get_bioparameter("neuron_iaf_C").value, "BlindGuess", "0.1")
        self.add_bioparameter("muscle_iaf_conductance", self.get_bioparameter("neuron_iaf_conductance").value, "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_neuron_chem_exc_syn_gbase", "0.01nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_chem_exc_syn_gbase", "0.01nS", "BlindGuess", "0.1")

        self.add_bioparameter("chem_exc_syn_erev", "0mV", "BlindGuess", "0.1")
        self.add_bioparameter("chem_exc_syn_rise", "3ms", "BlindGuess", "0.1")
        self.add_bioparameter("chem_exc_syn_decay", "10ms", "BlindGuess", "0.1")
        

        self.add_bioparameter("neuron_to_neuron_chem_inh_syn_gbase", "0.01nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_chem_inh_syn_gbase", "0.01nS", "BlindGuess", "0.1")

        self.add_bioparameter("chem_inh_syn_erev", "-80mV", "BlindGuess", "0.1")
        self.add_bioparameter("chem_inh_syn_rise", "3ms", "BlindGuess", "0.1")
        self.add_bioparameter("chem_inh_syn_decay", "10ms", "BlindGuess", "0.1")
        

        self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_elec_syn_gbase", "0nS", "BlindGuess", "0.1")

        self.add_bioparameter("elec_syn_erev", "0mV", "BlindGuess", "0.1")
        self.add_bioparameter("elec_syn_rise", "3ms", "BlindGuess", "0.1")
        self.add_bioparameter("elec_syn_decay", "10ms", "BlindGuess", "0.1")


        self.add_bioparameter("unphysiological_offset_current", "0pA", "KnownError", "0") # Can be activated later
        self.add_bioparameter("unphysiological_offset_current_del", "0ms", "KnownError", "0")
        self.add_bioparameter("unphysiological_offset_current_dur", "200ms", "KnownError", "0")

    def create_generic_muscle_cell(self):
        self.generic_muscle_cell = IafCell(id="generic_muscle_iaf_cell", 
                                C =                 self.get_bioparameter("muscle_iaf_C").value,
                                thresh =            self.get_bioparameter("muscle_iaf_thresh").value,
                                reset =             self.get_bioparameter("muscle_iaf_reset").value,
                                leak_conductance =  self.get_bioparameter("muscle_iaf_conductance").value,
                                leak_reversal =     self.get_bioparameter("muscle_iaf_leak_reversal").value)
   
   
    def create_generic_neuron_cell(self):
        self.generic_neuron_cell = IafCell(id="generic_neuron_iaf_cell", 
                                C =                 self.get_bioparameter("neuron_iaf_C").value,
                                thresh =            self.get_bioparameter("neuron_iaf_thresh").value,
                                reset =             self.get_bioparameter("neuron_iaf_reset").value,
                                leak_conductance =  self.get_bioparameter("neuron_iaf_conductance").value,
                                leak_reversal =     self.get_bioparameter("neuron_iaf_leak_reversal").value) 


    def create_offset(self):   
        self.offset_current = PulseGenerator(id="offset_current",
                                delay= self.get_bioparameter("unphysiological_offset_current_del").value,
                                duration= self.get_bioparameter("unphysiological_offset_current_dur").value,
                                amplitude= self.get_bioparameter("unphysiological_offset_current").value)     

    
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

        self.neuron_to_neuron_elec_syn = ExpTwoSynapse(id="neuron_to_neuron_elec_syn",
                                gbase =         self.get_bioparameter("neuron_to_neuron_elec_syn_gbase").value,
                                erev =          self.get_bioparameter("elec_syn_erev").value,
                                tau_decay =     self.get_bioparameter("elec_syn_decay").value,
                                tau_rise =      self.get_bioparameter("elec_syn_rise").value)


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

        self.neuron_to_muscle_elec_syn = ExpTwoSynapse(id="neuron_to_muscle_elec_syn",
                                gbase =         self.get_bioparameter("neuron_to_muscle_elec_syn_gbase").value,
                                erev =          self.get_bioparameter("elec_syn_erev").value,
                                tau_decay =     self.get_bioparameter("elec_syn_decay").value,
                                tau_rise =      self.get_bioparameter("elec_syn_rise").value)


    def create_models(self):
        self.create_generic_muscle_cell()
        self.create_generic_neuron_cell()
        self.create_offset()
        self.create_neuron_to_muscle_syn()
        self.create_neuron_to_neuron_syn()
        

    def get_elec_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False
        if type == 'neuron_to_neuron':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'neuron_to_neuron_elec_syn_%s', 'gbase')
            erev = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'erev')
            decay = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'decay')
            rise = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'rise')
            conn_id = 'neuron_to_neuron_elec_syn'
        elif type == 'neuron_to_muscle':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'neuron_to_muscle_elec_syn_%s', 'gbase')
            erev = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'erev')
            decay = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'decay')
            rise = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'rise')
            conn_id = 'neuron_to_muscle_elec_syn'
        elif type == 'muscle_to_muscle':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'muscle_to_muscle_elec_syn_%s', 'gbase')
            erev = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'erev')
            decay = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'decay')
            rise = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s', 'elec_syn_%s', 'rise')
            conn_id = 'muscle_to_muscle_elec_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_elec_syn' % (pre_cell, post_cell)

        return ExpTwoSynapse(id=conn_id,
                            gbase=gbase,
                            erev=erev,
                            tau_decay=decay,
                            tau_rise=rise)


    def get_exc_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False

        specific_param_template = '%s_to_%s_chem_exc_syn_%s'
        if type == 'neuron_to_neuron':
            gbase = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'neuron_to_neuron_chem_exc_syn_%s', 'gbase')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'chem_exc_syn_%s', 'erev')
            decay = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'chem_exc_syn_%s', 'decay')
            rise = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'chem_exc_syn_%s', 'rise')

            conn_id = 'neuron_to_neuron_exc_syn'

        elif type == 'neuron_to_muscle':
            gbase = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'neuron_to_muscle_chem_exc_syn_%s', 'gbase')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'chem_exc_syn_%s', 'erev')
            decay = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'chem_exc_syn_%s', 'decay')
            rise = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'chem_exc_syn_%s', 'rise')
            conn_id = 'neuron_to_muscle_exc_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_exc_syn' % (pre_cell, post_cell)

        return ExpTwoSynapse(id=conn_id,
                             gbase=gbase,
                             erev=erev,
                             tau_decay=decay,
                             tau_rise=rise)


    def get_inh_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False

        specific_param_template = '%s_to_%s_chem_inh_syn_%s'
        if type == 'neuron_to_neuron':
            gbase = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'neuron_to_neuron_chem_inh_syn_%s', 'gbase')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'chem_inh_syn_%s', 'erev')
            decay = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'chem_inh_syn_%s', 'decay')
            rise = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'chem_inh_syn_%s', 'rise')

            conn_id = 'neuron_to_neuron_inh_syn'

        elif type == 'neuron_to_muscle':
            gbase = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'neuron_to_muscle_chem_inh_syn_%s', 'gbase')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'chem_inh_syn_%s', 'erev')
            decay = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'chem_inh_syn_%s', 'decay')
            rise = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'chem_inh_syn_%s', 'rise')
            conn_id = 'neuron_to_muscle_inh_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_inh_syn' % (pre_cell, post_cell)

        return ExpTwoSynapse(id=conn_id,
                             gbase=gbase,
                             erev=erev,
                             tau_decay=decay,
                             tau_rise=rise)




