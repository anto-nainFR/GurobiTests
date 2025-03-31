#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctA/alpha_aleatoire/pmed_LP.csv"

source ../../.venv/bin/activate
for instance in `ls ../../instancesSurcharges/alpha_aleatoire/pmed`
do
    echo "pmed alpha_aleatoire $instance"
    python ../../solverGurobi.py ../../instancesSurcharges/alpha_aleatoire/pmed/$instance A "../../resultats/fctA/alpha_aleatoire/pmed_LP.csv" LP
done