## The c302 modelling framework for *C. elegans*

c302 is a framework for generating network models in NeuroML 2 based on C elegans connectivity data. *Note: the c302 framework has recently moved to this repository from https://github.com/openworm/CElegansNeuroML/tree/master/CElegans/pythonScripts/c302*.

![c302 structure](https://raw.githubusercontent.com/openworm/CElegansNeuroML/master/CElegans/pythonScripts/c302/images/c302.png)

It uses information on the synaptic connectivity of the network (from
[here](https://github.com/openworm/c302/blob/master/c302/data/CElegansNeuronTables.xls)) and uses
[libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) to generate
a network in valid NeuroML, which can be run in [jNeuroML](https://github.com/NeuroML/jNeuroML) or [pyNeuroML](https://github.com/NeuroML/pyNeuroML).


### To install & test

The full set of dependencies for c302 can be installed with the following (see also the [Travis-CI script](https://github.com/openworm/c302/blob/master/.travis.yml)):

    git clone https://github.com/openworm/c302.git
    cd c302
    python setup.py install

This will install c302 as well as all dependencies, including [pyNeuroML](https://github.com/NeuroML/pyNeuroML) 
and [PyOpenWorm](https://github.com/openworm/PyOpenWorm).


#### Quick test

To ensure everything is set up correctly try:

1) Regenerate the NeuroML & LEMS files for one instance of the model:

       python c302/c302_Pharyngeal.py B  # generate pharyngeal network (see fig. above) using parameter set B

2) Run a simulation with pyNeuroML:

       pynml examples/LEMS_c302_B_Pharyngeal.xml      

To test all of the working features of the framework run [test.sh](https://raw.githubusercontent.com/openworm/CElegansNeuroML/master/CElegans/pythonScripts/c302/test.sh):

     ./test.sh  # or ./test3.sh if you use Python 3


### Usage Examples

#### 1a) Run standard examples with pyNeuroML

There are a number of [example models](https://github.com/openworm/c302/tree/master/examples) included with the standard distribution. 
These consist of: A) generated NeuroML 2 network description file ([example](https://github.com/openworm/c302/blob/master/examples/c302_A_IClamp.net.nml)), 
containing the definitions of the cells to use (e.g. **iafCell** for an integrate and fire cell), any inputs (e.g. **pulseGenerator**) as well as the 
**populations**, **projections** and **inputLists** contained within the **network** (for a full description of the NeuroML elements see 
[here](https://www.neuroml.org/NeuroML2CoreTypes/Networks.html)); and B) a LEMS simulation file 
([example](https://github.com/openworm/c302/blob/master/examples/LEMS_c302_A_IClamp.xml)) describing how long to simulate, the timestep and what to plot/record.

       # generate 2 neurons & 1 muscle with current inputs using parameter set A
       pynml examples/LEMS_c302_A_IClamp.xml      

       # generate full scale network using parameter set C
       pynml examples/LEMS_c302_C_Full.xml    

       # generate pharyngeal network using parameter set B
       pynml examples/LEMS_c302_B_Pharyngeal.xml

Screenshots of a simulation with pyNeuroML of c302_B_Pharyngeal are shown below (left: 
membrane potential of 20 cells, right: "activity" of 20 cells - a value from 0-1 
showing time smoothed activity of each cell):

![c302_B_Pharyngeal](images/c302_B_Pharyngeal.png)

#### 1b) Run standard examples with Neuron

The models can also be run using the Neuron simulator. This should be installed as outlined [here](https://www.neuron.yale.edu/neuron/download). 

       cd examples
       pynml LEMS_c302_A_IClamp.xml -neuron   # Generate the Neuron files (Python/hoc/mod)
       nrnivmodl                              # Compile the mod files (used for cell/ion channel definitions)
       nrngui LEMS_c302_A_IClamp_nrn.py       # Run the main Python file for the simulation using Neuron

Note: models with the D parameter set can only be run using Neuron (not pyNeuroML), simnce they consist of multicompartmental Neurons, e.g.

       pynml LEMS_c302_D_Pharyngeal.xml -neuron  
       nrnivmodl                         
       nrngui LEMS_c302_D_Pharyngeal_nrn.py

This produces the following (graph on top is [Ca2+], bottom is membrane potential; 3D view on right can be produced by selecting in the Neuron main menu: Graph -> Shape plot)

![Neuron](images/Neuron.png)


#### 2) Use command line interface to create new network

The **c302** command line utility can be used to generate customised networks of varying size, with different cells stimulated, of varying duration from the command line:

    c302 MyNetwork parameters_C -cells ["AVBR","VD3"] -cellstostimulate ["AVBR"] -paramoverride {"unphysiological_offset_current":"2.9pA"} -duration 300

This will create a NeuroML 2 file and a LEMS file to execute it, containing 2 cells, stimulating 1 of them, and with a duration of 300 ms. It can be run with:

    pynml LEMS_MyNetwork.xml 

To see the structure of the network, use pyNeuroML:

    pynml MyNetwork.net.nml -graph 4c  # Try other options like 1, 2f, 5c for varying levels of detail


![MyNetwork](images/MyNetwork.png)


More options for using the **c302** command can be found with

    c302 -h


#### 3) Change parameters in a file

To investigate how the behaviour of a model changes when parameters are varied, it is possible to change the parameters in the parameters_X.py files and regenerate.

For example in [parameters_C.py](https://github.com/openworm/c302/blob/master/c302/parameters_C.py) there are lists of parameters like:

        self.add_bioparameter("muscle_leak_cond_density", "5e-7 S_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("neuron_leak_cond_density", "0.005 mS_per_cm2", "BlindGuess", "0.1")
        self.add_bioparameter("leak_erev", "-50 mV", "BlindGuess", "0.1")

To change the model behaviour alter one of these values, e.g. 

        self.add_bioparameter("neuron_leak_cond_density", "0.02 mS_per_cm2", "BlindGuess", "0.1")

and look at the behaviour afterwards (note the package needs to be reinstalled)

        sudo python setup.py install           # reinstall package after change
        python c302/c302_IClamp.py C           # regenerate c302_C_IClamp
        pynml examples/LEMS_c302_C_IClamp.xml  # run simulation

The plots below show the neuron's membrane potential on application of 6 increasing pulses of current before (left) and after (right) the change, indicating how increasing the leak conductance removes the spiking:

<p><img src="images/changePre.png" width=400/> <img src="images/changePost.png" width=400/></p>
    

### Comparing activity across scales/parameter sets

<a href="https://github.com/openworm/c302/blob/master/examples/summary/README.md"><img src="https://raw.githubusercontent.com/openworm/c302/master/images/activity.png" alt="activity"  height="250"/></a>

See [here](https://github.com/openworm/c302/blob/master/examples/summary/README.md) for more details on this.

### Background info: Understanding how c302_Full.py works

<a href="https://docs.google.com/drawings/d/1urLRCe--ymaFTevRWp-etS06E9Rl82b627lC4RmUumI/edit?usp=sharing"><img src="https://docs.google.com/drawings/d/1urLRCe--ymaFTevRWp-etS06E9Rl82b627lC4RmUumI/pub?w=1307&amp;h=712"></a>


[![Build Status](https://travis-ci.org/openworm/c302.svg?branch=master)](https://travis-ci.org/openworm/c302)
