#!/bin/bash



# tmux new-session -d -s MIPpmed03B './pmedB_MIP_03.sh'

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "resultat_LP_aleatoire.csv"

source .venv/bin/activate

python solverGurobi.py ./instancesSurcharges/alpha0_3/pmed/pmed16_4.txt A "resultat_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_3/pmed/pmed16_5.txt A "resultat_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_3/pmed/pmed17_4.txt A "resultat_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_3/pmed/pmed17_5.txt A "resultat_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_3/pmed/pmed21_4.txt A "resultat_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_3/pmed/pmed21_5.txt A "resultat_LP_aleatoire.csv" LP






















