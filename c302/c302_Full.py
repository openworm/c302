import c302
import sys

def setup(parameter_set, 
          generate=False,
          duration=1000, 
          dt=0.05,
          target_directory='examples',
          muscles_to_include = None, # None => All!
          data_reader="SpreadsheetDataReader",
          param_overrides={},
          config_param_overrides={},
          verbose=True):
    
    exec('from parameters_%s import ParameterisedModel'%parameter_set, globals())
    params = ParameterisedModel()
    
    # Some random set of neurons
    cells_to_stimulate = ["ADAL", "ADAR", "M1","M2L","M3L","M3R","M4","I1R","I2L","I5","I6","MI","NSMR","MCL","ASEL", "AVEL", "AWAR", "DB1", "DVC", "RIAR", "RMDDL"]
    cells_to_stimulate = ['PVCL','PVCR']
    cells_to_stimulate = ['PLML','PLMR']
    #cells_to_stimulate = ['AVBL','AVBR']
    
    # Plot some directly stimulated & some not stimulated
    cells_to_plot      = ["ADAL", "ADAR", "PVDR", "BDUR","I1R","I2L"]
    cells_to_plot      = ['AVBL','AVBR','PVCL', 'PVCR', 'DB1','DB2','VB1','VB2','DD1','DD2','VD1','VD2']
    
    params.set_bioparameter("unphysiological_offset_current", "5pA", "Testing Full net", "0")
    params.set_bioparameter("unphysiological_offset_current_del", "50 ms", "Testing Full net", "0")
    params.set_bioparameter("unphysiological_offset_current_dur", "900 ms", "Testing Full net", "0")
    
    reference = "c302_%s_Full"%parameter_set
    
    cell_names, conns = c302.get_cell_names_and_connection()
    
    nml_doc = None
    
    if generate:
        nml_doc = c302.generate(reference, 
             params, 
             cells_to_plot=cells_to_plot, 
             cells_to_stimulate=cells_to_stimulate, 
             muscles_to_include = muscles_to_include,
             duration=duration, 
             dt=dt, 
             vmin=-72 if parameter_set=='A' else -52, 
             vmax=-48 if parameter_set=='A' else -28,
             target_directory=target_directory,
             param_overrides=param_overrides,
             verbose=verbose,
             data_reader=data_reader)
             
    return cell_names, cells_to_stimulate, params, muscles_to_include, nml_doc


if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)
