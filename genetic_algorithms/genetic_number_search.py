import random
import math
from genetic_support import Chromosome
from collections import defaultdict

### OPTIONS ###\

# The value that is sought through evolution.
target_value = 42

# Number of chromosomes to start with.
starting_population = 200

# Breeding can be between 0 and 1 inclusive.
breeding_proportion = 0.5

# Kill proportion. Controls how many of the inviable solutions die per generation
# Killing of inviable genomes is 0.005 by default.
kill_chance = 0.005

# Mutation chance can be between 0.000 and 1. 0.001 recommended.
mutation_chance = 0.01

# How many iterations of breeding/mutation are allowed.
generations_limit = 1000

# Sort population by fitness or shuffle.
shuffle = False

# Number of trials to run with parameters above.
trials = 50

#### END OPTIONS ####

population = [Chromosome(None, target_value) for _ in range(starting_population)]

def reset():
  global population
  population = [Chromosome(None, target_value) for _ in range(starting_population)]
  
# Breed two chromosomes by selecting a random pivot index
# and swapping the genes after that pivot forming
# two new offspring.
def breed(chrom1, chrom2):
  # select a pivot that ensures at least one base swaps
  pivot = random.randint(1, (len(chrom1.genome)-2))
  new_chrom1 = chrom1.genome[:pivot] + chrom2.genome[pivot:]
  new_chrom2 = chrom2.genome[:pivot] + chrom1.genome[pivot:]
  return (Chromosome(new_chrom1, target_value), Chromosome(new_chrom2, target_value))

# Mutate a chromosome by choosing a random location
# and 'flipping' the gene at that location.
def mutate(chrom):
  mutation_location = random.randint(0, (len(chrom.genome)-1))
  bases = list(chrom.genome)
  
  # Flip the base
  bases[mutation_location] = str((int(bases[mutation_location])-1)**2)
  return Chromosome("".join(bases), target_value)

# Determine if a chromosome matches the desired value.
def eval_population():
  for chromosome in population:
    if chromosome.value() == target_value:
      return chromosome
  return False

generations = 0 

def run_simulation(simulation_index):
  global generations
  global population

  # Counter for generations that have passed.
  generations = 0 
  # Loop until a solution is found, or the generation limit is reached, or 
  # the population dies out.
  while not eval_population() and (generations < generations_limit) and (len(population) > 0):
    print "trial:", simulation_index+1, "/", trials, "generation: ", generations + 1, "population: ", len(population)
    
    # Kill some chromosomes, if configured to do so.
    # if kill_chance > 0:
    population = [x for x in population if not ((not x.is_viable()) and (1000*kill_chance >= random.randint(1, 1000)))]

    if shuffle:
    # Shuffle chromosome order to randomise breeding.
      random.shuffle(population)
    else:
      population.sort()
    
    # Breed the number of pairs based on breeding proportion.
    num_breeding_pairs = int((len(population)/2)*breeding_proportion)

    for index in range(0, num_breeding_pairs, 2):
      (new_crom1, new_crom2) = breed(population[index], population[index+1])
      population[index] = new_crom1
      population[index+1] = new_crom2

    # Mutate some chromosomes based on chance.
    for index, chromosome in enumerate(population):
      if 1000*mutation_chance >= random.randint(1, 1000):
        population[index] = mutate(chromosome)

    generations += 1

# Run analysis on parameters. 
print "######"

results = []

# Run simulations and store results.
for index in range(trials):
  run_simulation(index)
  result = {}
  if eval_population():
    result["success"] = True
    result["genome"] = eval_population().genome
    result["decoded genome"] = eval_population().genome +":" + eval_population().decode_genome() + "=" + str(target_value)
    result["generations taken"] = generations
  elif generations >= generations_limit: 
    result["success"] = False
    result["failure_reason"] = "Gen Limit"
  elif len(population) == 0:
    result["success"] = False
    result["failure_reason"] = "Extinct"
  else:
    print "oh oh"

  results.append(result)
  reset()

# Analyze results.
def zero():
  return 0

successes = 0
valid_genomes = defaultdict(zero)
generation_failures = 0
extinction_failures = 0

for result in results:

  if result["success"]:
    successes += 1
    valid_genomes[result["decoded genome"]] += 1
  else:
    if result["failure_reason"] == "Gen Limit":
      generation_failures += 1
    elif result["failure_reason"] == "Extinct":
      extinction_failures += 1

print
print "successes: ", successes
print "Generation limit failures: ", generation_failures 
print "Population extinction failures: ", extinction_failures 
print "valid genomes"
print  "count: ", "genome" 
for genome, count in valid_genomes.iteritems():
  print count,":", genome



