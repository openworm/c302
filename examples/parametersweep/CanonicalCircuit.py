from neuromllite import *
from neuromllite.NetworkGenerator import *
from neuromllite.utils import create_new_model
import sys

sys.path.append("..")

INTERNEURON = 'interneuron'
MOTORNEURON = 'motorneuron'
MUSCLE = 'muscle'


neuron_id = 'GenericNeuronCell'
neuron_nmllite = Cell(id=neuron_id, neuroml2_source_file='%s.cell.nml'%(neuron_id))

muscle_id = 'GenericMuscleCell'
muscle_nmllite = Cell(id=muscle_id, neuroml2_source_file='%s.cell.nml'%(muscle_id))

interneuron_region = RectangularRegion(id='%ss'%INTERNEURON, x=0,y=0,z=0,width=100,height=100,depth=100)
motorneurons_region = RectangularRegion(id='%ss'%MOTORNEURON, x=200,y=0,z=0,width=100,height=100,depth=100)
muscles_region = RectangularRegion(id='%ss'%MUSCLE, x=300,y=0,z=0,width=1000,height=100,depth=1000)

regions = {INTERNEURON:interneuron_region, MOTORNEURON:motorneurons_region, MUSCLE:muscles_region}

colors = {INTERNEURON:'1 0 .4', MOTORNEURON:'.5 .4 1', MUSCLE:'0 0.6 0'}

all_cell_pops = {}

def add_cell(net, name, type):
    
    cell_pop = Population(id=name, 
                          size=1, 
                          component=neuron_nmllite.id, 
                          properties={'color':colors[type]},
                          random_layout = RandomLayout(region=regions[type].id))
                          
    all_cell_pops[name] = cell_pop
    net.populations.append(cell_pop)
    
    
def add_connection(net, pre, post, syn, weight):
    
    net.projections.append(Projection(id='proj_%s_%s'%(pre,post),
                                      presynaptic=pre, 
                                      postsynaptic=post,
                                      synapse=syn.id,
                                      delay=0,
                                      weight=weight,
                                      type='continuousProjection',
                                      random_connectivity=RandomConnectivity(probability=1)))
    

def generate(duration=1000):
    
    #reference = "%s_%s"%(config, cell)
    
    reference = "Canonical_C"  #%(config, cell)
    
    
    net = Network(id=reference)
    net.parameters = {}

    net.cells.append(neuron_nmllite)
    #net.cells.append(muscle_nmllite)


    net.regions.append(interneuron_region)    
    net.regions.append(motorneurons_region)
    net.regions.append(muscles_region)
    
    
    
    add_cell(net, 'AVB', INTERNEURON)
    add_cell(net, 'VB', MOTORNEURON)
    add_cell(net, 'DB', MOTORNEURON)
    add_cell(net, 'VD', MOTORNEURON)
    add_cell(net, 'DD', MOTORNEURON)
    
    
    exc_syn = Synapse(id='neuron_to_neuron_exc_syn', neuroml2_source_file='test_syns.xml')
    net.synapses.append(exc_syn)
    inh_syn = Synapse(id='neuron_to_neuron_inh_syn', neuroml2_source_file='test_syns.xml')
    net.synapses.append(inh_syn)
    
    
    net.parameters['stim_duration'] = '2000ms'
    net.parameters['stim_amp'] = '2.5pA'
    net.parameters['weight_IN_MN'] = 3
    net.parameters['weight_MN_MN_Exc'] = 15
    net.parameters['weight_MN_MN_Inh'] = 35
    
    add_connection(net, 'AVB', 'VB', exc_syn, 'weight_IN_MN')
    add_connection(net, 'AVB', 'DB', exc_syn, 'weight_IN_MN * 0.9')
    add_connection(net, 'DB', 'VD', exc_syn, 'weight_MN_MN_Exc')
    add_connection(net, 'DB', 'DD', exc_syn, 'weight_MN_MN_Exc')
    add_connection(net, 'VB', 'VD', exc_syn, 'weight_MN_MN_Exc')
    add_connection(net, 'VB', 'DD', exc_syn, 'weight_MN_MN_Exc')
    
    add_connection(net, 'VD', 'VB', inh_syn, 'weight_MN_MN_Inh')
    add_connection(net, 'DD', 'DB', inh_syn, 'weight_MN_MN_Inh')


    input_source = InputSource(id='iclamp_0', 
                               neuroml2_input='PulseGenerator', 
                               parameters={'amplitude':'stim_amp', 'delay':'500ms', 'duration':'stim_duration'})
                                   
    net.input_sources.append(input_source)

    net.inputs.append(Input(id='stim',
                            input_source=input_source.id,
                            population='AVB',
                            percentage=100))
                            
    print(net.to_json())
    new_file = net.to_json_file('%s.json'%net.id)
    

    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='Sim%s'%net.id,
                     network=new_file,
                     duration=duration,
                     dt='0.1',
                     recordTraces={'all':'*'})

    sim.to_json_file()
    
    return sim, net



if __name__ == "__main__":
    
    if '-all' in sys.argv:
        for cell in colors:
            generate(cell, 3000, config="IClamp",parameters={'stim_amp':'1pA'})
            
        
    else:
        
        #sim, net = generate('cADpyr229_L23_PC_c292d67a2e_0_0', 3000, config="IClamp")
        
        sim, net = generate(duration=3000)
        
        check_to_generate_or_run(sys.argv, sim)
    
