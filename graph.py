import csv

class Graph:
    def __init__(self):
        self.adjacency = {} # { node: [(neighbor, weight), ...] }
        self.edges = [] # [(u, v, weight), ...]
    def add_edge(self, source, target, weight):
        
        if source not in self.adjacency:
        #Add source node to adjacency list if not already present
            self.adjacency[source] = []
        if target not in self.adjacency:
        #Add target node to adjacency list if not already present
            self.adjacency[target] = []

        #Add the connection between source and target with the given weight
        self.adjacency[source].append((target, weight))
        self.adjacency[target].append((source, weight))

        #Add the raw edge to the edges list, passing source, target, and weight as a tuple
        self.edges.append((source, target, weight))  

    def load_from_file(self, filepath):
        with open(filepath, 'r') as file: #Open the file in read mode
            reader = csv.reader(file) #initialize CSV reader to read the file
            next(reader)  # Skip header source,target,weight        
            for row in reader: #Iterate through each row in the CSV file
                source = int(row[0]) #Extract source column value and convert to integer (row values are strings by default)
                target = int(row[1]) #Extract target column value and convert to integer (row values are strings by default)
                weight = float(row[2]) #Extract weight column value and convert to float
                self.add_edge(source, target, weight) #Add the edge to the graph using the add_edge method
    
