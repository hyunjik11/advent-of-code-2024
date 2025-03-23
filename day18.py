import numpy as np

def import_txt_file(filename: str) -> list[tuple[int, int]]:
  with open(filename, 'r') as file:
    coords_list = []
    for line in file:
      coords = tuple([int(x) for x in line.strip().split(',')])
      coords_list.append(coords)
    return coords_list

filename = 'inputs/day18.txt'
# filename = 'inputs/day18_test.txt'

coords_list = import_txt_file(filename)
# print(coords_list)

# Get num_rows and num_cols by finding the maximum values of the coordinates
numx = max([x[0] for x in coords_list]) + 1
numy = max([x[1] for x in coords_list]) + 1
print(numx, numy)

# Part 1: Compute shortest distance from coord (0,0) to coord (numx-1, numy-1).
# First set number of bytes to use.
if 'test' in filename:
  num_bytes = 12
else:
  num_bytes = 1024

# Create a 2D array of bytes using the first `num_bytes` bytes in `coords_list`
byte_array = np.zeros((numy, numx), dtype=int)
for i in range(num_bytes):
  x, y = coords_list[i]
  byte_array[y][x] = 1
# print(byte_array)

# For shortest distance, construct array `sd` of same size as `byte_array` st
# `sd[i][j]` is the shortest distance from (0,0) to(i, j). Initialize to -1.
# This can be constructed by iterating over distances from (0,0), starting from
# 0. Finish iteration when (numx-1, numy-1) is reached.
sd = np.zeros((numy, numx), dtype=int) - 1
finish = False
distance = 0
coords_at_distance = [(0, 0)]
sd[0][0] = 0
while not finish:
  distance += 1
  new_coords_at_distance = []
  for coords in coords_at_distance:
    x, y = coords
    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for xn, yn in neighbours:
      # Check that xn, yn are valid coords
      if xn < 0 or xn >= numx or yn < 0 or yn >= numy:
        continue
      # Check that (xn, yn) is not occupied by a wall.
      if byte_array[yn][xn] == 1:
        continue
      # Check that (xn, yn) has not been visited before.
      if sd[yn][xn] != -1:
        continue
      # Update sd[yn][xn] to distance.
      sd[yn][xn] = distance
      new_coords_at_distance.append((xn, yn))
  # Update coords_at_distance to new_coords_at_distance
  coords_at_distance = new_coords_at_distance
  # Finish if (numx-1, numy-1) has been reached.
  if sd[numy-1][numx-1] != -1:
    finish = True
# print(sd)
print('Part 1:', sd[numy-1][numx-1])

# Part 2: Find the coordinates of bytes that will block path from start to end.
# First adapt above code to write a function that determines whether path is
# blocked or not for a given byte_array.
def is_path_blocked(byte_array: np.array) -> bool:
  sd = np.zeros((numy, numx), dtype=int) - 1
  blocked = False
  distance = 0
  coords_at_distance = [(0, 0)]
  sd[0][0] = 0
  while True:
    distance += 1
    new_coords_at_distance = []
    for coords in coords_at_distance:
      x, y = coords
      neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
      for xn, yn in neighbours:
        # Check that xn, yn are valid coords
        if xn < 0 or xn >= numx or yn < 0 or yn >= numy:
          continue
        # Check that (xn, yn) is not occupied by a wall.
        if byte_array[yn][xn] == 1:
          continue
        # Check that (xn, yn) has not been visited before.
        if sd[yn][xn] != -1:
          continue
        # Update sd[yn][xn] to distance.
        sd[yn][xn] = distance
        new_coords_at_distance.append((xn, yn))
    # If new_coords_at_distance is empty, then path is blocked.
    if len(new_coords_at_distance) == 0:
      blocked = True
      break
    # Update coords_at_distance to new_coords_at_distance
    coords_at_distance = new_coords_at_distance
    # Finish if (numx-1, numy-1) has been reached.
    if sd[numy-1][numx-1] != -1:
      break
  return blocked

# Use binary search to determine the min number of bytes that block the path.
low = 1
high = len(coords_list)
while low < high:
  mid = (low + high) // 2
  # Show `mid` bytes in byte_array
  byte_array = np.zeros((numy, numx), dtype=int)
  for i in range(mid):
    x, y = coords_list[i]
    byte_array[y][x] = 1
  # Check whether path is blocked.  
  blocked = is_path_blocked(byte_array)
  if blocked:
    high = mid
  else:
    low = mid + 1
print('Smallest number of bytes that block path:', low)
print('Part 2:', coords_list[low - 1])