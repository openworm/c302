import c302
import sys

def setup(parameter_set, 
          generate=False,
          duration=1000, 
          dt=0.05,
          target_directory='examples',
          data_reader="SpreadsheetDataReader",
          param_overrides={},
          config_param_overrides={},
          verbose=True):
    
    exec('from parameters_%s import ParameterisedModel'%parameter_set, globals())
    params = ParameterisedModel()
    
    params.set_bioparameter("unphysiological_offset_current", "0pA", "Disabling offset current", "0")
    
    
    #params.set_bioparameter("exc_syn_conductance", ".20 nS", "BlindGuess", "0.1")  
    params.set_bioparameter("chem_exc_syn_decay", "5 ms", "BlindGuess", "0.1")
    
    #params.set_bioparameter("inh_syn_conductance", ".35 nS", "BlindGuess", "0.1")
    params.set_bioparameter("chem_inh_syn_decay", "200 ms", "BlindGuess", "0.1")
    
    #params.set_bioparameter("elec_syn_gbase", "0.001 nS", "BlindGuess", "0.1")
    
    # Any neurons connected to muscles
    
    cells = ['AS1', 'AS10', 'AS11', 'AS2', 'AS3', 'AS4', 'AS5', 'AS6', 'AS7', 'AS8', 'AS9', 
             'AVFL', 'AVFR', 'AVKR', 'AVL', 
             'CEPVL', 'CEPVR', 
             'DA1', 'DA2', 'DA3', 'DA4', 'DA5', 'DA6', 'DA7', 'DA8', 'DA9', 
             'DB1', 'DB2', 'DB3', 'DB4', 'DB5', 'DB6', 'DB7', 
             'DD1', 'DD2', 'DD3', 'DD4', 'DD5', 'DD6', 
             'DVB', 
             'HSNL', 'HSNR', 
             'IL1DL', 'IL1DR', 'IL1L', 'IL1R', 'IL1VL', 'IL1VR', 
             'PDA', 'PDB', 
             'PVNL', 'PVNR', 
             'RID', 'RIML', 'RIMR', 'RIVL', 'RIVR', 
             'RMDDL', 'RMDDR', 'RMDL', 'RMDR', 'RMDVL', 'RMDVR', 'RMED', 'RMEL', 'RMER', 'RMEV', 'RMFL', 'RMGL', 'RMGR', 'RMHL', 'RMHR', 
             'SMBDL', 'SMBDR', 'SMBVL', 'SMBVR', 'SMDDL', 'SMDDR', 'SMDVL', 'SMDVR', 
             'URADL', 'URADR', 'URAVL', 'URAVR', 
             'VA1', 'VA10', 'VA11', 'VA12', 'VA2', 'VA3', 'VA4', 'VA5', 'VA6', 'VA7', 'VA8', 'VA9', 
             'VB1', 'VB10', 'VB11', 'VB2', 'VB3', 'VB4', 'VB5', 'VB6', 'VB7', 'VB8', 'VB9', 
             'VC1', 'VC2', 'VC3', 'VC4', 'VC5', 'VC6', 
             'VD1', 'VD10', 'VD11', 'VD12', 'VD13', 'VD2', 'VD3', 'VD4', 'VD5', 'VD6', 'VD7', 'VD8', 'VD9']
             
    cells+=['AVAL', 'AVAR', 'AVBL', 'AVBR','AVDL', 'AVDR', 'PVCL', 'PVCR']
    #cells=None  # implies all cells...     
    
    ## Some random set of neurons
    #probability = 0.1
    cells_to_stimulate = []
    '''
    for cell in cells:
        #if random.random()<probability:
        #    cells_to_stimulate.append(cell)
        if cell.startswith("xxVB") or cell.startswith("DB"):
            cells_to_stimulate.append(cell)'''
    #cells_to_stimulate = ['DB1', 'VB1']
    
    cells_to_stimulate = ['PVCL', 'AVBL']
    cells_to_stimulate.extend(['DB1', 'VB1'])
    cells_to_stimulate = ['PVCL','PVCR']
    cells_to_stimulate = ['PLML','PLMR']
    cells_to_stimulate = ['AVBL','AVBR']
    
    # Plot some directly stimulated & some not stimulated
    cells_to_plot      = ['AS1', 'AS10', 'AVFL', 'DA1','DB1','DB4','DB7','IL1DL','RID', 'RIML','SMBDL', 'SMBDR', 'VB1', 'VB5', 'VB10','VC1', 'VC2']
    cells_to_plot      = ['AVBL','AVBR','PVCL', 'PVCR', 'DB1','DB2','VB1','VB2','DD1','DD2','VD1','VD2']
    
    reference = "c302_%s_MusclesSine"%parameter_set
    
    muscles_to_include = None
    nml_doc = None
    
    if generate:
        nml_doc = c302.generate(reference, 
                    params, 
                    cells=cells,
                    cells_to_plot=cells_to_plot, 
                    cells_to_stimulate=cells_to_stimulate, 
                    muscles_to_include = muscles_to_include,
                    duration=duration, 
                    dt=dt, 
                    target_directory=target_directory,
                    param_overrides=param_overrides,
                    verbose=verbose,
                    data_reader=data_reader)
                    
    # Import from libNeuroML      
    from neuroml import SineGenerator, InputList, Input
    import neuroml.writers as writers
    
    # Create the sine wave current generator & add to NeuroML document
    sw_input = SineGenerator(id='NewSineWaveInput', 
                          delay='100ms', 
                          phase='0', 
                          duration='800ms', 
                          amplitude='4.5pA', 
                          period='200ms')
                          
    nml_doc.sine_generators.append(sw_input)
    
    # Which cell to stimulate
    cell = 'AVBL'
    
    # create an InputList and add one Input to that cell
    input_list = InputList(id="Input_%s_%s" % (cell, sw_input.id), component=sw_input.id, populations='%s' % cell)
    input_list.input.append(Input(id=0, target="../%s/0/GenericNeuronCell"%cell, destination="synapses"))
    nml_doc.networks[0].input_lists.append(input_list)

    # Write over network file created already...
    nml_file = target_directory+'/'+reference+'.net.nml'
    writers.NeuroMLWriter.write(nml_doc, nml_file) 
    
    
    c302.print_("(Re)written network file to: "+nml_file)

    return cells, cells_to_stimulate, params, muscles_to_include, nml_doc
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)
