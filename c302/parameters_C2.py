'''

    Parameters C2 for c302 still under developemnt!!
    
    
    C2 adds analogue synapses... Might be merged into C or bumped up to D
    
    Subject to change without notice!!
    
'''

from neuroml import Cell, PulseGenerator, FixedFactorConcentrationModel
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

from parameters_C import ParameterisedModel as ParameterisedModel_C


'''

    The values below are a FIRST APPROXIMATION of conductance based neurons for use in a network to 
    investigate the synaptic connectivity of C elegans
        
'''

class ParameterisedModel(ParameterisedModel_C):

    def __init__(self):
        super(ParameterisedModel, self).__init__()
        self.level = "C2"
        self.custom_component_types_definitions = ['cell_C.xml', 'custom_muscle_components.xml', 'custom_synapses.xml']
        
        self.set_default_bioparameters()
        print("Set default parameters for %s"%self.level)


    def set_default_bioparameters(self):

        self.add_bioparameter("cell_diameter", "5", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_length", "20", "BlindGuess", "0.1")

        self.add_bioparameter("initial_memb_pot", "-60 mV", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_initial_memb_pot", "-28 mV", "BlindGuess", "0.1")

        self.add_bioparameter("specific_capacitance", "5 uF_per_cm2", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_specific_capacitance", "1 uF_per_cm2", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_spike_thresh", "-55 mV", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_spike_thresh", "-10 mV", "BlindGuess", "0.1")

        #self.add_bioparameter("muscle_leak_cond_density", "0.0172 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_leak_cond_density", "0.002 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_leak_cond_density", "0.002 mS_per_cm2", "BlindGuess", "0.1")

        self.add_bioparameter("leak_erev", "-60 mV", "BlindGuess", "0.1")
        #self.add_bioparameter("muscle_leak_erev", "-13 mV", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_leak_erev", "-20 mV", "BlindGuess", "0.1")

        #self.add_bioparameter("muscle_k_slow_cond_density", "0.564 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_k_slow_cond_density", "0.45833751019872582 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_k_slow_cond_density", "0.45833751019872582 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("k_slow_erev", "-60 mV", "BlindGuess", "0.1")
        #self.add_bioparameter("muscle_k_slow_erev", "-70 mV", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_k_slow_erev", "-30 mV", "BlindGuess", "0.1")

        #self.add_bioparameter("muscle_k_fast_cond_density", "1.015 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_k_fast_cond_density", "0.042711643917483308 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("k_fast_erev", "-70 mV", "BlindGuess", "0.1")
        #self.add_bioparameter("muscle_k_fast_erev", "-50 mV", "BlindGuess", "0.1")

        self.add_bioparameter("muscle_k_fast_cond_density", "0.042711643917483308 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_k_fast_erev", "-30 mV", "BlindGuess", "0.1")

        #self.add_bioparameter("muscle_ca_boyle_cond_density", "0.284 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_ca_boyle_cond_density", "0.812775772264702 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_ca_boyle_cond_density", "1.812775772264702 mS_per_cm2", "BlindGuess", "0.1")

        self.add_bioparameter("ca_boyle_erev", "10 mV", "BlindGuess", "0.1")
        #self.add_bioparameter("muscle_ca_boyle_erev", "46 mV", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_ca_boyle_erev", "0 mV", "BlindGuess", "0.1")
        
        self.add_bioparameter("ca_conc_decay_time", "13.811870945509265 ms", "BlindGuess", "0.1")
        self.add_bioparameter("ca_conc_rho", "0.000238919 mol_per_m_per_A_per_s", "BlindGuess", "0.1")


        self.add_bioparameter("ca_conc_decay_time_muscle", "60.811870945509265 ms", "BlindGuess", "0.1")
        self.add_bioparameter("ca_conc_rho_muscle", "0.002238919 mol_per_m_per_A_per_s", "BlindGuess", "0.1")
        #self.add_bioparameter("ca_conc_xRho_muscle", "0.0238919 mol_per_m_per_A_per_s", "BlindGuess", "0.1")
        #self.add_bioparameter("ca_conc_iCaSigmoidMid_muscle", "3 pA", "BlindGuess", "0.1")
        #self.add_bioparameter("ca_conc_iCaSigmoidSlope_muscle", "0.01 pA", "BlindGuess", "0.1")
        #self.add_bioparameter("ca_conc_xSigmoidMid_muscle", "1E-7 M", "BlindGuess", "0.1")
        #self.add_bioparameter("ca_conc_xSigmoidSlope_muscle", "1E-9 M", "BlindGuess", "0.1")
        #self.add_bioparameter("ca_conc_xDecay_muscle", "0.01 ms", "BlindGuess", "0.1")


        self.add_bioparameter("neuron_to_neuron_exc_syn_conductance", "0.49 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_neuron_exc_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_neuron_exc_syn_vth", "00 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_neuron_exc_syn_erev", "-10 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_neuron_exc_syn_k", "0.5per_ms", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_muscle_exc_syn_conductance", "0.10 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_weight", "1", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_delta", "19 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_vth", "27 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_erev", "37 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_k", "1.205per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_sigma", "0.5 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_exc_syn_mu", "5 mV", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_neuron_inh_syn_conductance", "0.29 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_conductance", "1.29 nS", "BlindGuess", "0.1")
        
        self.add_bioparameter("neuron_to_neuron_inh_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_neuron_inh_syn_vth", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_neuron_inh_syn_erev", "-70 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_neuron_inh_syn_k", "0.015per_ms", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_muscle_inh_syn_delta", "5 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_vth", "0 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_erev", "-35 mV", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_inh_syn_k", "0.025per_ms", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_neuron_elec_syn_weight", "1", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_muscle_elec_syn_gbase", "0.00152 nS", "BlindGuess", "0.1")


        #self.add_bioparameter("muscle_to_muscle_elec_syn_gbase", "0.0002 nS", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_to_muscle_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_motor_delayed_elec_syn_weight", "1", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_motor_delayed_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_motor_delayed_elec_syn_sigma", "0.4", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_motor_delayed_elec_syn_mu", "-30", "BlindGuess", "0.1")



        #self.add_bioparameter("muscle_to_muscle_elec_syn_gbase", "0.0002 nS", "BlindGuess", "0.1")
        self.add_bioparameter("muscle_to_muscle_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")

        self.add_bioparameter("neuron_to_motor_delayed_elec_syn_weight", "1", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_motor_delayed_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_motor_delayed_elec_syn_sigma", "0.4", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_to_motor_delayed_elec_syn_mu", "-30", "BlindGuess", "0.1")


        self.add_bioparameter("unphysiological_offset_current", "0 pA", "KnownError", "0")  # Can be activated later
        self.add_bioparameter("unphysiological_offset_current_del", "0 ms", "KnownError", "0")
        self.add_bioparameter("unphysiological_offset_current_dur", "2000 ms", "KnownError", "0")

        # Different parameters for different synapses
        """self.add_bioparameter("AVAR_to_DA1_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAL_to_DA1_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAR_to_DA2_elec_syn_gbase", "0.01052 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAL_to_DA2_elec_syn_gbase", "0.01052 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAR_to_DA3_elec_syn_gbase", "0.00852 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAL_to_DA3_elec_syn_gbase", "0.00852 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAR_to_DA4_elec_syn_gbase", "0.00652 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAL_to_DA4_elec_syn_gbase", "0.00652 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAR_to_DA5_elec_syn_gbase", "0.00452 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAL_to_DA5_elec_syn_gbase", "0.00452 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAR_to_DA6_elec_syn_gbase", "0.00252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAR_to_DA7_elec_syn_gbase", "0.00092 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAL_to_DA7_elec_syn_gbase", "0.00092 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAR_to_DA8_elec_syn_gbase", "0.00072 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAL_to_DA8_elec_syn_gbase", "0.00072 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAR_to_DA9_elec_syn_gbase", "0.00052 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVAL_to_DA9_elec_syn_gbase", "0.00052 nS", "BlindGuess", "0.1")"""

        #self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")

        """self.add_bioparameter("AVBL_to_DB2_elec_syn_delay", "250ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB3_elec_syn_delay", "500ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB4_elec_syn_delay", "750ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB5_elec_syn_delay", "1000ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB6_elec_syn_delay", "1250ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB7_elec_syn_delay", "1500ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBR_to_DB1_elec_syn_delay", "0ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB2_elec_syn_delay", "250ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB3_elec_syn_delay", "500ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB4_elec_syn_delay", "750ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB5_elec_syn_delay", "1000ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB6_elec_syn_delay", "1250ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB7_elec_syn_delay", "1500ms", "BlindGuess", "0.1")"""

        """self.add_bioparameter("DB1_to_DB2_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB2_to_DB1_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")

        self.add_bioparameter("DB2_to_DB3_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB3_to_DB2_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")

        self.add_bioparameter("DB3_to_DB4_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB4_to_DB3_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")

        self.add_bioparameter("DB4_to_DB5_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB5_to_DB4_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")

        self.add_bioparameter("DB5_to_DB6_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB6_to_DB5_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")

        self.add_bioparameter("DB6_to_DB7_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB7_to_DB6_elec_syn_gbase", "0.02252 nS", "BlindGuess", "0.1")"""


        """self.add_bioparameter("DB2_to_AVBL_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB3_to_AVBL_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB4_to_AVBL_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB5_to_AVBL_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB6_to_AVBL_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB7_to_AVBL_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB1_to_AVBR_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB2_to_AVBR_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB3_to_AVBR_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB4_to_AVBR_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB5_to_AVBR_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB6_to_AVBR_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")
        self.add_bioparameter("DB7_to_AVBR_elec_syn_gbase", "0 nS", "BlindGuess", "0.1")"""


        #self.add_bioparameter("AVBR_to_DB4_exc_syn_conductance", "0 nS", "BlindGuess", "0.1")

        """self.add_bioparameter("neuron_to_neuron_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")

        #self.add_bioparameter("AVBL_to_AVBR_elec_syn_gbase", "1 nS", "BlindGuess", "0.1")

        syns = [
                      'DB1_to_MDL06_exc_syn_conductance',
                      'DB1_to_MDL08_exc_syn_conductance',
                      'DB1_to_MDL09_exc_syn_conductance',
                      'DB1_to_MDR08_exc_syn_conductance',
                      'DB1_to_MDR09_exc_syn_conductance',
                      'DB2_to_MDL09_exc_syn_conductance',
                      'DB2_to_MDL10_exc_syn_conductance',
                      'DB2_to_MDL11_exc_syn_conductance',
                      'DB2_to_MDL12_exc_syn_conductance',
                      'DB2_to_MDR09_exc_syn_conductance',
                      'DB2_to_MDR10_exc_syn_conductance',
                      'DB2_to_MDR11_exc_syn_conductance',
                      ]

        for syn in syns:
            self.add_bioparameter(syn, "0.10 nS", "BlindGuess", "0.1")
        syns = [
            'DB1_to_MDL06_exc_syn_delta',
            'DB1_to_MDL08_exc_syn_delta',
            'DB1_to_MDL09_exc_syn_delta',
            'DB1_to_MDR08_exc_syn_delta',
            'DB1_to_MDR09_exc_syn_delta',
            'DB2_to_MDL09_exc_syn_delta',
            'DB2_to_MDL10_exc_syn_delta',
            'DB2_to_MDL11_exc_syn_delta',
            'DB2_to_MDL12_exc_syn_delta',
            'DB2_to_MDR09_exc_syn_delta',
            'DB2_to_MDR10_exc_syn_delta',
            'DB2_to_MDR11_exc_syn_delta',
        ]

        for syn in syns:
            self.add_bioparameter(syn, self.get_bioparameter('neuron_to_muscle_exc_syn_delta').value, "BlindGuess", "0.1")

        syns = [
            'DB1_to_MDL06_exc_syn_vth',
            'DB1_to_MDL08_exc_syn_vth',
            'DB1_to_MDL09_exc_syn_vth',
            'DB1_to_MDR08_exc_syn_vth',
            'DB1_to_MDR09_exc_syn_vth',
            'DB2_to_MDL09_exc_syn_vth',
            'DB2_to_MDL10_exc_syn_vth',
            'DB2_to_MDL11_exc_syn_vth',
            'DB2_to_MDL12_exc_syn_vth',
            'DB2_to_MDR09_exc_syn_vth',
            'DB2_to_MDR10_exc_syn_vth',
            'DB2_to_MDR11_exc_syn_vth',
        ]

        for syn in syns:
            self.add_bioparameter(syn, self.get_bioparameter('neuron_to_muscle_exc_syn_vth').value, "BlindGuess", "0.1")


        syns = [
            'DB1_to_MDL06_exc_syn_k',
            'DB1_to_MDL08_exc_syn_k',
            'DB1_to_MDL09_exc_syn_k',
            'DB1_to_MDR08_exc_syn_k',
            'DB1_to_MDR09_exc_syn_k',
            'DB2_to_MDL09_exc_syn_k',
            'DB2_to_MDL10_exc_syn_k',
            'DB2_to_MDL11_exc_syn_k',
            'DB2_to_MDL12_exc_syn_k',
            'DB2_to_MDR09_exc_syn_k',
            'DB2_to_MDR10_exc_syn_k',
            'DB2_to_MDR11_exc_syn_k',
        ]

        for syn in syns:
            self.add_bioparameter(syn, self.get_bioparameter('neuron_to_muscle_exc_syn_k').value, "BlindGuess", "0.1")
        """

        #self.add_bioparameter("DB1_to_MDL06_exc_syn_delta", "5 mV", "BlindGuess", "0.1")
        #self.add_bioparameter("DB1_to_MDL06_exc_syn_vth", "0 mV", "BlindGuess", "0.1")
        #self.add_bioparameter("DB1_to_MDL06_exc_syn_erev", "-50 mV", "BlindGuess", "0.1")
        #self.add_bioparameter("DB1_to_MDL06_exc_syn_k", "0.50per_ms", "BlindGuess", "0.1")

        """self.add_bioparameter("AVBR_to_DB1_elec_syn_weight", "1", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB1_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB1_elec_syn_sigma", "0.7 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB1_elec_syn_mu", "-50 mV", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_DB2_elec_syn_weight", "1", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB2_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB2_elec_syn_sigma", "0.6 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB2_elec_syn_mu", "-45 mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB2_elec_syn_weight", "1", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB2_elec_syn_gbase", "0.01052 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB2_elec_syn_sigma", "0.6 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB2_elec_syn_mu", "-45 mV", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_DB3_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB3_elec_syn_sigma", "0.5 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB3_elec_syn_mu", "-40 mV", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBR_to_DB3_elec_syn_gbase", "0.00852 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB3_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB3_elec_syn_sigma", "0.5 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB3_elec_syn_mu", "-40 mV", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_DB4_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB4_elec_syn_sigma", "0.4 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB4_elec_syn_mu", "-35 mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB4_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB4_elec_syn_sigma", "0.4 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB4_elec_syn_mu", "-35 mV", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_DB5_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB5_elec_syn_sigma", "0.3 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB5_elec_syn_mu", "-30 mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB5_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB5_elec_syn_sigma", "0.3 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB5_elec_syn_mu", "-30 mV", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_DB6_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB6_elec_syn_sigma", "0.2 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB6_elec_syn_mu", "-25 mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB6_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB6_elec_syn_sigma", "0.2 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB6_elec_syn_mu", "-25 mV", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_DB7_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB7_elec_syn_sigma", "0.1 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_DB7_elec_syn_mu", "-20 mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB7_elec_syn_gbase", "0.01252 nS", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB7_elec_syn_sigma", "0.1 per_mV", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_DB7_elec_syn_mu", "-20 mV", "BlindGuess", "0.1")"""



        """self.add_bioparameter("AVBL_to_VB1_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB1_elec_syn_mu", "50ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB2_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB2_elec_syn_mu", "55ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB2_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB2_elec_syn_mu", "55ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBR_to_VB3_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB3_elec_syn_mu", "60ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB4_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB4_elec_syn_mu", "65ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB4_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB4_elec_syn_mu", "65ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB5_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB5_elec_syn_mu", "70ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB5_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB5_elec_syn_mu", "70ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB6_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB6_elec_syn_mu", "75ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB6_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB6_elec_syn_mu", "75ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB7_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB7_elec_syn_mu", "80ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB7_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB7_elec_syn_mu", "80ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB8_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB8_elec_syn_mu", "85ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB8_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB8_elec_syn_mu", "85ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB9_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB9_elec_syn_mu", "90ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB9_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB9_elec_syn_mu", "90ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB10_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB10_elec_syn_mu", "95ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB10_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB10_elec_syn_mu", "95ms", "BlindGuess", "0.1")

        self.add_bioparameter("AVBL_to_VB11_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBL_to_VB11_elec_syn_mu", "100ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB11_elec_syn_sigma", "0.3per_ms", "BlindGuess", "0.1")
        self.add_bioparameter("AVBR_to_VB11_elec_syn_mu", "100ms", "BlindGuess", "0.1")"""

        #self.add_bioparameter("AVBL_to_DB4_elec_syn_gbase", "0.00652 nS", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBR_to_DB4_elec_syn_gbase", "0.00652 nS", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBR_to_DB4_exc_syn_conductance", "0.49 nS", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBL_to_DB5_elec_syn_gbase", "0.00452 nS", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBR_to_DB5_elec_syn_gbase", "0.00452 nS", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBL_to_DB6_elec_syn_gbase", "0.00252 nS", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBR_to_DB6_elec_syn_gbase", "0.00252 nS", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBL_to_DB7_elec_syn_gbase", "0.000002 nS", "BlindGuess", "0.1")
        #self.add_bioparameter("AVBR_to_DB7_elec_syn_gbase", "0.000002 nS", "BlindGuess", "0.1")


        motors = ['DB1', 'DB2', 'DB3', 'DB4', 'DB5', 'DB6', 'DB7']

        neuron_to_neuron_sigma_unit = 'per_mV'
        neuron_to_neuron_mu_unit = 'mV'

        """values = [0.02662421961090314, 0.03534736844496468, 0.24117986141424783, 0.728445888242295, -31.097782892768087, -70.4530293802399, 0.0027901748325678665, 0.04819419381285881, 0.23145430508321702, 0.43259522880823403, -36.33291776403307, -59.353240638482205, 0.05582343246072261, 0.02190008612606287, 0.01, 0.31362780659357425, -66.21115226650004, -52.771417774165776, 0.022627891796868617, 0.019850673688929135, 0.5369334557283133, 0.6157151722578514, -56.58839267667179, -31.98566849893263, 0.0005311880646276632, 0.0007106752078277979, 0.5403093047212282, 0.851692451899331, -26.21928028856079, -36.07220973721469, 0.02239184298106873, 0.00557754534270731, 0.7336559136122108, 0.5396665394749418, -64.251546993354, -58.86832496681512, 0.05911723837418301, 0.05906803856778177, 0.3889133592395809, 0.9, -63.690021804793005, -65.0201808538768, 0.06252, 0.042808104791508095, 0.3870392542369817, 0.359369090000899, -62.00034119097063, -52.385364801981375, 0.01982498040815311, 0.0006263956386551118, 0.01, 0.07344429039663045, 3.2623740935761845, -24.383527105537627, 0.003234785879364064, 0.0013257779195953625, 0.6187551784924861, 0.02010414785586577, 3.037646907306896, -15.804515459300069, 0.008737088303665016, 0.005164680784308186, 0.6646075833887313, 0.6585834274110807, 3.8543086695981366, -60.13096941077282, 0.012477100014060296, 0.022424408328393895, 0.128433033088237, 0.31642838666989964, -5.188754434920856, 5.659506146829591, 0.002580608318239302, 0.011268010981673115, 0.38691673081318745, 0.4051876112158369, 0.08969391093452314, -38.19673533204123, 0.003652415316987105, 0.01447855276084489, 2e-05, 0.032406033165681754, 0.012313305082229144, 0.010630678619124256, 2e-05, 0.040750179035623724, 0.004113193789608253, 0.001621502777546093, 0.01857066607998348, 0.020426074336082088]
        v = 0
        for command in ['AVBL', 'AVBR']:
            for motor in motors:
                if command == 'AVBL' and motor == 'DB1':
                    continue
                self.add_bioparameter('%s_to_%s_elec_syn_gbase' % (command, motor), "%s nS" % values[v], "BlindGuess", "0.1")
                v += 1
                self.add_bioparameter('%s_to_%s_elec_syn_gbase' % (motor, command), "%s nS" % values[v], "BlindGuess", "0.1")
                v += 1
                self.add_bioparameter('%s_to_%s_elec_syn_sigma' % (command, motor), "%s per_mV" % values[v], "BlindGuess",
                                      "0.1")
                v += 1
                self.add_bioparameter('%s_to_%s_elec_syn_sigma' % (motor, command), "%s per_mV" % values[v], "BlindGuess",
                                      "0.1")
                v += 1
                self.add_bioparameter('%s_to_%s_elec_syn_mu' % (command, motor), "%s mV" % values[v], "BlindGuess",
                                      "0.1")
                v += 1
                self.add_bioparameter('%s_to_%s_elec_syn_mu' % (motor, command), "%s mV" % values[v], "BlindGuess",
                                      "0.1")
                v += 1

        for i in range(len(motors))[:-1]:
            m1, m2 = motors[i], motors[i + 1]
            self.add_bioparameter('%s_to_%s_elec_syn_gbase' % (m1, m2), "%s nS" % values[v], "BlindGuess",
                                  "0.1")
            v += 1
            self.add_bioparameter('%s_to_%s_elec_syn_gbase' % (m2, m1), "%s nS" % values[v], "BlindGuess",
                                  "0.1")
            v += 1"""



    def create_models(self):
        self.create_offsetcurrent_concentrationmodel()
        self.create_generic_muscle_cell()
        self.create_generic_neuron_cell()
        self.create_neuron_to_neuron_syn()
        self.create_neuron_to_muscle_syn()
        self.create_muscle_to_muscle_syn()


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

        mp.init_memb_potentials.append(InitMembPotential(value=self.get_bioparameter("muscle_initial_memb_pot").value))

        mp.specific_capacitances.append(SpecificCapacitance(value=self.get_bioparameter("muscle_specific_capacitance").value))

        mp.spike_threshes.append(SpikeThresh(value=self.get_bioparameter("muscle_spike_thresh").value))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_leak_cond_density").value,
                                                   id="Leak_all",
                                                   ion_channel="Leak",
                                                   erev=self.get_bioparameter("muscle_leak_erev").value,
                                                   ion="non_specific"))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_k_slow_cond_density").value,
                                                   id="k_slow_all",
                                                   ion_channel="k_slow_muscle",
                                                   erev=self.get_bioparameter("muscle_k_slow_erev").value,
                                                   ion="k"))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_k_fast_cond_density").value,
                                                   id="k_fast_all",
                                                   ion_channel="k_fast_muscle",
                                                   erev=self.get_bioparameter("muscle_k_fast_erev").value,
                                                   ion="k"))

        mp.channel_densities.append(ChannelDensity(cond_density=self.get_bioparameter("muscle_ca_boyle_cond_density").value,
                                                   id="ca_boyle_all",
                                                   ion_channel="ca_boyle_muscle",
                                                   erev=self.get_bioparameter("muscle_ca_boyle_erev").value,
                                                   ion="ca"))

        ip = IntracellularProperties()
        self.generic_muscle_cell.biophysical_properties.intracellular_properties = ip

        # NOTE: resistivity/axial resistance not used for single compartment cell models, so value irrelevant!
        ip.resistivities.append(Resistivity(value="0.1 kohm_cm"))


        # NOTE: Ca reversal potential not calculated by Nernst, so initial_ext_concentration value irrelevant!
        species = Species(id="ca",
                          ion="ca",
                          concentration_model="CaPoolMuscle",
                          initial_concentration="0 mM",
                          initial_ext_concentration="2E-6 mol_per_cm3")

        ip.species.append(species)

    def create_neuron_to_neuron_syn(self):
        self.neuron_to_neuron_exc_syn = GradedSynapse(id="neuron_to_neuron_exc_syn",
                                conductance =        self.get_bioparameter("neuron_to_neuron_exc_syn_conductance").value,
                                delta =              self.get_bioparameter("neuron_to_neuron_exc_syn_delta").value,
                                Vth =                self.get_bioparameter("neuron_to_neuron_exc_syn_vth").value,
                                erev =               self.get_bioparameter("neuron_to_neuron_exc_syn_erev").value,
                                k =                  self.get_bioparameter("neuron_to_neuron_exc_syn_k").value)


        self.neuron_to_neuron_inh_syn = GradedSynapse(id="neuron_to_neuron_inh_syn",
                                conductance =        self.get_bioparameter("neuron_to_neuron_inh_syn_conductance").value,
                                delta =              self.get_bioparameter("neuron_to_neuron_inh_syn_delta").value,
                                Vth =                self.get_bioparameter("neuron_to_neuron_inh_syn_vth").value,
                                erev =               self.get_bioparameter("neuron_to_neuron_inh_syn_erev").value,
                                k =                  self.get_bioparameter("neuron_to_neuron_inh_syn_k").value)

        self.neuron_to_neuron_elec_syn = GapJunction(id="neuron_to_neuron_elec_syn",
                               conductance =    self.get_bioparameter("neuron_to_neuron_elec_syn_gbase").value)

        self.neuron_to_motor_elec_syn = DelayedGapJunction(id="neuron_to_motor_delayed_elec_syn",
                                                       weight=self.get_bioparameter(
                                                           "neuron_to_motor_delayed_elec_syn_weight").value,
                                                       conductance=self.get_bioparameter(
                                                           "neuron_to_motor_delayed_elec_syn_gbase").value,
                                                       sigma=self.get_bioparameter(
                                                           "neuron_to_motor_delayed_elec_syn_sigma").value,
                                                       mu=self.get_bioparameter(
                                                           "neuron_to_motor_delayed_elec_syn_mu").value)

    def create_offsetcurrent_concentrationmodel(self):

        self.offset_current = PulseGenerator(id="offset_current",
                                             delay=self.get_bioparameter("unphysiological_offset_current_del").value,
                                             duration=self.get_bioparameter("unphysiological_offset_current_dur").value,
                                             amplitude=self.get_bioparameter("unphysiological_offset_current").value)

        self.concentration_model_neuron = FixedFactorConcentrationModel(id="CaPool",
                                                                 ion="ca",
                                                                 resting_conc="0 mM",
                                                                 decay_constant=self.get_bioparameter(
                                                                     "ca_conc_decay_time").value,
                                                                 rho=self.get_bioparameter("ca_conc_rho").value)

        if self.get_bioparameter('ca_conc_xRho_muscle'):

            self.concentration_model_muscle = MuscleConcentrationModel2(id="CaPoolMuscle",
                                                                     ion="ca",
                                                                     resting_conc="0 mM",
                                                                     decay_constant=self.get_bioparameter(
                                                                         "ca_conc_decay_time_muscle").value,
                                                                     rho=self.get_bioparameter("ca_conc_rho_muscle").value,
                                                                       xRho=self.get_bioparameter("ca_conc_xRho_muscle").value,
                                                                      iCaSigmoidMid=self.get_bioparameter("ca_conc_iCaSigmoidMid_muscle").value,
                                                                       iCaSigmoidSlope=self.get_bioparameter("ca_conc_iCaSigmoidSlope_muscle").value,
                                                                       xSigmoidMid=self.get_bioparameter("ca_conc_xSigmoidMid_muscle").value,
                                                                        xSigmoidSlope=self.get_bioparameter(
                                                                            "ca_conc_xSigmoidSlope_muscle").value,
                                                                       xDecay=self.get_bioparameter("ca_conc_xDecay_muscle").value,
                                                                        xrest=self.get_bioparameter("ca_conc_xrest_muscle").value,)
        else:
            self.concentration_model_muscle = FixedFactorConcentrationModel(id="CaPoolMuscle",
                                                                            ion="ca",
                                                                            resting_conc="0 mM",
                                                                            decay_constant=self.get_bioparameter(
                                                                                "ca_conc_decay_time_muscle").value,
                                                                            rho=self.get_bioparameter(
                                                                                "ca_conc_rho_muscle").value)

        self.concentration_model = [self.concentration_model_neuron, self.concentration_model_muscle]


    def create_neuron_to_muscle_syn(self):
        self.neuron_to_muscle_exc_syn = GradedSynapse(id="neuron_to_muscle_exc_syn",
                                conductance =        self.get_bioparameter("neuron_to_muscle_exc_syn_conductance").value,
                                delta =              self.get_bioparameter("neuron_to_muscle_exc_syn_delta").value,
                                Vth =                self.get_bioparameter("neuron_to_muscle_exc_syn_vth").value,
                                erev =               self.get_bioparameter("neuron_to_muscle_exc_syn_erev").value,
                                k =                  self.get_bioparameter("neuron_to_muscle_exc_syn_k").value)


        self.neuron_to_muscle_inh_syn = GradedSynapse(id="neuron_to_muscle_inh_syn",
                                conductance =        self.get_bioparameter("neuron_to_muscle_inh_syn_conductance").value,
                                delta =              self.get_bioparameter("neuron_to_muscle_inh_syn_delta").value,
                                Vth =                self.get_bioparameter("neuron_to_muscle_inh_syn_vth").value,
                                erev =               self.get_bioparameter("neuron_to_muscle_inh_syn_erev").value,
                                k =                  self.get_bioparameter("neuron_to_muscle_inh_syn_k").value)

        self.neuron_to_muscle_elec_syn = GapJunction(id="neuron_to_muscle_elec_syn",
                               conductance =    self.get_bioparameter("neuron_to_muscle_elec_syn_gbase").value)


    def create_muscle_to_muscle_syn(self):
        self.muscle_to_muscle_elec_syn = GapJunction(id="muscle_to_muscle_elec_syn",
                               conductance =    self.get_bioparameter("muscle_to_muscle_elec_syn_gbase").value)

    def get_elec_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False
        sigma = mu = p_gbase = ar = ad = beta = gbase = vth = erev = conn_id = None
        if type == 'neuron_to_neuron':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                                              'neuron_to_neuron_elec_syn_%s', 'gbase')
            sigma = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                                              'neuron_to_neuron_elec_syn_%s', 'sigma')
            mu = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                                              'neuron_to_neuron_elec_syn_%s', 'mu')
            p_gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                     'neuron_to_neuron_elec_syn_%s', 'p_gbase')

            ar = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                          'neuron_to_neuron_elec_syn_%s', 'p_ar')

            ad = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                          'neuron_to_neuron_elec_syn_%s', 'p_ad')

            beta = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                     'neuron_to_neuron_elec_syn_%s', 'beta')

            vth = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                     'neuron_to_neuron_elec_syn_%s', 'vth')

            erev = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                     'neuron_to_neuron_elec_syn_%s', 'erev')

            if sigma and mu or p_gbase and mu:
                self.found_specific_param = True

            conn_id = 'neuron_to_neuron_elec_syn'
        elif type == 'neuron_to_muscle':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                                              'neuron_to_muscle_elec_syn_%s', 'gbase')
            conn_id = 'neuron_to_muscle_elec_syn'
        elif type == 'muscle_to_muscle':
            gbase = self.get_conn_param(pre_cell, post_cell, '%s_to_%s_elec_syn_%s',
                                                              'muscle_to_muscle_elec_syn_%s', 'gbase')
            conn_id = 'muscle_to_muscle_elec_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_elec_syn' % (pre_cell, post_cell)

        if sigma and mu and not p_gbase:
            conn_id = '%s_to_%s_delayed_elec_syn' % (pre_cell, post_cell)
            return DelayedGapJunction(id=conn_id,
                                      conductance=gbase,
                                      sigma=sigma,
                                      mu=mu)

        elif p_gbase and sigma:
            conn_id = '%s_to_%s_proprioceptive_elec_syn' % (pre_cell, post_cell)
            if ar and ad:
                conn_id = '%s_to_%s_proprioceptive2_elec_syn' % (pre_cell, post_cell)
                return ProprioGapJunction2(id=conn_id,
                                          conductance=gbase,
                                          p_conductance=p_gbase,
                                          ar=ar,
                                          ad=ad,
                                           beta=beta,
                                           vth=vth,
                                           erev=erev,
                                          sigma=sigma,
                                          mu=mu)
            return ProprioGapJunction(id=conn_id,
                                      conductance=gbase,
                                      p_conductance=p_gbase,
                                      sigma=sigma,
                                      mu=mu)
        return GapJunction(id=conn_id, conductance=gbase)

    def get_exc_syn(self, pre_cell, post_cell, type):
        self.found_specific_param = False

        specific_param_template = '%s_to_%s_exc_syn_%s'

        cath = ar = ad = beta = vth = erev = None

        if type == 'neuron_to_neuron':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_neuron_exc_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'neuron_to_neuron_exc_syn_%s', 'erev')
            delta = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'neuron_to_neuron_exc_syn_%s', 'delta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                            'neuron_to_neuron_exc_syn_%s', 'vth')
            k = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                          'neuron_to_neuron_exc_syn_%s', 'k')
            ar = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                    'neuron_to_neuron_exc_syn_%s', 'ar')
            ad = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                    'neuron_to_neuron_exc_syn_%s', 'ad')
            beta = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                    'neuron_to_neuron_exc_syn_%s', 'beta')

            conn_id = 'neuron_to_neuron_exc_syn'

        elif type == 'neuron_to_muscle':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                              'neuron_to_muscle_exc_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                       'neuron_to_muscle_exc_syn_%s', 'erev')
            delta = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                        'neuron_to_muscle_exc_syn_%s', 'delta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                      'neuron_to_muscle_exc_syn_%s', 'vth')
            k = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                    'neuron_to_muscle_exc_syn_%s', 'k')

            conn_id = 'neuron_to_muscle_exc_syn'



        elif type == 'muscle_to_neuron':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                              'muscle_to_neuron_exc_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'muscle_to_neuron_exc_syn_%s',
                                       'erev')
            ar = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'muscle_to_neuron_exc_syn_%s',
                                     'ar')
            ad = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'muscle_to_neuron_exc_syn_%s',
                                     'ad')
            beta = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'muscle_to_neuron_exc_syn_%s',
                                       'beta')
            cath = self.get_conn_param(pre_cell, post_cell, specific_param_template, 'muscle_to_neuron_exc_syn_%s',
                                       'cath')

            conn_id = 'muscle_to_neuron_exc_syn'

        if self.found_specific_param:
            conn_id = '%s_to_%s_exc_syn' % (pre_cell, post_cell)

        if cath:
            return NeuronMuscle(id=conn_id,
                                  conductance=conductance,
                                  ar=ar,
                                  ad=ad,
                                  beta=beta,
                                  cath=cath,
                                  erev=erev)

        if ar and ad and beta:
            return GradedSynapse2(id=conn_id,
                                 conductance=conductance,
                                 ar=ar,
                                 ad=ad,
                                 beta=beta,
                                 vth=vth,
                                  erev=erev,)

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
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'neuron_to_neuron_inh_syn_%s',
                                                             'erev')
            delta = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'neuron_to_neuron_inh_syn_%s',
                                                              'delta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                            'neuron_to_neuron_inh_syn_%s',
                                                            'vth')
            k = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                          'neuron_to_neuron_inh_syn_%s',
                                                          'k')

            conn_id = 'neuron_to_neuron_inh_syn'

        elif type == 'neuron_to_muscle':
            conductance = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                                    'neuron_to_muscle_inh_syn_%s', 'conductance')
            erev = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                             'neuron_to_muscle_inh_syn_%s',
                                                             'erev')
            delta = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                              'neuron_to_muscle_inh_syn_%s',
                                                              'delta')
            vth = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                            'neuron_to_muscle_inh_syn_%s',
                                                            'vth')
            k = self.get_conn_param(pre_cell, post_cell, specific_param_template,
                                                          'neuron_to_muscle_inh_syn_%s',
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

    def create_n_connection_synapse(self, prototype_syn, n, nml_doc, existing_synapses):
        if prototype_syn.id in existing_synapses: 
            return existing_synapses[prototype_syn.id]

        if isinstance(prototype_syn, (DelayedGapJunction, ProprioGapJunction, ProprioGapJunction2)):
            existing_synapses[prototype_syn.id] = prototype_syn
            nml_doc.gap_junctions.append(prototype_syn)
            return prototype_syn
        elif isinstance(prototype_syn, (NeuronMuscle, GradedSynapse, GradedSynapse2)):
            existing_synapses[prototype_syn.id] = prototype_syn
            nml_doc.graded_synapses.append(prototype_syn)
            return prototype_syn
        else:
            return super(ParameterisedModel, self).create_n_connection_synapse(prototype_syn, n, nml_doc, existing_synapses)

    def is_elec_conn(self, syn):
        return super(ParameterisedModel, self).is_elec_conn(syn) \
               or isinstance(syn, (DelayedGapJunction, ProprioGapJunction, ProprioGapJunction2))

    def is_analog_conn(self, syn):
        return super(ParameterisedModel, self).is_analog_conn(syn) or isinstance(syn, (NeuronMuscle, GradedSynapse2))



class SwitchedGapJunction():
    def __init__(self, id, conductance, delay):
        self.id = id
        self.conductance = conductance
        self.delay = delay

    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write(
            '    ' * level + '<switchedGapJunction id="%s" conductance="%s" delay="%s" />\n' % (
            self.id, self.conductance, self.delay))


class DelayedGapJunction():
    def __init__(self, id, conductance, sigma, mu, weight=1):
        self.id = id
        self.weight = weight
        self.conductance = conductance
        self.sigma = sigma
        self.mu = mu

    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write(
            '    ' * level + '<delayedGapJunction id="%s" weight="%s" conductance="%s" sigma="%s" mu="%s" />\n'
            % (self.id, self.weight, self.conductance, self.sigma, self.mu))

    def __repr__(self):
        return "DelayedGapJunction(id=%s, weight=%s, conductance=%s, sigma=%s, mu=%s)" % (self.id, self.weight, self.conductance, self.sigma, self.mu)


class ProprioGapJunction():
    def __init__(self, id, conductance, p_conductance, mu, weight=1, sigma='0.3 per_mV'):
        self.id = id
        self.weight = weight
        self.conductance = conductance
        self.p_conductance = p_conductance
        self.sigma = sigma
        self.mu = mu

    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write(
            '    ' * level + '<proprioGapJunction id="%s" weight="%s" conductance="%s" p_conductance="%s" sigma="%s" mu="%s" />\n'
            % (self.id, self.weight, self.conductance, self.p_conductance, self.sigma, self.mu))

    def __repr__(self):
        return "ProprioGapJunction(id=%s, weight=%s, conductance=%s, p_conductance=%s, sigma=%s mu=%s)" % (self.id, self.weight, self.conductance, self.p_conductance, self.sigma, self.mu)

class ProprioGapJunction2():
    def __init__(self, id, conductance, p_conductance, mu, ar=None, ad=None, beta=None, vth=None, erev=None, weight=1, sigma='0.3 per_mV'):
        self.id = id
        self.weight = weight
        self.conductance = conductance
        self.p_conductance = p_conductance
        self.sigma = sigma
        self.mu = mu
        self.ar = ar
        self.ad = ad
        self.beta = beta
        self.vth = vth
        self.erev = erev

    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write(
            '    ' * level + '<proprioGapJunction2 id="%s" weight="%s" ar="%s" ad="%s" beta="%s" vth="%s" erev="%s" conductance="%s" p_conductance="%s" sigma="%s" mu="%s" />\n'
            % (self.id, self.weight, self.ar, self.ad, self.beta, self.vth, self.erev, self.conductance, self.p_conductance, self.sigma, self.mu))

    def __repr__(self):
        return "ProprioGapJunction2(id=%s, weight=%s, ar=%s, ad=%s, beta=%s, vth=%s, erev=%s, conductance=%s, p_conductance=%s, sigma=%s mu=%s)" % (self.id, self.weight, self.ar, self.ad, self.beta, self.vth, self.erev, self.conductance, self.p_conductance, self.sigma, self.mu)


class DelayedGradedSynapse():
    def __init__(self, id=None, weight=1, conductance=None, delta=None, vth=None, k=None, erev=None, sigma=None, mu=None):
        self.id = id
        self.weight = weight
        self.conductance = conductance
        self.delta = delta
        self.vth = vth
        self.k = k
        self.erev = erev
        self.sigma = sigma
        self.mu = mu

    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write(
            '    ' * level + '<delayedGradedSynapse id="%s" weight="%s" conductance="%s" delta="%s" vth="%s" k="%s" erev="%s" sigma="%s" mu="%s" />\n'
            % (self.id, self.weight, self.conductance, self.delta, self.vth, self.k, self.erev, self.sigma, self.mu))

    def __repr__(self):
        return "DelayedGradedSynapse(id=%s, weight=%s, conductance=%s, delta=%s, vth=%s, k=%s, erev=%s, sigma=%s, mu=%s)" \
               % (self.id, self.weight, self.conductance, self.delta, self.vth, self.k, self.erev, self.sigma, self.mu)


class NeuronMuscle():
    def __init__(self, id, conductance, ar, ad, beta, cath, erev):
        self.id = id
        self.conductance = conductance
        self.ar = ar
        self.ad = ad
        self.beta = beta
        self.cath = cath
        self.erev = erev

    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write(
            '    ' * level + '<proprio id="%s" conductance="%s" ar="%s" ad="%s" beta="%s" cath="%s" erev="%s"/>\n' % (
            self.id, self.conductance, self.ar, self.ad, self.beta, self.cath, self.erev))


class MuscleConcentrationModel():
    def __init__(self, id, ion, resting_conc, decay_constant, rho):
        self.id = id
        self.ion = ion
        self.resting_conc = resting_conc
        self.decay_constant = decay_constant
        self.rho = rho


    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write(
            '    ' * level + '<muscleConcentrationModel id="%s" ion="%s" restingConc="%s" decayConstant="%s" rho="%s" />\n'
            % (self.id, self.ion, self.resting_conc, self.decay_constant, self.rho))

    def __repr__(self):
        return "MuscleConcentrationModel(id=%s, ion=%s, resting_conc=%s, decay_constant=%s, rho=%s)" % (self.id, self.ion, self.resting_conc, self.decay_constant, self.rho)



class MuscleConcentrationModel2():
    def __init__(self, id, ion, resting_conc, decay_constant, rho, xRho, xrest, iCaSigmoidMid='', iCaSigmoidSlope='', xSigmoidMid='', xSigmoidSlope='', xDecay=''):
        self.id = id
        self.ion = ion
        self.resting_conc = resting_conc
        self.decay_constant = decay_constant
        self.rho = rho
        self.xRho = xRho
        self.iCaSigmoidMid = iCaSigmoidMid
        self.iCaSigmoidSlope = iCaSigmoidSlope
        self.xSigmoidMid = xSigmoidMid
        self.xSigmoidSlope = xSigmoidSlope
        self.xDecay = xDecay
        self.xrest = xrest


    def export(self, outfile, level, namespace, name_, pretty_print=True):
        outfile.write(
            '    ' * level + '<muscleConcentrationModel2 id="%s" ion="%s" restingConc="%s" decayConstant="%s" rho="%s" xRho="%s" iCaSigmoidMid="%s" iCaSigmoidSlope="%s" xSigmoidMid="%s" xSigmoidSlope="%s" xDecay="%s" xrest="%s" />\n'
            % (self.id, self.ion, self.resting_conc, self.decay_constant, self.rho, self.xRho, self.iCaSigmoidMid, self.iCaSigmoidSlope, self.xSigmoidMid, self.xSigmoidSlope, self.xDecay, self.xrest))

    def __repr__(self):
        return "MuscleConcentrationModel2(id=%s, ion=%s, resting_conc=%s, decay_constant=%s, rho=%s, xRho=%s, iCaSigmoidMid=%s, iCaSigmoidSlope=%s xSigmoidMid=%s xSigmoidSlope=%s xDecay=%s xrest=%s)" % (self.id, self.ion, self.resting_conc, self.decay_constant, self.rho, self.xRho, self.iCaSigmoidMid, self.iCaSigmoidSlope, self.xSigmoidMid, self.xSigmoidSlope, self.xDecay, self.xrest)


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
        outfile.write(
            '    ' * level + '<gradedSynapse2 id="%s" conductance="%s" ar="%s" ad="%s" beta="%s" vth="%s" erev="%s"/>\n' % (
            self.id, self.conductance, self.ar, self.ad, self.beta, self.vth, self.erev))

