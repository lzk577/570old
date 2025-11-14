#!/bin/bash

for i in {1..15}
do
    in_file="in$i.txt"
    out_file="out$i.txt"
    echo "Processing $in_file -> $out_file"
    python3 efficient_3.py "$in_file" "$out_file"
done
