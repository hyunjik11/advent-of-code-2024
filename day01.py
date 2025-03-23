def import_txt_file(filename: str) -> tuple[list[int], list[int]]:
  column1 = []
  column2 = []
  
  with open(filename, 'r') as file:
    for line in file:
      num1, num2 = line.strip().split()
      column1.append(int(num1))
      column2.append(int(num2))
  
  return column1, column2

# Part 1: Compute total distance between sorted elements of two lists.
# Read numbers in file into lists.
list1, list2 = import_txt_file('inputs/day01.txt')
# Test with sample data:
# list1 = [3, 4, 2, 1, 3, 3]
# list2 = [4, 3, 5, 3, 9, 3]
list1 = sorted(list1)
list2 = sorted(list2)
# Sum distances between elements of lists
total_dist = 0
for x, y in zip(list1, list2):
  dist = abs(x - y)
  total_dist += dist
print(f'Part 1: {total_dist}')

# Part 2: Compute similarity score between the two sorted lists.
import collections
# Create a hastable for each list where key is the number and value is the
# count.
hash1 = collections.defaultdict(int)
hash2 = collections.defaultdict(int)
for num in list1:
  hash1[num] += 1
for num in list2:
  hash2[num] += 1
# Compute the similarity score by traversing through the keys of hash1
similarity_score = 0
for k, v1 in hash1.items():
  score = v1 * hash2[k] * k
  similarity_score += score
print('Part 2:', similarity_score)