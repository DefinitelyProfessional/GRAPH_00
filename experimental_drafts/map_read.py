import heapq

class WorldGraph:
    def __init__(self, map_str):
        self.raw_map = [list(line) for line in map_str.strip().split('\n')]
        self.height = len(self.raw_map)
        self.width = len(self.raw_map[0])
        self.nodes = [] # List of (y, x)
        self.graph = {} # Adjacency List: {(y,x): [((ny,nx), weight), ...]}
        self.start = None
        self.end = None
        self.pois = [] # Points of Interest for MST
        
        self._build_graph()

    def _build_graph(self):
        for y in range(self.height):
            for x in range(self.width):
                char = self.raw_map[y][x]
                if char != '#':
                    node = (y, x)
                    self.nodes.append(node)
                    if char == 'S': self.start = node
                    if char == 'E': self.end = node
                    if char == 'P': self.pois.append(node)
                    
                    # Check 4-way neighbors
                    self.graph[node] = []
                    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < self.height and 0 <= nx < self.width:
                            if self.raw_map[ny][nx] != '#':
                                self.graph[node].append(((ny, nx), 1))

    def dijkstra(self, start_node, end_node):
        """Finds the shortest path between two points."""
        distances = {node: float('inf') for node in self.nodes}
        previous = {node: None for node in self.nodes}
        distances[start_node] = 0
        pq = [(0, start_node)]

        while pq:
            current_dist, u = heapq.heappop(pq)

            if u == end_node: break
            if current_dist > distances[u]: continue

            for v, weight in self.graph[u]:
                alt = current_dist + weight
                if alt < distances[v]:
                    distances[v] = alt
                    previous[v] = u
                    heapq.heappush(pq, (alt, v))

        # Reconstruct path
        path = []
        curr = end_node
        while curr:
            path.append(curr)
            curr = previous[curr]
        return path[::-1] if distances[end_node] != float('inf') else None

    def prim_mst(self):
        """Generates the Minimum Spanning Tree of all traversable nodes."""
        if not self.nodes: return []
        
        start_node = self.nodes[0]
        mst_edges = []
        visited = {start_node}
        edges = [ (weight, start_node, v) for v, weight in self.graph[start_node] ]
        heapq.heapify(edges)

        while edges:
            weight, u, v = heapq.heappop(edges)
            if v not in visited:
                visited.add(v)
                mst_edges.append((u, v))
                for next_v, next_w in self.graph[v]:
                    if next_v not in visited:
                        heapq.heappush(edges, (next_w, v, next_v))
        return mst_edges

    def display(self, path=None, mst=None):
        """Translates machine data back to human-readable ASCII."""
        display_map = [row[:] for row in self.raw_map]
        
        if mst:
            for u, v in mst:
                # We use small dots to show the 'skeleton' of the MST
                y, x = v
                if display_map[y][x] == '.': display_map[y][x] = '·'

        if path:
            for y, x in path:
                if display_map[y][x] not in ['S', 'E']:
                    display_map[y][x] = 'X' # X marks the path

        print("\n" + "\n".join(["".join(row) for row in display_map]))

# --- Usage Example ---

world_layout = """
##########
#S.......#
#.######.#
#.#P...#.#
#.#.##.#.#
#.#....#.#
#.####.#.#
#......E.#
##########
"""

world = WorldGraph(world_layout)

print("--- Shortest Path (Dijkstra) ---")
path = world.dijkstra(world.start, world.end)
world.display(path=path)

print("\n--- Minimum Spanning Tree (Prim's Skeleton) ---")
mst = world.prim_mst()
world.display(mst=mst)