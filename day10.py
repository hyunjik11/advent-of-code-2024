import collections

def import_txt_file(filename: str) -> list[list[int]]:
  map_arr = []
  with open(filename, 'r') as file:
    for line in file:
      row = [int(x) for x in line.strip()]
      map_arr.append(row)
  return map_arr

def reachable_neighbors(
    map_arr: list[list[int]], start_row: int, start_col: int
) -> list[tuple[int, int]]:
  # Given `starting row & col indices in `map_arr`,
  # return list of reachable neighbors.
  nrow = len(map_arr)
  ncol = len(map_arr[0])
  current_value = map_arr[start_row][start_col]
  assert 0 <= current_value < 9, current_value
  # Get list of 4 candidate neighboring indices (including starting indices)
  candidates = [
    (start_row - 1, start_col),
    (start_row + 1, start_col),
    (start_row, start_col - 1),
    (start_row, start_col + 1),
  ]
  # Only return valid indices.
  def cond(x):
    i, j = x
    return (
      0 <= i < nrow and 0 <= j < ncol and map_arr[i][j] == current_value + 1
    )
  valid = list(filter(cond, candidates))
  return valid

filename = 'inputs/day10.txt'
# filename = 'inputs/day10_test.txt'
map_arr = import_txt_file(filename)
# print(map_arr)

# Find indices of 0s in the map
zero_indices = []
for i, row in enumerate(map_arr):
  for j, val in enumerate(row):
    if val == 0:
      zero_indices.append((i, j))

# Part 1: For each 0 (trailhead), get count of 9s that are reachable
# via trails that increase by exactly 1 per step, then add up scores.
# 1. For each 0, get a set of indices of 1s that are reachable.
# 2. Get set of indices of 2s that are reachable from these 1s.
# 3. Repeat to get set of indices of 9s that are reachable.
score_list = []
for start in zero_indices:
  indices = collections.defaultdict(set)
  indices[0] = {start}
  for target in range(1, 10):
    # Break early if there are no valid reachable neighbours.
    if not indices[target - 1]:
      break
    for current_index in indices[target - 1]:
      i, j = current_index
      indices[target].update(reachable_neighbors(map_arr, i, j))
  score = len(indices[9])
  score_list.append(score)
  # print(f'zero at {start} has {score=}')
print(f'Part 1:', sum(score_list))

# Part 2: For each 0 (trailhead), get count of distinct trails to 9
# that increase by exactly 1 per step, then add up ratings.
# Repeat process above with lists instead of sets, to count distinct
# trails as separate elements of the list in `indices[9]`
score_list = []
for start in zero_indices:
  indices = collections.defaultdict(list)
  indices[0] = [start]
  for target in range(1, 10):
    # Break early if there are no valid reachable neighbours.
    if not indices[target - 1]:
      break
    for current_index in indices[target - 1]:
      i, j = current_index
      indices[target] += reachable_neighbors(map_arr, i, j)
  score = len(indices[9])
  score_list.append(score)
  # print(f'zero at {start} has {score=}')
print(f'Part 2:', sum(score_list))