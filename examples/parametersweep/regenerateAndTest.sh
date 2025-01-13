set -ex

python GenerateExamples.py -all
python GenerateExamples.py -jnml
python GenerateExamples.py -x
python GenerateExamples.py -x -jnml

python CanonicalCircuit.py 
python CanonicalCircuit.py -jnml
python CanonicalCircuit.py -x -jnml

