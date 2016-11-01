import random
import numpy as np 
import matplotlib.pyplot as plt

a_weight = random.random()
b_weight = random.random()
bias_weight = random.random()
weights = {"a": np.array([[0, a_weight]]), "b": np.array([[0, b_weight]]), "bias": np.array([[0, bias_weight]])}
learning_constant = 1
logical_function_to_model = raw_input("Develop a perceptron for what logical operator? (and/or)\n")
print

# Valid data for the two logical functions.
and_valid = [(0,0,-1), (0,1,-1), (1,0,-1), (1,1,1)]
or_valid = [(0,0,-1), (0,1,1), (1,0,1), (1,1,1)]

if logical_function_to_model == "and":
  valid_data = and_valid
elif logical_function_to_model == "or":
  valid_data = or_valid
else:
  raise

# Take inputs A and B
# Calculate an activation sum and then use the activation function
# to determine if perceptron should activate, simply
# return the value it provides.
def predict(a, b):
  activation_sum = a*a_weight + b*b_weight + bias_weight
  return activation_function(activation_sum, logical_function_to_model)

# Take an activation sum and return 1 if that sum is greater than/equal 1
# -1 if it isn't. 
# Also takes the logical function being modelled to determine activation function.
def activation_function(activation_sum, function):
  if function == "and":
    if activation_sum >= 1:
      return 1
    else:
      return -1
  elif function == "or":
    return np.sign(activation_sum)
  else:
    raise

# Take inputs and the error they produced and adjust the weights
# by input times error times learning_constant.
def adjust(a, b, error):
  global a_weight
  global b_weight
  global bias_weight
  
  a_weight += a * error * learning_constant
  b_weight += b * error * learning_constant
  bias_weight += error * learning_constant

# Return a random set of training data. A set is two inputs and an output.
def training_set():
  return random.sample(valid_data, 1)[0]

# This training function is a little more effecient than in the first version. 
# It gets a random training set, uses the perceptron to predict the value, and then
# adjust weights based on error between predicted val and the correct value.
# It will repeat this until the perceptron gets 4 in a row correct or 1000 attempts are made.
# Getting 4 in a row right doesn't mean all 4 different cases are predicted correctly.
# This approach looks for an easy to train perceptron, rather than brute force training
# a single perceptron.
def train():
  correct_count = 0
  attempts = 0

  while correct_count < 4 and attempts < 1000:
    attempts += 1
    capture_weights(attempts)
  
    value_set = training_set()
    predicted = predict(value_set[0], value_set[1])
    if predicted == value_set[2]:
      correct_count += 1
    else:
      correct_count = 0
      error = value_set[2] - predicted
      adjust(value_set[0], value_set[1], error)
  print "Training runs:", attempts

# This function tests how many of the 4 possible input scenarios the current
# percepton would get right. It returns a number between 0 and 4.
def evaluate():
  correct = 0
  for values in valid_data:
    predicted = predict(values[0], values[1])
    if predicted == values[2]:
      correct += 1
  return correct

# Captures the weights at the time of call for use in graphing.
def capture_weights(attempt):
  global weights
  weights["a"] = np.vstack([weights["a"], np.array([attempt, a_weight])])
  weights["b"] = np.vstack([weights["b"], np.array([attempt, b_weight])])
  weights["bias"] =  np.vstack([weights["bias"], np.array([attempt, bias_weight])])

def plot_weights():
  plt.plot(weights["a"][:, 0], weights["a"][:, 1])
  plt.plot(weights["b"][:, 0], weights["b"][:, 1])
  plt.plot(weights["bias"][:, 0], weights["bias"][:, 1])
  plt.show()

def print_perceptron():
  print "weights:", "a:", a_weight, "b:", b_weight, "bias:", bias_weight
  print "Accuracy:", evaluate(), "/4"
  print

def reset():
  global a_weight
  global b_weight
  global bias_weight
  global weights

  a_weight = random.random()
  b_weight = random.random()
  bias_weight = random.random()
  weights = {"a": np.array([[0, a_weight]]), "b": np.array([[0, b_weight]]), "bias": np.array([[0, bias_weight]])}

def find_a_valid_perceptron():
  print "Starting with:"
  print_perceptron()

  counter = 0
  while evaluate() != 4 and counter < 10000:
    print "Training attempt:", counter + 1
    counter += 1
    reset()
    train()
    print_perceptron()
    
  plot_weights()

find_a_valid_perceptron()  

