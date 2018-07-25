'''

    Tap-Withdrawal circuit still under development - it does not produce the correct behavior!
    
'''

import c302
import sys

import neuroml.writers as writers

range_incl = lambda start, end:range(start, end + 1)

def setup(parameter_set,
          generate=False,
          duration=400,
          dt=0.05,
          target_directory='examples',
          data_reader="UpdatedSpreadsheetDataReader",
          param_overrides={},
          config_param_overrides={},
          verbose=True):
    
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
    AS_motors = []
    TW_cells = ['AVAL', 'AVAR', 'AVBL', 'AVBR', 'PVCL', 'PVCR', 'AVDL', 'AVDR', 'DVA', 'PVDL', 'PVDR', 'PLML', 'PLMR',
                'AVM', 'ALML', 'ALMR']
    TW_sensory = ["PLML", "PLMR", "AVM", "ALML", "ALMR"]
    all_motors = list(VA_motors + VB_motors + DA_motors + DB_motors + DD_motors + VD_motors + AS_motors)
    #all_motors = []
    
    #neurons = ['AVAL', 'AVAR', 'AVBL', 'AVBR', 'PVCL', 'PVCR', 'AVDL', 'AVDR', 'DVA', 'PVDL', 'PVDR', 'PLML', 'PLMR', 'AVM', 'ALML', 'ALMR']

    muscles_to_include = False
    #muscles_to_include = True # ALL muscles
    #muscles_to_include = ['MVL01', 'MVL10']

    cells = list(TW_cells + all_motors)
    
    cells_to_plot = list(cells)
    #cells_to_plot = ["VB5", "VA4"]

    cells += [  # 'AS1', 'AS10', 'AS11', 'AS2', 'AS3', 'AS4', 'AS5', 'AS6', 'AS7', 'AS8', 'AS9',
        # 'AVFL', 'AVFR', 'AVKR', 'AVL',
        # 'CEPVL', 'CEPVR',
        #
        #
        # 'DVB',
        # 'HSNL', 'HSNR',
        # 'IL1DL', 'IL1DR', 'IL1L', 'IL1R', 'IL1VL', 'IL1VR',
        # 'PDA', 'PDB',
        # 'PVNL', 'PVNR',
        # 'RID', 'RIML', 'RIMR', 'RIVL', 'RIVR',
        # 'RMDDL', 'RMDDR', 'RMDL', 'RMDR', 'RMDVL', 'RMDVR', 'RMED', 'RMEL', 'RMER', 'RMEV', 'RMFL', 'RMGL', 'RMGR',
        # 'RMHL', 'RMHR',
        # 'SMBDL', 'SMBDR', 'SMBVL', 'SMBVR', 'SMDDL', 'SMDDR', 'SMDVL', 'SMDVR',
        # 'URADL', 'URADR', 'URAVL', 'URAVR',
        # 'VC1', 'VC2', 'VC3', 'VC4', 'VC5', 'VC6',
    ]

    # cells = None
    #cells_to_stimulate = ['PLML', 'PLMR', 'AVM']
    cells_to_stimulate = []

    #cells_to_plot = ['AVAL', 'AVAR', 'AVBL', 'AVBR', 'PLML', 'PLMR', 'AVM', 'ALML', 'ALMR', 'PVDL', 'PVDR', 'AVDL', 'AVDR']
    #cells_to_plot = ['PLML', 'AVM', 'AVBL', 'AVAL']
    #cells_to_plot = cells
    #cells_to_plot += motors
    reference = "c302_%s_TapWithdrawal" % parameter_set

    conn_polarity_override = {
        'ALML-ALML':'inh',
        'ALML-PVCL':'inh',
        'ALML-PVCR':'inh',
        'ALML-AVDR':'inh', ##
        'ALMR-PVCR':'inh',

        'AVM-PVCL':'inh',
        'AVM-PVCR':'inh',
        'AVM-AVBL':'inh',
        'AVM-AVBR':'inh',
        'AVM-AVDL':'inh', ##
        'AVM-AVDR':'inh', ##

        'PVDL-PVDR':'inh',
        'PVDL-PVCL':'exc',
        'PVDL-PVCR':'exc',
        'PVDL-AVAL':'inh',
        'PVDL-AVAR':'inh',
        'PVDL-AVDL':'inh',
        'PVDL-AVDR':'inh',
        'PVDR-PVDL':'inh',
        'PVDR-DVA':'exc',
        'PVDR-PVCL':'exc',
        'PVDR-PVCR':'exc',
        'PVDR-AVAL':'inh',
        'PVDR-AVAR':'inh',
        'PVDR-AVDL':'inh',

        'DVA-PVCL':'inh',#
        'DVA-PVCR':'inh',#
        'DVA-AVAL':'inh',
        'DVA-AVAR':'inh',
        'DVA-AVBL':'inh',#
        'DVA-AVBR':'inh',#
        'DVA-AVDR':'inh',

        'PVCL-DVA':'exc',
        'PVCL-PVCL':'inh',
        'PVCL-PVCR':'inh',
        'PVCL-AVAL':'inh',
        'PVCL-AVAR':'inh',
        'PVCL-AVBL':'exc',
        'PVCL-AVBR':'exc',
        'PVCL-AVDL':'inh',
        'PVCL-AVDR':'inh',
        'PVCR-PVDL':'inh',
        'PVCR-PVDR':'inh',
        'PVCR-DVA':'exc',
        'PVCR-PVCL':'inh',
        'PVCR-AVAL':'inh',
        'PVCR-AVAR':'inh',
        'PVCR-AVBL':'exc',
        'PVCR-AVBR':'exc',
        'PVCR-AVDL':'inh',
        'PVCR-AVDR':'inh',

        'AVAL-PVCL':'inh',
        'AVAL-PVCR':'inh',
        'AVAL-AVAR':'inh',
        'AVAL-AVBL':'inh',
        'AVAL-AVDL':'inh',
        'AVAL-AVDR':'inh',

        'AVAR-PVCL':'inh',
        'AVAR-PVCR':'inh',
        'AVAR-AVAL':'inh',
        'AVAR-AVBL':'inh',
        'AVAR-AVBR':'inh',
        'AVAR-AVDL':'inh',
        'AVAR-AVDR':'inh',

        'AVBL-DVA':'inh',
        'AVBL-PVCR':'inh',
        'AVBL-AVAL':'inh',
        'AVBL-AVAR':'inh',
        'AVBL-AVBR':'inh',
        'AVBL-AVDR':'inh',
        'AVBR-AVAL':'inh',
        'AVBR-AVAR':'inh',
        'AVBR-AVBL':'inh',
        'AVBR-AVDL':'inh',

        'AVDL-PVCL':'inh',
        'AVDL-AVAL':'exc',
        'AVDL-AVAR':'exc',
        'AVDL-AVDR':'exc',
        'AVDR-PVCR':'inh',
        'AVDR-AVAL':'exc',
        'AVDR-AVAR':'exc',
        'AVDR-AVBL':'inh',
        'AVDR-AVDL':'exc',

        'DA9-DVA':'inh',

        'DVA-DA2':'inh',
        'PVCL-DA5':'inh',
        'PVCL-DA8':'inh',
        'PVCR-DA2':'inh',
        'PVCR-DA4':'inh',
        'PVCR-DA5':'inh',
        'PVCR-DA7':'inh',
        'AVBL-DA5':'inh',
        'AVBL-DA7':'inh',
        'AVBR-DA3':'inh',
        'AVBR-DA4':'inh',
        'AVBR-DA7':'inh',
        'AVDL-DA1':'inh',
        'AVDL-DA2':'inh',
        'AVDL-DA3':'inh',
        'AVDL-DA4':'inh',
        'AVDL-DA5':'inh',
        'AVDL-DA8':'inh',
        'AVDR-DA1':'inh',
        'AVDR-DA2':'inh',
        'AVDR-DA3':'inh',
        'AVDR-DA4':'inh',
        'AVDR-DA5':'inh',
        'AVDR-DA8':'inh',
        'DB1-DA1':'inh',
        'DB1-DA2':'inh',
        'DB2-DA2':'inh',
        'DB2-DA3':'inh',
        'DB2-DA4':'inh',
        'DB3-DA4':'inh',
        'DB3-DA5':'inh',
        'DB4-DA5':'inh',
        'DB5-DA6':'inh',
        'DB5-DA7':'inh',
        'DB5-DA8':'inh',
        'DB6-DA8':'inh',
        'DB6-DA9':'inh',
        'DB7-DA9':'inh',

        'AVAR-DB2':'inh',
        'AVAR-DB3':'inh',
        'AVAL-DB7':'inh',
        'DA1-DB1':'inh',
        'DA2-DA3':'inh',
        'DA2-DB1':'inh',
        'DA3-DB3':'inh',
        'DA4-DB2':'inh',
        'DA5-DB4':'inh',
        'DA6-DB5':'inh',
        'DA7-DB6':'inh',
        'DA8-DB7':'inh',
        'DA9-DB7':'inh',


        'DVA-VA2':'inh',
        'DVA-VA6':'inh',
        'DVA-VA8':'inh',
        'DVA-VA12':'inh',
        'PVCL-VA11':'inh',
        'PVDR-VA9':'inh',
        'PVDR-VA12':'inh',
        'AVBL-VA2':'inh',
        'AVBL-VA10':'inh',
        'AVBR-VA3':'inh',
        'AVBR-VA4':'inh',
        'AVDL-VA3':'inh',
        'AVDL-VA5':'inh',
        'AVDL-VA10':'inh',
        'AVDL-VA12':'inh',
        'AVDR-VA2':'inh',
        'AVDR-VA3':'inh',
        'AVDR-VA5':'inh',
        'AVDR-VA11':'inh',

        'VB1-VA1':'inh',
        'VB1-VA2':'inh',
        'VB1-VA3':'inh',
        'VB1-VA4':'inh',
        'VB2-VA2':'inh',
        'VB2-VA3':'inh',
        'VB3-VA4':'inh',
        'VB3-VA5':'inh',
        'VB4-VA4':'inh',
        'VB4-VA5':'inh',
        'VB5-VA6':'inh',
        'VB6-VA7':'inh',
        'VB6-VA8':'inh',
        'VB7-VA9':'inh',
        'VB7-VA10':'inh',
        'VB8-VA11':'inh',
        'VB9-VA11':'inh',
        'VB10-VA11':'inh',
        'VB11-VA12':'inh',

        'VB11-PVCR':'inh',
        'VB4-VB5':'inh',


        'VA2-VB1':'inh',
        'VA2-VB2':'inh',
        'VA3-VB2':'inh',
        'VA3-VB3':'inh',
        'VA4-AVDL':'inh',
        'VA4-VB3':'inh',
        'VA4-VB4':'inh',
        'VA5-VB4':'inh',
        'VA6-VB4':'inh',
        'VA6-VB5':'inh',
        'VA7-VB6':'inh',
        'VA8-VB6':'inh',
        'VA9-VB7':'inh',
        'VA9-VB8':'inh',
        'VA10-VB8':'inh',
        'VA10-VB9':'inh',
        'VA11-VB10':'inh',
        'VA12-PVCL':'inh',
        'VA12-PVCR':'inh',
        'VA12-DB7':'inh',
        'VA12-VB11':'inh',


        'AVM-VB3':'inh',
        #'VB4-VB5':'exc',

        #'DD1-DA2':'inh',
        #'DD1-VB2':'inh',
        #'DD2-DA3':'inh',
        #'DD3-DA5':'inh',
    }

    conn_number_override = {
        #'PVCL-AVDL':7*0.1,
        #'PVCL-AVDR':11*0.1,
        #'PVCR-AVDL':16*0.1,
        #'PVCR-AVDR':6*0.1,

        #'PVCR-AVDR_GJ':2 * 0.01,
        #'AVDR-PVCR_GJ':2 * 0.01,

        'PVCL-AVAL_GJ':5 * 0.01,
        'AVAL-PVCL_GJ':5 * 0.01,
        'PVCL-AVAR_GJ':10 * 0.01,
        'AVAR-PVCL_GJ':10 * 0.01,
        'PVCR-AVAL_GJ':15 * 0.01,
        'AVAL-PVCR_GJ':15 * 0.01,
        'PVCR-AVAR_GJ':22 * 0.01,
        'AVAR-PVCR_GJ':22 * 0.01,

        'PVCL-PLML_GJ':4 * 0.01, ##
        'PVCR-PLMR_GJ':8 * 0.01, ##

        #'AVDL-AVM_GJ':8 * 0.01,
        #'ALML-AVM_GJ':1 * 0.01,
        #'ALMR-AVM_GJ':1 * 0.01,
        
        #'AVDR-ALMR_GJ':1 * 0.01,

        # 'AVDL-AVAL':37*0.1,
        # 'AVDL-AVAR':37*0.1,
        # 'AVDR-AVAL':41*0.1,
        # 'AVDR-AVAR':52*0.1,

        # 'AVDL-AVAL_GJ':7*0.1,
        # 'AVAL-AVDL_GJ':7*0.1,
        # 'AVDL-AVAR_GJ':2*0.1,
        # 'AVAR-AVDL_GJ':2*0.1,
        # 'AVDR-AVAL_GJ':9*0.1,
        # 'AVAL-AVDR_GJ':9*0.1,
        # 'AVDR-AVAR_GJ':15*0.1,
        # 'AVAR-AVDR_GJ':15*0.1,


        # 'ALMR-AVDR_GJ':2*5,
        # 'AVDR-ALMR_GJ':2*5,

        'AVAR-AVBL_GJ':3*0.01,
        'AVBL-AVAR_GJ':3*0.01,

        # 'AVAR-AVAL_GJ':18*2,
        # 'AVAL-AVAR_GJ':18*2,


        'PVDL-AVAR_GJ':4 * 0.01,
        'AVAR-PVDL_GJ':4 * 0.01,
        'PVDR-AVAL_GJ':6 * 0.01,
        'AVAL-PVDR_GJ':6 * 0.01,

        'AVBL-VA11_GJ':1 * 0.01,
        'VA11-AVBL_GJ':1 * 0.01,
        'AVBR-VA11_GJ':3 * 0.01,
        'VA11-AVBR_GJ':3 * 0.01,
        'PVCR-VA11_GJ':3 * 0.01,
        'VA11-PVCR_GJ':3 * 0.01,
        'DVA-VA11_GJ':1 * 0.01,
        'VA11-DVA_GJ':1 * 0.01,

        'PVCL-VA12_GJ':18 * 0.01,
        'VA12-PVCL_GJ':18 * 0.01,
        'PVCR-VA12_GJ':8 * 0.01,
        'VA12-PVCR_GJ':8 * 0.01,

        'AVAL-VB11_GJ':2 * 0.01,
        'VB11-AVAL_GJ':2 * 0.01,

        'PVCL-DA4_GJ':1 * 0.01,
        'DA4-PVCL_GJ':1 * 0.01,

        'PVCL-DA7_GJ':1 * 0.01,
        'DA7-PVCL_GJ':1 * 0.01,
        'PVCR-DA7_GJ':3 * 0.01,
        'DA7-PVCR_GJ':3 * 0.01,

        'PVCL-DA8_GJ':17 * 0.01,
        'DA8-PVCL_GJ':17 * 0.01,
        'PVCR-DA8_GJ':1 * 0.01,
        'DA8-PVCR_GJ':1 * 0.01,

        'DVA-DA9_GJ':3 * 0.01,
        'DA9-DVA_GJ':3 * 0.01,
        'PVCR-DA9_GJ':3 * 0.01,
        'DA9-PVCR_GJ':3 * 0.01,

        'DB7-VA10_GJ':1 * 0.01,
        'VA10-DB7_GJ':1 * 0.01,

        'VA4-VB3_GJ':1 * 0.01,
        'VB3-VA4_GJ':1 * 0.01,


        'VA11-VB10_GJ':3 * 0.01,
        'VB10-VA11_GJ':3 * 0.01,

        'VA12-VB11_GJ':7 * 0.01,
        'VB11-VA12_GJ':7 * 0.01,

        'VB11-DA9_GJ':7 * 0.01,
        'DA9-VB11_GJ':7 * 0.01,
    }
    
    nml_doc = None

    if generate:
        nml_doc = c302.generate(reference,
                                params,
                                cells=cells,
                                cells_to_plot=cells_to_plot,
                                cells_to_stimulate=cells_to_stimulate,
                                conn_polarity_override=conn_polarity_override,
                                conn_number_override=conn_number_override,
                                muscles_to_include=muscles_to_include,
                                duration=duration,
                                dt=dt,
                                target_directory=target_directory,
                                data_reader=data_reader,
                                param_overrides=param_overrides,
                                verbose=verbose)

        stim_amplitude = "6pA"
        # stim_amplitude = "5.135697186048022pA"

        for vb in VB_motors:
            c302.add_new_sinusoidal_input(nml_doc, cell=vb, delay="0ms", duration="1000ms", amplitude="3pA",
                                          period="150ms", params=params)

        for db in DB_motors:
            c302.add_new_sinusoidal_input(nml_doc, cell=db, delay="0ms", duration="1000ms", amplitude="3pA",
                                          period="150ms", params=params)

        #c302.add_new_input(nml_doc, "AVM", "10ms", "700ms", stim_amplitude, params)
        #c302.add_new_input(nml_doc, "ALML", "10ms", "700ms", stim_amplitude, params)
        #c302.add_new_input(nml_doc, "ALMR", "10ms", "700ms", stim_amplitude, params)
        #c302.add_new_input(nml_doc, "PLML", "10ms", "700ms", stim_amplitude, params)
        #c302.add_new_input(nml_doc, "PLMR", "10ms", "700ms", stim_amplitude, params)

        nml_file = target_directory + '/' + reference + '.net.nml'
        writers.NeuroMLWriter.write(nml_doc, nml_file)  # Write over network file written above...

        c302.print_("(Re)written network file to: " + nml_file)

    return cells, cells_to_stimulate, params, muscles_to_include, nml_doc


if __name__ == '__main__':
    parameter_set = sys.argv[1] if len(sys.argv) == 2 else 'C2'

    setup(parameter_set, generate=True, data_reader="UpdatedSpreadsheetDataReader")
