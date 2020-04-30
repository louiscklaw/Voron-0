#!/usr/bin/env python3

import os,sys
from pprint import pprint

from multiprocessing.dummy import Pool as ThreadPool

from fabric.api import local, lcd

stl_files = local('find . -name "*stl"|sort', capture=True).split('\n') + local('find . -name "*STL"|sort', capture=True).split('\n')

def get_step_filename(in_stl):
  temp_l = in_stl.split('.')
  temp_l[-1] = 'step'
  return '.'.join(temp_l)

run_input_outputs = list(zip(stl_files,map(lambda x: get_step_filename(x), stl_files)))


def convert(run_config):
  [stl_file, step_file] = run_config
  local('python3 convert_stl_to_step.py "{}" "{}"'.format(stl_file, step_file))

def calculateParallel(numbers, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(convert, numbers)
    pool.close()
    pool.join()
    return results

if __name__ == "__main__":
  calculateParallel(run_input_outputs, 96)
