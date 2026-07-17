import csv



class Graph:
    def __init__(self):
        self.adjacency = {}  # { node: [(neighbor, weight), ...] }
        self.edges = []      # [(u, v, weight), ...]

    def add_edge(self, source, target, weight):

        if source not in self.adjacency:
            # Add source node to adjacency list if not already present
            self.adjacency[source] = []
        if target not in self.adjacency:
            # Add target node to adjacency list if not already present
            self.adjacency[target] = []

        # Add the connection between source and target with the given weight
        self.adjacency[source].append((target, weight))
        self.adjacency[target].append((source, weight))

        # Add the raw edge to the edges list, passing source, target, and weight as a tuple
        self.edges.append((source, target, weight))

    def load_from_file(self, filepath):
        with open(filepath, 'r') as file:  # Open the file in read mode
            reader = csv.reader(file)  # initialize CSV reader to read the file
            next(reader)  # Skip header source,target,weight
            for row in reader:  # Iterate through each row in the CSV file
                source = int(row[0])  # Extract source column value and convert to integer
                target = int(row[1])  # Extract target column value and convert to integer
                weight = float(row[2])  # Extract weight column value and convert to float
                self.add_edge(source, target, weight)  # Add the edge to the graph

    def check_degree(self, node):
        if node not in self.adjacency:
            return None
        return len(self.adjacency[node])  # esto debe estar FUERA del if

    def is_simple(self):
        for source, target, weight in self.edges:
            # check for self-loops
            if source == target:
                return False

        # check for duplicate edges
        pairs = [(min(s, t), max(s, t)) for s, t, w in self.edges]
        if len(pairs) != len(set(pairs)):
            return False

        return True

    def is_complete(self):
        # primero debe ser simple
        if not self.is_simple():
            return False

        n = len(self.adjacency)  # total de nodos

        for node in self.adjacency:
            if len(self.adjacency[node]) != n - 1:
                return False

        return True

    def odd_degree_nodes(self):
        impares = []
        for node in self.adjacency:
            if self.check_degree(node) % 2 == 1:
                impares.append(node)
        return impares

    def is_connected(self):
        active_nodes = [node for node in self.adjacency if self.check_degree(node) > 0]
        if len(active_nodes) <= 1:
            return True

        start = active_nodes[0]
        visited = {start}
        queue = [start]

        while queue:
            node = queue.pop(0)
            for neighbor, _ in self.adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == len(active_nodes)

    # ---------------------------------------------------------------
    # Point 7: Eulerian path
    # ---------------------------------------------------------------
    def has_eulerian_path(self):
        if not self.is_connected():
            return False
        cantidad = len(self.odd_degree_nodes())
        return cantidad == 0 or cantidad == 2

    # ---------------------------------------------------------------
    # Point 8: Eulerian circuit
    # ---------------------------------------------------------------
    def has_eulerian_circuit(self):
        if not self.is_connected():
            return False
        return len(self.odd_degree_nodes()) == 0

    def is_Eulerian(self):
        return self.has_eulerian_circuit()

    # ---------------------------------------------------------------
    # Point 2: Is the graph a tree?
    # A tree is a simple, connected graph with exactly n-1 edges
    # (this avoids cycles without needing an extra traversal for detection).
    # ---------------------------------------------------------------
    def is_tree(self):
        if not self.adjacency:
            return False

        if not self.is_simple():
            return False

        if not self.is_connected():
            return False

        n = len(self.adjacency)   # number of nodes
        m = len(self.edges)       # number of edges

        return m == n - 1

    # Point 3: Is the graph a forest?
    # A forest is a collection of trees: a simple graph where every
    # connected component is acyclic. For a simple graph, this holds
    # exactly when edges == nodes - number_of_connected_components
    # (each tree with k nodes has exactly k-1 edges, so summing that
    # over every component gives n - c; any extra edge closes a cycle).

    def is_forest(self):
        if not self.is_simple():
            return False

        visited = set()
        num_components = 0

        for node in self.adjacency:
            if node not in visited:
                num_components += 1
                  # BFS to walk the whole component starting at this node
                queue = [node]
                visited.add(node)
                while queue:
                    current = queue.pop(0)
                    for neighbor, _ in self.adjacency[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

        n = len(self.adjacency)
        m = len(self.edges)
        return m == n - num_components