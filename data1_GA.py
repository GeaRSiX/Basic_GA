#!/usr/bin/python

#
# author: Alexander Collins
# note:
#   This file is almost exactly the same as binary_GA,
#   the reason i've re-added all the re-used functions
#   is so the other data GA files don't get a mixed up
#   Solution() class returned.
#


# =======
# imports
# =======
import time
import random


# =======
# globals
# =======
# data set variables
data_file = "data_sets/data1.txt"
data_R_count = 32   # number of rows within data
data_c_size = 5     # size of variables within data
# genetic algorithm variables
c_size = data_c_size            # size of Rule's condition
#R_count = 10 #getting started  # number of rules per individual
R_count = 32
generation_limit = 1000
#P_size = 10  #getting started
P_size = 400                     # size of population (of Solutions)
G_size = (c_size + 1) * R_count # size of Solution's genome (+ 1 for output)
C_rate = 0.9                      # crossover rate (0.0 to 1.0)  # NOTE: "typically 0.6 to 0.9"
M_rate = 1 / P_size             # mutation rate (0.0 to 1.0)   # NOTE: 1 / P_size or 1 / G_size


# =======
# classes
# =======
class Rule:
  def __init__(self):
    self.condition = []
    self.output = -1
    
  def __str__(self):
    return str(self.condition) + "\t" + str(self.output)
  
  def condition_matches(self, target):
    matching = 0
    
    for i, c in enumerate(self.condition):
      if c == 2 or c == int(target[i]):
        matching += 1
        
    return matching == data_c_size


class Solution():
  def __init__(self, genome):
    self.genome = genome	
    self.fitness = -1
    self.rules = []

  def __str__(self):
    return str(self.genome) + ' = ' + str(self.fitness)
    
  def build_rules(self):
    self.rules = []
    g = 0
    
    for r in range(R_count):
      rule = Rule()
      
      for c in range(c_size):
        rule.condition.append(self.genome[g])
        g += 1
      
      rule.output = self.genome[g]
      g += 1
      
      self.rules.append(rule)


# =========
# functions
# =========
def fitness(individual):
  individual.fitness = 0
  individual.build_rules()
  
  data = open(data_file)
  # loop through each rule in data_file
  for r in range(data_R_count):
    data_rule = data.readline()
    # loop through & compare each rule in individual.rules
    for rule in individual.rules:
      if rule.condition_matches(data_rule[:data_c_size]):
        if rule.output == int(data_rule[data_c_size + 1]):
          individual.fitness += 1
        break
          
  return individual.fitness


def eval(population):
  fittest = 0

  for i in population:
      if fitness(i) > fittest:
          fittest = i.fitness
      
  return fittest


def termination_criteria(generation, population):
  if eval(population) == R_count or generation == generation_limit:
    return True
  else:
    return False


def debug_print(generation, population, genome_size):
  unfittest = genome_size
  fittest = 0
  overall = 0
  
  for i in population:
    if i.fitness < unfittest:
      unfittest = i.fitness
    if i.fitness > fittest:
      fittest = i.fitness
    overall += i.fitness
  average = int(overall / len(population))

  print("GENERATION "+str(generation))
  print("Unfittest:\t" + str(unfittest))
  print("Average:\t" + str(average))
  print("Fittest:\t" + str(fittest) + "/" + str(R_count))
  print("Overall:\t" + str(overall) + "/" + str(len(population) * R_count))
  print("-------------------------")

  
def main(generation_limit, P_size, G_size, C_rate, M_rate):
  # initialisation
  random.seed(time.time())
  generation = 0
  population = init(P_size, G_size)
  # main loop
  while termination_criteria(generation, population) is False:
    debug_print(generation, population, G_size)
    parents = tournament_selection(population, 2)
    offspring = single_crossover(parents, C_rate, G_size)
    offspring = mutate(offspring, M_rate)
    population = elitism(population, offspring)
    generation += 1
  debug_print(generation, population, G_size)
  
def init(population_size, genome_size):
  population = []

  for p in range(population_size):
    genome = [random.randint(0, 1) for g in range(genome_size)]
    population.append(Solution(genome))

  return population


def tournament_selection(population, p_count):
  parents = []
  
  for i in population:
      # select candidates
      candidates = [random.choice(population) for p in range(p_count)]
      # tournament
      fittest = candidates[0]
      for c in candidates:
          if c.fitness > fittest.fitness:
              fittest = c
      # add fittest candidate as parent
      parents.append(fittest)

  return parents

  
def roulette_selection(population):
  parents = []
  
  # roulette
  for i in population:
      # get total population fitness
      overall = 0
      for i in population:
          overall += i.fitness
      # wheel selection
      selection = random.randint(0, overall)
      # spin wheel
      f_count = 0
      for i in population:
          if f_count < selection:
              f_count += i.fitness
          if f_count >= selection:
              parent = i
              break
      # add selected parent to parents
      parents.append(parent)
  
  return parents
  
  
def single_crossover(population, crossover_rate, genome_size):
  offspring = []

  for i in population:
      # pick two random population
      parent1 = random.choice(population)
      parent2 = random.choice(population)
      # crossover
      if random.random() <= crossover_rate:
          split = random.randint(0, genome_size)
          child1 = parent1.genome[0:split] + parent2.genome[split:genome_size]
          child2 = parent2.genome[0:split] + parent1.genome[split:genome_size]
      else:
          child1 = parent1.genome
          child2 = parent2.genome
      # append child1, child2 to offspring
      offspring.append(Solution(child1))
      offspring.append(Solution(child2))
      
  return offspring
  
  
def mutate(population, mutation_rate):
  offspring = []
  
  for i in population:
      genome = []
      # mutate
      for g in i.genome:
          if random.random() <= mutation_rate:
              genome.append(int(not g))
          else:
              genome.append(g)
      # append mutated genome
      offspring.append(Solution(genome))
             
  return offspring
  
  
def elitism(old_population, new_population):
  survivors = []

  # find fittest in old_population and least fit in new_population
  o_best = 0  # index of the fittest in old_population 
  n_worst = 0 # index of the least fit in new_population
  for p in range(len(old_population)):
      if old_population[p].fitness > old_population[o_best].fitness:
          o_best = p
      if new_population[p].fitness < new_population[n_worst].fitness:
          n_worst = p
          
  # replace least fit in new_population with fittest in new_population
  for p in range(len(old_population)):
      if p == n_worst and old_population[o_best].fitness > new_population[n_worst].fitness:
          genome = old_population[o_best].genome
      else:
          genome = new_population[p].genome
      survivors.append(Solution(genome))

  return survivors
  
  
# ===========
# entry point
# ===========
if __name__ == '__main__':
  if (len(sys.argv) >= 2):
    generation_limit = int(sys.argv[1])
  if (len(sys.argv) >= 3):
    P_size = int(sys.argv[2])
  if (len(sys.argv) >= 4):
    G_size = int(sys.argv[3])
  if (len(sys.argv) >= 5):
    C_rate = float(sys.argv[4])
  if (len(sys.argv) >= 6):
    M_rate = float(sys.argv[5])
  
  main(generation_limit, P_size, G_size, C_rate, M_rate)
