from graph import Graph
from view import GraphView

# testing graph class
g = Graph()
g.load_from_file('./data/grafos/grafo4.csv')
print(g.adjacency)
print(g.edges)
print(g.check_degree(0))  # grado del nodo 0

if g.is_simple():  # comprobar si el grafo es simple
    print("El grafo es simple")
else:
    print("El grafo es multigrafo")

impares = g.odd_degree_nodes()
print("Nodos con grado impar:", impares)

# Punto 8: circuito de Euler
if g.has_eulerian_circuit():
    print("Tiene circuito euleriano")

# Punto 7: camino de Euler
if g.has_eulerian_path():
    print("Tiene camino euleriano")

# Punto 2: ¿es un árbol?
if g.is_tree():
    print("El grafo es un arbol")
else:
    print("El grafo no es un arbol")

# Punto 4: ¿es plano?
if g.is_planar():
    print("El grafo es plano")
else:
    print("El grafo no es plano")

view = GraphView(g)
view.display()