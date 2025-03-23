import re

def import_txt_file_as_array(filename: str) -> list[list[str]]:
  with open(filename, 'r') as file:
    return [list(line.strip()) for line in file]

def count_occurrences(pattern: str, text: str) -> int:
  # Count number of occurrences of pattern in text
  # with overlaps allowed.
  # Special characters become escaped
  # e.g. "hello.world*" -> "hello\.world\*"
  escaped_pattern = re.escape(pattern)
  regex = f'(?=({escaped_pattern}))'
  return len(re.findall(regex, text))

def list_to_str(list_of_chars):
  # Convert list of characters to string
  return ''.join(list_of_chars)

filename = 'day4.txt'
# filename = 'day4_test.txt'
letters = import_txt_file_as_array(filename)
nrow = len(letters)
ncol = len(letters[0])  # Assumes that all rows have same num cols
minrc = min(nrow, ncol)
print(f'{nrow=}, {ncol=}')

# Test list_to_str and count_occurrences
# print(list_to_str(letters[0]))
# print(count_occurrences('XMAS', list_to_str(letters[0])))
# print(count_occurrences('SAMX', list_to_str(letters[0])))
# print(list_to_str(letters[1]))
# print(count_occurrences('XMAS', list_to_str(letters[1])))
# print(count_occurrences('SAMX', list_to_str(letters[1])))

# Part 1: Count number of occurrences of 'XMAS' and 'SAMX' in
# rows/cols/diagonals
target = "XMAS"
tegrat = target[::-1]
print(f'{target=}, {tegrat=}')
count = 0
# Count occurrences in rows
for row in range(nrow):
  row_letters = list_to_str(letters[row])
  count += count_occurrences(target, row_letters)
  count += count_occurrences(tegrat, row_letters)
# Count occurrences in cols
for col in range(ncol):
  col_letters = list_to_str([letters[row][col] for row in range(nrow)])
  count += count_occurrences(target, col_letters)
  count += count_occurrences(tegrat, col_letters)
# Count occurrences in TL->BR diagonals
init_rows = list(range(nrow - 1, 0, -1)) + [0]*ncol
init_cols = [0]*nrow + list(range(1, ncol))
for row, col in zip(init_rows, init_cols):
  diag_letters = list_to_str([
    letters[row + i][col + i] for i in range(0, minrc - (row + col))
  ])
  count += count_occurrences(target, diag_letters)
  count += count_occurrences(tegrat, diag_letters)
# Count occurrences in TR->BL diagonals
init_rows = [0]*ncol + list(range(1, nrow))
init_cols = list(range(ncol - 1)) + [ncol - 1]*nrow
for row, col in zip(init_rows, init_cols):
  diag_letters = list_to_str([
    letters[row + i][col - i] for i in range(0, col - row + 1)
  ])
  count += count_occurrences(target, diag_letters)
  count += count_occurrences(tegrat, diag_letters)

print('Part 1:', count)

# Part 2: Count number of X-MAS patterns.
# There are 4 possible patterns:
# M.S | M.M | S.S | S.M
# .A. | .A. | .A. | .A.
# M.S | S.S | M.M | S.M
def is_pattern(arr: list[list[str]]) -> bool:
  # Given a 3x3 array, check whether it is a valid pattern.
  assert len(arr) == 3
  assert len(arr[0]) == len(arr[1]) == len(arr[2]) == 3
  # First check whether middle element is 'A'
  if arr[1][1] != 'A':
    return False
  # Check first & last rows
  valid_letters = [
    ('M', 'S', 'M', 'S'),
    ('M', 'M', 'S', 'S'),
    ('S', 'S', 'M', 'M'),
    ('S', 'M', 'S', 'M'),
  ]
  for (l1, l2, l3, l4) in valid_letters:
    if (
      arr[0][0] == l1 and arr[0][2] == l2 and
      arr[2][0] == l3 and arr[2][2] == l4
    ):
      return True

  return False
# Iterate through array to count number of valid patterns.
count = 0
for row in range(nrow - 2):
  for col in range(ncol - 2):
    subarr = [letters[row + i][col:col + 3] for i in range(3)]
    if is_pattern(subarr):
      count += 1
print('Part 2', count)
