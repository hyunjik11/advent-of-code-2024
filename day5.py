import collections

def import_data(
    filename: str
) -> tuple[dict[int, list[int]], list[list[int]], set[int]]:
  # Express rules using a dict where key is the first number and
  # value is a list of second numbers.
  rules = collections.defaultdict(list)
  updates = []
  all_values = set()
  with open (filename, 'r') as file:
    section = 'top'
    for line in file:
      line = line.strip()
      # After reading blank line, switch to logic for
      # processing bottom section.
      if line == '':
        section = 'bottom'
        continue
      # Section 1:
      if section == 'top':
        p1, p2 = [int(x) for x in line.split('|')]
        rules[p1].append(p2)
      elif section == 'bottom':
        update = [int(x) for x in line.split(',')]
        all_values.update(update)
        updates.append(update)
      else:
        raise ValueError(f'Invalid section: {section}')
  return rules, updates, all_values

filename = 'day5.txt'
# filename = 'day5_test.txt'
rules, updates, all_values = import_data(filename)
# print(all_values)
# print(rules)
# print(updates)
# Check that there is a rule for every pair of values in updates.
num_distinct_values = len(all_values)
num_distinct_pairs = num_distinct_values * (num_distinct_values - 1) // 2
assert num_distinct_pairs == sum([len(v) for k, v in rules.items()])

# Part 1: Sum middle number of all correctly ordered updates.
total = 0
incorrect_updates = []
for update in updates:
  num_pages = len(update)
  # Check num pages in update is odd, so that unique middle exists
  assert num_pages % 2 == 1, update
  update_correct = True
  for i in range(num_pages - 1):
    page = update[i]
    next_pages = update[i + 1:]
    if not set(rules[page]) >= set(next_pages):
      update_correct = False
      incorrect_updates.append(update)
      # print('Incorrect update:', update)
      # print(rules[page])
      # print(next_pages)
      break
  if update_correct:
    total += update[num_pages // 2]
print('Part 1:', total)

# Part 2: For incorrect updates, reorder them correctly and
# sum their middle numbers (exclude originally correct udpates).
total = 0
for update in incorrect_updates:
  # For each number x in the update, find size of intersection btw
  # set(rules[x]) and set(update).
  # If size is 0, then x is the last element.
  # If size is len(update) - 1, then x is the first element.
  # So len(update) - 1 - size is the index of the correct position of x.
  num_pages = len(update)
  corrected_update = [None] * num_pages
  for x in update:
    idx = num_pages - 1 - len(set(update) & set(rules[x]))
    corrected_update[idx] = x
  assert None not in corrected_update
  # print('Corrected update:', corrected_update)
  total += corrected_update[num_pages // 2]
print('Part 2:', total)