#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctAB/alpha0_2/GalvaoData_LP.csv"


source ../../.venv/bin/activate
for instance in `ls ../../instancesSurcharges/alpha0_2/GalvaoData`
do
    echo "GalvaoData alpha0_2 $instance"
    python ../../solverGurobi.py ../../instancesSurcharges/alpha0_2/GalvaoData/$instance AB "../../resultats/fctAB/alpha0_2/GalvaoData_LP.csv" LP
done

