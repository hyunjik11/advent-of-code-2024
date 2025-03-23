def import_data(filename: str) -> list[list[str]]:
  # Extract characters per line as array.
  map_arr = []
  with open (filename, 'r') as file:
    for line in file:
      map_arr.append(list(line.strip()))
    return map_arr

def print_map(map_arr: list[list[str]]):
  str_to_print = ''
  for row in map_arr:
    row_to_print = ''.join(row)
    row_to_print += '\n'
    str_to_print += row_to_print
  print(str_to_print)

def find_target_pos(map_arr: list[list[str]], target: str) -> tuple[int, int]:
  # Find target string in map_arr.
  for i, row in enumerate(map_arr):
    for j, val in enumerate(row):
      if val == target:
        return (i, j)

def get_dir(u: tuple[int, int], v: tuple[int, int]) -> str:
  # Get direction of u -> v
  ui, uj = u
  vi, vj = v
  assert abs(ui - vi) + abs(uj - vj) == 1, f'Nodes {u} and {v} not adjacent.'
  if ui < vi:
    return 'd'
  elif ui > vi:
    return 'u'
  elif uj < vj:
    return 'r'
  elif uj > vj:
    return 'l'

def opposite(dir: str):
  assert dir in ['l', 'r', 'u', 'd'], f'Invalid direction {dir}.'
  if dir == 'l':
    return 'r'
  elif dir == 'r':
    return 'l'
  elif dir == 'u':
    return 'd'
  elif dir == 'd':
    return 'u'

filename = 'day16.txt'
# filename = 'day16_test.txt'
# filename = 'day16_test2.txt'
map_arr = import_data(filename)
print_map(map_arr)

class UndirectedGraph:
    def __init__(self):
        """Initialize an empty graph using adjacency list representation"""
        self.graph = {}
    
    def add_vertex(self, vertex):
        """Add a vertex to the graph if it's not already present"""
        if vertex not in self.graph:
            self.graph[vertex] = set()
            
    def add_edge(self, v1, v2):
        """Add an undirected edge between vertices v1 and v2"""
        # Add vertices if they don't exist
        self.add_vertex(v1)
        self.add_vertex(v2)
        # Add edges in both directions
        self.graph[v1].add(v2)
        self.graph[v2].add(v1)
            
    def get_neighbors(self, vertex):
        """Return all vertices connected to the given vertex"""
        return self.graph.get(vertex, set())
    
    def get_vertices(self):
        """Return all vertices in the graph"""
        return set(self.graph.keys())
    
    def get_edges(self):
        """Return all edges in the graph as set of tuples"""
        edges = set()
        for v1 in self.graph:
            for v2 in self.graph[v1]:
                # Add edge only once (in sorted order to avoid duplicates)
                edge = tuple(sorted([v1, v2]))
                edges.add(edge)
        return edges
    
    def __str__(self):
        """String representation of the graph"""
        return f"Vertices: {self.get_vertices()}\nEdges: {self.get_edges()}"

# Find the starting position.
start_pos = find_target_pos(map_arr, 'S')
# print(start_pos)

#  Find end position.
end_pos = find_target_pos(map_arr, 'E')
# print(end_pos)

# Convert map array into a graph, where nodes are tuples
# ((pos_row, pos_col), dir) and edges show which positions are adjacent.
# Two positions are adjacent if:
# 1) they are next to each other horizontally or vertically and neither of them
#    is a wall.
# or
# 2) `pos_{row,col}` are same but `dir` differs by 90 degrees.
g = UndirectedGraph()
for i, row in enumerate(map_arr):
  for j, val in enumerate(row):
    assert val in ['.', 'S', 'E', '#']
    if val != '#':
      cur_pos = (i, j)
      # Find neighbours of current position.
      relevant_dirs = set()
      for k, l in [(i, j-1), (i, j+1), (i-1, j), (i+1, j)]:
        if 0 <= k < len(map_arr) and 0 <= l < len(row) and map_arr[k][l] != '#':
          dir = get_dir(cur_pos, (k, l))
          relevant_dirs.add(dir)
          relevant_dirs.add(opposite(dir))
          g.add_edge(((i, j), dir), ((k, l), dir))
      # Add edges for turns.
      if len(relevant_dirs) == 4:
        g.add_edge(((i, j), 'r'), ((i, j), 'u'))
        g.add_edge(((i, j), 'r'), ((i, j), 'd'))
        g.add_edge(((i, j), 'l'), ((i, j), 'u'))
        g.add_edge(((i, j), 'l'), ((i, j), 'd'))
# Make sure that (start_pos, 'r') is in graph.
if (start_pos, 'r') not in g.get_vertices():
  assert (start_pos, 'u') in g.get_vertices()
  g.add_edge((start_pos, 'r'), (start_pos, 'u'))
# print(g)

# Part 1: Find score of shortest path from start to end
# where a move has score 1 and a turn has score 1000.
# Score of a given (start, dir) can be found by working backwards:
# From (end_pos, 'r') and (end_pos, 'u') fill in scores for neighbours,
# then repeat for neighbours of neighbours, etc.
# until we reach (start_pos, 'r').
# The possible directions are: 'l', 'r', 'u', 'd'.
# If a neighbour already has a score, overwrite only if the new score is < old
# score. This way, we can be sure that we always find the shortest path.
scores = {(end_pos, 'r'): 0, (end_pos, 'u'): 0}
candidate_key = [(end_pos, 'r'), (end_pos, 'u')]
while candidate_key:
  v, dir_v = candidate_key.pop(0)
  assert (v, dir_v) in scores, f'({v=}, {dir_v=}) not in {scores.keys()}.'
  score_v = scores[(v, dir_v)]
  # Find neighbours of v.
  for (u, dir_u) in g.get_neighbors((v, dir_v)):
    if u == v:
      # This means there is a turn from u to v.
      assert dir_u != dir_v
      new_score = score_v + 1000
    else:
      assert dir_u == dir_v
      # This means there is no turn from u to v, just a move.
      new_score = score_v + 1
    # Add (u, dir_u) to candidate_key if it hasn't been visited yet,
    # or update value if the new score is better than the old score.
    if (u, dir_u) in scores:
      old_score = scores[(u, dir_u)]
      if new_score < old_score:
        scores[(u, dir_u)] = new_score
        candidate_key.append((u, dir_u))
    else:
      scores[(u, dir_u)] = new_score
      candidate_key.append((u, dir_u))

# After the loop, assert that start_pos is covered.
assert (start_pos, 'r') in scores, (
   f'Start position {(start_pos, "r")} not covered.'
)
print(f'Part 1: {scores[(start_pos, "r")]}')

# Part 2: Find the number of positions that lie on
# any best path from start to end.
# To do this, use `scores` to traverse (pos, dir) from (start_pos, 'r')
# to (end_pos, 'u') or (end_pos, 'r').
# Note that the best paths always go down in score.
candidate_key = [(start_pos, 'r')]
tiles_on_best_path = set([start_pos])
candidates_completed = set()
while candidate_key:
  v, dir_v = candidate_key.pop(0)
  assert (v, dir_v) in scores, f'({v=}, {dir_v=}) not in {scores.keys()}.'
  if (v, dir_v) not in candidates_completed:
    score_v = scores[(v, dir_v)]
    # Find neighbours of v.
    for (u, dir_u) in g.get_neighbors((v, dir_v)):
      # Get score of u.
      score_u = scores[(u, dir_u)]
      # Check if u is on the best path.
      # u is on the best path if score_u < score_v
      if score_u < score_v:
        tiles_on_best_path.add(u)
        candidate_key.append((u, dir_u))
    candidates_completed.add((v, dir_v))
# print(sorted(tiles_on_best_path))
print(f'Part 2: {len(tiles_on_best_path)}')