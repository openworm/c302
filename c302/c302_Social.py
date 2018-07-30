
# Model of a decision making circuit

# See https://github.com/openworm/OpenWorm/issues/212

# To run:
#          python c302_Social.py A   (uses parameters_A, requires jNeuroML to run)
# or
#          python c302_Social.py B   (uses parameters_B, requires jNeuroML built from the 
#                                     experimental branches to run: 'python getNeuroML experimental'
#                                     see https://github.com/NeuroML/jNeuroML)

import c302

import neuroml.writers as writers

import sys
    
def setup(parameter_set, 
          generate=False,
          duration=2500, 
          dt=0.05,
          target_directory='examples',
          data_reader="SpreadsheetDataReader",
          param_overrides={},
          config_param_overrides={},
          verbose=True):
    
    exec('from parameters_%s import ParameterisedModel'%parameter_set, globals())
    params = ParameterisedModel()
    
    cells = ["RMGR","ASHR","ASKR","AWBR","IL2R","RMHR","URXR"]
    cells_to_stimulate      = []
    
    reference = "c302_%s_Social"%parameter_set
    
    nml_doc = None
    
    if generate:
        nml_doc = c302.generate(reference, 
                       params, 
                       cells=cells, 
                       cells_to_stimulate=cells_to_stimulate, 
                       duration=duration, 
                       dt=dt, 
                       target_directory=target_directory,
                       param_overrides=param_overrides,
                       verbose=verbose,
                       data_reader=data_reader)
             
    stim_amplitude = "5pA"
    c302.add_new_input(nml_doc, "RMGR", "100ms", "200ms", stim_amplitude, params)
    c302.add_new_input(nml_doc, "ASHR", "400ms", "200ms", stim_amplitude, params)
    c302.add_new_input(nml_doc, "ASKR", "700ms", "200ms", stim_amplitude, params)
    c302.add_new_input(nml_doc, "AWBR", "1000ms", "200ms", stim_amplitude, params)
    c302.add_new_input(nml_doc, "IL2R", "1300ms", "200ms", stim_amplitude, params)
    c302.add_new_input(nml_doc, "RMHR", "1600ms", "200ms", stim_amplitude, params)
    c302.add_new_input(nml_doc, "URXR", "1900ms", "200ms", stim_amplitude, params)
    
    
    nml_file = target_directory+'/'+reference+'.net.nml'
    writers.NeuroMLWriter.write(nml_doc, nml_file) # Write over network file written above...
    
    c302.print_("(Re)written network file to: "+nml_file)
    
    return cells, cells_to_stimulate, params, [], nml_doc
    
    
if __name__ == '__main__':
    
    parameter_set = sys.argv[1] if len(sys.argv)==2 else 'A'
    
    setup(parameter_set, generate=True)