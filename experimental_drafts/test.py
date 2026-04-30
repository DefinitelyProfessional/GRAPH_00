class Graph:
    def __init__(self, directed=False):
        self.adjacency_list = {}
        self.directed = directed

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def remove_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            return
        del self.adjacency_list[vertex]
        for v in self.adjacency_list:
            if vertex in self.adjacency_list[v]:
                self.adjacency_list[v].remove(vertex)

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        if not self.directed:
            if u not in self.adjacency_list[v]:
                self.adjacency_list[v].append(u)

    def remove_edge(self, u, v):
        if u in self.adjacency_list and v in self.adjacency_list[u]:
            self.adjacency_list[u].remove(v)
        if not self.directed:
            if v in self.adjacency_list and u in self.adjacency_list[v]:
                self.adjacency_list[v].remove(u)

    def has_vertex(self, vertex):
        return vertex in self.adjacency_list

    def has_edge(self, u, v):
        return u in self.adjacency_list and v in self.adjacency_list[u]

    def get_vertices(self):
        return list(self.adjacency_list.keys())

    def get_edges(self):
        edges = []
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                if self.directed:
                    edges.append((u, v))
                elif (v, u) not in edges:
                    edges.append((u, v))
        return edges

    def get_neighbors(self, vertex):
        return list(self.adjacency_list.get(vertex, []))

    def vertex_count(self):
        return len(self.adjacency_list)

    def edge_count(self):
        return len(self.get_edges())

    def bfs(self, start):
        if start not in self.adjacency_list:
            return []
        visited = []
        queue = [start]
        visited.append(start)
        while queue:
            vertex = queue.pop(0)
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
        return visited

    def display(self):
        print("Graph Adjacency List:")
        for vertex in self.adjacency_list:
            neighbors = self.adjacency_list[vertex]
            print(f" {vertex} -> {neighbors}")

if __name__ == "__main__":
    print("Graph ADT - Undirected Graph Demo")
    print("=" * 33)
    g = Graph(directed=False)
    vertices = [ ("A", "B"), ("A", "D"), ("A", "E"), ("B", "C"), ("B", "E"),
                 ("C", "E"), ("C", "F"), ("C", "G"), ("E", "F"), ("F", "G") ]
    for (orig, dest) in vertices:
        g.add_edge(orig, dest)
    g.display()
    print(f"\nVertices : {g.get_vertices()}")
    print(f"Edges    : {g.get_edges()}")
    print(f"Vertex count : {g.vertex_count()}")
    print(f"Edge count   : {g.edge_count()}")
    print("\n--- BFS from A ---")
    print("Traversal order:", g.bfs("A"))