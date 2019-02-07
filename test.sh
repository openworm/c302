set -e

##   Install

python setup.py install

##   Test readers

python c302/SpreadsheetDataReader.py 
python c302/UpdatedSpreadsheetDataReader.py                                                                                                                                                                      
python c302/UpdatedSpreadsheetDataReader2.py                                                                                                                                                                  
python c302/OpenWormReader.py 


##   (Re)generate NeuroML 2 & LEMS files from the python scripts

python c302/c302_IClamp.py A
python c302/c302_Syns.py A
python c302/c302_Social.py A
python c302/c302_Pharyngeal.py A
python c302/c302_Full.py A
python c302/c302_Muscles.py A
python c302/c302_Oscillator.py A


python c302/c302_IClamp.py B
python c302/c302_Syns.py B
python c302/c302_Social.py B
python c302/c302_Pharyngeal.py B
python c302/c302_Full.py B
python c302/c302_Muscles.py B
python c302/c302_Oscillator.py B


python c302/c302_IClamp.py C
python c302/c302_Syns.py C
python c302/c302_Social.py C
python c302/c302_Pharyngeal.py C
python c302/c302_Full.py C
python c302/c302_Muscles.py C
python c302/c302_Oscillator.py C

python c302/c302_IClamp.py C0
python c302/c302_Syns.py C0
python c302/c302_Social.py C0
python c302/c302_Pharyngeal.py C0
python c302/c302_Full.py C0
python c302/c302_Muscles.py C0
python c302/c302_Oscillator.py C0

python c302/c302_IClamp.py C1
python c302/c302_Syns.py C1
python c302/c302_Social.py C1
python c302/c302_Pharyngeal.py C1
python c302/c302_Full.py C1
python c302/c302_Muscles.py C1
python c302/c302_Oscillator.py C1

python c302/c302_IClamp.py C2
python c302/c302_Syns.py C2
python c302/c302_Social.py C2
python c302/c302_Pharyngeal.py C2
python c302/c302_Full.py C2
python c302/c302_Muscles.py C2
python c302/c302_Oscillator.py C2
python c302/c302_FW.py C2

python c302/c302_IClamp.py D
python c302/c302_Syns.py D
python c302/c302_Social.py D
python c302/c302_Pharyngeal.py D
python c302/c302_Full.py D
python c302/c302_Muscles.py D
python c302/c302_Oscillator.py D

python c302/c302_IClamp.py D1
python c302/c302_Syns.py D1
python c302/c302_Social.py D1
python c302/c302_Pharyngeal.py D1
python c302/c302_Full.py D1
python c302/c302_Muscles.py D1
python c302/c302_Oscillator.py D1

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

python  c302/__init__.py c302_A_Syns2 parameters_A -cells ["ADAL","AIBL","RIVR","RMEV"] -cellstostimulate ["ADAL","RIVR"] -duration 500 -dt 0.1 -vmin -72 -vmax -48

python  c302/__init__.py c302_A_Weights parameters_A -cells ["ADAL","AIBL","I1L","I3","DB5","PVCR"] -cellstostimulate ["ADAL","I1L","PVCR"] -connnumberoverride=["I1L-I3":2.5] -connnumberscaling=["PVCR-DB5":5] -duration 500 -dt 0.1 -vmin -72 -vmax -48

python  c302/__init__.py c302_C1_Test parameters_C1 -cellstostimulate AFDL -connnumberscaling {"I1L-I3":2}

mkdir -p cells

python  c302/__init__.py c302_D1_Weights parameters_D1 -cells ["ADAL","AIBL","I1L","I3","DB5","PVCR"] -cellstostimulate ["ADAL","I1L","PVCR"] -connnumberoverride=["I1L-I3":2.5] -connnumberscaling=["PVCR-DB5":5] -duration 500 -dt 0.1

cd examples

## Try converting some to NEURON

pynml LEMS_c302_A_Full.xml -neuron
pynml LEMS_c302_B_Pharyngeal.xml -neuron
pynml LEMS_c302_C_Syns.xml -neuron
nrnivmodl

cd -

## Try helper scripts

python c302/runAndPlot.py -test

python c302/c302_utils.py -nogui

echo
echo "  Successfully completed all c302 tests!"
echo
  

