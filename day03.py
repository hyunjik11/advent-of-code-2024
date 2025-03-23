import re

def compute_sum_product(content: str) -> int:
  # Get pair of integers in brackets, separated by a comma.
  p = re.compile(r'mul\([0-9]{1,3},[0-9]{1,3}\)')
  matches = p.findall(content)
  # print(matches)
  # Compute product for each match
  products = []
  p = re.compile('[0-9]{1,3}')
  for match in matches:
    numbers = [int(num) for num in p.findall(match)]
    assert len(numbers) == 2
    products.append(numbers[0] * numbers[1])
  # print(products)
  return sum(products)

# Read txt file as a single string
with open('inputs/day03.txt', 'r') as f:
  content = f.read()
# Remove newline strings
content = content.replace('\n', '')

# Test content
# content = (
#   "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
# )

# Part 1: Get valid `mul` instructions and compute sum of products
sum_product = compute_sum_product(content)
print('Part 1:', sum_product)

# Part 2: Compute sum of products for enabled `mul` instructions only
# First check whether instruction ends with `do()` or `don't()`
# Then get all disabled `mul` instructions accordingly
# and subtract from `sum(products)` computed in part 1.
p = re.compile(r"don't\(\)|do\(\)")
matches = p.findall(content)
if matches[-1] == "do()":
  print("instruction ends with `do()`")
  p = re.compile(r"don't\(\).*?do\(\)")
  disabled_matches = p.findall(content)
  print(matches)
  disabled_products = []
  for disabled_match in disabled_matches:
    assert disabled_match.count("do()") == 1
    disabled_products.append(compute_sum_product(disabled_match))
  print(f'{disabled_products=}')
else:
  # Haven't dealt with this case yet, but can be done by 
  # treating the final r"don't\(\).*" string separately.
  raise ValueError("instruction ends with `don't()`")
print('Part 2:', sum_product - sum(disabled_products))
