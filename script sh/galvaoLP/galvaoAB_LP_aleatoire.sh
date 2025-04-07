#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctAB/alpha_aleatoire/GalvaoData_LP.csv"

source ../../.venv/bin/activate

for instance in `ls ../../instancesSurcharges/alpha_aleatoire/GalvaoData`
do
    echo "GalvaoData alpha_aleatoire $instance"
    python ../../solverGurobi.py ../../instancesSurcharges/alpha_aleatoire/GalvaoData/$instance AB "../../resultats/fctAB/alpha_aleatoire/GalvaoData_LP.csv" LP
done