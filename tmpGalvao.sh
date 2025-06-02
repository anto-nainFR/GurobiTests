#!/bin/bash

# instance Galvao

dir="instancesSurcharges/alpha0_3/GalvaoData/"

for instance in $(ls $dir)
do
    python3 solverGurobi.py $dir$instance AB galvao.csv MIP
done