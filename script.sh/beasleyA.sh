#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctA/alpha0_1/beasley.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctA/alpha0_2/beasley.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctA/alpha0_3/beasley.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctA/alpha_aleatoire/beasley.csv"

source ../.venv/bin/activate
for instance in `ls ../instancesSurcharges/alpha0_1/Beasley`
do
    echo "Beasley alpha0_1 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_1/Beasley/$instance A "../resultats/fctA/alpha0_1/beasley.csv"
done

for instance in `ls ../instancesSurcharges/alpha0_2/Beasley`
do
    echo "Beasley alpha0_2 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_2/Beasley/$instance A "../resultats/fctA/alpha0_2/beasley.csv"
done


for instance in `ls ../instancesSurcharges/alpha0_3/Beasley`
do
    echo "Beasley alpha0_3 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_3/Beasley/$instance A "../resultats/fctA/alpha0_3/beasley.csv"
done


for instance in `ls ../instancesSurcharges/alpha_aleatoire/Beasley`
do
    echo "Beasley alpha_aleatoire $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha_aleatoire/Beasley/$instance A "../resultats/fctA/alpha_aleatoire/beasley.csv"
done