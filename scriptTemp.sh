#!/bin/bash

famille=("alea" "beasley" "galvao" "lorena" "pmed")



for i in "${famille[@]}"
do
    for instance in $(ls $i)
    do
        output="CSV_$i.csv"
        echo -n -e "$instance\t" >> "$output"
        # cat $i/$instance | grep "valeur objective" | cut -d ' ' -f 4
        grep "valeur objective" "$i/$instance" | awk '{printf "%s\t", $4}' >> "$output"

        echo "" >> "$output"
    done
done