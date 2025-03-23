import tqdm
from collections import defaultdict

def import_data(filename: str) -> list[int]:
  numbers = []
  with open(filename, 'r') as file:
    for line in file:
      line = int(line.strip())
      numbers.append(line)
  return numbers

# Note this is equal to 2**24
PRUNE_NO = 2**24
assert PRUNE_NO == 16777216

filename = 'inputs/day22.txt'
# filename = 'inputs/day22_test.txt'
numbers = import_data(filename)
# numbers = [123]
# print(numbers)

def prune(n: int) -> int:
  """Efficient version of modulo 2**24 using binary arithmetic."""
  # Mask with 24 1s
  mask = (1 << 24) - 1
  return n & mask

def secret_number(n: int) -> int:
  """Compute next secret number."""
  # Multiply by 64, mix then prune
  # Note below is equivalent to ((64 * n) ^ n) % 2**24
  n = prune((n << 6) ^ n) 
  # Divide by 32, round down, mix then prune.
  # Note below is equivalent to (math.floor(n / 32) ^ n) % 2**24
  n = prune((n >> 5) ^ n)
  # Multiply by 2048, mix then prune.
  # Note below is equivalent to ((2048 * n) ^ n) % 2**24
  n = prune((n << 11) ^ n)
  return n

# Part 1: Get sum of secret numbers after 2000 iterations.
num_iter = 2000
new_secret_numbers = []
for n in tqdm.tqdm(numbers, total=len(numbers)):
  for _ in range(num_iter):
    n = secret_number(n)
  new_secret_numbers.append(n)
print('Part 1:', sum(new_secret_numbers))

# Part 2: Get largest number of bananas that can be obtained.
# First construct array of 1st digits of the secret numbers, where we have
# one row per buyer and one column per iteration.

# Note that the test case for part 2 is different to that of part 1.
if 'test' in filename:
  numbers = [1, 2, 3, 2024]

price_array = []
for n in tqdm.tqdm(numbers, total=len(numbers)):
  prices = [n % 10]
  for _ in range(num_iter):
    n = secret_number(n)
    prices.append(n % 10)
  price_array.append(prices)
nrow = len(price_array)
ncol = len(price_array[0])
print(f'price_array is an {nrow}x{ncol} array')

# Based on price_array, construct an array of size nrow x (ncol-4)
# where entry [i][j] is a 4-tuple showing the price differences up to
# price_array[i][j+4].
seq_array = []
for i in tqdm.tqdm(range(nrow), total=nrow):
  row = []
  for j in range(ncol - 4):
    a, b, c, d, e = price_array[i][j:j+5]
    row.append((b-a, c-b, d-c, e-d))
  seq_array.append(row)

# Get sum of prices for each value of seq_array, but only using the first
# occurrence of the sequence in each row.
prices = defaultdict(int)
for i, row in enumerate(seq_array):
  seq_occurrences_in_row = {}
  for j, seq in enumerate(row):
    if seq not in seq_occurrences_in_row:
      prices[seq] += price_array[i][j+4]
    # placeholder to mark that seq has already occurred.
    seq_occurrences_in_row[seq] = 1

# Get highest price
max_price = max(list(prices.values()))
print('Part 2:', max_price)
