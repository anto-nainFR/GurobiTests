#!/bin/bash



# tmux new-session -d -s MIPpmed03B './pmedB_MIP_03.sh'

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap" > "resultat_B_LP_02.csv"

source .venv/bin/activate

python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed11_4.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed11_5.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed16_3.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed16_4.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed16_5.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed17_4.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed17_5.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed21_3.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed21_4.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed21_5.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed22_3.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed22_4.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed22_5.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed23_5.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed24_5.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed26_3.txt B "resultat_B_LP_02.csv" LP
python solverGurobi.py ./instancesSurcharges/alpha0_2/pmed/pmed26_5.txt B "resultat_B_LP_02.csv" LP






























