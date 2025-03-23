def import_txt_file(file_path: str) -> list[int]:
  with open(file_path, 'r') as file:
    for line in file:
      return list(map(int, line.strip()))

filename = 'inputs/day09.txt'
# filename = 'inputs/day09_test.txt'
int_list = import_txt_file(filename)
# print(int_list)

# Check that length of list is odd
assert len(int_list) % 2 == 1
# print(len(int_list))
# Get largest integer of fragmented file layout
max_int = len(int_list) // 2
# Get total space required for unfragmented file
required_space = sum(int_list[::2])
# Get list of file IDs with repetition
file_ids = []
for i, num_int in enumerate(int_list[::2]):
  file_ids += [i]*num_int
# print(file_ids)

# Part 1: Compute checksum
# First compute a list of integers that corresponds to the
# fragmented file layout.
fragmented_list = []
for i, num_int in enumerate(int_list):
  # Check whether num_int corresponds to file ID or free space
  if i % 2 == 0:
    # For file ID, the file ID should equal `(i - 1)/2`
    id = i // 2
    fragmented_list += [id]*num_int
  else:
    # For free space, we need to add on file ID by popping from `file_ids`.
    for _ in range(num_int):
      id = file_ids.pop()
      fragmented_list.append(id)
  
  # Criterion for stopping
  if len(fragmented_list) >= required_space:
    break

# Ignore tail
fragmented_list = fragmented_list[:required_space]
# print(fragmented_list)

# Compute checksum
checksum = sum([i * x for i, x in enumerate(fragmented_list)])
print('Part 1:', checksum)

# Part 2: Compute checksum by moving whole files.
# `file_id_counts[i]` is the number of ID i values in file
file_id_counts = int_list[::2]
# print(file_id_counts)

# `space_counts[i]` is the number of spaces between file ID `i` and `i+1`.
space_counts = int_list[1::2]
# print(space_counts)

# `file_id_pos_start_end[i] = (j, k)` means in the unfragmented file,
# file ID `i` starts at position `j` and ends at position `k`,
# so there are `k - j` values of file ID `i`.
# Similarly `space_pos_start_end[i] = (j, k)` means the `i`th space
# starts at position `j` and ends at position `k`.
cur_pos = file_id_counts[0]
file_id_pos_start_end = [(0, cur_pos)]
space_pos_start_end = []
for count, space_count in zip(file_id_counts[1:], space_counts):
  space_pos_start_end.append((cur_pos, cur_pos + space_count))
  cur_pos += space_count
  file_id_pos_start_end.append((cur_pos, cur_pos + count))
  cur_pos += count
# print(file_id_pos_start_end)

# `checksum_contrib[i]` is the checksum contribution of
# each file in unfragmented layout
checksum_contrib = []
for file_id, (start, end) in enumerate(file_id_pos_start_end):
  contrib = sum(list(range(start, end))) * file_id
  checksum_contrib.append(contrib)
# print(checksum_contrib)

# Now compute checksum contributions by looping through
# `file_id_pos_start_end` from end to start.
checksum = 0
for file_id, (start, end) in reversed(list(enumerate(file_id_pos_start_end))):
  file_size = end - start
  # Compute checksum contribution of file in the case it cannot be moved.
  contrib = sum(list(range(start, end))) * file_id
  # For each file, sweep across `space_pos_start_end` until
  # `space_start > start` i.e. only sweep spaces to the left of file,
  # and update checksum contribution if the file can be moved.
  for space_idx, (space_start, space_end) in enumerate(space_pos_start_end):
    # Break out of loop when done sweeping over spaces to left of file.
    if space_start > start:
      break
    space_size = space_end - space_start
    # File can be moved if space >= file_size
    if space_size >= file_size:
      # Update `space_pos_start_end` accordingly.
      new_space_start = space_start + file_size
      space_pos_start_end[space_idx] = (new_space_start, space_end)
      # Update contrib accordingly.
      contrib = sum(list(range(space_start, new_space_start))) * file_id
      break
  # print(f'{file_id=} has {contrib=}')
  checksum += contrib
print('Part 2:', checksum)