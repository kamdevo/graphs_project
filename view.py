import networkx as nx
import matplotlib.pyplot as plt

class GraphView:
    def __init__(self, graph):
        self.graph = graph # Graph instance passed to the view

    def display(self):
        G = nx.Graph() # Create a new NetworkX graph object
        for source, target, weight in self.graph.edges: # Iterate through the edges in the graph
            G.add_edge(source, target, weight=weight) # Add each edge to the NetworkX graph with its weight as an attributeE

            pos = nx.spring_layout(G) # Compute the layout for the graph visualization

            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500) # Draw the graph with labels and styling

            edge_labels = { (u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True) } # Create edge labels showing weights formatted to 2 decimal places
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # Draw the edge labels on the graph

            plt.title("Graph Visualization") # Set the title of the plot
            plt.show() # Display the graph visualization