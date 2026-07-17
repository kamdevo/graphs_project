from graph import Graph
from view import GraphView

# testing graph class
g = Graph()
g.load_from_file('./data/grafos/grafo4.csv')
print(g.adjacency)
print(g.edges)
print(g.check_degree(0))  # node 0 degree

if g.is_simple():  # checlk if graph is simple
    print("El grafo es simple")
else:
    print("El grafo es multigrafo")

impares = g.odd_degree_nodes()
print("Nodos con grado impar:", impares)

# Exercise 8: Eulerian circuit
if g.has_eulerian_circuit():
    print("Tiene circuito euleriano")

# Exercise 7: Eulerian path
if g.has_eulerian_path():
    print("Tiene camino euleriano")

# Exercise 2: Is the graph a tree?
if g.is_tree():
    print("El grafo es un arbol")
else:
    print("El grafo no es un arbol")

# Exercise 3: Is the graph a forest?
if g.is_forest():
    print("El grafo es un bosque")
else:
    print("El grafo no es un bosque")

view = GraphView(g)
view.display()