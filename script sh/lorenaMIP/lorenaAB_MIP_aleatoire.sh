#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "../../resultats/fctAB/alpha_aleatoire/Lorena_MIP.csv"

source ../../.venv/bin/activate

for instance in `ls ../../instancesSurcharges/alpha_aleatoire/Lorena`
do
    echo "Lorena alpha_aleatoire $instance"
    python ../../solverGurobi.py ../../instancesSurcharges/alpha_aleatoire/Lorena/$instance AB "../../resultats/fctAB/alpha_aleatoire/Lorena_MIP.csv" MIP
done