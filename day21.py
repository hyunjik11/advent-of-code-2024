import math
from collections import defaultdict

def import_data(filename: str) -> list[str]:
  codes = []
  with open(filename, 'r') as file:
    for line in file:
      line = line.strip()
      codes.append(line)
  return codes

filename = 'day21.txt'
# filename = 'day21_test.txt'
codes = import_data(filename)
print(codes)

NUM2COORD = {
    'A': (2, 0), '0': (1, 0),
    '1': (0, 1), '2': (1, 1), '3': (2, 1),
    '4': (0, 2), '5': (1, 2), '6': (2, 2),
    '7': (0, 3), '8': (1, 3), '9': (2, 3),
}
DIR2COORD = {
  '<': (0, 0), 'v': (1, 0), '>': (2, 0), '^': (1, 1), 'A': (2, 1)
}


def num2dir(start: str, target: str) -> list[str]:
  """Directional commands for moving start->target on numerical keypad."""
  # Example input: start='3', target='7'
  # Example output: ['^^<<', '<<^^']
  # Convert start and target to coords, where 'A' is (2, 0) and '7' is (0, 3)
  start_x, start_y = NUM2COORD[start]
  target_x, target_y = NUM2COORD[target]
  xdiff = target_x - start_x
  ydiff = target_y - start_y
  # Based on the coordinate differences, compute the directional command.
  xdiff2dir_dict = {
    -2: '<<', -1: '<', 0: '', 1: '>', 2: '>>'
  }
  ydiff2dir_dict = {
    -3: 'vvv', -2: 'vv', -1: 'v', 0: '', 1: '^', 2: '^^', 3: '^^^'
  }
  xcommand = xdiff2dir_dict[xdiff]
  ycommand = ydiff2dir_dict[ydiff]
  # It's clear that when xcommand & ycommand are non-empty and one of them has
  # at least 2 commands, we don't want to interleave them, and either want
  # xcommand + ycommand or ycommand + xcommand, to minimize the number of
  # moves for the robot behind. Out of these two, ensure that we exclude cases
  # where the commands go over the gap to the left of '0'.
  if xcommand == '' or ycommand == '':
    # In this case, xcommand + ycommand == ycommand + xcommand
    return [xcommand + ycommand]
  if start_x == 0 and target_y == 0:
    # When starting from '1'/'4'/'7' and ending at '0'/'A',
    # ycommand + xcommand will go over the gap.
    # So only xcommand + ycommand is valid.
    return [xcommand + ycommand]
  if start_y == 0 and target_x == 0:
    # Conversely when starting from '0'/'A' and ending at '1'/'4'/'7',
    # xcommand + ycommand will go over the gap.
    # So only ycommand + xcommand is valid.
    return [ycommand + xcommand]
  # return both options in all other cases. 
  return [xcommand + ycommand, ycommand + xcommand]


def dir2dir(start: str, target: str) -> list[str]:
  """Directional commands for moving start->target on directional keypad."""
  # Example input: start='v', target='A'
  # Example output: dir_command=['>^', '^>']
  # Convert start and target to coords, where '<' is (0, 0) and 'A' is (2, 1)
  start_x, start_y = DIR2COORD[start]
  target_x, target_y = DIR2COORD[target]
  xdiff = target_x - start_x
  ydiff = target_y - start_y
  # Based on the coordinate differences, compute the directional command.
  xdiff2dir_dict = {
    -2: '<<', -1: '<', 0: '', 1: '>', 2: '>>'
  }
  ydiff2dir_dict = {
   -1: 'v', 0: '', 1: '^'
  }
  xcommand = xdiff2dir_dict[xdiff]
  ycommand = ydiff2dir_dict[ydiff]
  # It's clear that when xcommand & ycommand are non-empty and one of them has
  # at least 2 commands, we don't want to interleave them, and either want
  # xcommand + ycommand or ycommand + xcommand, to minimize the number of
  # moves for the robot behind. Out of these two, ensure that we exclude cases
  # where the commands go over the gap to the left of '0'.
  if xcommand == '' or ycommand == '':
    # In this case, xcommand + ycommand == ycommand + xcommand
    return [xcommand + ycommand]
  if start == '<' and target_y == 1:
    # When starting from '<' and ending at '^'/'A',
    # ycommand + xcommand will go over the gap.
    # So only xcommand + ycommand is valid.
    return [xcommand + ycommand]
  if start_y == 1 and target == '<':
    # Conversely when starting from '^'/'A' and ending at '<',
    # xcommand + ycommand will go over the gap.
    # So only ycommand + xcommand is valid.
    return [ycommand + xcommand]
  # return both options in all other cases. 
  return [xcommand + ycommand, ycommand + xcommand]


# Part 1: Compute sum of complexities of codes in list.
# Note that the commands required would control robot3 that controls robot2
# that controls robot1. We need to work backwards:
# numerical_code -> dir_code_robot1 -> dir_code_robot2 -> dir_code_robot3
# The command we wish to obtain is dir_code_robot3.

# dir_code_robot{n} -> dir_code_robot{n+1}
def dirs2dirs(code: str) -> list[str]:
  """Directional commands for typing code on directional keypad."""
  # Example input: code='<A'
  # Example output: list of all possible commands ['<<vA>>^A', ...]
  # Prepend `A` to `code` as robot always starts at `A`
  code = 'A' + code
  command_list = ['']
  for start, target in zip(code[:-1], code[1:]):
    commands_from_start2target = dir2dir(start, target)
    command_list = [
      c + nc for c in command_list for nc in commands_from_start2target
    ]
    command_list = [c + 'A' for c in command_list]
  return command_list

# Get robot3's dir_code for each start & end number in `code` and
# compute complexities using the min length code.
complexity_list = []
for code in codes:
  code = 'A' + code
  code_min_dir_code_length = 0
  for start, target in zip(code[:-1], code[1:]):
    command_list = num2dir(start, target)
    command_list = [c + 'A' for c in command_list]
    # Get min_dir_code for each elt of command_list and add its length to 
    # min_command_length
    min_length_for_command = math.inf
    for dir_code1 in command_list:
      dir_code2_list = dirs2dirs(dir_code1)
      for dir_code2 in dir_code2_list:
        dir_code3_list = dirs2dirs(dir_code2)
        min_length_for_dir_code2 = min([len(x) for x in dir_code3_list])
        min_length_for_command = min(
          min_length_for_command, min_length_for_dir_code2
        )
    code_min_dir_code_length += min_length_for_command
  complexity = code_min_dir_code_length * int(code[1:-1])
  print('code:', code)
  print(f'length {code_min_dir_code_length}, numeric {int(code[1:-1])}')
  complexity_list.append(complexity)
print('Part 1:', sum(complexity_list))

# Part 2: Repeat above with 25+1 layers of robots instead of 2+1.
def recursive_nested_loop(dir_code: str, depth: int, max_depth: int) -> int:
  next_list = dirs2dirs(dir_code)
  if depth == max_depth:
    return min([len(x) for x in next_list])
  # print(f'{depth=}, len(next_list)={len(next_list)}')
  return min(
    [recursive_nested_loop(x, depth + 1, max_depth) for x in next_list]
  )

# However using the recursive noop naively will not be feasible for 25 loops.
# Instead, we'd like to figure out the optimal command for each pair of
# start & target number keys that have 2 choices
# xcommand+ycommand and ycommand+xcommand in num2dir, and also for each pair of
# start & target directional keys in dir2dir. To do this, let us use
# max_depth=3 to see if there is a difference between two commands.
max_depth = 3
candidate_start_target_numbers = [
  ('1', '5'),  # >^ or ^>
  ('1', '6'),  # >>^ or ^>>
  ('1', '8'),  # >^^ or ^^>
  ('1', '9'),  # >>^^ or ^^>>
  ('3', '5'),  # <^ or ^<
  ('3', '4'),  # <<^ or ^<<
  ('3', '8'),  # <^^ or ^^<
  ('3', '7'),  # <<^^ or ^^<<
]
# Also include the reverse directions
reverse_numbers = [(y, x) for (x, y) in candidate_start_target_numbers]
candidate_start_target_numbers += reverse_numbers
for start, target in candidate_start_target_numbers:
  command_list = num2dir(start, target)
  command_list = [c + 'A' for c in command_list]
  min_length_for_command_list = [
    recursive_nested_loop(x, 1, max_depth) for x in command_list
  ]
  assert len(min_length_for_command_list) == 2
  if min_length_for_command_list[0] < min_length_for_command_list[1]:
    min_idx = 0
    print_depth = max_depth
  elif min_length_for_command_list[0] > min_length_for_command_list[1]:
    min_idx = 1
    print_depth = max_depth
  else:
    # Increase the depth by 1 and redo.
    min_length_for_command_list = [
      recursive_nested_loop(x, 1, max_depth+1) for x in command_list
    ]
    print_depth = max_depth + 1
    if min_length_for_command_list[0] < min_length_for_command_list[1]:
      min_idx = 0
    elif min_length_for_command_list[0] > min_length_for_command_list[1]:
      min_idx = 1
    else:
      min_idx = 0
      print(f'{start=}, {target=}: both commands have same min length')
  c = command_list[min_idx]
  l = min_length_for_command_list[min_idx]
  print(f'{start=}, {target=}: {c} len={l} at depth {print_depth}')

# From the above, it's evident that for num2dir we should use:
# '^' and 'v' before '>'
# '<' before '^' and 'v'

# Repeat analysis for dir2dir:
max_depth = 3
candidate_start_target_dirs = [
  ('v', 'A'),  # >^ or ^>
  ('>', '^'),  # <^ or ^<
]
# Also include the reverse directions
reverse_dirs = [(y, x) for (x, y) in candidate_start_target_dirs]
candidate_start_target_dirs += reverse_dirs
for start, target in candidate_start_target_dirs:
  command_list = dir2dir(start, target)
  command_list = [c + 'A' for c in command_list]
  min_length_for_command_list = [
    recursive_nested_loop(x, 1, max_depth) for x in command_list
  ]
  assert len(min_length_for_command_list) == 2
  if min_length_for_command_list[0] < min_length_for_command_list[1]:
    min_idx = 0
    print_depth = max_depth
  elif min_length_for_command_list[0] > min_length_for_command_list[1]:
    min_idx = 1
    print_depth = max_depth
  else:
    # Increase the depth by 1 and redo.
    min_length_for_command_list = [
      recursive_nested_loop(x, 1, max_depth+1) for x in command_list
    ]
    print_depth = max_depth + 1
    if min_length_for_command_list[0] < min_length_for_command_list[1]:
      min_idx = 0
    elif min_length_for_command_list[0] > min_length_for_command_list[1]:
      min_idx = 1
    else:
      min_idx = 0
      print(f'{start=}, {target=}: both commands have same min length')
  c = command_list[min_idx]
  l = min_length_for_command_list[min_idx]
  print(f'{start=}, {target=}: {c} len={l} at depth {print_depth}')

# From the above, it's evident that for dir2dir we should use:
# '^' and 'v' before '>'
# '<' before '^' and 'v'
# Same observations as num2dir.
# Use this information to modify num2dir and dir2dir

def num2dir_opt(start: str, target: str) -> str:
  """Directional command for moving start->target on numerical keypad."""
  # Example input: start='3', target='7'
  # Example output: '<<^^'
  # Convert start and target to coords, where 'A' is (2, 0) and '7' is (0, 3)
  start_x, start_y = NUM2COORD[start]
  target_x, target_y = NUM2COORD[target]
  xdiff = target_x - start_x
  ydiff = target_y - start_y
  # Based on the coordinate differences, compute the directional command.
  xdiff2dir_dict = {
    -2: '<<', -1: '<', 0: '', 1: '>', 2: '>>'
  }
  ydiff2dir_dict = {
    -3: 'vvv', -2: 'vv', -1: 'v', 0: '', 1: '^', 2: '^^', 3: '^^^'
  }
  xcommand = xdiff2dir_dict[xdiff]
  ycommand = ydiff2dir_dict[ydiff]
  # It's clear that when xcommand & ycommand are non-empty and one of them has
  # at least 2 commands, we don't want to interleave them, and either want
  # xcommand + ycommand or ycommand + xcommand, to minimize the number of
  # moves for the robot behind. Out of these two, ensure that we exclude cases
  # where the commands go over the gap to the left of '0'.
  if xcommand == '' or ycommand == '':
    # In this case, xcommand + ycommand == ycommand + xcommand
    return xcommand + ycommand
  if start_x == 0 and target_y == 0:
    # When starting from '1'/'4'/'7' and ending at '0'/'A',
    # ycommand + xcommand will go over the gap.
    # So only xcommand + ycommand is valid.
    return xcommand + ycommand
  if start_y == 0 and target_x == 0:
    # Conversely when starting from '0'/'A' and ending at '1'/'4'/'7',
    # xcommand + ycommand will go over the gap.
    # So only ycommand + xcommand is valid.
    return ycommand + xcommand
  # For remaining cases, stick to the following rule observed above:
  # '^' and 'v' before '>'
  # '<' before '^' and 'v'
  if '>' in xcommand:
    return ycommand + xcommand
  if '<' in xcommand:
    return xcommand + ycommand
  raise ValueError('Not all cases have been covered')

def dir2dir_opt(start: str, target: str) -> str:
  """Directional command for moving start->target on directional keypad."""
  # Example input: start='v', target='A'
  # Example output: dir_command='^>'
  # Convert start and target to coords, where '<' is (0, 0) and 'A' is (2, 1)
  start_x, start_y = DIR2COORD[start]
  target_x, target_y = DIR2COORD[target]
  xdiff = target_x - start_x
  ydiff = target_y - start_y
  # Based on the coordinate differences, compute the directional command.
  xdiff2dir_dict = {
    -2: '<<', -1: '<', 0: '', 1: '>', 2: '>>'
  }
  ydiff2dir_dict = {
   -1: 'v', 0: '', 1: '^'
  }
  xcommand = xdiff2dir_dict[xdiff]
  ycommand = ydiff2dir_dict[ydiff]
  # It's clear that when xcommand & ycommand are non-empty and one of them has
  # at least 2 commands, we don't want to interleave them, and either want
  # xcommand + ycommand or ycommand + xcommand, to minimize the number of
  # moves for the robot behind. Out of these two, ensure that we exclude cases
  # where the commands go over the gap to the left of '0'.
  if xcommand == '' or ycommand == '':
    # In this case, xcommand + ycommand == ycommand + xcommand
    return xcommand + ycommand
  if start == '<' and target_y == 1:
    # When starting from '<' and ending at '^'/'A',
    # ycommand + xcommand will go over the gap.
    # So only xcommand + ycommand is valid.
    return xcommand + ycommand
  if start_y == 1 and target == '<':
    # Conversely when starting from '^'/'A' and ending at '<',
    # xcommand + ycommand will go over the gap.
    # So only ycommand + xcommand is valid.
    return ycommand + xcommand
  # For remaining cases, stick to the following rule observed above:
  # '^' and 'v' before '>'
  # '<' before '^' and 'v'
  if '>' in xcommand:
    return ycommand + xcommand
  if '<' in xcommand:
    return xcommand + ycommand
  raise ValueError('Not all cases have been covered')

# Note that for dirs2dirs, the length of the commands will increase by a factor
# of 2~3 for each depth, which makes it very slow to iterate over commands at
# depth=25. So instead, use the observation that:
# given input code, if we know the counts of adjacent pairs, we can get the
# counts of adjacent pairs of output code. Then this can be used to compute the
# length of the code.
# Compute conversion table for dir codes, of the form:
# {(start, target): {(start_code, target_code): count}}
DIR_CONVERSION = {}
for start in DIR2COORD.keys():
  for target in DIR2COORD.keys():
    code = 'A' + dir2dir_opt(start, target) + 'A'
    # Assemble counts of adjacent pairs of 'code'
    code_pair_counts = defaultdict(int)
    for x, y in zip(code[:-1], code[1:]):
      code_pair_counts[(x, y)] += 1
    DIR_CONVERSION[(start, target)] = dict(code_pair_counts)
# for k, v in DIR_CONVERSION.items():
#   print(f'{k=}: {v=}')

def count2count(count_dict: dict[str, int]) -> dict[str, int]:
  # Note that count_dict includes the initial 'A'.
  out_dict = defaultdict(int)
  for code_pair, count in count_dict.items():
    count_dict_deeper = DIR_CONVERSION[(code_pair)]
    for code_pair_deeper, count_deeper in count_dict_deeper.items():
      out_dict[code_pair_deeper] += count * count_deeper
  return out_dict

def apply_n_times(func, x, n):
    """Apply function func to x, n times recursively."""
    if n == 0:
        return x
    return apply_n_times(func, func(x), n - 1)

max_depth = 25
complexity_list = []
for code in codes:
  code = 'A' + code
  code_min_dir_code_length = 0
  for start, target in zip(code[:-1], code[1:]):
    print(f'{code=}: {start=}, {target=}')
    command = 'A' + num2dir_opt(start, target) + 'A'
    # Get counts of adjacent pairs in `command`
    count_dict = defaultdict(int)
    for x, y in zip(command[:-1], command[1:]):
      count_dict[(x, y)] += 1
    # Get count dict after max_depth recursive applications.
    count_dict = apply_n_times(count2count, count_dict, max_depth)
    code_min_dir_code_length += sum(count_dict.values())
  complexity = code_min_dir_code_length * int(code[1:-1])
  print('code:', code)
  print(f'length {code_min_dir_code_length}, numeric {int(code[1:-1])}')
  complexity_list.append(complexity)
print('Part 2:', sum(complexity_list))
