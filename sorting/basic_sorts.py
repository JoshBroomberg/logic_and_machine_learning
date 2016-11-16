import sys

def selection_sort(data):
  sorted_list = []
  for _ in range(len(data)):
    minimum_index = 0
    for index in range(len(data)):
      if data[index] < data[minimum_index]:
        minimum_index = index

    sorted_list.append(data[minimum_index])
    data[minimum_index] = sys.maxint
  return sorted_list

def insertion_sort(data):
  sorted_until_index = 1
  while sorted_until_index < (len(data) - 1):
    value_to_insert = data[sorted_until_index]
    print "value:", value_to_insert
    for index in range(sorted_until_index):
      if data[index+1] > value_to_insert:
        # shifting
        for shift_index in range(index+1, sorted_until_index)[::-1]:
          data[shift_index] = data[shift_index-1]
          print "shift", data
        data[index] = value_to_insert
        break
    sorted_until_index += 1
    print data
  return data

print insertion_sort([1,3, 4,2, 7,6,5,9,8])
      


