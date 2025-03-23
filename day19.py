def import_data(filename: str) -> tuple[tuple[str, ...], list[str]]:
  # There are two parts to the text file.
  # For top part, extract strings separated by comma as list.
  # For bottom part, extract strings on each line as an element of a list.
  part = 'top'
  designs = []
  with open (filename, 'r') as file:
    for line in file:
      if line.strip() == '':
        # Move to bottom part
        part = 'bottom'
        continue
      if part == 'top':
        patterns = line.strip().split(', ')
      elif part == 'bottom':
        designs.append(line.strip())
      else:
        raise ValueError(f'Invlid {part=}')
    return tuple(patterns), designs

filename = 'inputs/day19.txt'
# filename = 'inputs/day19_test.txt'
patterns, designs = import_data(filename)
# print(patterns)
# print(designs)

# Part 1: Find number of designs that can be constructed from patterns.
# We can use dynamic programming to solve this. Also cache results such that
# we don't recompute function for the same design multiple times.
from functools import lru_cache
@lru_cache(maxsize=None)
def is_possible(design: str) -> bool:
  """Check if target can be constructed from patterns."""
  if design in patterns:
    return True
  valid_init_patterns = [p for p in patterns if design.startswith(p)]
  if not valid_init_patterns:
    return False
  else:
    return any([is_possible(design[len(p):]) for p in valid_init_patterns])

num_possible_designs = 0
for design in designs:
  possible = is_possible(design)
  num_possible_designs += possible
  # if possible:
  #   print(f'{design} is possible.')
  # else:
  #   print(f'{design} is impossible.')
print('Part 1:', num_possible_designs)

# Part 2: Count the total number of distinct constructions of all designs.
@lru_cache(maxsize=None)
def num_possible(design: str, patterns: tuple[str]) -> bool:
  """Count number of distinct constructions of design from patterns."""
  if design in patterns:
    # Count number of ways each pattern can be constructed among patterns.
    valid_init_patterns_exclusive = tuple([
      p for p in patterns if p in design and p != design
    ])
    return 1 + num_possible(design, valid_init_patterns_exclusive)
  valid_init_patterns = [p for p in patterns if design.startswith(p)]
  if not valid_init_patterns:
    return 0
  else:
    return sum([
      num_possible(design[len(p):], patterns) for p in valid_init_patterns
    ])

num_distinct_design_constructions = 0
for design in designs:
  count = num_possible(design, patterns)
  num_distinct_design_constructions += count
  # print(f'{design} has {count=}')
print('Part 2:', num_distinct_design_constructions)