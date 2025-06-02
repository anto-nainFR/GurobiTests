#!/bin/bash

# instance aleatoire

dir="instancesSurcharges/alpha0_3/Aleatoire/"

for instance in $(ls $dir)
do
    python3 solverGurobi.py $dir$instance AB alea.csv MIP
done