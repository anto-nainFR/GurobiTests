#!/bin/bash


echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctB/alpha0_1/pmed.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctB/alpha0_2/pmed.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctB/alpha0_3/pmed.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctB/alpha_aleatoire/pmed.csv"

source ../.venv/bin/activate
for instance in `ls ../instancesSurcharges/alpha0_1/pmed`
do
    echo "pmed alpha0_1 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_1/pmed/$instance B "../resultats/fctB/alpha0_1/pmed.csv"
done


for instance in `ls ../instancesSurcharges/alpha0_2/pmed`
do
    echo "pmed alpha0_2 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_2/pmed/$instance B "../resultats/fctB/alpha0_2/pmed.csv"
done


for instance in `ls ../instancesSurcharges/alpha0_3/pmed`
do
    echo "pmed alpha0_3 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_3/pmed/$instance B "../resultats/fctB/alpha0_3/pmed.csv"
done


for instance in `ls ../instancesSurcharges/alpha_aleatoire/pmed`
do
    echo "pmed alpha_aleatoire $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha_aleatoire/pmed/$instance B "../resultats/fctB/alpha_aleatoire/pmed.csv"
done