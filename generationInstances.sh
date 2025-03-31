#!/bin/bash

for i in `ls ./instancesSurcharges/alpha0_1/Beasley`
do
    echo $i
    python instances.py ./instancesSurcharges/alpha0_1/Beasley/$i ./instancesSurcharges/alpha0_1/BeasleyTest/$i
done

for i in `ls ./instancesSurcharges/alpha0_2/Beasley`
do
    echo $i
    python instances.py ./instancesSurcharges/alpha0_2/Beasley/$i ./instancesSurcharges/alpha0_2/BeasleyTest/$i
done

for i in `ls ./instancesSurcharges/alpha0_3/Beasley`
do
    echo $i
    python instances.py ./instancesSurcharges/alpha0_3/Beasley/$i ./instancesSurcharges/alpha0_3/BeasleyTest/$i
done


 