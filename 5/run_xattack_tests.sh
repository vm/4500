#!/bin/bash

for directory in ./test/*
do
  for infile in $directory/*-in.json
  do
    echo "Running $infile"
    outfile="${infile/in.json/out.json}"
    outfile_output="$(cat $outfile)"
    xattack_output="$(./xattack < $infile)"

    if [ "$xattack_output" == "$outfile_output" ]; then
        echo 'TEST PASSED'
    else
      echo 'TEST FAILED'
      echo "xattack output: $xattack_output"
      echo "expected output: $outfile_output"
    fi
    echo ""
  done
done
