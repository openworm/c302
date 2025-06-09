#!/bin/bash
set -ex

ruff format *.py
ruff check  *.py

python GenerateExamples.py -all
python GenerateExamples.py -jnml
python GenerateExamples.py -w2d
python GenerateExamples.py -w2d -jnml
python GenerateExamples.py -w2d -jnmlnrn

python CanonicalCircuit.py 
python CanonicalCircuit.py -jnml
python CanonicalCircuit.py -w2d -jnml
python CanonicalCircuit.py -w2d -jnmlnrn

omv all -V 

