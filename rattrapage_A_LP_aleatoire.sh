#!/bin/bash



# tmux new-session -d -s MIPpmed03B './pmedB_MIP_03.sh'

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "resultat_A_LP_aleatoire.csv"

source .venv/bin/activate

python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed11_5.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed12_5.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed16_3.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed16_4.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed16_5.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed17_4.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed17_5.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed21_4.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed21_5.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed22_3.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed22_4.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed22_5.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed27_4.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/pmed/pmed27_5.txt A "resultat_A_LP_aleatoire.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha_aleatoire/Beasley/p20_5.txt A "resultat_A_LP_aleatoire.csv" LP

















