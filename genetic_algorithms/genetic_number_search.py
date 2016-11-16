import random
import math
from genetic_support import Chromosome

### OPTIONS ###
target_value = 42

starting_population = 100
# Breeding can be between 0 and 1 inclusive.
breeding_proportion = 0.5

# Kill proportion. Controls how many of the inviable solutions die per generation
# Killing is off by default
kill_chance = 0

# Mutation chance can be between 0.000 and 1. 0.001 recommended.
mutation_chance = 0.01

generations_limit = 1000
#### END OPTIONS ####

population = [Chromosome(None) for _ in range(starting_population)]

def reset():
  global population
  population = [Chromosome(None) for _ in range(starting_population)]
  
# Breed two chromosomes by selecting a random pivot index
# and swapping the genes after that pivot forming
# two new offspring.
def breed(chrom1, chrom2):
  # select a pivot that ensures at least one base swaps
  pivot = random.randint(1, (len(chrom1.genome)-2))
  new_chrom1 = chrom1.genome[:pivot] + chrom2.genome[pivot:]
  new_corom2 = chrom2.genome[:pivot] + chrom1.genome[pivot:]
  return (Chromosome(new_chrom1), Chromosome(new_corom2))

# Mutate a chromosome by choosing a random location
# and 'flipping' the gene at that location.
def mutate(chrom):
  mutation_location = random.randint(0, (len(chrom.genome)-1))
  bases = list(chrom.genome)
  
  # Flip the base
  bases[mutation_location] = str((int(bases[mutation_location])-1)**2)
  return Chromosome("".join(bases))

# Determine if a chromosome matches the desired value.
def eval_population():
  for chromosome in population:
    if chromosome.value() == target_value:
      return chromosome
  return False

# Counter for generations that have passed.
generations = 0 

# Loop until a solution is found, or the generation limit is reached, or 
# the population dies out.
while not eval_population() and (generations < generations_limit) and (len(population) > 0):
  print "generation: ", generations + 1, "population: ", len(population)
  
  # Kill some chromosomes, if configured to do so.
  if kill_chance > 0:
    population = [x for x in population if (not x.is_viable()) and (random.randint(0, 1000)/1000.0 < kill_chance)]

  # Shuffle chromosome order to randomise breeding.
  random.shuffle(population)
  
  # Breed the number of pairs based on breeding proportion.
  num_breeding_pairs = int((len(population)/2)*breeding_proportion)

  for index in range(0, num_breeding_pairs, 2):
    (new_crom1, new_crom2) = breed(population[index], population[index+1])
    population[index] = new_crom1
    population[index+1] = new_crom2

  # Mutate some chromosomes based on chance.
  for index, chromosome in enumerate(population):
    if random.randint(0, 1000)/1000.0 < mutation_chance:
      population[index] = mutate(chromosome)

  generations += 1

# Display results. 
print ""
print "######"

if eval_population():
  print "solution found!"
  print "Genome: ", eval_population().genome
  print "Decoded genome: ", eval_population().decode_genome(), "=", target_value
  print "Generations taken: ", generations
elif generations >= generations_limit: 
  print "Generations limit exceeded: ", generations_limit
elif len(population) == 0:
  print "population went extinct! Try upping your population size, or decreasing kill chance."
