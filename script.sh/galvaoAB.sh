#!/bin/bash

echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctAB/alpha0_1/galvao.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctAB/alpha0_2/galvao.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctAB/alpha0_3/galvao.csv"
echo -e "Instances\t nnodes\t p\t strates\t faisabilite\t temps\t fctObj\t As\t Bs\t As+Bs\t noeuds\t borne\t gap\t As_pmedian\t Bs_pmedian\t As+Bs_pmedian" > "../resultats/fctAB/alpha_aleatoire/galvao.csv"

source ../.venv/bin/activate
for instance in `ls ../instancesSurcharges/alpha0_1/GalvaoData`
do
    echo "GalvaoData alpha0_1 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_1/GalvaoData/$instance B "../resultats/fctAB/alpha0_1/galvao.csv"
done

for instance in `ls ../instancesSurcharges/alpha0_2/GalvaoData`
do
    echo "GalvaoData alpha0_2 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_2/GalvaoData/$instance B "../resultats/fctAB/alpha0_2/galvao.csv"
done


for instance in `ls ../instancesSurcharges/alpha0_3/GalvaoData`
do
    echo "GalvaoData alpha0_3 $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha0_3/GalvaoData/$instance B "../resultats/fctAB/alpha0_3/galvao.csv"
done


for instance in `ls ../instancesSurcharges/alpha_aleatoire/GalvaoData`
do
    echo "GalvaoData alpha_aleatoire $instance"
    python ../solverGurobi.py ../instancesSurcharges/alpha_aleatoire/GalvaoData/$instance B "../resultats/fctAB/alpha_aleatoire/galvao.csv"
done