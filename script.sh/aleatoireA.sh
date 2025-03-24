#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctA/alpha0_1/aleatoire.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctA/alpha0_2/aleatoire.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctA/alpha0_3/aleatoire.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctA/alpha_aleatoire/aleatoire.csv"

source ../.venv/bin/activate
for instance in `ls ../instancesSurcharges/alpha0_1/Aleatoire`
do
    echo "Aleatoire alpha0_1 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_1/Aleatoire/$instance A "../resultats/fctA/alpha0_1/aleatoire.csv"
done

for instance in `ls ../instancesSurcharges/alpha0_2/Aleatoire`
do
    echo "Aleatoire alpha0_2 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_2/Aleatoire/$instance A "../resultats/fctA/alpha0_2/aleatoire.csv"
done


for instance in `ls ../instancesSurcharges/alpha0_3/Aleatoire`
do
    echo "Aleatoire alpha0_3 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_3/Aleatoire/$instance A "../resultats/fctA/alpha0_3/aleatoire.csv"
done


for instance in `ls ../instancesSurcharges/alpha_aleatoire/Aleatoire`
do
    echo "Aleatoire alpha_aleatoire $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha_aleatoire/Aleatoire/$instance A "../resultats/fctA/alpha_aleatoire/aleatoire.csv"
done