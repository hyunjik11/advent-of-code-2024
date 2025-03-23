import math
import tqdm

def import_txt_file(filename: str) -> list[int]:
  with open(filename, 'r') as file:
    for line in file:
      return [int(x) for x in line.strip().split()]

filename = 'inputs/day11.txt'
# filename = 'inputs/day11_test.txt'
stones = import_txt_file(filename)
print(stones)

def num_digits(x: int) -> int:
  assert x > 0, x
  return math.floor(math.log10(x)) + 1

def blink(stones: list[int]) -> list[int]:
  new_stones = []
  for x in stones:
    if x == 0:
      new_stones.append(1)
    else:
      nd = num_digits(x)
      hnd = nd // 2
      if nd % 2 == 0:
        div = 10 ** hnd
        x1 = x // div
        x2 = x % div
        new_stones += [x1, x2]
      else:
        new_stones.append(x * 2024)
  return new_stones

# Part 1: Compute total no stones after 25 blinks.
num_blinks = 25
for _ in range(num_blinks):
  stones = blink(stones)
  # print(stones)
print('Part 1:', len(stones))

# Part 2: Compute total no stones after 75 blinks.
# This method takes too long for high number of blinks
# because the length of `stones` grows exponentially.
# Note that "blink" has the additive property on lists:
# blink(a + b) = blink(a) + blink(b)
# for lists a, b. So we have that
# blink^n(a + b) = blink^n(a) + blink^n(b)
# So we can focus on obtaining blink^n([x]) for each value of x.
# Note that in order to compute len

# Hence we can pre-compute blink^n(a) for small values of a and n,
# then use this to speed up the computation.
# Store these as a tree, continuing to expand new nodes that aren't already
# part of the tree. Let root node be -1, and its children are:
# 0, 1, ..., MAX_A - 1.
from treelib import Tree
init_stones = list(range(10)) + list(range(100, 1000))
# Add extra stones from file
file_stones = import_txt_file(filename)
init_stones = list(set(init_stones) | set(file_stones))
unique_tags = set()
print('Precomputing tree:')
tree = Tree()
tree.create_node("-1", -1)
stones = init_stones.copy()
for i in stones:
  tree.create_node(str(i), i, parent=-1)
  unique_tags.add(i)
while stones:
  stones_next = []
  for x in stones:
    children = blink([x])
    for child in children:
      if tree.contains(child):
        # Use random id for node whose id already exists,
        # using the tag to specify the number.
        tree.create_node(str(child), parent=x)
      else:
        tree.create_node(str(child), child, parent=x)
        unique_tags.add(child)  
        stones_next.append(child)
  stones = stones_next
print(tree.show(stdout=False))
print('tree depth:', tree.depth())
print('num unique_tags:', len(unique_tags))

# Traverse the nodes x to add values of len(blink^n(x)) for
# n up to max_num_blinks_precomputed.
# Store results in num_stones_at_depth such that
# num_stones_at_depth[(x, n)] = len(blink^n(x))
print('Precomputing num_stones_at_depth for each unique tag:')
max_num_blinks_precomputed = 10
num_stones_at_depth = {}
for x in tqdm.tqdm(unique_tags, total=len(unique_tags)):
  stones = [x]
  num_stones_at_depth[(x, 0)] = len(stones)
  for n in range(1, max_num_blinks_precomputed + 1):
    stones = blink(stones)
    num_stones_at_depth[(x, n)] = len(stones)

# Test that num_stones_at_depth is correct.
# node_id = 79424
# for n in range(max_num_blinks_precomputed + 1):
#   print(f'num_stones for {node_id}, {n=}', num_stones_at_depth[(node_id, n)])

# Use the tree to compute len(blink^n([a]))
# for a in tree and arbitrary n.
# Also cache function outputs so that count(a, n) is not re-computed
# for the same values of (a, n).
from functools import lru_cache
@lru_cache(maxsize=None)
def count(a: int, n: int) -> int:
  assert a in tree.nodes, a
  node = tree.get_node(a)
  # If num_stones_at_depth[(a, n)] is already known, return it.
  if (a, n) in num_stones_at_depth.keys():
    return num_stones_at_depth[(a, n)]
  # O/w sum up count(x, n - level(x)) for all
  # leaves x of subtree of a, where level(x) is the level of x
  # in the subtree.
  subtree = tree.subtree(a)
  counts = [
    count(int(x.tag), n - subtree.level(x.identifier)) for x in subtree.leaves()
  ]
  return sum(counts)

num_blinks = 75
total_count = 0
for x in file_stones:
  total_count += count(x, num_blinks)
print('Part 2:', total_count)