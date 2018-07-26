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
    
    params.set_bioparameter("unphysiological_offset_current", "4pA", "Testing Osc", "0")
    params.set_bioparameter("unphysiological_offset_current_del", "100 ms", "Testing Osc", "0")
    params.set_bioparameter("unphysiological_offset_current_dur", "800 ms", "Testing Osc", "0")
    
    #params.set_bioparameter("chem_exc_syn_gbase", ".02 nS", "BlindGuess", "0.1")
    params.set_bioparameter("chem_exc_syn_decay", "5 ms", "BlindGuess", "0.1")
    
    #params.set_bioparameter("chem_inh_syn_gbase", ".02 nS", "BlindGuess", "0.1")
    params.set_bioparameter("chem_inh_syn_decay", "30 ms", "BlindGuess", "0.1")
    params.set_bioparameter("inh_syn_erev", "-90 mV", "BlindGuess", "0.1")
    
    #params.set_bioparameter("elec_syn_gbase", "0.001 nS", "BlindGuess", "0.1")
    
    # Any neurons connected to muscles
    
    cells = ['DB1', 'DB2', 'DB3', 'DB4', 'DB5', 'DB6', 'DB7', 
             'DD1', 'DD2', 'DD3', 'DD4', 'DD5', 'DD6',
             'VB1', 'VB10', 'VB11', 'VB2', 'VB3', 'VB4', 'VB5', 'VB6', 'VB7', 'VB8', 'VB9',
             'VD1', 'VD10', 'VD11', 'VD2', 'VD3', 'VD4', 'VD5', 'VD6', 'VD7', 'VD8', 'VD9']
    
    cells = ['DB3', 'VB3', 'DD3', 'VD3', 'DB4', 'VB4', 'DD4', 'VD4']
    
    cells = ['DB2', 'VB2', 'DD2', 'VD2', 'DB3', 'VB3', 'DD3', 'VD3']
    cells += ['DA2', 'VA2','DA3','VA3']
    #cells = ['DB3', 'VB3', 'DB4', 'VB4']
             
    #cells+=['AVBL','PVCL','AVBR','PVCR']
    #cells+=[]
    #cells+=['PVCL', 'PVCR','AVBL','AVBR']
    #cells+=['PLML', 'PLMR','AVAL','AVAR']
    cells+=['AVBL','AVBR']
    #cells=None  # implies all cells...     
    
    
    #cells_to_stimulate = ['PVCL','PVCR']
    #cells_to_stimulate = ['PLML','PLMR']
    cells_to_stimulate = ['AVBL','AVBR']
    #cells_to_stimulate = ['AVBL']
    
    # Plot some directly stimulated & some not stimulated
    # cells_to_plot      = ['AVBL','PVCL', 'PVCR', 'DB1','DB2','DB3', 'DB4','DD1','DD2','DD3', 'DD4','DB4','VB1','VB2', 'VB3', 'VB4','VD1','VD2', 'VD3', 'VD4']
    cells_to_plot      = cells
    
    reference = "c302_%s_Oscillator"%parameter_set
    
    muscles_to_include = []
    
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

    return cells, cells_to_stimulate, params, muscles_to_include, nml_doc
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)
