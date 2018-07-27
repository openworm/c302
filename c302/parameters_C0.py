'''

    Parameters C0:
        Cells:           Simplified conductance based cell model (Morris Lecar like); No fast K channel. No inactivation on Ca channel. No [Ca2+] dependence
        Chem Synapses:   Analogue/graded synapses; continuous transmission (voltage dependent) (same as C1)
        Gap junctions:   Electrical connection; current linerly depends on difference in voltages 
        
    ASSESSMENT:
        A good prospect for a simple neuronal model with analog synapses => can have non spiking neurons

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

from neuroml import GapJunction


from parameters_C import ParameterisedModel as ParameterisedModel_C


class ParameterisedModel(ParameterisedModel_C):

    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "C0"
        self.custom_component_types_definitions = ['cell_C.xml','custom_synapses.xml']
        
        self.set_default_bioparameters()
        self.print_("Set default parameters for %s"%self.level)

    def set_default_bioparameters(self):

        '''
        param_C = ParameterisedModel_C()
        param_C.set_default_bioparameters()
        for b in param_C.bioparameters:
            if not 'syn' in b.name:
                self.add_bioparameter_obj(b)'''
                        
        self.add_bioparameter("cell_diameter", "5", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_length", "20", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_specific_capacitance", ".6860 uF_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_specific_capacitance", "5 uF_per_cm2", "BlindGuess", "0.1")

        self.add_bioparameter("initial_memb_pot", "-50 mV", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_spike_thresh", "-20 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_spike_thresh", "-20 mV", "BlindGuess", "0.1")


        self.add_bioparameter("muscle_leak_cond_density", "0.00105 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_leak_cond_density", "0.05 mS_per_cm2", "BlindGuess", "0.1")
        
        
        self.add_bioparameter("muscle_k_slow_cond_density", "0.3 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_k_slow_cond_density", "0.1 mS_per_cm2", "BlindGuess", "0.1")
        
        
        self.add_bioparameter("muscle_ca_simple_cond_density", "0.25 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_ca_simple_cond_density", "0.06 mS_per_cm2", "BlindGuess", "0.1")
        
        
        self.add_bioparameter("leak_erev", "-44 mV", "BlindGuess", "0.1")
        self.add_bioparameter("k_slow_erev", "-80 mV", "BlindGuess", "0.1")
        self.add_bioparameter("ca_simple_erev", "50 mV", "BlindGuess", "0.1")
        
        self.add_bioparameter("ca_conc_decay_time", "20 ms", "BlindGuess", "0.1")
        self.add_bioparameter("ca_conc_rho", "0.0002 mol_per_m_per_A_per_s", "BlindGuess", "0.1")


        self.add_bioparameter("global_connectivity_power_scaling", "0", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_neuron_exc_syn_conductance", "5 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_conductance", "22.3 nS", "BlindGuess", "0.1")
        
        self.add_bioparameter("exc_syn_ar", ".5 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_ad", "20 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_beta", "0.25 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_vth", "-20 mV", "BlindGuess", "0.1")
        self.add_bioparameter("exc_syn_erev", "0 mV", "BlindGuess", "0.1")
        
    
        self.add_bioparameter("neuron_to_neuron_inh_syn_conductance", "260 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_conductance", "0.25 nS", "BlindGuess", "0.1")
        
        
        self.add_bioparameter("inh_syn_ar", ".005 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_ad", "10 per_s", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_beta", "0.5 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_vth", "-25 mV", "BlindGuess", "0.1")
        self.add_bioparameter("inh_syn_erev", "-80 mV", "BlindGuess", "0.1")
        

        self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0.05 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_elec_syn_gbase", "0.0001 nS", "BlindGuess", "0.1")

        self.add_bioparameter("unphysiological_offset_current", "0 pA", "KnownError", "0") # Can be activated later
        self.add_bioparameter("unphysiological_offset_current_del", "0 ms", "KnownError", "0")
        self.add_bioparameter("unphysiological_offset_current_dur", "2000 ms", "KnownError", "0")



    def create_models(self):
        self.create_generic_muscle_cell()
        self.create_generic_neuron_cell()
        self.create_offsetcurrent_concentrationmodel()
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

        mp.specific_capacitances.append(SpecificCapacitance(value=self.get_bioparameter("muscle_specific_capacitance").value))

        mp.spike_threshes.append(SpikeThresh(value=self.get_bioparameter("muscle_spike_thresh").value))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_leak_cond_density").value, 
                                                   id="Leak_all", 
                                                   ion_channel="Leak", 
                                                   erev=self.get_bioparameter("leak_erev").value,
                                                   ion="non_specific"))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_k_slow_cond_density").value, 
                                                   id="k_slow_all", 
                                                   ion_channel="k_slow", 
                                                   erev=self.get_bioparameter("k_slow_erev").value,
                                                   ion="k"))
        '''
        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_k_fast_cond_density").value, 
                                                   id="k_fast_all", 
                                                   ion_channel="k_fast", 
                                                   erev=self.get_bioparameter("k_fast_erev").value,
                                                   ion="k"))'''

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_ca_simple_cond_density").value, 
                                                   id="ca_simple_all", 
                                                   ion_channel="ca_simple", 
                                                   erev=self.get_bioparameter("ca_simple_erev").value,
                                                   ion="ca"))

        ip = IntracellularProperties()
        self.generic_muscle_cell.biophysical_properties.intracellular_properties = ip

        # NOTE: resistivity/axial resistance not used for single compartment cell models, so value irrelevant!
        ip.resistivities.append(Resistivity(value="0.1 kohm_cm"))


        # NOTE: Ca reversal potential not calculated by Nernst, so initial_ext_concentration value irrelevant!
        species = Species(id="ca", 
                          ion="ca",
                          concentration_model="CaPool",
                          initial_concentration="0 mM",
                          initial_ext_concentration="2E-6 mol_per_cm3")

        ip.species.append(species)  


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

        mp.specific_capacitances.append(SpecificCapacitance(value=self.get_bioparameter("neuron_specific_capacitance").value))

        mp.spike_threshes.append(SpikeThresh(value=self.get_bioparameter("neuron_spike_thresh").value))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("neuron_leak_cond_density").value, 
                                                   id="Leak_all", 
                                                   ion_channel="Leak", 
                                                   erev=self.get_bioparameter("leak_erev").value,
                                                   ion="non_specific"))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("neuron_k_slow_cond_density").value, 
                                                   id="k_slow_all", 
                                                   ion_channel="k_slow", 
                                                   erev=self.get_bioparameter("k_slow_erev").value,
                                                   ion="k"))
        '''
        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("neuron_k_fast_cond_density").value, 
                                                   id="k_fast_all", 
                                                   ion_channel="k_fast", 
                                                   erev=self.get_bioparameter("k_fast_erev").value,
                                                   ion="k"))'''

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("neuron_ca_simple_cond_density").value, 
                                                   id="ca_simple_all", 
                                                   ion_channel="ca_simple", 
                                                   erev=self.get_bioparameter("ca_simple_erev").value,
                                                   ion="ca"))

        ip = IntracellularProperties()
        self.generic_neuron_cell.biophysical_properties.intracellular_properties = ip

        # NOTE: resistivity/axial resistance not used for single compartment cell models, so value irrelevant!
        ip.resistivities.append(Resistivity(value="0.1 kohm_cm"))


        # NOTE: Ca reversal potential not calculated by Nernst, so initial_ext_concentration value irrelevant!
        species = Species(id="ca", 
                          ion="ca",
                          concentration_model="CaPool",
                          initial_concentration="0 mM",
                          initial_ext_concentration="2E-6 mol_per_cm3")

        ip.species.append(species)




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

