#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctB/alpha0_3/GalvaoData_MIP.csv"

source ../../.venv/bin/activate


for instance in `ls ../../instancesSurcharges/alpha0_3/GalvaoData`
do
    echo "GalvaoData alpha0_3 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_3/GalvaoData/$instance B "../../resultats/fctB/alpha0_3/GalvaoData_MIP.csv" MIP
done

