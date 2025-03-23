import collections

def import_txt_file_as_array(filename: str) -> list[list[str]]:
  with open(filename, 'r') as file:
    return [list(line.strip()) for line in file]

filename = 'inputs/day12.txt'
# filename = 'inputs/day12_test.txt'
map_arr = import_txt_file_as_array(filename)
nrow = len(map_arr)
ncol = len(map_arr[0])

# For each value, gather the corresponding indices
index_dict = collections.defaultdict(list)
for i, row in enumerate(map_arr):
  for j, plant in enumerate(row):
    index_dict[plant].append((i, j))
# print(index_dict)

# Get unique plants of the array
unique_plants = list(index_dict.keys())
print(unique_plants)

# For each plant type, partition the list of indices into different regions.
# For each index, also record the number of neighbouring plants of the same type
# (to be used for perimeter computation).
num_neighbours = collections.defaultdict(int)  # {index: num_neighbours}
region_dict = {}  # {index: region}
region = 0
for plant, fixed_indices in index_dict.items():
  indices = fixed_indices.copy()
  while indices:
    cur_index = indices.pop()
    region_indices = [cur_index]
    while region_indices:
      i, j = region_indices.pop()
      # Make sure that (i, j) exists in `num_neighbours`.
      num_neighbours[(i, j)] = 0
      region_dict[(i, j)] = region
      neighbour_candidates = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
      for c in neighbour_candidates:
        if c in indices:
          # If c in region, move from indices to region_indices
          indices.remove(c)
          region_indices.append(c)
        if c in fixed_indices:
          num_neighbours[(i, j)] += 1
    region += 1
assert region_dict.keys() == num_neighbours.keys()
# Using these two dicts, create a dict of form {region: list[perim_contrib]}
regions_and_perim_list = collections.defaultdict(list)
for k in region_dict.keys():
  region = region_dict[k]
  nn = num_neighbours[k]
  perim = 4 - nn  # Note that 4 - nn is the contribution of plant to the perim.
  regions_and_perim_list[region].append(perim)

# Compute total price
total_price = 0
for region, perim_list in regions_and_perim_list.items():
  price = len(perim_list) * sum(perim_list)
  total_price += price
  # print(price)
print('Part 1:', total_price)

# Get list of indices for each region.
indices_per_region = collections.defaultdict(list)
for index in region_dict.keys():
  region = region_dict[index]
  indices_per_region[region].append(index)

def num_consecutive_stretches(int_list: list[int]) -> int:
  # Compute number of consecutive stretches of integers.
  # e.g. [1,2,3,4,6,7,9,10,11] has 3 consecutive stretches
  # (1,2,3,4), (6,7), (9,10,11)
  if not int_list:
    return 0
  assert sorted(int_list) == int_list, int_list
  stretch_count = 1
  for i in range(1, len(int_list)):
    # If there is a gap bigger than 1, we've found a new stretch 
    if int_list[i] - int_list[i-1] > 1:
      stretch_count += 1
  return stretch_count

# Part 2: Compute total cost with discounted perimeter.
# Compute discounted perimeter given a list of indices.
def discounted_perimeter(indices: list[tuple[int, int]]) -> int:
  """
  Given min(i), max(i), min(j), max(j) among indices (i, j),
  sweep over i and j to count the number of top, bottom, left, right edges
  respectively.
  """
  row_indices = [i for (i, j) in indices]
  col_indices = [j for (i, j) in indices]
  min_row, max_row = min(row_indices), max(row_indices)
  min_col, max_col = min(col_indices), max(col_indices)
  # Count number of top edges
  num_top_edges = 0
  for i in range(min_row, max_row + 1):
    # Get columns for which (i-1, j) is not in indices,
    # but (i, j) is in indices.
    top_edge_cols = []
    for j in range(min_col, max_col + 1):
      if (i - 1, j) not in indices and (i, j) in indices:
        top_edge_cols.append(j)
    # Compute number of consecutive int stretches in top_edge_cols
    num_top_edges += num_consecutive_stretches(top_edge_cols)
  # Similarly count number of bottom edges
  num_bottom_edges = 0
  for i in range(min_row, max_row + 1):
    # Get columns for which (i+1, j) is not in indices,
    # but (i, j) is in indices.
    bottom_edge_cols = []
    for j in range(min_col, max_col + 1):
      if (i + 1, j) not in indices and (i, j) in indices:
        bottom_edge_cols.append(j)
    # Compute number of consecutive int stretches in top_edge_cols
    num_bottom_edges += num_consecutive_stretches(bottom_edge_cols)
  # Count number of left edges
  num_left_edges = 0
  for j in range(min_col, max_col + 1):
    # Get rows for which (i, j-1) is not in indices,
    # but (i, j) is in indices.
    left_edge_rows = []
    for i in range(min_row, max_row + 1):
      if (i, j - 1) not in indices and (i, j) in indices:
        left_edge_rows.append(i)
    # Compute number of consecutive int stretches in top_edge_cols
    num_left_edges += num_consecutive_stretches(left_edge_rows)
  # Similarly count number of right edges
  num_right_edges = 0
  for j in range(min_col, max_col + 1):
    # Get rows for which (i, j+1) is not in indices,
    # but (i, j) is in indices.
    right_edge_rows = []
    for i in range(min_row, max_row + 1):
      if (i, j + 1) not in indices and (i, j) in indices:
        right_edge_rows.append(i)
    # Compute number of consecutive int stretches in top_edge_cols
    num_right_edges += num_consecutive_stretches(right_edge_rows)
  return num_top_edges + num_bottom_edges + num_left_edges + num_right_edges

total_price = 0
for region, indices in indices_per_region.items():
  area = len(indices)
  num_edges = discounted_perimeter(indices)
  # print(area, num_edges)
  total_price += area * num_edges
print('Part 2:', total_price)


  
  
