import c302
import sys
import neuroml.writers as writers
    
def setup(parameter_set, 
          generate=False,
          duration=2000, 
          dt=0.05,
          target_directory='examples',
          data_reader="SpreadsheetDataReader",
          param_overrides={},
          verbose=True):

    exec('from parameters_%s import ParameterisedModel'%parameter_set, globals())
    params = ParameterisedModel()
    
    
    
    my_cells = []
    muscles_to_include = ['MDR01']
    
    cells               = my_cells
    cells_total  = my_cells + muscles_to_include
    
    reference = "c302_%s_IClampMuscle"%parameter_set
    nml_doc = None
    
    
    if generate:
        nml_doc = c302.generate(reference, 
                    params, 
                    cells=cells, 
                    cells_to_stimulate=muscles_to_include, 
                    muscles_to_include = muscles_to_include,
                    duration=duration, 
                    dt=dt, 
                    target_directory=target_directory,
                    param_overrides=param_overrides,
                    verbose=verbose,
                    data_reader=data_reader)
                    
    
                    
    return cells, cells_total, params, muscles_to_include, nml_doc
             
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)
