import sys
import os

sys.path.insert(0, os.path.abspath('.'))

import c302

import neuroml.writers as writers

range_incl = lambda start, end:range(start, end + 1)


def setup(parameter_set,
          generate=False,
          duration=2000,
          dt=0.05,
          target_directory='examples',
          data_reader="UpdatedSpreadsheetDataReader2",
          param_overrides={},
          verbose=True,
          config_param_overrides={}):

    exec ('from parameters_%s import ParameterisedModel' % parameter_set, globals())
    params = ParameterisedModel()

    params.set_bioparameter("unphysiological_offset_current", "0pA", "Testing TapWithdrawal", "0")
    params.set_bioparameter("unphysiological_offset_current_del", "0 ms", "Testing TapWithdrawal", "0")
    params.set_bioparameter("unphysiological_offset_current_dur", "2000 ms", "Testing TapWithdrawal", "0")

    VA_motors = ["VA%s" % c for c in range_incl(1, 12)]
    VB_motors = ["VB%s" % c for c in range_incl(1, 11)]
    DA_motors = ["DA%s" % c for c in range_incl(1, 9)]
    DB_motors = ["DB%s" % c for c in range_incl(1, 7)]
    DD_motors = ["DD%s" % c for c in range_incl(1, 6)]
    VD_motors = ["VD%s" % c for c in range_incl(1, 13)]
    AS_motors = ["AS%s" % c for c in range_incl(1, 11)]

    cells = list(['AVBL', 'AVBR'] + DB_motors + VD_motors + VB_motors + DD_motors)
    
    muscles_to_include = True

    cells_to_stimulate = []

    cells_to_plot = list(cells)
    reference = "c302_%s_FW" % parameter_set


    conns_to_include = []
    conns_to_exclude = [
        'VB2-VB4_GJ',
        'VB4-VB2_GJ',
    ]    
    conn_polarity_override = {
        r'^DB\d+-DD\d+$': 'inh',
        r'^VB\d+-VD\d+$': 'inh',
    }
    conn_number_override = {
        '^.+-.+$': 1,
    }
    
    input_list = []

    '''dur = '250ms'
    amp = '3pA'
    for muscle_num in range(24):
        mdlx = 'MDL0%s' % (muscle_num + 1)
        mdrx = 'MDR0%s' % (muscle_num + 1)
        #mvlx = 'MVL0%s' % (muscle_num + 1)
        #mvrx = 'MVR0%s' % (muscle_num + 1)
        
        if muscle_num >= 9:
            mdlx = 'MDL%s' % (muscle_num + 1)
            mdrx = 'MDR%s' % (muscle_num + 1)
            #mvlx = 'MVL%s' % (muscle_num + 1)
            #mvrx = 'MVR%s' % (muscle_num + 1)

        
        startd = '%sms' % (muscle_num * 10)
        #startv = '%sms' % ((stim_num * 800 + 400) + muscle_num * 30)
        
        input_list.append((mdlx, startd, dur, amp))
        input_list.append((mdrx, startd, dur, amp))'''
        

 
    


    input_list.append(('MVR10', '0ms', '150ms', '1pA'))
    input_list.append(('MVR11', '0ms', '150ms', '2pA'))
    input_list.append(('MVR12', '0ms', '150ms', '3pA'))
    input_list.append(('MVR13', '0ms', '150ms', '3pA'))
    input_list.append(('MVR14', '0ms', '150ms', '2pA'))
    input_list.append(('MVR15', '0ms', '150ms', '1pA'))
    
    input_list.append(('MVL10', '0ms', '150ms', '1pA'))
    input_list.append(('MVL11', '0ms', '150ms', '2pA'))
    input_list.append(('MVL12', '0ms', '150ms', '3pA'))
    input_list.append(('MVL13', '0ms', '150ms', '3pA'))
    input_list.append(('MVL14', '0ms', '150ms', '2pA'))
    input_list.append(('MVL15', '0ms', '150ms', '1pA'))

    input_list.append(('MDL21', '0ms', '250ms', '3pA'))
    input_list.append(('MDL22', '0ms', '250ms', '3pA'))
    input_list.append(('MDR21', '0ms', '250ms', '3pA'))
    input_list.append(('MDR22', '0ms', '250ms', '3pA'))


    amp = '4pA'
    dur = '250ms'

    for stim_num in range(15):
        for muscle_num in range(7):
            mdlx = 'MDL0%s' % (muscle_num + 1)
            mdrx = 'MDR0%s' % (muscle_num + 1)
            mvlx = 'MVL0%s' % (muscle_num + 1)
            mvrx = 'MVR0%s' % (muscle_num + 1)
            
            if muscle_num >= 9:
                mdlx = 'MDL%s' % (muscle_num + 1)
                mdrx = 'MDR%s' % (muscle_num + 1)
                mvlx = 'MVL%s' % (muscle_num + 1)
                mvrx = 'MVR%s' % (muscle_num + 1)
            
            startd = '%sms' % (stim_num * 800 + muscle_num * 30)
            startv = '%sms' % ((stim_num * 800 + 400) + muscle_num * 30)
            
            input_list.append((mdlx, startd, dur, amp))
            input_list.append((mdrx, startd, dur, amp))
            if muscle_num != 6:
                input_list.append((mvlx, startv, dur, amp))
                input_list.append((mvrx, startv, dur, amp))


    d_v_delay = 400

    start = 190
    motor_dur = '250ms'

    input_list.append(('AVBL', '0ms', '1e9ms', '15pA'))
    input_list.append(('AVBR', '0ms', '1e9ms', '15pA'))
    input_list.append(('DB1', '%sms'%(start), motor_dur, '3pA'))
    input_list.append(('VB1', '%sms'%(start+d_v_delay), motor_dur, '3pA'))

    i = start + 2 * d_v_delay
    j = start + 3 * d_v_delay
    for pulse_num in range(1,15):
        input_list.append(('DB1', '%sms'%i, motor_dur, '3pA'))
        input_list.append(('VB1', '%sms'%j, motor_dur, '3pA'))
        i += d_v_delay * 2
        j += d_v_delay * 2

        
    #input_list = []
    #input_list.append(('AVBL', '0ms', '1900ms', '15pA'))
    #input_list.append(('AVBR', '0ms', '1900ms', '15pA'))


    config_param_overrides['input'] = input_list

    param_overrides = {
        'mirrored_elec_conn_params': {
            
            r'^AVB._to_DB\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            r'^AVB._to_VB\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            
            r'^DB\d+_to_DB\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            #'^DB\d+_to_DB\d+\_GJ$_elec_syn_p_gbase': '0.08 nS',
            #'^DB\d+_to_DB\d+\_GJ$_elec_syn_sigma': '0.2 per_mV',
            #'^DB\d+_to_DB\d+\_GJ$_elec_syn_mu': '-20 mV',
            
            r'^VB\d+_to_VB\d+\_GJ$_elec_syn_gbase': '0.001 nS',
            #'^VB\d+_to_VB\d+\_GJ$_elec_syn_p_gbase': '0.1 nS',
            #'^VB\d+_to_VB\d+\_GJ$_elec_syn_sigma': '0.3 per_mV',
            #'^VB\d+_to_VB\d+\_GJ$_elec_syn_mu': '-30 mV',
            
            #'VB2_to_VB4_elec_syn_gbase': '0 nS',
            
            r'^DB\d+_to_VB\d+\_GJ$_elec_syn_gbase': '0 nS',
            r'^DB\d+_to_DD\d+\_GJ$_elec_syn_gbase': '0 nS',
            r'^VB\d+_to_VD\d+\_GJ$_elec_syn_gbase': '0 nS',
            #'^VD\d+_to_DD\d+\_GJ$_elec_syn_gbase': '0 nS',
            
            'DD1_to_MVL08_elec_syn_gbase': '0 nS',
            'VD2_to_MDL09_elec_syn_gbase': '0 nS',
        },
        
        r'^VB\d+_to_VB\d+$_exc_syn_conductance': '18 nS',
        r'^VB\d+_to_VB\d+$_exc_syn_ar': '0.19 per_s',
        r'^VB\d+_to_VB\d+$_exc_syn_ad': '73 per_s',
        r'^VB\d+_to_VB\d+$_exc_syn_beta': '2.81 per_mV',
        r'^VB\d+_to_VB\d+$_exc_syn_vth': '-22 mV',
        r'^VB\d+_to_VB\d+$_exc_syn_erev': '10 mV',
        
        r'^DB\d+_to_DB\d+$_exc_syn_conductance': '20 nS',
        r'^DB\d+_to_DB\d+$_exc_syn_ar': '0.08 per_s',
        r'^DB\d+_to_DB\d+$_exc_syn_ad': '18 per_s',
        r'^DB\d+_to_DB\d+$_exc_syn_beta': '0.21 per_mV',
        r'^DB\d+_to_DB\d+$_exc_syn_vth': '-10 mV',
        r'^DB\d+_to_DB\d+$_exc_syn_erev': '10 mV',
        
        'initial_memb_pot': '-50 mV',
        
        'AVBR_to_DB4_exc_syn_conductance': '0 nS',
        
        #'VB4_to_VB5_exc_syn_conductance': '0 nS',
        'AVBL_to_VB2_exc_syn_conductance': '0 nS',
        
        'AVBR_to_VD3_exc_syn_conductance': '0 nS',
        
        
        #'^DB\d+_to_DD\d+$_exc_syn_conductance': '0 nS',
        #'^DD\d+_to_DB\d+$_inh_syn_conductance': '0 nS',
        #'^VB\d+_to_VD\d+$_exc_syn_conductance': '0 nS',
        #'^VD\d+_to_VB\d+$_inh_syn_conductance': '0 nS',
        
        'DD1_to_VB2_inh_syn_conductance': '0 nS',
        
        'neuron_to_muscle_exc_syn_conductance': '0.5 nS',
        r'^DB\d+_to_MDL\d+$_exc_syn_conductance': '0.4 nS',
        r'^DB\d+_to_MDR\d+$_exc_syn_conductance': '0.4 nS',
        r'^VB\d+_to_MVL\d+$_exc_syn_conductance': '0.6 nS',
        r'^VB\d+_to_MVR\d+$_exc_syn_conductance': '0.6 nS',
        'neuron_to_muscle_exc_syn_vth': '37 mV',
        'neuron_to_muscle_inh_syn_conductance': '0.6 nS',
        'neuron_to_neuron_inh_syn_conductance': '0.2 nS',
        
        #'DB2_to_MDL11_exc_syn_conductance': '1 nS',
        
        
        'AVBR_to_MVL16_exc_syn_conductance': '0 nS',
        'ca_conc_decay_time_muscle': '60.8 ms',
        'ca_conc_rho_muscle': '0.002338919 mol_per_m_per_A_per_s',
        
    }
    

    nml_doc = None
    if generate:
        nml_doc = c302.generate(reference,
                                params,
                                cells=cells,
                                cells_to_plot=cells_to_plot,
                                cells_to_stimulate=cells_to_stimulate,
                                conns_to_include=conns_to_include,
                                conns_to_exclude=conns_to_exclude,
                                conn_polarity_override=conn_polarity_override,
                                conn_number_override=conn_number_override,
                                muscles_to_include=muscles_to_include,
                                duration=duration,
                                dt=dt,
                                target_directory=target_directory,
                                data_reader=data_reader,
                                param_overrides=param_overrides,
                                verbose=verbose)

        #if config_param_overrides.has_key('input'):
        #    input_list = config_param_overrides['input']

        for stim_input in input_list:
            cell, start, dur, current = stim_input
            c302.add_new_input(nml_doc, cell, start, dur, current, params)

        nml_file = target_directory + '/' + reference + '.net.nml'
        writers.NeuroMLWriter.write(nml_doc, nml_file)  # Write over network file written above...

        c302.print_("(Re)written network file to: " + nml_file)


    return cells, cells_to_stimulate, params, muscles_to_include, nml_doc


if __name__ == '__main__':
    parameter_set = sys.argv[1] if len(sys.argv) == 2 else 'C2'
    data_reader = sys.argv[2] if len(sys.argv) == 3 else 'UpdatedSpreadsheetDataReader2'

    setup(parameter_set, generate=True, data_reader=data_reader)
