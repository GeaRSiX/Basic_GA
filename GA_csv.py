#!/usr/bin/python

#
# author: Alexander Collins
#

# =======
# imports
# =======
import os
import csv

# =======
# globals
# =======

# =========
# functions
# =========
def init(file_name):
  global out_file
  global out_writer
  
  out_file = open(file_name, 'w', newline='')
  out_writer = csv.writer(out_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  out_writer.writerow(['generation', 'fittest', 'average', 'unfittest'])

  
def write(generation, data):
  # write csv data
  out_writer.writerow([generation, data[0], data[1], data[2]])

  
def close():
  out_file.close()
  