import random
import numpy as np 
import matplotlib.pyplot as plt

a_weight = random.random()
b_weight = random.random()
bias_weight = random.random()
weights = {"a": np.array([[0, a_weight]]), "b": np.array([[0, b_weight]]), "bias": np.array([[0, bias_weight]])}
learning_constant = 0.5
logical_function_to_model = raw_input("Develop a perceptron for what logical operator? (and/or)\n")

and_valid = [(0,0,-1), (0,1,-1), (1,0,-1), (1,1,1)]
or_valid = [(0,0,-1), (0,1,1), (1,0,1), (1,1,1)]

if logical_function_to_model == "and":
  valid_data = and_valid
else:
  valid_data = or_valid

def predict(a, b):
  activation_sum = a*a_weight + b*b_weight + bias_weight
  return activation_function(activation_sum, logical_function_to_model)

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

def adjust(a, b, error):
  global a_weight
  global b_weight
  global bias_weight
  
  a_weight += a * error * learning_constant
  b_weight += b * error * learning_constant
  bias_weight += error * learning_constant

def training_set():
  return random.sample(valid_data, 1)[0]

def train():
  correct_count = 0
  attempts = 0

  while correct_count < 4 and attempts < 100000:
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

def evaluate():
  correct = 0
  for values in valid_data:
    predicted = predict(values[0], values[1])
    if predicted == values[2]:
      correct += 1
  return correct

def capture_weights(attempt):
  global weights
  weights["a"] = np.vstack([weights["a"], np.array([attempt, a_weight])])
  weights["b"] = np.vstack([weights["b"], np.array([attempt, b_weight])])
  weights["bias"] =  np.vstack([weights["bias"], np.array([attempt, bias_weight])])

def reset():
  global a_weight
  global b_weight
  global bias_weight
  global weights

  a_weight = random.random()
  b_weight = random.random()
  bias_weight = random.random()
  weights = {"a": np.array([[0, a_weight]]), "b": np.array([[0, b_weight]]), "bias": np.array([[0, bias_weight]])}

number_correct = 0
counter = 0
while number_correct != 4 and counter < 10000:
  print "Training attempt:", counter + 1
  counter += 1
  reset()
  train()
  number_correct = evaluate()
  
  print "weights:", "a:", a_weight, "b:", b_weight, "bias:", bias_weight
  print "Accuracy:", number_correct, "/4"
  print

plt.plot(weights["a"][:, 0], weights["a"][:, 1])
plt.plot(weights["b"][:, 0], weights["b"][:, 1])
plt.plot(weights["bias"][:, 0], weights["bias"][:, 1])
plt.show()

