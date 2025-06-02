#!/bin/bash

# instance beasley

dir="instancesSurcharges/alpha0_3/Beasley/"

for instance in $(ls $dir)
do
    python3 solverGurobi.py $dir$instance AB beasley.csv MIP
done