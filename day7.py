import tqdm

def import_txt_file(filename: str) -> list[dict[int, list[int]]]:
  result = []
  with open(filename, 'r') as file:
    for line in file:
      key, values = line.strip().split(':')
      key = int(key)
      values = [int(x) for x in values.strip().split()]
      # Add to result as dict with single key-value pair
      result.append({key: values})
  return result

filename = 'day7.txt'
# filename = 'day7_test.txt'
# data[i] is a dict of the form {key: [v1, v2, ...]} representing
# a single line of the text file.
data = import_txt_file(filename)
num_keys = len(data)

# Part 1: Sum of keys for lines which can be made into an equation.
def is_valid(d):
  # Check if the dict d can be made into an equation.
  assert len(d) == 1
  k = list(d.keys())[0]  # k is int
  v = list(d.values())[0]  # v is list[int]
  if len(v) == 1:
    return k == v[0]
  # Denote d = {k: [v[0], ..., v[n]]}
  # d is valid if either {k - v[n]: [v[0], ..., v[n-1]]} is valid or
  # {k/v[n]: [v[0], ..., v[n-1]]} is valid, assuming v[n] divides k.
  k_new_mul = k // v[-1]
  k_new_add = k - v[-1]
  if k % v[-1] != 0:
    return is_valid({k_new_add: v[:-1]})
  else:
    return is_valid({k_new_mul: v[:-1]}) or is_valid({k_new_add: v[:-1]})

valid_keys = []
for d in tqdm.tqdm(data, total=num_keys):
  if is_valid(d):
    key = list(d.keys())[0]
    # print(key)
    valid_keys.append(key)
print(f'Part 1: {sum(valid_keys)}')

# Part 2: Sum of keys for lines which can be made into an equation
# Including the new concatenation operator.
def is_valid(d):
  # Check if the dict d can be made into an equation.
  assert len(d) == 1
  k = list(d.keys())[0]  # k is int
  v = list(d.values())[0]  # v is list[int]
  if len(v) == 1:
    return k == v[0]
  # Denote d = {k: [v[0], ..., v[n]]}
  # d is valid if either {k - v[n]: [v[0], ..., v[n-1]]} is valid or
  # {k/v[n]: [v[0], ..., v[n-1]]} is valid, assuming v[n] divides k.
  k_new_add = k - v[-1]
  add_valid = k_new_add >= 0
  if not add_valid:
    return False
  k_new_mul = k // v[-1]
  mul_valid = k % v[-1] == 0
  num_char = len(str(v[-1]))
  concat_valid = (str(v[-1]) == str(k)[-num_char:]) and v[-1] < k
  if concat_valid:
    k_new_concat = int(str(k)[:-num_char])
  
  if concat_valid:
    if mul_valid:
      return (
        is_valid({k_new_concat: v[:-1]}) or
        is_valid({k_new_mul: v[:-1]}) or
        is_valid({k_new_add: v[:-1]})
      )
    else:
      return is_valid({k_new_concat: v[:-1]}) or is_valid({k_new_add: v[:-1]})
  else:
    if mul_valid:
      return is_valid({k_new_mul: v[:-1]}) or is_valid({k_new_add: v[:-1]})
    else:
      return is_valid({k_new_add: v[:-1]})

valid_keys = []
for d in tqdm.tqdm(data, total=num_keys):
  if is_valid(d):
    key = list(d.keys())[0]
    # print(key)
    valid_keys.append(key)
print(f'Part 2: {sum(valid_keys)}')

