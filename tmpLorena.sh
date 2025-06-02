#!/bin/bash

# instance lorena

dir="instancesSurcharges/alpha0_3/Lorena/"

for instance in $(ls $dir)
do
    python3 solverGurobi.py $dir$instance AB lorena.csv MIP
done