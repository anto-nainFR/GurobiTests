#!/bin/bash

# Ce script permet de lancer plusieurs instances dans le but de tester l'utilisté de certaines contraintes

dir="instancesSurcharges/alpha0_3/"

# liste des instances à tester
famille=("Aleatoire/" "Beasley/" "GalvaoData/" "Lorena/" "pmed/")

source venv/bin/activate

# pour chaque famille d'instances, nous allons prendre toutes les instances présentes et lancer le programme
for i in "${famille[@]}"
do
    # on va chercher les instances dans le repertoire
    for instance in $(ls $dir$i)
    do
        echo "Lancement de l'instance $instance"
        python solverNuage.py $dir$i$instance
    done
done