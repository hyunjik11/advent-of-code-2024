def import_data(filename: str) -> tuple[list[list[str]], list[str]]:
  # There are two parts to the text file.
  # For top part, extract characters per line as array.
  # For bottom part, extract all lines as a single string.
  # Move onto bottom part when there is a blank line.
  part = 'top'
  map_arr = []
  moves = []
  with open (filename, 'r') as file:
    for line in file:
      if line.strip() == '':
        # Move to bottom part
        part = 'bottom'
        continue
      if part == 'top':
        map_arr.append(list(line.strip()))
      elif part == 'bottom':
        moves.append(line.strip())
      else:
        raise ValueError(f'Invlid {part=}')
    moves = ''.join(moves)
    return map_arr, moves

def find_pos(map_arr: list[list[str]]) -> tuple[int, int]:
  # Find position of lanternfish in map_arr.
  for i, row in enumerate(map_arr):
    for j, val in enumerate(row):
      if val == '@':
        return (i, j)

def find_first(source_list : list[str], target: str) -> int | None:
  # In source_list, find first element in list matching target.
  # If target not in source list, return None.
  for i, x in enumerate(source_list):
    if x == target:
      return i
  return None

def find_last(source_list : list[str], target: str) -> int | None:
  # In source_list, find last element in list matching target.
  # If target not in source list, return None.
  n = len(source_list)
  for i, x in enumerate(source_list[::-1]):
    if x == target:
      return n - 1 - i
  return None

def print_map(map_arr: list[list[str]]):
  str_to_print = ''
  for row in map_arr:
    row_to_print = ''.join(row)
    row_to_print += '\n'
    str_to_print += row_to_print
  print(str_to_print)
  

filename = 'day15.txt'
# filename = 'day15_test.txt'
# filename = 'day15_test2.txt'
map_arr, moves = import_data(filename)
# print_map(map_arr)
# print(moves)

# Part 1: Compute sum of coords of boxes 'O' after moving
# lanternfish '@' with moves.
# First identify position of lanternfish.
fish_pos = find_pos(map_arr)

# Iterate over moves to update map position.
for move in moves:
  i, j = fish_pos
  if move == '<':
    # Try moving left.
    left = map_arr[i][j-1]
    if left == '#':
      # Wall is in the way. Do nothing.
      pass
    elif left == '.':
      # left is free.
      fish_pos = (i, j-1)
      map_arr[i][j-1] = '@'
      map_arr[i][j] = '.'
    elif left == 'O':
      # Box is on the left. Check if it's movable.
      # Find the next '.' to the left, up to next '#'.
      # Only move if '.' appears after '#' in row.
      source_list = map_arr[i][:j-1]
      target_ind = find_last(source_list, target='.')
      block_ind = find_last(source_list, target='#')
      if target_ind is not None and target_ind > block_ind:
        # Box is movable as there is empty space to the left.
        # map_arr[i][target_ind:j] is '.O**O'
        # that should be turned into 'O**O@'
        for pos in range(target_ind, j-1):
          map_arr[i][pos] = 'O'
        fish_pos = (i, j-1)
        map_arr[i][j-1] = '@'
        map_arr[i][j] = '.'
    else:
      raise ValueError(f'map_arr[{i=}][{j-1=}] is {left}, which is invalid')
  elif move == '>':
    # Try moving right.
    right = map_arr[i][j+1]
    if right == '#':
      # Wall is in the way. Do nothing.
      pass
    elif right == '.':
      # right is free.
      fish_pos = (i, j+1)
      map_arr[i][j+1] = '@'
      map_arr[i][j] = '.'
    elif right == 'O':
      # Box is on the right. Check if it's movable.
      # Find the next '.' to the right, up to next '#'.
      # Only move if '.' appears before '#' in row.
      source_list = map_arr[i][j+2:]
      target_ind = find_first(source_list, target='.')
      block_ind = find_first(source_list, target='#')
      if target_ind is not None and target_ind < block_ind:
        # Note that `target_ind` above is relative to source_list,
        # so shift appropriately so that it's relative to map_arr[i].
        target_ind += j + 2
        # Box is movable as there is empty space to the right.
        # map_arr[i][j+1:target_ind+1] is 'O**O.'
        # that should be turned into '@O**O'
        fish_pos = (i, j+1)
        map_arr[i][j+1] = '@'
        map_arr[i][j] = '.'
        for pos in range(j+2, target_ind+1):
          map_arr[i][pos] = 'O'
    else:
      raise ValueError(f'map_arr[{i=}][{j+1=}] is {right}, which is invalid')
  elif move == '^':
    # Try moving up.
    up = map_arr[i-1][j]
    if up == '#':
      # Wall is in the way. Do nothing.
      pass
    elif up == '.':
      # up is free.
      fish_pos = (i-1, j)
      map_arr[i-1][j] = '@'
      map_arr[i][j] = '.'
    elif up == 'O':
      # Box is above. Check if it's movable.
      # Find the next '.' to the top, up to next '#'.
      # Only move if '.' appears before '#' in col.
      source_list = [map_arr[k][j] for k in range(i-1)]
      target_ind = find_last(source_list, target='.')
      block_ind = find_last(source_list, target='#')
      if target_ind is not None and target_ind > block_ind:
        # Box is movable as there is empty space to the top.
        # map_arr[target_ind:i][j] is '.O**O'
        # that should be turned into 'O**O@'
        for pos in range(target_ind, i-1):
          map_arr[pos][j] = 'O'
        # Update fish pos
        fish_pos = (i-1, j)
        map_arr[i-1][j] = '@'
        map_arr[i][j] = '.'
    else:
      raise ValueError(f'map_arr[{i-1=}][{j=}] is {up}, which is invalid')
  elif move == 'v':
    # Try moving down.
    down = map_arr[i+1][j]
    if down == '#':
      # Wall is in the way. Do nothing.
      pass
    elif down == '.':
      # down is free.
      fish_pos = (i+1, j)
      map_arr[i+1][j] = '@'
      map_arr[i][j] = '.'
    elif down == 'O':
      # Box is below. Check if it's movable.
      # Find the next '.' below, up to next '#'.
      # Only move if '.' appears before '#' in col.
      end = len(map_arr)
      source_list = [map_arr[k][j] for k in range(i+2, end)]
      target_ind = find_first(source_list, target='.')
      block_ind = find_first(source_list, target='#')
      if target_ind is not None and target_ind < block_ind:
        # Note that `target_ind` above is relative to source_list,
        # so shift appropriately so that it's relative to map_arr[:][j].
        target_ind += i + 2
        # Box is movable as there is empty space below.
        # map_arr[i+1:target_ind+1][j] is 'O**O.'
        # that should be turned into '@O**O'
        fish_pos = (i+1, j)
        map_arr[i+1][j] = '@'
        map_arr[i][j] = '.'
        for pos in range(i+2, target_ind+1):
          map_arr[pos][j] = 'O'
    else:
      raise ValueError(f'map_arr[{i+1=}][{j=}] is {down}, which is invalid')
  else:
    raise ValueError(f'{move=} is invalid')
  
# print_map(map_arr)

# Compute box coordinates and sum up.
sum_coords = 0
for i, row in enumerate(map_arr):
  for j, val in enumerate(row):
    if val == 'O':
      box_coord = 100*i + j
      sum_coords += box_coord
print('Part 1:', sum_coords)

# Part 2: Compute sum of coords of boxes '[]' in resized map
# after moving lanternfish '@' with moves.
def resize_map(map_arr: list[list[str]]) -> list[list[str]]:
  resized_map_arr = []
  for i, row in enumerate(map_arr):
    resized_row = []
    for j, val in enumerate(row):
      if val == '#' or val == '.':
        resized_row += [val, val]
      elif val == '@':
        resized_row += ['@', '.']
      elif val == 'O':
        resized_row += ['[', ']']
      else:
        raise ValueError(f'Unrecognized {val=}')
    resized_map_arr.append(resized_row)
  return resized_map_arr

map_arr, moves = import_data(filename)
map_arr = resize_map(map_arr)
# print_map(map_arr)
# print(moves)

# Then identify position of lanternfish.
fish_pos = find_pos(map_arr)

# Iterate over moves to update map position.
# For resized map, the logic for shifting boxes up/down
# changes (left/right stays the same, treating [] as OO)
# because the boxes have size 2, so only pushing one
# half of the box leads to both halves moving, also
# meaning that e.g. when moving boxes up, you might
# also move boxes that are not directly above the box
# immediately above. So need to identify boxes that
# will move together. Note that if any one of these boxes
# are blocked by '#', then all of them are blocked.
# e.g.
# Init:
##############
##......##..##
##..........##
##...[][]...##
##....[]....##
##.....@....##
##############
# Move ^:
##############
##......##..##
##...[][]...##
##....[]....##
##.....@....##
##..........##
##############
for move_no, move in enumerate(moves):
  i, j = fish_pos
  if move == '<':
    # Try moving left.
    left = map_arr[i][j-1]
    if left == '#':
      # Wall is in the way. Do nothing.
      pass
    elif left == '.':
      # left is free.
      fish_pos = (i, j-1)
      map_arr[i][j-1] = '@'
      map_arr[i][j] = '.'
    elif left == ']':
      # Box is on the left. Check if it's movable.
      # Find the next '.' to the left, up to next '#'.
      # Only move if '.' appears after '#' in row.
      source_list = map_arr[i][:j-1]
      target_ind = find_last(source_list, target='.')
      block_ind = find_last(source_list, target='#')
      if target_ind is not None and target_ind > block_ind:
        # Box is movable as there is empty space to the left.
        # map_arr[i][target_ind:j] is '.[**]'
        # that should be turned into '[**]@'
        assert (j - target_ind) % 2 == 1
        for pos in range(target_ind, j-2, 2):
          map_arr[i][pos] = '['
          map_arr[i][pos+1] = ']'
        fish_pos = (i, j-1)
        map_arr[i][j-1] = '@'
        map_arr[i][j] = '.'
    else:
      raise ValueError(f'map_arr[{i=}][{j-1=}] is {left}, which is invalid')
  elif move == '>':
    # Try moving right.
    right = map_arr[i][j+1]
    if right == '#':
      # Wall is in the way. Do nothing.
      pass
    elif right == '.':
      # right is free.
      fish_pos = (i, j+1)
      map_arr[i][j+1] = '@'
      map_arr[i][j] = '.'
    elif right == '[':
      # Box is on the right. Check if it's movable.
      # Find the next '.' to the right, up to next '#'.
      # Only move if '.' appears before '#' in row.
      source_list = map_arr[i][j+2:]
      target_ind = find_first(source_list, target='.')
      block_ind = find_first(source_list, target='#')
      if target_ind is not None and target_ind < block_ind:
        # Note that `target_ind` above is relative to source_list,
        # so shift appropriately so that it's relative to map_arr[i].
        target_ind += j + 2
        # Box is movable as there is empty space to the right.
        # map_arr[i][j+1:target_ind+1] is '[**].'
        # that should be turned into '@[**]'
        fish_pos = (i, j+1)
        map_arr[i][j+1] = '@'
        map_arr[i][j] = '.'
        assert (target_ind - j) % 2 == 1
        for pos in range(j+2, target_ind, 2):
          map_arr[i][pos] = '['
          map_arr[i][pos+1] = ']'
    else:
      raise ValueError(f'map_arr[{i=}][{j+1=}] is {right}, which is invalid')
  elif move == '^':
    # Try moving up.
    up = map_arr[i-1][j]
    if up == '#':
      # Wall is in the way. Do nothing.
      pass
    elif up == '.':
      # up is free.
      fish_pos = (i-1, j)
      map_arr[i-1][j] = '@'
      map_arr[i][j] = '.'
    elif up == '[' or ']':
      # Box is above. Check if it's movable.
      # Recursively find position of boxes to be moved together
      # at each row, until either:
      # 1. A box has '#' above so cannot be moved
      # or
      # 2. All boxes in row have '.' above, so can be moved.
      box_left_indices = set([(i-1, j) if up == '[' else (i-1, j-1)])
      box_right_indices = set([(i-1, j+1) if up == '[' else (i-1, j)])
      prev_box_indices = set()
      check_next_level = True
      while check_next_level:
        box_indices = box_left_indices | box_right_indices
        candidate_indices = box_indices - prev_box_indices
        next_level_indices_to_check = [
          (k-1, l) for (k, l) in candidate_indices
        ]
        # Overwrite prev_box_indices for next iteration.
        prev_box_indices = box_indices.copy()
        empty_space_indices = set()
        for k, l in next_level_indices_to_check:
          if map_arr[k][l] == '[':
            box_left_indices.add((k, l))
            box_right_indices.add((k, l+1))
          elif map_arr[k][l] == ']':
            box_right_indices.add((k, l))
            box_left_indices.add((k, l-1))
          elif map_arr[k][l] == '#':
            check_next_level = False
            boxes_movable = False
          else:
            assert map_arr[k][l] == '.'
            empty_space_indices.add((k, l))
        # If all indices are empty, then boxes are movable
        if len(empty_space_indices) == len(next_level_indices_to_check):
          check_next_level = False
          boxes_movable = True
      if boxes_movable:
        # First set boxes to be empty space.
        for k, l in box_left_indices | box_right_indices:
          map_arr[k][l] = '.'
        # Then set index above all boxes to be '[' or ']'
        for k, l in box_left_indices:
          map_arr[k - 1][l] = '['
        for k, l in box_right_indices:
          map_arr[k - 1][l] = ']'
        # Update fish pos
        fish_pos = (i-1, j)
        map_arr[i-1][j] = '@'
        map_arr[i][j] = '.'
    else:
      raise ValueError(f'map_arr[{i-1=}][{j=}] is {up}, which is invalid')
  elif move == 'v':
    # Try moving down.
    down = map_arr[i+1][j]
    if down == '#':
      # Wall is in the way. Do nothing.
      pass
    elif down == '.':
      # down is free.
      fish_pos = (i+1, j)
      map_arr[i+1][j] = '@'
      map_arr[i][j] = '.'
    elif down == '[' or ']':
      # Box is below. Check if it's movable.
      # Recursively find position of boxes to be moved together
      # at each row, until either:
      # 1. A box has '#' below so cannot be moved
      # or
      # 2. All boxes in row have '.' below, so can be moved.
      box_left_indices = set([(i+1, j) if down == '[' else (i+1, j-1)])
      box_right_indices = set([(i+1, j+1) if down == '[' else (i+1, j)])
      prev_box_indices = set()
      check_next_level = True
      while check_next_level:
        box_indices = box_left_indices | box_right_indices
        candidate_indices = box_indices - prev_box_indices
        next_level_indices_to_check = [
          (k+1, l) for (k, l) in candidate_indices
        ]
        # Overwrite prev_box_indices for next iteration.
        prev_box_indices = box_indices.copy()
        empty_space_indices = set()
        for k, l in next_level_indices_to_check:
          if map_arr[k][l] == '[':
            box_left_indices.add((k, l))
            box_right_indices.add((k, l+1))
          elif map_arr[k][l] == ']':
            box_right_indices.add((k, l))
            box_left_indices.add((k, l-1))
          elif map_arr[k][l] == '#':
            check_next_level = False
            boxes_movable = False
          else:
            assert map_arr[k][l] == '.'
            empty_space_indices.add((k, l))
        # If all indices are empty, then boxes are movable
        if len(empty_space_indices) == len(next_level_indices_to_check):
          check_next_level = False
          boxes_movable = True
      if boxes_movable:
        # First set boxes to be empty space.
        for k, l in box_left_indices | box_right_indices:
          map_arr[k][l] = '.'
        # Then set index below all boxes to be '[' or ']'
        for k, l in box_left_indices:
          map_arr[k + 1][l] = '['
        for k, l in box_right_indices:
          map_arr[k + 1][l] = ']'
        # Update fish pos
        fish_pos = (i+1, j)
        map_arr[i+1][j] = '@'
        map_arr[i][j] = '.'
    else:
      raise ValueError(f'map_arr[{i+1=}][{j=}] is {down}, which is invalid')
  else:
    raise ValueError(f'{move=} is invalid')
  # print(f'{move=}, {move_no=}')
  # print_map(map_arr)

# Compute box coordinates and sum up.
sum_coords = 0
for i, row in enumerate(map_arr):
  for j, val in enumerate(row):
    if val == '[':
      box_coord = 100*i + j
      sum_coords += box_coord
print('Part 2:', sum_coords)

    

