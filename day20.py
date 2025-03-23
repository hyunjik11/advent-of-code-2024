import numpy as np
import tqdm

def import_data(filename: str) -> list[list[str]]:
  # Extract characters per line as array.
  map_arr = []
  with open (filename, 'r') as file:
    for line in file:
      map_arr.append(list(line.strip()))
    return map_arr

def print_map(map_arr: list[list[str]]):
  str_to_print = ''
  for row in map_arr:
    row_to_print = ''.join(row)
    row_to_print += '\n'
    str_to_print += row_to_print
  print(str_to_print)

def find_target_pos(map_arr: list[list[str]], target: str) -> tuple[int, int]:
  # Find target string in map_arr.
  for i, row in enumerate(map_arr):
    for j, val in enumerate(row):
      if val == target:
        return (i, j)

filename = 'day20.txt'
# filename = 'day20_test.txt'
map_arr = import_data(filename)
# print_map(map_arr)

# Find the starting position.
start_pos = find_target_pos(map_arr, 'S')
print('Start:', start_pos)

#  Find end position.
end_pos = find_target_pos(map_arr, 'E')
print('End:', end_pos)

# Part 1: Find number of cheats that saves at least 100 steps.
# Note that for a given cheat position 1, there is only one possible cheat
# position 2 that saves steps, since the given path has width 1.
# Each cheat position 1 corresponds to a wall position, so we just need to loop
# over all possible wall positions and see how many steps are saved for each.
# Note that the walls that save steps have the form:
#  .      #
# .#. or .#.
#  #      #
# and their 90/180/270 degree rotations.
# Using this observation, we can narrow down the wall positions to check.
# To find the number of steps needed to reach the end position, we can use
# the breadth-first search logic used on day 18.
def is_within_bounds(pos: tuple[int, int], map_arr: list[list[str]]) -> bool:
  """Check if pos is within bounds of map_arr."""
  i, j = pos
  return i >= 0 and i < len(map_arr) and j >= 0 and j < len(map_arr[0])

def exactly_one_neighbour(
    pos: tuple[int, int], map_arr: list[list[str]]
) -> bool:
  """Check if pos has exactly one neighbour that is a wall."""
  i, j = pos
  # First check that the position is a wall.
  if map_arr[i][j] != '#':
    return False
  neighbours = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
  num_neighbour_walls = 0
  for ni, nj in neighbours:
    if not is_within_bounds((ni, nj), map_arr):
      continue
    if map_arr[ni][nj] == '#':
      num_neighbour_walls += 1
  return num_neighbour_walls == 1

def exactly_two_neighbours_opposite(
    pos: tuple[int, int], map_arr: list[list[str]]
) -> bool:
  """Check if pos has exactly two neighbours that are walls and opposite."""
  i, j = pos
  # First check that the position is a wall.
  if map_arr[i][j] != '#':
    return False
  neighbours = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
  neighbour_wall_pos = []
  for ni, nj in neighbours:
    if not is_within_bounds((ni, nj), map_arr):
      continue
    if map_arr[ni][nj] == '#':
      neighbour_wall_pos.append((ni, nj))
  # Check that there are exactly two neighbours that are walls.
  if len(neighbour_wall_pos) != 2:
    return False
  # Check that the two neighbours are in opposite positions.
  # Note that they are opposite if their i or j values are the same.
  ni1, nj1 = neighbour_wall_pos[0]
  ni2, nj2 = neighbour_wall_pos[1]
  return ni1 == ni2 or nj1 == nj2

# For computing the number of steps from a given start to end point, we just
# need to label the open positions from 0 to n where n is the distance between
# the start and the end. Then the distance between any two points can be
# determined by subtracting the values of their labels. This is true only
# because there is a unique path from start to end.
nrow = len(map_arr)
ncol = len(map_arr[0])
labels = {start_pos: 0}
cur_pos = start_pos
dist = 0
finish = False
while not finish:
  # Find next position
  i, j = cur_pos
  neighbours = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
  for ni, nj in neighbours:
    # Check that ni, nj are valid coords
    if not is_within_bounds((ni, nj), map_arr):
      continue
    # Check that (ni, nj) is not a wall.
    if map_arr[ni][nj] == '#':
      continue
    # Check that (ni, nj) has not been visited before.
    if (ni, nj) in labels:
      continue
    # Update cur_pos, dist, and labels
    dist += 1
    cur_pos = (ni, nj)
    assert cur_pos not in labels
    labels[cur_pos] = dist
    if cur_pos == end_pos:
      finish = True
# print(labels)

def num_steps(start: tuple[int, int], end: tuple[int, int]) -> int:
  """Find shortest distance to end from start."""
  return abs(labels[end] - labels[start])

# Find all valid cheat positions.
# Find valid cheat positions of type 1 (walls with one neighbouring wall) and
# type 2 (walls with two neighbouring walls that are opposite)
valid_one_neighbour_walls = []
valid_two_neighbour_walls = []
for i in range(1, len(map_arr) - 1):
  for j in range(1, len(map_arr[0]) - 1):
    if exactly_one_neighbour((i, j), map_arr):
      valid_one_neighbour_walls.append((i, j))
    if exactly_two_neighbours_opposite((i, j), map_arr):
      valid_two_neighbour_walls.append((i, j))

# For the test case, we want to search both type 1 and type 2 walls.
# For the non-test case, we only want walls that are of type 2, since the one
# neighbour walls can only save 2 steps. This narrows the search space a bit.
if 'test' in filename:
  valid_cheat_positions = valid_one_neighbour_walls + valid_two_neighbour_walls
else:
  valid_cheat_positions = valid_two_neighbour_walls

# Find number of steps from start to end as a sanity check
# Note this is not actually needed to find the number of saved steps.
num_steps_baseline = num_steps(start_pos, end_pos)
print(f'Num steps from start to end:', num_steps_baseline)

# For each valid cheat position, note that the number of steps saved is equal
# to the number of steps required to go from one open side of the wall to the
# other open side minus 2, since there is a unique path from start to end.
num_steps_saved_list = []
threshold_steps_saved = 1 if 'test' in filename else 100
for pos in valid_cheat_positions:
  i, j = pos
  # Find the two empty sides of the wall.
  if map_arr[i-1][j] != '#' and map_arr[i+1][j] != '#':
    start, end = (i-1, j), (i+1, j)
  elif map_arr[i][j-1] != '#' and map_arr[i][j+1] != '#':
    start, end = (i, j-1), (i, j+1)
  else:
    raise ValueError(f'Position {pos} is an invalid candidate for cheating.')
  num_steps_saved = num_steps(start, end) - 2
  if num_steps_saved >= threshold_steps_saved:
    num_steps_saved_list.append(num_steps_saved)
    # print(f'{pos=}, {num_steps_saved=}')

if 'test' in filename:
  # Count number of positions for each num_steps_saved.
  counts = {}
  for num in num_steps_saved_list:
      counts[num] = counts.get(num, 0) + 1
  # Print counts
  for value, count in sorted(counts.items()):
      print(f"There are {count} instances of {value} steps saved")
else:
  print('Part 1:', len(num_steps_saved_list))

# Part 2: Count number of cheats that save >=100 steps where you can move
# freely for up to 20 steps. Previously in part 1, the candidate start & end
# positions for the cheats were adjacent to a fixed wall. Now in part 2, they
# can be any open positions that are at most 20 steps apart. So we just need
# to modify the logic for getting the candidate start and end positions.

def distance(start: tuple[int, int], end: tuple[int, int]) -> int:
  """Distance from start to end ignoring walls."""
  return abs(start[0] - end[0]) + abs(start[1] - end[1])

open_positions = [k for k, _ in sorted(labels.items(), key=lambda x: x[1])]
# print(open_positions)

# For each `start` in `open_positions`, we can either
# 1) sweep over all possible `end` in `open_positions` and check
# distance(start, end) <= 20
# or
# 2) sweep over all possible `end` that satisfy distance(start, end) <= 20 and
# check whether `end` is an open position.
# The inner loop should be similarly fast for both. However,
# 2) only has a few hundred iterations in the inner loop whereas 1) has a few
# thousand for the non-test case, so 2) is more efficient.

dist_thresh = 20
offset_within_thresh = []
for i_offset in range(-dist_thresh, dist_thresh + 1):
  max_j_offset = dist_thresh - abs(i_offset)
  for j_offset in range(-max_j_offset, max_j_offset + 1):
    assert abs(i_offset) + abs(j_offset) <= dist_thresh
    offset_within_thresh.append((i_offset, j_offset))

num_steps_saved_list = []
threshold_steps_saved = 50 if 'test' in filename else 100
for start in tqdm.tqdm(open_positions[:-1], total=len(open_positions)-1):
  i, j = start
  # Sweep over all possible end satisfying distance(start, end) <= dist_thresh
  for i_off, j_off in offset_within_thresh:
    end = (i + i_off, j + j_off)
    # Skip if `end` is not an open position or doesn't come after `start`.
    if end not in labels or labels[end] <= labels[start]:
      continue
    num_steps_saved = num_steps(start, end) - distance(start, end)
    if num_steps_saved >= threshold_steps_saved:
      num_steps_saved_list.append(num_steps_saved)

if 'test' in filename:
  # Count number of positions for each num_steps_saved.
  counts = {}
  for num in num_steps_saved_list:
      counts[num] = counts.get(num, 0) + 1
  # Print counts
  for value, count in sorted(counts.items()):
      print(f"There are {count} instances of {value} steps saved")
else:
  print('Part 2:', len(num_steps_saved_list))