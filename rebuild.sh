#!/usr/bin/env bash

set -ex

echo 'start'

for i in $(find . -name '*.stl'); do
  echo $i;
done

# python3 convert_stl_to_step.py /home/logic/_workspace/freecad-playlist/test.stl /home/logic/result.step

echo 'done'