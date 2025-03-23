import re

def extract_ints(string: str) -> list[int]:
  # Also detect negative integers
  return [int(x) for x in re.findall(r'-?\d+', string)]

def import_data(
    filename: str
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
  # For example:
  # p=0,4 v=3,-3
  # store this as a tuple of two tuples ((0, 4), (3, -3))
  pos_vel = []
  with open (filename, 'r') as file:
    for line in file:
      line = line.strip()
      pv = extract_ints(line)
      assert len(pv) == 4, pv
      pv = ((pv[0], pv[1]), (pv[2], pv[3]))
      pos_vel.append(pv)
  return pos_vel

filename = 'inputs/day14.txt'
# filename = 'inputs/day14_test.txt'
if 'test' in filename:
  num_x = 11
  num_y = 7
else:
  num_x = 101
  num_y = 103
pos_vel = import_data(filename)
# print(pos_vel)

def future_pos(
      pos: tuple[int, int], vel: tuple[int, int], time: int,
) -> tuple[int, int]:
  # Compute location `time` seconds from `pos`.
  x, y = pos
  xv, yv = vel
  future_x = (x + time * xv) % num_x
  future_y = (y + time * yv) % num_y
  return (future_x, future_y)

def safety_factor(
    pos_indices: list[tuple[int, int]]
) -> int:
  # Compute safety factor from position indicies.
  # Split up position indices into quadrants.
  x_boundary = num_x // 2
  y_boundary = num_y // 2
  q1 = []  # Top left
  q2 = []  # Bottom left
  q3 = []  # Bottom right
  q4 = []  # Top right
  for x, y in pos_indices:
    if x < x_boundary and y < y_boundary:
      q1.append((x, y))
    elif x < x_boundary and y > y_boundary:
      q2.append((x, y))
    elif x > x_boundary and y > y_boundary:
      q3.append((x, y))
    elif x > x_boundary and y < y_boundary:
      q4.append((x, y))
    else:
      # Ignore positions on the boundaries.
      continue
  sf = len(q1) * len(q2) * len(q3) * len(q4)
  return sf

# Part 1: Compute safety factor after 100 seconds
time = 100
pos_indices = [future_pos(pos, vel, time) for (pos, vel) in pos_vel]
# print(pos_indices)
sf = safety_factor(pos_indices)
print('Part 1:', sf)

# Part 2: When are the robots arranged as a Christmas tree?
# Print the robot positions after each second, writing onto a txt file.
# 1. First, set times = list(range(1000)) and observe that there are some
# patterns that repeat every 103 steps, at 65, 168, 271 and so on.
# 2. Then set times = [65 + i*103 for i in range(100)] and scroll
# (with minimap in VScode) to see when the tree is visible.
times = [65 + i*103 for i in range(100)]
out_file = 'outputs/day14_part2_out.txt'
with open(out_file, 'w') as f:
  for time in times:
    f.write(f'{time=}:' + '\n')
    pos_indices = [future_pos(pos, vel, time) for (pos, vel) in pos_vel]
    # remove duplicates
    pos_indices = set(pos_indices)
    arrangement = [
      ['1' if (x, y) in pos_indices else '.' for x in range(num_x)]
      for y in range(num_y)
    ]
    for row in arrangement:
      # Join elements with space and add newline
      line = ''.join(row)
      f.write(line + '\n')
    


