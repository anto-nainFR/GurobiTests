#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctAB/alpha0_1/lorena.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctAB/alpha0_2/lorena.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctAB/alpha0_3/lorena.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctAB/alpha_aleatoire/lorena.csv"

source ../.venv/bin/activate
for instance in `ls ../instancesSurcharges/alpha0_1/Lorena`
do
    echo "Lorena alpha0_1 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_1/Lorena/$instance AB "../resultats/fctAB/alpha0_1/lorena.csv"
done


for instance in `ls ../instancesSurcharges/alpha0_2/Lorena`
do
    echo "Lorena alpha0_2 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_2/Lorena/$instance AB "../resultats/fctAB/alpha0_2/lorena.csv"
done


for instance in `ls ../instancesSurcharges/alpha0_3/Lorena`
do
    echo "Lorena alpha0_3 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_3/Lorena/$instance AB "../resultats/fctAB/alpha0_3/lorena.csv"
done


for instance in `ls ../instancesSurcharges/alpha_aleatoire/Lorena`
do
    echo "Lorena alpha_aleatoire $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha_aleatoire/Lorena/$instance AB "../resultats/fctAB/alpha_aleatoire/lorena.csv"
done