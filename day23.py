def import_data(filename: str) -> list[tuple[str, str]]:
  edges = []
  with open(filename, 'r') as file:
    for line in file:
      line = line.strip().split('-')
      edges.append(line)
  return edges

filename = 'day23.txt'
# filename = 'day23_test.txt'
edges = import_data(filename)
# print(edges)

# Part 1: Count number of triangles containing at least one node that start
# with 't'.
# Get class for undirected graph from day16.py.
class UndirectedGraph:
  def __init__(self):
    """Initialize an empty graph."""
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
    """Return all vertices in the graph."""
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

# Express edge list as an undirected graph.
g = UndirectedGraph()
for v1, v2 in edges:
  g.add_edge(v1, v2)
# print(g.get_vertices())

# Loop over all edges to find distinct triangles, expressed as sets.
triangles = set()
for v1, v2 in g.get_edges():
  for v3 in g.graph[v1]:
    if v3 in g.graph[v2]:
      # Add triangle only once (in sorted order to avoid duplicates)
      triangles.add(tuple(sorted([v1, v2, v3])))
# print(sorted(list(triangles)))

# Loop over triangles to find number of triangles with at least one vertex
# starting with t.
num_t_start_t = 0
for v1, v2, v3 in triangles:
  if v1.startswith('t') or v2.startswith('t') or v3.startswith('t'):
    num_t_start_t += 1
print('Part 1:', num_t_start_t)

# Part 2: Get vertices in largest clique of graph.
# Start with the list of triangles (3-cliques). If there is a 4-clique, then
# all four triplets of its vertices would be included in the list of triangles.
# So loop over triangles to find the set of all 4-cliques, and repeat for
# n-cliques until there are no (n+1)-cliques.
def find_cliques_next_size(
    g: UndirectedGraph, cliques_size_n: set[tuple[str, ...]]
) -> set[tuple[str, ...]]:
  """Given graph g and cliques_size_n, find all cliques of size n+1."""
  cliques_next_size = set()
  for clique in cliques_size_n:
    v1, v_rest = clique[0], clique[1:]
    # Sweep over neighbours of v1 to see which ones for a clique of size n with
    # v_rest
    for v_next in g.graph[v1] - set(v_rest):
      candidate_vertices = tuple(sorted(v_rest + (v_next,)))
      if candidate_vertices in cliques_size_n:
        cliques_next_size.add(tuple(sorted(clique + (v_next,))))
  return cliques_next_size

clique_size = 3
largest_cliques = triangles
while largest_cliques:
  prev_largest_clique = largest_cliques.copy()
  largest_cliques = find_cliques_next_size(g, largest_cliques)

assert len(prev_largest_clique) == 1
prev_largest_clique = prev_largest_clique.pop()
code = ','.join(prev_largest_clique)
print('Part 2:', code)