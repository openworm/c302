'''

    Parameters C1:
        Cells:           Single compartment, conductance based cell models with HH like ion channels
        Chem Synapses:   Analogue/graded synapses; continuous transmission (voltage dependent)
        Gap junctions:   Electrical connection; current linerly depends on difference in voltages 
        
    ASSESSMENT:
        A good prospect, but cell model could be simpler. See C0

'''

from neuroml import GradedSynapse
from neuroml import GapJunction

from parameters_C import ParameterisedModel as ParameterisedModel_C


class ParameterisedModel(ParameterisedModel_C):

    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "C1"
        self.custom_component_types_definitions = 'cell_C.xml'
        
        self.set_default_bioparameters()
        print("Set default parameters for %s"%self.level)
        

    def set_default_bioparameters(self):

        param_C = ParameterisedModel_C()
        param_C.set_default_bioparameters()
        for b in param_C.bioparameters:
            if not 'syn' in b.name:
                self.add_bioparameter_obj(b)

        self.add_bioparameter("neuron_to_neuron_exc_syn_conductance", "0.09 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_conductance", "0.09 nS", "BlindGuess", "0.1")
        
        self.add_bioparameter("exc_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_vth", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_erev", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_k", "0.025per_ms", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_neuron_inh_syn_conductance", "0.09 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_conductance", "0.09 nS", "BlindGuess", "0.1")
        
        self.add_bioparameter("inh_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_vth", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_erev", "-70 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_k", "0.025per_ms", "BlindGuess", "0.1")
        
        self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0.00052 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_elec_syn_gbase", "0.00052 nS", "BlindGuess", "0.1")



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