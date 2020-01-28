from neuromllite import *
from neuromllite.NetworkGenerator import *
from neuromllite.utils import create_new_model
import sys

sys.path.append("..")


colors = {'GenericNeuronCell':'0 0 0.8', 'GenericMuscleCell':'0.8 0 0'}

def generate(duration=1000):
    
    #reference = "%s_%s"%(config, cell)
    
    reference = "Canonical_C"  #%(config, cell)
    
    
    net = Network(id=reference)
    net.parameters = {}

    neuron_id = 'GenericNeuronCell'
    neuron_nmllite = Cell(id=neuron_id, neuroml2_source_file='%s.cell.nml'%(neuron_id))
    net.cells.append(neuron_nmllite)
    muscle_id = 'GenericMuscleCell'
    muscle_nmllite = Cell(id=muscle_id, neuroml2_source_file='%s.cell.nml'%(muscle_id))
    #net.cells.append(muscle_nmllite)

    interneurons = RectangularRegion(id='interneurons', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    net.regions.append(interneurons)
    
    motorneurons = RectangularRegion(id='motorneurons', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    net.regions.append(motorneurons)
    
    muscles = RectangularRegion(id='muscles', x=0,y=0,z=0,width=1000,height=100,depth=1000)
    #net.regions.append(muscles)
    
    
    avb = Population(id='AVB', size=1, component=neuron_nmllite.id, properties={'color':colors[neuron_nmllite.id]},random_layout = RandomLayout(region=interneurons.id))
    net.populations.append(avb)
    
    vb = Population(id='VB', size=1, component=neuron_nmllite.id, properties={'color':colors[neuron_nmllite.id]},random_layout = RandomLayout(region=motorneurons.id))
    net.populations.append(vb)
    
    
    exc_syn = Synapse(id='neuron_to_neuron_exc_syn', neuroml2_source_file='test_syns.xml')
    net.synapses.append(exc_syn)
    net.parameters['weight_in_mn'] = 1
    

    net.projections.append(Projection(id='proj0',
                                      presynaptic=avb.id, 
                                      postsynaptic=vb.id,
                                      synapse=exc_syn.id,
                                      delay=0,
                                      weight='weight_in_mn',
                                      type='continuousProjection'))
    net.projections[0].random_connectivity=RandomConnectivity(probability=1)
    

    net.parameters['stim_amp'] = '350pA'

    input_source = InputSource(id='iclamp_0', 
                               neuroml2_input='PulseGenerator', 
                               parameters={'amplitude':'stim_amp', 'delay':'500ms', 'duration':'2000ms'})
                                   
    net.input_sources.append(input_source)

    net.inputs.append(Input(id='stim',
                            input_source=input_source.id,
                            population=avb.id,
                            percentage=100))
                            
    print(net.to_json())
    new_file = net.to_json_file('%s.json'%net.id)
    

    ################################################################################
    ###   Build Simulation object & save as JSON

    sim = Simulation(id='Sim%s'%net.id,
                     network=new_file,
                     duration=duration,
                     dt='0.01',
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
    
