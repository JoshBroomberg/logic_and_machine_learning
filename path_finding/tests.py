from sanfrancisco import nodes
from data_structures import RoutingQueue, RoutingStack

# Sets system limit for recursive depth.
# Important to allow the plotting of long paths later on.
import sys
sys.setrecursionlimit(100)

# This function is a generic brute-force search.
# It takes a start node, a desired destination co-ordinate, and a storage class.
# Whether it is depth/breadth first search is determined by the storage class passed in.
def findRoute(startingNode, soughtValue, storageClass):
  # This is the processing store. It is an instance of the storage class. 
  # It can accept a node, and give a node back. 
  # Implementation of these operations is hidden in data_structures.py.
  node_store = storageClass()
  node_store.put_node(startingNode)
  
  # Visited nodes tracks the paths taken as the function explores.
  # The node visited is the key, the node that lead to that node is the value.
  # The starting node has a None origin node.
  visited_nodes = {}
  visited_nodes[startingNode.value] = None

  # While there are nodes left to process, do the code below.
  while node_store.has_next():
    # Set the current node to be the next node to process.
    current_node = node_store.get_node()
    
    # Check if the current node has the desired co-ords.
    if current_node.value == soughtValue:
      # If it does, use traversePath to return the path used to get here.
      return traversePath(visited_nodes, current_node.value)

    # If the current node is not the desired one, explore each of the nodes next to it.
    for node in current_node.adjacentNodes:
      # If the node hasn't been visited, visit it.
      # This involves two things. One, tracking how we visited it by storing it in visited_nodes.
      # Two, adding it to the node_store to be processed. 
      if node.value not in visited_nodes.keys():
          visited_nodes[node.value] = current_node.value
          node_store.put_node(node)
  
  # If no nodes are left to process, and the desired node was not found
  # return a message saying no route found.
  return "no path found."

# This function uses a node dictionary, in the format of visited_nodes, to return
# a string version of the path to the given node value via recursion.
# It starts with the destination value, and prepends the path to the node that lead to that destination.
# This is repeated, building the path until a node with no origin node is hit.
def traversePath(node_path_dictionary, destination_node_value):
  if node_path_dictionary[destination_node_value] == None:
    return "Path found. \n\nStart:\n"
  else:  
    return traversePath(node_path_dictionary, node_path_dictionary[destination_node_value]) + str(destination_node_value) + "\n"
# Use the findRoute method with a queue.
# This means that the 'children nodes' of each node are added to the back of the processing list. 
# This means all sibling nodes, stemming from a grandfather node, are processed before (grand)children.
def breadthFirst(startingNode, soughtValue):
  return findRoute(startingNode, soughtValue, RoutingQueue)

# Use the findRoute method with a stack.
# This means that the 'children nodes' of each node are added to the front of the processing list. 
# This means all children nodes of the node in question are processed before sibling nodes.
def depthFirst(startingNode, soughtValue):
  return findRoute(startingNode, soughtValue, RoutingStack)

print "Breadth-first search in progess:", breadthFirst(nodes[(1501, 4118)], (6173,7065))
print "Depth-first search:", depthFirst(nodes[(5641,3193)], (6173,7065))