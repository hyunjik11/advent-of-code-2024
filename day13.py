import re

def extract_ints(string: str) -> list[int]:
    return [int(x) for x in re.findall(r'\d+', string)]

def import_data(filename: str) -> list[tuple[list[list[int]], list[int]]]:
  # For example:
  # Button A: X+94, Y+34
  # Button B: X+22, Y+67
  # Prize: X=8400, Y=5400
  # store this as two arrays [[94, 22], [34, 67]] and [8400, 5400]
  claws = []
  a = b = c = d = e = f = None
  with open (filename, 'r') as file:
    for line in file:
      line = line.strip()
      if line.startswith('Button A'):
        a, c = extract_ints(line)
      elif line.startswith('Button B'):
        b, d = extract_ints(line)
      elif line.startswith('Prize'):
        e, f = extract_ints(line)
      elif line == '':
        # Move to next set of arrays
        a = b = c = d = e = f = None
      else:
        raise ValueError(f'Invalid line: {line}')
      if a and b and c and d and e and f:
        claws.append(([[a, b], [c, d]], [e, f]))
  return claws

filename = 'inputs/day13.txt'
# filename = 'inputs/day13_test.txt'
claws = import_data(filename)
# print(claws)

# Part 1: Compute number of tokens needed to win as many prizes as possible
# Note that for a set of linear equations
# ax + by = e
# cx + dy = f
# There is a unique solution if ad - bc != 0.
# This solution is: x = (ed-bf)/(ad-bc), y = (af-ec)/(ad-bc).
# We need to check that the solutions x,y are non-negative integers.
# If ad - bc = 0, then there isn't a unique solution.
# We may check that this doesn't hold in our data with the assert below.
# So compute the unique solution for each claw,
# and check that the solutions are valid.
def compute_total_tokens(
    claws: list[tuple[list[list[int]], list[int]]], offset: int = 0
) -> int:
  total_tokens = 0
  for claw in claws:
    a = claw[0][0][0]
    b = claw[0][0][1]
    c = claw[0][1][0]
    d = claw[0][1][1]
    e = claw[1][0] + offset
    f = claw[1][1] + offset
    det = a * d - b * c
    assert det != 0, (a, b, c, d)
    x = (e * d - b * f) / det
    y = (a * f - e * c) / det
    if int(x) == x and int(y) == y and x >= 0 and y >= 0:
      tokens = x * 3 + y
      total_tokens += tokens
  return total_tokens

total_tokens = compute_total_tokens(claws)
print('Part 1:', int(total_tokens))

# Part 2: Repeat,  but after adding 10000000000000 to e and f.
total_tokens = compute_total_tokens(claws, offset=10000000000000)
print('Part 2:', int(total_tokens))
