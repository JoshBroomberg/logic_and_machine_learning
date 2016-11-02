from collections import deque

class RoutingQueue:
  
  def __init__(self):
    self.queue = deque()

  def has_next(self):
    return len(self.queue)

  def put_node(self, node):
    self.queue.appendleft(node)

  def get_node(self):
    return self.queue.pop()

class RoutingStack:
  def __init__(self):
    self.stack = []

  def has_next(self):
    return len(self.stack)

  def put_node(self, node):
    self.stack.append(node)

  def get_node(self):
    return self.stack.pop()