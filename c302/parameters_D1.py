'''

    Parameters D:
        Cells:           Multicompartmental, conductance based cell models with HH like ion channels
        Chem Synapses:   Analogue/graded synapses; continuous transmission (voltage dependent)
        Gap junctions:   Electrical connection; current linerly depends on difference in voltages 
        
    ASSESSMENT:
        May be the right target for the "full scale" model in the medium term...
        Similar issues to parameters D
        Note issue https://github.com/openworm/CElegansNeuroML/issues/71 regarding status of this
        

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
from neuroml import FixedFactorConcentrationModel

from neuroml import GapJunction
from neuroml import PulseGenerator

from parameters_D import ParameterisedModel as ParameterisedModel_D

class ParameterisedModel(ParameterisedModel_D):

    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "D1"
        self.custom_component_types_definitions = ['cell_C.xml','custom_synapses.xml']
        
        self.set_default_bioparameters()


    def set_default_bioparameters(self):

        self.add_bioparameter("cell_diameter", "5", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_length", "20", "BlindGuess", "0.1")

        self.add_bioparameter("initial_memb_pot", "-45 mV", "BlindGuess", "0.1")

        self.add_bioparameter("specific_capacitance", "1 uF_per_cm2", "BlindGuess", "0.1")
        
        self.add_bioparameter("resistivity", "3 kohm_cm", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_spike_thresh", "-26 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_spike_thresh", "-26 mV", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_leak_cond_density", "0.005 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_leak_cond_density", "0.005 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("leak_erev", "-50 mV", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_k_slow_cond_density", "4 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_k_slow_cond_density", "1.8333751019872582 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("k_slow_erev", "-60 mV", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_k_fast_cond_density", "0.2 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_k_fast_cond_density", "0.0711643917483308 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("k_fast_erev", "-60 mV", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_ca_boyle_cond_density", "4 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_ca_boyle_cond_density", "1.6862775772264702 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("ca_boyle_erev", "40 mV", "BlindGuess", "0.1")
        
        self.add_bioparameter("ca_conc_decay_time", "11.5943 ms", "BlindGuess", "0.1")
        self.add_bioparameter("ca_conc_rho", "0.000238919 mol_per_m_per_A_per_s", "BlindGuess", "0.1")


        self.add_bioparameter("global_connectivity_power_scaling", "0", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_neuron_exc_syn_conductance", "2 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_conductance", "2 nS", "BlindGuess", "0.1")
        
        self.add_bioparameter("exc_syn_ar", ".5 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_ad", "20 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_beta", "0.25 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_vth", "-35 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_erev", "0 mV", "BlindGuess", "0.1")
        
        
    

        self.add_bioparameter("neuron_to_neuron_inh_syn_conductance", "26 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_conductance", "0.25 nS", "BlindGuess", "0.1")
        
        
        self.add_bioparameter("inh_syn_ar", ".005 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_ad", "10 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_beta", "0.5 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_vth", "-55 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_erev", "-80 mV", "BlindGuess", "0.1")
        

        self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0.005 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_elec_syn_gbase", "0.0001 nS", "BlindGuess", "0.1")

        self.add_bioparameter("unphysiological_offset_current", "0 pA", "KnownError", "0")  # Can be activated later
        self.add_bioparameter("unphysiological_offset_current_del", "0 ms", "KnownError", "0")
        self.add_bioparameter("unphysiological_offset_current_dur", "2000 ms", "KnownError", "0")





    def create_neuron_to_neuron_syn(self):
        self.neuron_to_neuron_exc_syn = GradedSynapse2(id="neuron_to_neuron_exc_syn",
                                conductance =        self.get_bioparameter("neuron_to_neuron_exc_syn_conductance").value,
                                ar =                 self.get_bioparameter("exc_syn_ar").value,
                                ad =                 self.get_bioparameter("exc_syn_ad").value,
                                beta =               self.get_bioparameter("exc_syn_beta").value,
                                vth =                self.get_bioparameter("exc_syn_vth").value,
                                erev =               self.get_bioparameter("exc_syn_erev").value)


        self.neuron_to_neuron_inh_syn = GradedSynapse2(id="neuron_to_neuron_inh_syn",
                                conductance =        self.get_bioparameter("neuron_to_neuron_inh_syn_conductance").value,
                                ar =                 self.get_bioparameter("inh_syn_ar").value,
                                ad =                 self.get_bioparameter("inh_syn_ad").value,
                                beta =               self.get_bioparameter("inh_syn_beta").value,
                                vth =                self.get_bioparameter("inh_syn_vth").value,
                                erev =               self.get_bioparameter("inh_syn_erev").value)

        self.neuron_to_neuron_elec_syn = GapJunction(id="neuron_to_neuron_elec_syn",
                               conductance =    self.get_bioparameter("neuron_to_neuron_elec_syn_gbase").value)



    def create_neuron_to_muscle_syn(self):
        self.neuron_to_muscle_exc_syn = GradedSynapse2(id="neuron_to_muscle_exc_syn",
                                conductance =        self.get_bioparameter("neuron_to_muscle_exc_syn_conductance").value,
                                ar =                 self.get_bioparameter("exc_syn_ar").value,
                                ad =                 self.get_bioparameter("exc_syn_ad").value,
                                beta =               self.get_bioparameter("exc_syn_beta").value,
                                vth =                self.get_bioparameter("exc_syn_vth").value,
                                erev =               self.get_bioparameter("exc_syn_erev").value)


        self.neuron_to_muscle_inh_syn = GradedSynapse2(id="neuron_to_muscle_inh_syn",
                                conductance =        self.get_bioparameter("neuron_to_muscle_inh_syn_conductance").value,
                                ar =                 self.get_bioparameter("inh_syn_ar").value,
                                ad =                 self.get_bioparameter("inh_syn_ad").value,
                                beta =               self.get_bioparameter("inh_syn_beta").value,
                                vth =                self.get_bioparameter("inh_syn_vth").value,
                                erev =               self.get_bioparameter("inh_syn_erev").value)

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
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s', 'erev')
            ar = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                             'ar')
            ad = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                             'ad')
            beta = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                             'beta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                             'vth')

            conn_id = 'neuron_to_neuron_exc_syn'

        elif type == 'neuron_to_muscle':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_muscle_exc_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                             'erev')
            ar = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                           'ar')
            ad = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                           'ad')
            beta = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                             'beta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'exc_syn_%s',
                                                            'vth')
            conn_id = 'neuron_to_muscle_exc_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_exc_syn' % (pre_cell, post_cell)

        return GradedSynapse2(id=conn_id,
                              conductance=conductance,
                              ar=ar,
                              ad=ad,
                              beta=beta,
                              vth=vth,
                              erev=erev)

    def get_inh_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False

        specific_param_template = '%s_to_%s_inh_syn_%s'
        if type == 'neuron_to_neuron':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_neuron_inh_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                             'erev')
            ar = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                           'ar')
            ad = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                           'ad')
            beta = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                             'beta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                            'vth')

            conn_id = 'neuron_to_neuron_inh_syn'

        elif type == 'neuron_to_muscle':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_muscle_inh_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                             'erev')
            ar = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                           'ar')
            ad = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                           'ad')
            beta = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                             'beta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'inh_syn_%s',
                                                            'vth')

            conn_id = 'neuron_to_muscle_inh_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_inh_syn' % (pre_cell, post_cell)

        return GradedSynapse2(id=conn_id,
                              conductance=conductance,
                              ar=ar,
                              ad=ad,
                              beta=beta,
                              vth=vth,
                              erev=erev)
                              
                              
    def create_n_connection_synapse(self, prototype_syn, n, nml_doc, existing_synapses):
        if prototype_syn.id in existing_synapses:
            return existing_synapses[prototype_syn.id]

        if isinstance(prototype_syn, GradedSynapse2):
            existing_synapses[prototype_syn.id] = prototype_syn
            nml_doc.graded_synapses.append(prototype_syn)
            return prototype_syn
        else:
            return super(ParameterisedModel, self).create_n_connection_synapse(prototype_syn, n, nml_doc, existing_synapses)

    def is_analog_conn(self, syn):
        return super(ParameterisedModel, self).is_analog_conn(syn) or isinstance(syn, GradedSynapse2)

class GradedSynapse2():
    
    def __init__(self, id, conductance, ar, ad, beta, vth, erev):
        self.id = id
        self.conductance = conductance
        self.ar = ar
        self.ad = ad
        self.beta = beta
        self.vth = vth
        self.erev = erev
        
    
    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write('    '*level + '<gradedSynapse2 id="%s" conductance="%s" ar="%s" ad="%s" beta="%s" vth="%s" erev="%s"/>\n'%(self.id, self.conductance, self.ar, self.ad, self.beta, self.vth, self.erev))

