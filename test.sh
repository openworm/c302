set -ex

ruff format *.py */*.py */*/*.py

pip install .

python -m c302.backers # Generate OW backer info page

##   Test readers

python -m c302.SpreadsheetDataReader 
python -m c302.UpdatedSpreadsheetDataReader                                                                                                                                                                      
python -m c302.UpdatedSpreadsheetDataReader2                                                                                                                                                                  
python -m c302.OpenWormReader 


##   (Re)generate NeuroML 2 & LEMS files from the python scripts

python -m c302.c302_IClamp W2D


python -m c302.c302_IClamp A
python -m c302.c302_Syns A
python -m c302.c302_Social A
python -m c302.c302_Pharyngeal A
python -m c302.c302_Full A
python -m c302.c302_Muscles A
python -m c302.c302_Oscillator A


python -m c302.c302_IClamp B
python -m c302.c302_Syns B
python -m c302.c302_Social B
python -m c302.c302_Pharyngeal B
python -m c302.c302_Full B
python -m c302.c302_Muscles B
python -m c302.c302_Oscillator B


python -m c302.c302_IClamp C
python -m c302.c302_Syns C
python -m c302.c302_Social C
python -m c302.c302_Pharyngeal C
python -m c302.c302_Full C
python -m c302.c302_Muscles C
python -m c302.c302_Oscillator C

python -m c302.c302_IClamp C0
python -m c302.c302_Syns C0
python -m c302.c302_Social C0
python -m c302.c302_Pharyngeal C0
python -m c302.c302_Full C0
python -m c302.c302_Muscles C0
python -m c302.c302_Oscillator C0

python -m c302.c302_IClamp C1
python -m c302.c302_Syns C1
python -m c302.c302_Social C1
python -m c302.c302_Pharyngeal C1
python -m c302.c302_Full C1
python -m c302.c302_Muscles C1
python -m c302.c302_Oscillator C1

python -m c302.c302_IClamp C2
python -m c302.c302_Syns C2
python -m c302.c302_Social C2
python -m c302.c302_Pharyngeal C2
python -m c302.c302_Full C2
python -m c302.c302_Muscles C2
python -m c302.c302_Oscillator C2
python -m c302.c302_FW C2

python -m c302.c302_IClamp D
python -m c302.c302_Syns D
python -m c302.c302_Social D
python -m c302.c302_Pharyngeal D
python -m c302.c302_Full D
python -m c302.c302_Muscles D
python -m c302.c302_Oscillator D

python -m c302.c302_IClamp D1
python -m c302.c302_Syns D1
python -m c302.c302_Social D1
python -m c302.c302_Pharyngeal D1
python -m c302.c302_Full D1
python -m c302.c302_Muscles D1
python -m c302.c302_Oscillator D1

cd examples

## Validate generated NeuroML 2

pynml -validate c302_A_Full.net.nml
pynml -validate c302_A_Pharyngeal.net.nml
pynml -validate c302_A_Syns.net.nml
pynml -validate c302_A_Social.net.nml
pynml -validate c302_A_Muscles.net.nml

# Not validating B files as they use non NeuroML 2 compliant IaFCell model with activity...

pynml -validate c302_C_Full.net.nml
pynml -validate c302_C_Pharyngeal.net.nml

pynml -validate c302_C1_Full.net.nml
pynml -validate c302_C1_Pharyngeal.net.nml

pynml -validate c302_D_Full.net.nml
pynml -validate c302_D_Pharyngeal.net.nml

#pynml -validate c302_D1_Full.net.nml
#pynml -validate c302_D1_Pharyngeal.net.nml


## Try running these in jNeuroML with no GUI

#pynml LEMS_c302_A_Full.xml -nogui    #  Takes 2 mins to run!
pynml LEMS_c302_A_Pharyngeal.xml -nogui
pynml LEMS_c302_A_Syns.xml -nogui
pynml LEMS_c302_A_Social.xml -nogui

#pynml LEMS_c302_B_Full.xml -nogui    #  Takes 2 mins to run!
pynml LEMS_c302_B_Pharyngeal.xml -nogui
pynml LEMS_c302_B_Syns.xml -nogui
pynml LEMS_c302_B_Social.xml -nogui

## Try regenerating using command line options

cd ..

c302 MyNetwork parameters_C -cells ["AVBR","VD3"] -cellstostimulate ["AVBR"] -paramoverride {"unphysiological_offset_current":"2.9pA"} -duration 300

c302 c302_A_Syns2 parameters_A -cells ["ADAL","AIBL","RIVR","RMEV"] -cellstostimulate ["ADAL","RIVR"] -duration 500 -dt 0.1 -vmin -72 -vmax -48

c302 c302_A_Weights parameters_A -cells ["ADAL","AIBL","I1L","I3","DB5","PVCR"] -cellstostimulate ["ADAL","I1L","PVCR"] -connnumberoverride=["I1L-I3":2.5] -connnumberscaling=["PVCR-DB5":5] -duration 500 -dt 0.1 -vmin -72 -vmax -48

c302 c302_C1_Test parameters_C1 -cellstostimulate AFDL -connnumberscaling {"I1L-I3":2}

mkdir -p cells

c302 c302_D1_Weights parameters_D1 -cells ["ADAL","AIBL","I1L","I3","DB5","PVCR"] -cellstostimulate ["ADAL","I1L","PVCR"] -connnumberoverride=["I1L-I3":2.5] -connnumberscaling=["PVCR-DB5":5] -duration 500 -dt 0.1

cd examples

## Try converting some to NEURON

pynml LEMS_c302_A_Full.xml -neuron
pynml LEMS_c302_B_Pharyngeal.xml -neuron
pynml LEMS_c302_C_Syns.xml -neuron
pynml LEMS_c302_W2D_Syns.xml -neuron
nrnivmodl

cd -

## Try NeuroMLlite examples 
cd examples/parametersweep/
./regenerateAndTest.sh 
cd ../..

## Try helper scripts

python -m c302.runAndPlot -test

python -m c302.c302_utils -nogui

echo
echo "  Successfully completed all c302 tests!"
echo
  

