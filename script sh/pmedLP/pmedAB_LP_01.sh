#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctAB/alpha0_1/pmed_LP.csv"

source ../../.venv/bin/activate
for instance in `ls ../../instancesSurcharges/alpha0_1/pmed`
do
    echo "pmed alpha0_1 $instance"
    python ../../solverGurobi.py ../../instancesSurcharges/alpha0_1/pmed/$instance AB "../../resultats/fctAB/alpha0_1/pmed_LP.csv" LP
done
