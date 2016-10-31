import re # regex
import itertools # Dyanmically generate nested loops
import copy

# General helper functions.

# Checks if the values in two dicts are consistent.
# Here, consistent means that if a key appears in both sets, its value
# in each set must be the same.
def consistent_sets(set_one, set_two):
    for variable in set_one:
        consistent = ((not set_two.has_key(variable)) 
                      or (set_two[variable] == set_one[variable]))
        if not consistent:
            return False
    return True

# Merges the keys in two given dicts.
def merge_sets(set_one, set_two):
    if not consistent_sets(set_one, set_two):
        raise
        
    new_set = {}
    for item in set_one:
        new_set[item] = set_one[item]
    
    for item in set_two:
        new_set[item] = set_two[item]
        
    return new_set

# Logic helper functions and globals.

# Exclusive or. Only one input can be true 
# for the statement to be true.
def xor(x, y):
    # Assuming x and y are supplied as True/False
    # x != y only returns true if one of them, but not
    # both, is/are true.
    x != y

# Returns true if antecendent and consequent
# are both true or both false.
def deductiveif(antecedent, consequent):
    return not xor(antecedent, consequent)

# Returns the value of a <--> b
def ifandonlyif(a, b):
    return (a and b) or ((not a) and (not b))

def nand(a, b):
    # De Morgan's law, in its simplest form.
    return (not a) or (not b)

# This dictionary is passed to the evaluator to allow 
# the functions listed to be called dynamically.
method_dict = {
    'xor': xor,
    'ifandonlyif': ifandonlyif, # defined above.
    'deductiveif': deductiveif
}

# Global storage setup.

premises = {}
conclusions = {}

def reset_variable_values():
    global premises
    global conclusions
    premises = {}
    conclusions = {}

# Premise/conclusion input.
def input_expressions():
    
    # Re-init globals
    reset_variable_values()
    
    print "##### NB INPUT GUIDE #####"
    print ("All input in iPython must be inside double\n" + 
        "quotations \"your_input\"")
    print ("Enter variables as single, lower case letters,\n" + 
        " surrounded by 2 pounds signs. EG: #x#")
    print ("You may enter expressions using valid python\n" + 
           " boolean operators (and, or, not, ==)")
    print ("You can also use the following functions: \n" + 
           "ifandonlyif, xor, and deductiveif")
    print ("Use these by typing function(#var#, #var).\n" + 
           "EG: xor(#a#, #b#)")
    print ("Make sure to include parenthesis. Like \"(not #x#)\n" + 
           " or #y#\" to set binding.")
    print
    print ("You may enter any number of premises. \nWhen you are " + 
           "done, use \"exit\" to exit.")
    print ("You may then enter any number of conclusions. \nWhen you" + 
           "are done, use \"exit\" again to exit")
    print ("NB: conclusions are assumed to be linked by OR not AND. \n" + 
           "IE, conclusions may all be valid but")
    print ("May not be able to co-exist. The program will not tell \n" + 
           "determine this.")
    print ("####### END GUIDE #######")
    print
    
    expression_arrays = \
        {"premises": premises, "conclusions": conclusions}
    for name in expression_arrays:
        print "Capturing logical expressions for", name
        print
        while True:
            expression = input("Enter an expression then hit enter:")
            if expression == "exit":
                print name, "capture complete."
                print
                print
                break
            else:
                var_matcher = re.compile('#[a-z]{1,1}#')
                variables = ([ variable[1] for 
                              variable in \
                              var_matcher.findall(expression)])
                if len(variables) == 0:
                    print("Invalid expression, no variables")
                else:
                    for var in variables:
                        expression_arrays[name][expression.replace("#", "")] \
                        = {'variables': variables,
                           'variable_values': []}

def evaluate_premise(expression, variables):
    # This code iterates over all 
    # possible combinations of True and False 
    # for the number of variables in the expression.
    ranges = [[True, False] for _ in variables]
    for true_false_combo in itertools.product(*ranges):
        
        # Assign the True/False permutation to the
        # relevant expression variables.
        variable_values = {}
        for index, variable in enumerate(variables):
            variable_values[variable] = true_false_combo[index]
        
        # Evaluate the premise with the values.
        eval_value = eval(expression, method_dict,
                          variable_values)
        
        # If the premise evaluates to true,
        # capture the value set (if unique).
        if eval_value:
            if not variable_values in \
                premises[expression]['variable_values']:
                (premises[expression]['variable_values']
                    .append(variable_values))

def validate_argument():
    consistent_variable_value_sets = []
    
    # This code iterates over every possible combination of
    # every possible value set for each premise. 
    
    variable_value_hash_sets = \
        [ premises[premise]['variable_values'] \
        for premise in premises]
    
    for variable_value_hash_set \
        in itertools.product(*variable_value_hash_sets):
        
        # This code evaluates whether the given variable 
        # values are consistent and if so, merges them.
        consistent = True
        merged_set = {}
        for index, variable_hash in \
            enumerate(variable_value_hash_set):
            
            if consistent_sets(merged_set, variable_hash):
                merged_set = merge_sets(merged_set, \
                                        variable_hash)
            else:
                consistent = False
                break
        # If all the variable sets in a
        # permutation are consistent
        # the set is stored.
        if consistent:
            consistent_variable_value_sets.append(merged_set)
    
    # If no sets of values are consistent, inconsistent premises
    # have been supplied.
    if len(consistent_variable_value_sets) == 0:
        print ("Premises are not consistent")
        return False
    else:
        
        # This code goes through each set of variable values
        # that match the premises and checks if they satisfy
        # ALL conclusions. This is in accordence with 
        # the behaviour listed in the docs.
        all_conclusions_true = False
        for variable_set in consistent_variable_value_sets:
            premise_confirms_conclusions = True
            for conclusion in conclusions:
                conclusion_valid = True
                for var \
                in conclusions[conclusion]['variables']:
                    if not variable_set.has_key(var):
                        conclusion_valid = False
                if conclusion_valid:
                    conclusion_valid = eval(conclusion, 
                            method_dict, variable_set)
                if not conclusion_valid:
                    premise_confirms_conclusions = False
                    break
            if premise_confirms_conclusions:
                all_conclusions_true = True
                break
        
        if not all_conclusions_true:
            print("Premises do not support conclusions.")
            return False
        else:
            return True

def evaluate_argument():
    # Return an error if there are not at least 
    # some premises and conclusions.
    if len(premises) == 0 or len(conclusions) == 0:
        print("Please supply at least one premise and" +
              "at least one conclusion.")
        return
    
    # Evaluate all premises to determine which value sets 
    # they are satisfied by.
    for premise in premises:
        evaluate_premise(premise, 
            premises[premise]['variables'])
    
    # Validate the argument supplied.
    if validate_argument():
        print "Argument valid"
    else:
        print "Argument invalid"

input_expressions()
evaluate_argument()