import numpy as np
import tqdm

def import_txt_file_as_array(filename: str) -> list[list[str]]:
  with open(filename, 'r') as file:
    return [list(line.strip()) for line in file]

filename = 'day6.txt'
# filename = 'day6_test.txt'
map_arr = import_txt_file_as_array(filename)
nrow = len(map_arr)
ncol = len(map_arr[0])
route = np.zeros((nrow, ncol, 4), dtype=np.int32)
# Convert map to 2D array of integers with 0 for ".", 1 for "#"
# and also get array of route as a [nrow, ncol, 4] binary array
# where the last dim indicates the direction of movement
# (0: top, 1: right, 2: bottom, 3: left)
# as well as indices of starting position "^".
for i, row in enumerate(map_arr):
  for j, val in enumerate(row):
    if val == ".":
      map_arr[i][j] = 0
    elif val == "#":
      map_arr[i][j] = 1
    else:
      assert val == "^"
      map_arr[i][j] = 0
      start_pos = (i, j)
# print(np.array(map_arr))

def valid_pos(pos: tuple[int, int]) -> bool:
  assert len(pos) == 2
  assert isinstance(pos[0], int)
  assert isinstance(pos[1], int)
  return 0 <= pos[0] <= nrow - 1 and 0 <= pos[1] <= ncol - 1

def valid_dir(direction: int) -> bool:
  assert isinstance(direction, int)
  return 0 <= direction <= 3

def is_dead_end(pos: tuple[int, int], direction: int) -> bool:
  # Check whether pos & direction is a dead end.
  top_end = pos[0] == 0 and direction == 0
  right_end = pos[1] == ncol - 1 and direction == 1
  bottom_end = pos[0] == nrow - 1 and direction == 2
  left_end = pos[1] == 0 and direction == 3
  if top_end or right_end or bottom_end or left_end:
    return True
  return False

def is_cyclic(pos: tuple[int, int], direction: int, route: np.ndarray) -> bool:
  # Check whether pos & direction has started a cyclic route.
  if route[pos[0]][pos[1]][direction] == 1:
    return True
  return False

def update(
    pos: tuple[int, int], direction: int, route: np.ndarray,
    map_arr: list[list[str]]
) -> tuple[tuple[int, int], int, np.ndarray]:
  """Update pos, direction, route after making one step."""
  # Update route
  route[pos[0]][pos[1]][direction] = 1

  # Update pos and direction according to the map.
  # If there is an obstacle in direction of movement, only update direction.
  # Otherwise only update pos.
  if direction == 0:
    # Check whether there is obstacle above:
    if map_arr[pos[0] - 1][pos[1]]:
      direction = 1
    else:
      pos = (pos[0] - 1, pos[1])
  elif direction == 1:
    if map_arr[pos[0]][pos[1] + 1]:
      direction = 2
    else:
      pos = (pos[0], pos[1] + 1)
  elif direction == 2:
    if map_arr[pos[0] + 1][pos[1]]:
      direction = 3
    else:
      pos = (pos[0] + 1, pos[1])
  elif direction == 3:
    if map_arr[pos[0]][pos[1] - 1]:
      direction = 0
    else:
      pos = (pos[0], pos[1] - 1)
  else:
    raise ValueError(f'Invalid direction: {direction}')
  # Check validity of new position and direction
  assert valid_pos(pos)
  assert valid_dir(direction)
  return pos, direction, route

# Part 1: Count number of positions in the route after traversal.
# Fill in the route array according to the map.
pos = start_pos
direction = 0
while True:
  # Check whether the route is finished. There are two scenarios:
  # 1. Dead end: position is at the border of map and direction is into wall.
  # 2. The route is cyclic and we've returned to a previous (pos, direction).
  if is_dead_end(pos, direction) or is_cyclic(pos, direction, route):
    break
  # Update after one step.
  pos, direction, route = update(pos, direction, route, map_arr)

# Make sure last position is included in route
route[pos[0]][pos[1]][direction] = 1

# Count number of positions in route.
print(np.sum(route, axis=-1))
count = np.count_nonzero(np.sum(route, axis=-1))
print('Part 1:', count)

# Part 2: Count number of new obstacle positions that get the guard stuck
# in a cycle.
def is_route_cyclic(pos, direction, map_arr):
  # Function to check whether a guard will get stuck in a cycle
  # for given starting pos, direction and map_arr.
  route = np.zeros((nrow, ncol, 4), dtype=np.int32)
  while True:
    # Check whether the route is finished. There are two scenarios:
    # 1. Dead end: position is at the border of map and direction is into wall.
    # 2. The route is cyclic and we've returned to a previous (pos, direction).
    if is_dead_end(pos, direction):
      return 0
    elif is_cyclic(pos, direction, route):
      return 1
    # Update after one step.
    pos, direction, route = update(pos, direction, route, map_arr)

# Test with known cycle-inducing obsatacle positions for test case.
# if filename == 'day6_test.txt':
#   guard_stuck_list = []
#   for r, c in [
#     (0, 0),  # False
#     (1, 1),  # False
#     (7, 8),  # False
#     (6, 3),  # True
#     (7, 6),  # True
#     (7, 7),  # True
#     (8, 1),  # True
#     (8, 3),  # True
#     (9, 7),  # True
#     ]:
#     new_map_arr = np.copy(map_arr)
#     new_map_arr[r][c] = 1
#     guard_stuck_list.append(is_route_cyclic(start_pos, 0, new_map_arr))
#   print(guard_stuck_list)

# Sweep over all possible obstacle positions among non-zero positions of
# route in part 1, and check whether the guard gets stuck in a cycle.
guard_stuck_list = []
row_idx, col_idx = np.nonzero(np.sum(route, axis=-1))
num_candidates = len(row_idx)
print('num_candidates:', num_candidates)
for r, c in tqdm.tqdm(zip(row_idx, col_idx), total=num_candidates):
  if (r, c) == start_pos:
    # Don't count starting position as a possible obstacle position.
    continue
  new_map_arr = np.copy(map_arr)
  new_map_arr[r][c] = 1
  guard_stuck_list.append(is_route_cyclic(start_pos, 0, new_map_arr))
print('Part 2:', sum(guard_stuck_list))

