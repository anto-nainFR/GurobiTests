#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctA/alpha0_1/aleatoire_MIP.csv"

source ../../.venv/bin/activate
for instance in `ls ../../instancesSurcharges/alpha0_1/Aleatoire`
do
    echo "Aleatoire alpha0_1 $instance"
    python ../../solverGurobi.py ../../instancesSurcharges/alpha0_1/Aleatoire/$instance A "../../resultats/fctA/alpha0_1/aleatoire_MIP.csv" MIP
done