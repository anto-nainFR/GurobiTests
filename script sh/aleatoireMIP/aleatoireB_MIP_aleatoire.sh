#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctB/alpha_aleatoire/aleatoire_MIP.csv"

source ../../.venv/bin/activate

for instance in `ls ../../instancesSurcharges/alpha_aleatoire/Aleatoire`
do
    echo "Aleatoire alpha_aleatoire $instance"
    python ../../solverGurobi.py ../../instancesSurcharges/alpha_aleatoire/Aleatoire/$instance B "../../resultats/fctB/alpha_aleatoire/aleatoire_MIP.csv" MIP
done