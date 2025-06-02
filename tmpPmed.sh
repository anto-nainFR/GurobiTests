#!/bin/bash

# instance pmed

dir="instancesSurcharges/alpha0_3/pmed/"

for instance in $(ls $dir)
do
    python3 solverGurobi.py $dir$instance AB pmed.csv MIP
done