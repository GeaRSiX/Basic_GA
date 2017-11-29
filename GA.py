#!/usr/bin/python
#
# author: Alexander Collins
#

# =======
# imports
# =======
import os
import GA_csv
import GA_data2_wildcard as GA


# =========
# functions
# =========
SAMPLE_NAME = "results/GA_data2_wildcard_more_mr"
SAMPLE_SIZE = 10


# =========
# functions
# =========
def main():
    # run algorithm & write results to csv
    for s in range(SAMPLE_SIZE):
        GA.main(SAMPLE_NAME + str(s))
    # init averages samples csv file
    GA_csv.init(SAMPLE_NAME)
    # create averaged results csv from samples
    average_samples()
    # cleanup sample files
    for s in range(SAMPLE_SIZE):
        os.remove(SAMPLE_NAME + str(s) + '.csv')


def average_samples():
    # get all csv data for each sample
    rows = []
    for s in range(SAMPLE_SIZE):
        rows.append(GA_csv.get_rows(SAMPLE_NAME+str(s)))
    
    # average out & write data to csv
    for r in range(1, len(rows[0])-1):
        # get averaged data in row r
        fittest = 0
        average = 0
        unfittest = 0
        for s in range(SAMPLE_SIZE):
            fittest += int(rows[s][r][1])
            average += int(rows[s][r][2])
            unfittest += int(rows[s][r][3])
        fittest = int(fittest / SAMPLE_SIZE)
        average = int(average / SAMPLE_SIZE)
        unfittest = int(unfittest / SAMPLE_SIZE)
        
        GA_csv.write(SAMPLE_NAME, [r, fittest, average, unfittest])

        
# ============
# entry points
# ============
if __name__ == '__main__':
    main()
