import itertools
import numpy as np
import collections

def import_txt_file_as_array(filename: str) -> list[list[str]]:
  with open(filename, 'r') as file:
    return [list(line.strip()) for line in file]

def is_valid_pos(pos: tuple[int, int], nrow: int, ncol: int) -> bool:
  # Check whether pos is a valid position in the map.
  return 0 <= pos[0] < nrow and 0 <= pos[1] < ncol

filename = 'inputs/day08.txt'
# filename = 'inputs/day08_test.txt'
map_arr = import_txt_file_as_array(filename)
nrow = len(map_arr)
ncol = len(map_arr[0])

# Sweep over map to obtain dict of locations for each character.
antenna = collections.defaultdict(list)
for i, row in enumerate(map_arr):
  for j, val in enumerate(row):
    if val == ".":
      continue
    else:
      antenna[val].append((i, j))
# print(antenna)

# Part 1: Count number of unique antinode locations.
# Sweep over antenna dict to obtain valid antinode locations,
# storing the locations by marking it with `1` in a 2D array.
antinodes = np.zeros((nrow, ncol), dtype=np.int32)
for k, v in antenna.items():
  if len(v) > 1:
    # Loop over all pairs in v
    for v1, v2 in itertools.combinations(v, 2):
      # Compute diff between x, y coordinates of v1 and v2
      x_diff = v1[0] - v2[0]
      y_diff = v1[1] - v2[1]
      # print(x_diff, y_diff)
      c1 = (v1[0] + x_diff, v1[1] + y_diff)
      c2 = (v2[0] - x_diff, v2[1] - y_diff)
      if is_valid_pos(c1, nrow, ncol):
        antinodes[c1[0]][c1[1]] = 1
      if is_valid_pos(c2, nrow, ncol):
        antinodes[c2[0]][c2[1]] = 1
print('Part 1:', np.sum(antinodes))

# Part 2: Count antinodes at all distances from the antenna
antinodes = np.zeros((nrow, ncol), dtype=np.int32)
for k, v in antenna.items():
  if len(v) > 1:
    # Loop over all pairs in v
    for v1, v2 in itertools.combinations(v, 2):
      # Compute diff between x, y coordinates of v1 and v2
      x_diff = v1[0] - v2[0]
      y_diff = v1[1] - v2[1]
      # Sweep over all valid candidates
      # Note that we want to sweep over int n for coordinates:
      # (v1[0] +/- n * x_diff, v1[1] +/- n * y_diff)
      # such that both x and y coords are in the map.
      # Note we assume that gcd(x_diff, y_diff) = 1
      # (verified that this is the case for the test cases).
      # This can be done using a while loop, that keeps iterating until
      # both (v1[0] + n * x_diff, v1[1] + n * y_diff)
      # and (v1[0] - n * x_diff, v1[1] - n * y_diff) are invalid positions.
      n = 0
      while True:
        c1 = (v1[0] + n * x_diff, v1[1] + n * y_diff)
        c2 = (v1[0] - n * x_diff, v1[1] - n * y_diff)
        c1_valid = is_valid_pos(c1, nrow, ncol)
        c2_valid = is_valid_pos(c2, nrow, ncol)
        if c1_valid:
          antinodes[c1[0]][c1[1]] = 1
        if c2_valid:
          antinodes[c2[0]][c2[1]] = 1
        n += 1
        # Break out of while loop if both c1 and c2 are invalid.
        if not c1_valid and not c2_valid:
          break
# print(antinodes)
print('Part 2:', np.sum(antinodes))