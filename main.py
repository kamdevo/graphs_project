from graph import Graph
from view import GraphView
#testing graph class
g = Graph()
g.load_from_file('./data/grafos/grafo16.csv')
print(g.adjacency)
print(g.edges)

view = GraphView(g)
view.display()