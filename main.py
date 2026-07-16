from graph import Graph
from view import GraphView
#testing graph class
g = Graph()
g.load_from_file('./data/grafos/grafo16.csv')
print(g.adjacency)
print(g.edges)
print(g.check_degree(0))  # grado del nodo 0
if g.is_simple():  # comprobar si el grafo es simple
    print("El grafo es simple")
else:
    print("El grafo es multigrafo")

view = GraphView(g)
view.display()