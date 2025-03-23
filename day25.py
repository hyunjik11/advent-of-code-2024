from collections import defaultdict

def convert_pattern_to_int(arr: list[list[str]], type: str) -> list[int]:
  """Convert array of key/lock characters to list of ints."""
  if type == 'lock':
    arr = arr[1:]  # Ignore first line
  elif type == 'key':
    arr = arr[:-1]  # Ignore last line
  else:
    raise ValueError(f'Invalid {type=}')
  nrow = len(arr)
  out = []    
  for j in range(len(arr[0])):
    col = [arr[i][j] for i in range(nrow)]
    height = sum([x == '#' for x in col])
    out.append(height)
  return out

def import_data(filename: str) -> tuple[list[list[int]], list[list[int]]]:
  # Extract characters per line as array.
  out_dict = defaultdict(list)
  arr = []
  with open (filename, 'r') as file:
    for line in file:
      line = line.strip()
      if line == '':
        continue
      # Start from empty array
      if not arr:
        if line == '#####':
          type = 'lock'
        elif line == '.....':
          type = 'key'
        else:
          raise ValueError(f'Invalid first {line=}')
      arr.append([c for c in line])
      if len(arr) == 7:
        int_list = convert_pattern_to_int(arr, type)
        out_dict[type].append(int_list)
        arr = []
        continue
  return out_dict['lock'], out_dict['key']

filename = 'inputs/day25.txt'
# filename = 'inputs/day25_test.txt'
locks, keys = import_data(filename)
# print(locks)
# print(keys)

# Part 1: Find number of lock/key pairs that fit together.
num_kl_pairs = 0
for key in keys:
  for lock in locks:
    kl_sum = [k + l for k, l in zip(key, lock)]
    kl_sum_gt_5 = sum([x > 5 for x in kl_sum])
    if not kl_sum_gt_5:
      num_kl_pairs += 1
print('Part 1:', num_kl_pairs)