#!/bin/bash



# tmux new-session -d -s MIPpmed03B './pmedB_MIP_03.sh'

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "resultat_A_LP_01.csv"

source .venv/bin/activate

python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed11_4.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed13_5.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed16_3.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed16_4.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed16_5.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed17_4.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed17_5.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed21_4.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed21_5.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed22_5.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed23_1.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed23_5.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed26_3.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed27_4.txt A "resultat_A_LP_01.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_1/pmed/pmed27_5.txt A "resultat_A_LP_01.csv" LP































