# c302

*The c302 framework is in the process of moving here from https://github.com/openworm/CElegansNeuroML/tree/master/CElegans/pythonScripts/c302*

c302 is a framework for generating network models in NeuroML 2 based on C elegans connectivity data.

![c302 structure](https://raw.githubusercontent.com/openworm/CElegansNeuroML/master/CElegans/pythonScripts/c302/images/c302.png)

It uses information on the synaptic connectivity of the network (from
[here](https://github.com/openworm/c302/blob/master/c302/data/CElegansNeuronTables.xls)) and uses
[libNeuroML](https://github.com/NeuralEnsemble/libNeuroML) to generate
a network in valid NeuroML, which can be run in [jNeuroML](https://github.com/NeuroML/jNeuroML) or [pyNeuroML](https://github.com/NeuroML/pyNeuroML).


### To install & test

The full set of dependencies for c302 can be installed with the following (see also the [Travis-CI script](https://github.com/openworm/c302/blob/master/.travis.yml)):

    python setup.py install

To regenerate a set of NeuroML & LEMS files for one instance of the model and execute it:

    python c302/c302_Full.py                         # To regenerate the NeuroML & LEMS files
    pynml examples/LEMS_c302_A_Full.xml         # Run a simulation with jNeuroML via pyNeuroML

To test all of the working features of the framework run [test.sh](https://raw.githubusercontent.com/openworm/CElegansNeuroML/master/CElegans/pythonScripts/c302/test.sh):

    ./test.sh

### Command line interface

This package can be used to generate customised networks of varying size, with different cells stimulated, of varying duration from the command line:

    ./c302/c302.py MyNetwork parameters_A -cells ["ADAL","AIBL","RIVR","RMEV"] -cellstostimulate ["ADAL","RIVR"] -duration 500

This will create a NeuroML 2 file and a LEMS file to execute it, containing 4 cells, stimulating 2 of them, and with a duration of 500 ms

More options can be found with

    ./c302.py -h

### Mapping to NEURON

Due to the fact that the cells are in pure NeuroML2, they can be mapped to other formats using the export feature of jNeuroML. [Install NEURON](http://www.neuron.yale.edu/neuron/download) and map the network to this format using:

    cd examples
    
for jNeuroML:

    jnml LEMS_c302_A_Pharyngeal.xml -neuron
    
or instead for pyNeuroML:    

    pynml LEMS_c302_A_Pharyngeal.xml -neuron
    
then

    nrnivmodl
    nrngui -python LEMS_c302_A_Pharyngeal_nrn.py


### Understanding how c302_Full.py works

<a href="https://docs.google.com/drawings/d/1urLRCe--ymaFTevRWp-etS06E9Rl82b627lC4RmUumI/edit?usp=sharing"><img src="https://docs.google.com/drawings/d/1urLRCe--ymaFTevRWp-etS06E9Rl82b627lC4RmUumI/pub?w=1307&amp;h=712"></a>


[![Build Status](https://travis-ci.org/openworm/c302.svg?branch=master)](https://travis-ci.org/openworm/c302)
