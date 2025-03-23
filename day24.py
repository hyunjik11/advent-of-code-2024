from collections import defaultdict

def import_data(
    filename: str
) -> tuple[list[tuple[str, int]], list[tuple[set[str], str, str]]]:
  part = 'top'
  init = []
  gates = []
  with open (filename, 'r') as file:
    for line in file:
      if line.strip() == '':
        # Move to bottom part
        part = 'bottom'
        continue
      if part == 'top':
        node, value = line.strip().split(': ')
        init.append((node, int(value)))
      elif part == 'bottom':
        input1, gate, input2, _, output = line.strip().split(' ')
        gates.append(({input1, input2}, gate, output))
      else:
        raise ValueError(f'Invlid {part=}')
    return init, gates

filename = 'inputs/day24.txt'
# filename = 'inputs/day24_test.txt'
init, gates = import_data(filename)
# print(init)
# print(gates)

class BinaryLogicGates:
  def __init__(self):
    """Initialize in2out, inputs2out, out2in and values."""
    self.in2out = {}
    self.inputs2out = {}
    self.out2in = {}
    self.gate2inputs = defaultdict(list)
    self.gate2out = defaultdict(list)
    self.values = {}
  
  def add_input(self, node):
    """Add a node to the graph if it's not already present"""
    if node not in self.in2out:
      self.in2out[node] = set()

  def add_gate(self, input1, input2, gate, output):
    """Add gate that combines v_in_1 and v_in_2 with gate to give v_out."""
    # Add nodes if they don't exist
    self.add_input(input1)
    self.add_input(input2)
    self.in2out[input1].add(output)
    self.in2out[input2].add(output)
    input1, input2 = sorted([input1, input2])
    self.inputs2out[(input1, input2, gate)] = output
    self.out2in[output] = (input1, input2, gate)
    self.gate2inputs[gate].append({input1, input2})
    self.gate2out[gate].append(output)


  def add_value(self, node, value):
    self.values[node] = value
    # Update values for outputs that have input values available.
    if node in self.in2out:
      for output in self.in2out[node]:
        input1, input2, gate = self.out2in[output]
        if input1 in self.values and input2 in self.values:
          value1 = self.values[input1]
          value2 = self.values[input2]
          output_value = self.compute_value(value1, value2, gate)
          self.add_value(output, output_value)

  def compute_value(self, value1, value2, gate):
    if gate == 'AND':
      return value1 & value2
    elif gate == 'OR':
      return value1 | value2
    elif gate == 'XOR':
      return value1 ^ value2
    else:
      raise ValueError(f'Invalid {gate=}')

def is_present(
    inputs: set[str], gate: str, gates: list[tuple[set[str], str, str]]
) -> bool:
  """Check `inputs` & `gate` are co-present in `gates` and return `output`"""
  for temp_inputs, temp_gate, _ in gates:
    if temp_inputs == inputs and temp_gate == gate:
      return True
  return False

# Register `init` and `gates` to an instance of BinaryLogicGates.
g = BinaryLogicGates()
for inputs, gate, output in gates:
  input1, input2 = list(inputs)
  g.add_gate(input1, input2, gate, output)

for node, value in init:
  g.add_value(node, value)  

# for k, v in sorted(g.values.items()):
#   print(f'{k}: {v}')

# Get binary string for the `z*` nodes' values and convert to decimal
binary_string = ''
for k, v in reversed(sorted(g.values.items())):
  if k.startswith('z'):
    binary_string += str(v)
# print(binary_string)
print('Part 1:', int(binary_string, 2))

# Part 2: Find the 4 pairs of outputs that need to be swapped.
filename = 'inputs/day24.txt'
init, gates = import_data(filename)
# Note that we have x00-x44,y00-y44,z00-z45.
# The addition logic is regular for each binary digit, e.g.
# x01 AND y01 -> pjh   x02 AND y02 -> wrc
# x01 XOR y01 -> bgb   x02 XOR y02 -> wmw
# fgw XOR bgb -> z01   wwp XOR wmw -> z02
# fgw AND bgb -> gww   wwp AND wmw -> dng
# pjh OR  gww -> wwp   pjh OR  gww -> vmk
# Note that the first three rows of each column have the gates needed to
# compute each binary digit of z. The remaining two rows are needed to compute
# the digit carried forward for computing the next binary digit.
# So fgw is the digit carried forward from the 00th binary digit, wwp is the
# digit carried forward from the 01th binary digit, vmk is the digit carried
# forward from the 02th binary digit and so on.
mistaken_outputs = set()
# Note that the output of x* XOR y* should be used to compute z* for 01-44.
# First obtain such outputs.
assert g.out2in['z00'] == ('x00', 'y00', 'XOR')
x_xor_y = {0: 'z00'}
for inputs, gate, output in gates:
  input1, input2 = sorted(list(inputs))
  if (input1.startswith('x') and input2.startswith('y')) and gate == 'XOR':
    num = int(input1[1:])
    if num != 0:
      x_xor_y[num] = output
assert len(x_xor_y) == 45  # 00-44
# Then check that they are used to compute z* for 01-44
for inputs, gate, output in gates:
  if output.startswith('z') and output not in ['z00', 'z45']:
    num = int(output[1:])
    if gate != 'XOR':
      # If gate is not XOR, then output is wrong.
      mistaken_outputs.add(output)
      continue
    xor = x_xor_y[num]
    if xor not in inputs:
      # If the check fails, either output is wrong or xor is wrong.
      # We can check which is the case by checking whether
      # (inputs, 'AND') co-occurs in `gates`. If it co-occurs, then
      # xor is wrong. If not, then output is wrong
      if is_present(inputs, 'AND', gates):
        mistaken_outputs.add(xor)
        # In this case, the element that needs to be swapped with xor is one of
        # `inputs`. One of these is the digit carried forward from the previous
        # binary place, and the other is the one that needs to be swapped.
        # Running this block of code, we know that the other 3 mistaken outputs
        # are z14, z27, z39, so each needs to be replaced with a string that is
        # the output of a XOR gate. Hence we know that exactly one of the gates
        # outputting `input1` and `input2` are correct, where
        # `inputs=[input1, input2]`.
        # And we know that one of the two should be output by an OR gate and
        # the other should be output by an x* XOR y* -> gate. So anything that
        # is not output by one of these gates will be the wrong one.
        for input in inputs:
          _, _, gate = g.out2in[input]
          if gate not in ['OR', 'XOR']:
            mistaken_outputs.add(input)
            # Also correct x_xor_y[num]
            x_xor_y[num] = input
      else:
        mistaken_outputs.add(output)

# The above gives 3 outputs of the form z* and a pair of outputs ['qwf', 'cnk']
# that need to be swapped. Now we need to find the corresponding pairs for each
# of the three z*.
# To do this, construct dict x_and_y, similar to x_xor_y, using that 
# x{n} AND y{n} -> output
# implies:
# output OR ... -> ...
x_and_y = {0: 'fgw'}
for n in range(1, 45):
  if n == 9:
    # We know this from the code above, where 
    # x09 AND y09 -> cnk
    # x09 XOR y09 -> qwf
    # have been swapped.
    output = 'qwf'
  else:  
    output = g.inputs2out[(f'x{n:02d}', f'y{n:02d}', 'AND')]
  if output in set.union(*g.gate2inputs['OR']):
    x_and_y[n] = output
  else:
    # This means output is wrong, and it is in mistaken_outputs.
    assert output in mistaken_outputs
    # Only deal with the case where output.startswith('z'), otherwise case
    # has already been dealt with above.
    if output.startswith('z'):
      # The correct value in else branch above can be found by noting that it
      # appears in g.gate2inputs['OR'], and it is currently (mistakenly) output
      # by an XOR gate (as it needs to be swapped with z*). Also check that for
      # input1 XOR input2 -> target,
      # input1 or input2 is x_xor_y[n].
      for inputs in g.gate2inputs['OR']:
        for target in inputs:
          if target in g.gate2out['XOR']:
            input1, input2, gate = g.out2in[target]
            if x_xor_y[n] in [input1, input2]:
              x_and_y[n] = target
              mistaken_outputs.add(target)
              break  

# Now get the correct values of digits carried forward at each binary place.
# Note that the digits carried forward are the only ones output by OR gates,
# except for x00 AND y00 -> fgw. Also note 'z45' is a special case, because it
# is the final digit carried forward that is not used in any other gates.
# So first extract all instances of input1 OR input2 -> output.
# Then note that the corresponding binary digit place, say n, can be found
# because either input1 or input2 comes from x_and_y[n].
# In the case where output is z{n} in `mistaken_outputs`, we can find the value
# that needs to be replaced by noting that it is the output of
# x_xor_y[n] XOR * ->
digit_carried_forward = {0: 'fgw', 44: 'z45'}
for inputs, gate, output in gates:
  if gate == 'OR' and output != 'z45':
    input1, input2 = list(inputs)
    # One of input1 and input2 is given by x{n} AND y{n}
    for input in [input1, input2]:
      if input in x_and_y.values():
        n = [k for k, v in x_and_y.items() if v == input][0]
    if not output.startswith('z'):
      digit_carried_forward[n] = output
    else:
      assert output in mistaken_outputs
      # Find * where "x_xor_y[n] XOR ... -> * ".
      for inputs_, gate_, output_ in gates:
        if x_xor_y[n] in inputs_ and gate_ == 'XOR':
          digit_carried_forward[n] = output_
          mistaken_outputs.add(output_)
          break

# Now use x_xor_y, x_and_y, digit_carried_forward to find the output to swap
# with z39.
# Note that we need a XOR b -> z39 where a=digit_carried_forward[38] and
# b = x_xor_y[39]. So find output corresponding to a XOR b.
inputs = {digit_carried_forward[38], x_xor_y[39]}
input1, input2 = sorted(list(inputs))
mistaken_outputs.add(g.inputs2out[(input1, input2, 'XOR')])

assert len(mistaken_outputs) == 8
# Get code from mistaken_outputs
mistaken_outputs = sorted(list(mistaken_outputs))
print('Part 2:', ','.join(mistaken_outputs))
