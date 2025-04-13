#!/bin/bash



# tmux new-session -d -s MIPpmed03B './pmedB_MIP_03.sh'

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "resultat_B_MIP_01.csv"

source .venv/bin/activate

python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed12_5.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed21_3.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed21_5.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed22_4.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed22_5.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed23_2.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed23_3.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed23_4.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed23_5.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed25_2.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed25_3.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed26_1.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed26_2.txt B "resultat_B_MIP_01.csv" MIP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed27_1.txt B "resultat_B_MIP_01.csv" MIP

