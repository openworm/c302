import c302
import sys
import neuroml.writers as writers
    
def setup(parameter_set, 
          generate=False,
          duration=3000, 
          dt=0.05,
          target_directory='examples',
          data_reader="SpreadsheetDataReader",
          param_overrides={},
          config_param_overrides={},
          verbose=True):

    exec('from parameters_%s import ParameterisedModel'%parameter_set, globals())
    params = ParameterisedModel()
    
    params.set_bioparameter("unphysiological_offset_current", "15pA", "Testing IClamp", "0")
    params.set_bioparameter("unphysiological_offset_current_del", "1 ms", "Testing IClamp", "0")
    params.set_bioparameter("unphysiological_offset_current_dur", "20 ms", "Testing IClamp", "0")
    
    duration = 300
    
    
    my_cells = ["AVKR"]
    my_cells = ["RMHR"]
    muscles_to_include = None 
    
    cells               = my_cells
    
    reference = "c302_%s_TargetMuscle"%parameter_set
    
    nml_doc = None
    
    if generate:
        nml_doc = c302.generate(reference, 
                    params, 
                    cells=cells, 
                    cells_to_stimulate=cells, 
                    muscles_to_include = muscles_to_include,
                    duration=duration, 
                    dt=dt, 
                    target_directory=target_directory,
                    param_overrides=param_overrides,
                    verbose=verbose,
                    data_reader=data_reader,
                    print_connections=True)
                    
                    
    return cells, cells, params, muscles_to_include, nml_doc
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)
