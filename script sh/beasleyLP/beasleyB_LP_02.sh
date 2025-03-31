#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctB/alpha0_2/Beasley_LP.csv"


source ../../.venv/bin/activate

for instance in `ls ../../instancesSurcharges/alpha0_2/Beasley`
do
    echo "Beasley alpha0_2 $instance"
    python ../../solverGurobi.py ../../instancesSurcharges/alpha0_2/Beasley/$instance B "../../resultats/fctB/alpha0_2/Beasley_LP.csv" LP
done

