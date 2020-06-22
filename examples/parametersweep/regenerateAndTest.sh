set -e

python GenerateExamples.py -all
python GenerateExamples.py -jnml

python CanonicalCircuit.py 
python CanonicalCircuit.py -jnml

python CanonicalCircuit.py -x
python CanonicalCircuit.py -x -jnml
