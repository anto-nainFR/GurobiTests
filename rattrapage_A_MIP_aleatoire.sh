#!/bin/bash



# tmux new-session -d -s MIPpmed03B './pmedB_MIP_03.sh'

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "resultat_A_MIP_aleatoire.csv"

source .venv/bin/activate

python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed24_4.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed25_5.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed26_1.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed26_2.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed26_3.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed27_2.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed27_3.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed27_4.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed27_5.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed28_4.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed29_3.txt A "resultat_A_MIP_aleatoire.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed29_5.txt A "resultat_A_MIP_aleatoire.csv" MIP




























