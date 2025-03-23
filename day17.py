import re

def extract_ints(string: str) -> list[int]:
  # Also detect negative integers
  return [int(x) for x in re.findall(r'-?\d+', string)]

def import_data(filename: str):
  register_init = []
  with open (filename, 'r') as file:
    for line in file:
      line = line.strip()
      if line.startswith('Register'):
        reg_val = extract_ints(line)[0]
        register_init.append(reg_val)
      elif line.startswith('Program'):
        program = extract_ints(line)
  return register_init, program

filename = 'inputs/day17.txt'
# filename = 'inputs/day17_test.txt'

register_init, program = import_data(filename)
# print(register_init, program)

def combo_operand(operand: int, register: tuple[int, int, int]) -> int:
  if operand in [0, 1, 2, 3]:
    return operand
  elif operand in [4, 5, 6]:
    return register[operand - 4]
  else:
    raise ValueError(f'Invalid operand {operand}.')

def execute_op(
    program: list[int], register: tuple[int, int, int], pointer: int
) -> tuple[tuple[int, int, int], int, int | None]:
  assert pointer % 2 == 0, f'Pointer {pointer} is not even.'
  opcode = program[pointer]
  operand = program[pointer + 1]
  a, b, c = register
  out = None
  pointer_new = pointer + 2
  if opcode == 0:
    # Note below is equivalent to floor(a / 2**coperand)
    coperand = combo_operand(operand, register)
    a = a >> coperand
  elif opcode == 1:
    b = b ^ operand
  elif opcode == 2:
    coperand = combo_operand(operand, register)
    b = coperand % 8
  elif opcode == 3:
    if a == 0:
      pass
    else:
      pointer_new = operand
  elif opcode == 4:
    b = b ^ c
  elif opcode == 5:
    coperand = combo_operand(operand, register)
    out = coperand % 8
  elif opcode == 6:
    coperand = combo_operand(operand, register)
    b = a >> coperand
  elif opcode == 7:
    coperand = combo_operand(operand, register)
    c = a >> coperand
  else:
    raise ValueError(f'Invalid opcode {opcode}.')
  return (a, b, c), pointer_new, out, [opcode, operand]

# Part 1: Execute program and join output.
pointer = 0
register = tuple(register_init)
program_len = len(program)
output = []
print(program)
print('init:', register, pointer, None)
while pointer < program_len:
  register, pointer, out, etc = execute_op(program, register, pointer)
  print(etc, register, pointer, out)
  if out is not None:
    output.append(str(out))

joined_output = ','.join(output)
print(f'Part 1: {joined_output}')

# Part 2: Find smallest value of register A that gives output equal to program.
# Start from final value of program and work backwards.
# Note that this solution is specific to the given input program in day17.txt.
# It may not work for other programs.
# The program: 2,4,1,3,7,5,0,3,1,5,4,4,5,5,3,0 does the following:
# [2, 4]: b = a % 8
# [1, 3]: b = b ^ 3
# [7, 5]: c = a >> b
# [0, 3]: a = a >> 3
# [1, 5]: b = b ^ 5
# [4, 4]: b = b ^ c
# [5, 5]: out = b % 8
# [3, 0]: go back to top unless a == 0, in which case halt.
# Note that the program is a loop that keeps truncating the last 3 binary digits of a.
# And note that the initial values of b and c are unused in each round of program.
# b, c are completely determined by a.
# Let's start from the first 3 binary digits of a, that should give us the last output 0.
# We want the values of a in [0, 1, ..., 7] such that the output of the program is 0.
# Then repeat for the next 3 binary digits of a, to get the penultimate output 3, and so on.
# Note that there can be multiple values of a that give the same output.
# We need to keep all possible solutions, since the smallest solution for a given round's target
# may not be compatible with the next round's target.
# Let's keep these solutions in `binary_string_candidates`.
binary_string_candidates = ['']
targets_reversed = []
for target in program[::-1]:
  targets_reversed.append(target)
  old_binary_string_candidates = binary_string_candidates.copy()
  binary_string_candidates = []
  for binary_string in old_binary_string_candidates:
    for candidate_a in range(8):
      new_a = binary_string + bin(candidate_a)[2:].zfill(3)
      new_a = int(new_a, 2)
      register = (new_a, 0, 0)
      pointer = 0
      output = []
      while pointer < program_len:
        register, pointer, out, etc = execute_op(program, register, pointer)
        if out is not None:
          output.append(out)
      if output == targets_reversed[::-1]:
        valid_binary_string = binary_string + bin(candidate_a)[2:].zfill(3)
        binary_string_candidates.append(valid_binary_string)
  if not binary_string_candidates:
    raise ValueError(
      f'No valid binary strings for outputs {targets_reversed[::-1]}.'
    )
  for binary_string in binary_string_candidates:
    print(f'a={binary_string} gives outputs {targets_reversed[::-1]}')
# Now take the smallest of the valid binary strings.
smallest = sorted([int(x, 2) for x in binary_string_candidates])[0]
print(f'Part 2: {smallest}')