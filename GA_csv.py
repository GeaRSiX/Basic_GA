#!/usr/bin/python

#
# author: Alexander Collins
#

# =======
# imports
# =======
import csv


# =========
# functions
# =========
def init(file_name):
    out_file = open(file_name+'.csv', 'w', newline='')
    out_writer = csv.writer(out_file, delimiter=',', quotechar='|')
    out_writer.writerow(['generation', 'fittest', 'average', 'unfittest'])
    out_file.close()


def write(file_name, data):
    out_file = open(file_name+'.csv', 'a', newline='')
    out_writer = csv.writer(out_file, delimiter=',', quotechar='|')
    out_writer.writerow(data)
    out_file.close()


def get_rows(file_name):
    out_file = open(file_name+'.csv', 'r', newline='')
    out_reader = csv.reader(out_file)
    rows = list(out_reader)
    out_file.close()
    return rows
