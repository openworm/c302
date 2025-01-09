set -ex

python GenerateExamples.py -all
python GenerateExamples.py -jnml
python GenerateExamples.py -x -jnml

python CanonicalCircuit.py 
python CanonicalCircuit.py -jnml

