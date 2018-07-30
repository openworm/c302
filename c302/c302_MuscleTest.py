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
          data_reader="SpreadsheetDataReader",
          param_overrides={},
          verbose=True,
          config_param_overrides={}):

    exec('from parameters_%s import ParameterisedModel'%parameter_set, globals())
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


    cells = []

    muscles_to_include = True

    if config_param_overrides.has_key('muscles_to_include'):
        muscles_to_include = config_param_overrides['muscles_to_include']

    cells_to_stimulate = []

    cells_to_plot = list(cells)
    reference = "c302_%s_MuscleTest" % parameter_set


    conns_to_include = []
    if config_param_overrides.has_key('conns_to_include'):
        conns_to_include = config_param_overrides['conns_to_include']

    conns_to_exclude = ['^.+-.+$']
    if config_param_overrides.has_key('conns_to_exclude'):
        conns_to_exclude = config_param_overrides['conns_to_exclude']

    conn_polarity_override = {}
    if config_param_overrides.has_key('conn_polarity_override'):
        conn_polarity_override.update(config_param_overrides['conn_polarity_override'])

    conn_number_override = {

    }
    if config_param_overrides.has_key('conn_number_override'):
        conn_number_override.update(config_param_overrides['conn_number_override'])



    param_overrides = {
        'ca_conc_decay_time_muscle': '60 ms',
        'ca_conc_rho_muscle': '0.002138919 mol_per_m_per_A_per_s',
    }


    end = '%sms' % (int(duration) - 100)


    input_list = []

    
    #input_list.append(('MDL02', '0ms', '250ms', '3pA'))
    #input_list.append(('MDL03', '0ms', '250ms', '3pA'))
    #input_list.append(('MDR02', '0ms', '250ms', '3pA'))
    #input_list.append(('MDR03', '0ms', '250ms', '3pA'))

    input_list.append(('MVR10', '0ms', '250ms', '1pA'))
    input_list.append(('MVR11', '0ms', '250ms', '2pA'))
    input_list.append(('MVR12', '0ms', '250ms', '3pA'))
    input_list.append(('MVR13', '0ms', '250ms', '3pA'))
    input_list.append(('MVR14', '0ms', '250ms', '2pA'))
    input_list.append(('MVR15', '0ms', '250ms', '1pA'))
    
    input_list.append(('MVL10', '0ms', '250ms', '1pA'))
    input_list.append(('MVL11', '0ms', '250ms', '2pA'))
    input_list.append(('MVL12', '0ms', '250ms', '3pA'))
    input_list.append(('MVL13', '0ms', '250ms', '3pA'))
    input_list.append(('MVL14', '0ms', '250ms', '2pA'))
    input_list.append(('MVL15', '0ms', '250ms', '1pA'))

    input_list.append(('MDL21', '0ms', '250ms', '3pA'))
    input_list.append(('MDL22', '0ms', '250ms', '3pA'))
    input_list.append(('MDR21', '0ms', '250ms', '3pA'))
    input_list.append(('MDR22', '0ms', '250ms', '3pA'))



    for stim_num in range(5):
        for muscle_num in range(24):
            mdlx = 'MDL0%s' % (muscle_num + 1)
            mdrx = 'MDR0%s' % (muscle_num + 1)

            mvlx = 'MVL0%s' % (muscle_num + 1)
            mvrx = 'MVR0%s' % (muscle_num + 1)

            if muscle_num >= 9:
                mdlx = 'MDL%s' % (muscle_num + 1)
                mdrx = 'MDR%s' % (muscle_num + 1)

                mvlx = 'MVL%s' % (muscle_num + 1)
                if muscle_num != 23:
                    mvrx = 'MVR%s' % (muscle_num + 1)

            startd = '%sms' % (stim_num * 1000 + muscle_num * 50)
            startv = '%sms' % ((stim_num  * 1000 + 500) + muscle_num * 50)
            dur = '250ms'
            amp = '3pA'

            input_list.append((mdlx, startd, dur, amp))
            input_list.append((mdrx, startd, dur, amp))

            input_list.append((mvlx, startv, dur, amp))
            input_list.append((mvrx, startv, dur, amp))

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

        if config_param_overrides.has_key('input'):
            input_list = config_param_overrides['input']

        for stim_input in input_list:
            cell, start, dur, current = stim_input
            c302.add_new_input(nml_doc, cell, start, dur, current, params)

        nml_file = target_directory + '/' + reference + '.net.nml'
        writers.NeuroMLWriter.write(nml_doc, nml_file)  # Write over network file written above...

        c302.print_("(Re)written network file to: " + nml_file)


    return cells, cells_to_stimulate, params, muscles_to_include, nml_doc


if __name__ == '__main__':
    parameter_set = sys.argv[1] if len(sys.argv) == 2 else 'C2'
    data_reader = sys.argv[2] if len(sys.argv) == 3 else 'UpdatedSpreadsheetDataReader'

    setup(parameter_set, generate=True, data_reader=data_reader)
