import numpy as np
import textwrap

class Chromosome:
  gene_dict = {
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9",
    "1010": "+",
    "1011": "-",
    "1100": "*",
    "1101": "/",
  }

  def __init__(self, genome):
    if genome:
      self.genome = genome
    else:
      self.genome = Chromosome.random_genome()

  # Return a string version of the binary genome as numbers/operators
  def decode_genome(self):
    # Split the genome into 4 genes
    genes = textwrap.wrap(self.genome, 4)
    
    # decode the binary genes into string form.
    decoded_genes = [Chromosome.lookup_gene(gene) for gene in genes]
    # Validate the genome
    if not Chromosome.validate_genome(decoded_genes):
      return None
    
    # If valid, join the genome together and return
    return "".join(decoded_genes)

  # Boolean value which represents if the genome is viable for evaluation.
  def is_viable(self):
    # note: "not not" just converts truthy/falsey value to True/False
    return not not self.decode_genome()

  # Return the value of the chromosome.
  def value(self):
    if not self.is_viable():
      return None
    else:
      return eval(self.decode_genome())


  ### STATIC UTILITY METHODS ###

  # Create a random 20 gene 'genome string'
  @staticmethod
  def random_genome():
    return ''.join([str(x) for x in np.random.randint(2, size=(20,))])

  # Converts binary gene to literal version.
  @staticmethod
  def lookup_gene(gene):
    try:
      return Chromosome.gene_dict[gene]
    except KeyError:
      return ""
  
  # Takes an array of genes.
  # Validates genome is mathematically operable.
  @staticmethod
  def validate_genome(genes):
    # First gene must be a number
    number_required = True
    for gene in genes:
      is_number = False
      # Try to convert string value into an int.
      try:
        int(gene)
        # If line above doesn't throw an error, string is number.
        is_number = True
      except ValueError:
        False
    
      if number_required and (not is_number):
        return False

      elif (not number_required) and is_number:
        return False

      elif gene == genes[-2]:
        number_required = True
      
      elif gene == "":
        continue

      elif number_required and is_number:
        # next run, number is not required.
        number_required = False
      elif (not number_required) and (not is_number):
        # next run, number is required.
        number_required = True

    # Return true if loop completes without failure.
    return True
