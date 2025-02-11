#!/bin/bash
set -ex

ruff format *.py
ruff check  *.py

python GenerateExamples.py -all
python GenerateExamples.py -jnml
python GenerateExamples.py -x
python GenerateExamples.py -x -jnml
python GenerateExamples.py -x -jnmlnrn

python CanonicalCircuit.py 
python CanonicalCircuit.py -jnml
python CanonicalCircuit.py -x -jnml
python CanonicalCircuit.py -x -jnmlnrn

