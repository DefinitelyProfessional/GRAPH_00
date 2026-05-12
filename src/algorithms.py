"""
# CLASS DEFINITIONS FOR THE GRAPH BASED ALGORITHMS
"""
from graphdataclass import GRAPHDATA, AUTOLOADGRAPHDATA
from heapq import heappop as pop, heappush as push # Make use of efficient priority queue

class GRAPHSTRUCTURE(AUTOLOADGRAPHDATA):
    def __init__(self, graphdata: GRAPHDATA):
        super().__init__(graphdata)
        self._INF = float("inf") # a preference to define infinity
        self.MST_edge_set = set() # to store the MST edge set IF the user wants to build one
    # ========================================================================================================
    def shortest_path(self, start: str, end: str):
        """
        ## The simplest most efficient dijkstra implemntation in python
        By Stephen Matthews
        """
        if start not in self.name_to_id or end not in self.name_to_id:
            return None, [], "Non-Existant Nodes !!!"
            
        # Convert to node id's being integer indexes !
        start_node = self.name_to_id[start]
        end_node = self.name_to_id[end]

        # Refer to code_breakdown\dijkstra.ipynb for explanations
        wgh_sum = [self._INF] * self.nodecount
        visited = [False] * self.nodecount
        predecessors = [-1] * self.nodecount
        
        wgh_sum[start_node] = 0 # trivially we start at the starting node with wgh 0
        
        # Priority Queue of nodes to visit : (current_wgh_sum, node_id)
        visit_queue = [(0, start_node)]
        # Visit every node that needs to be explored
        while visit_queue:
            # Pop the node with the shortest known wgh_sum !
            current_wgh_sum, current_node = pop(visit_queue)
            
            # Program arrived at destination !
            if current_node == end_node: break
                
            # Skip already visited nodes
            if visited[current_node]: continue
                
            # Mark current node visited
            visited[current_node] = True
            
            # Explore ALL "neighbors", if no path exists from start to end
            # The visit_queue will be exhausted and this loop stops
            for neighbor, wgh in self.ADJ_list[current_node]: 
                if visited[neighbor]: continue # SKIP
                
                new_wgh_sum = current_wgh_sum + wgh
                
                # Skip greater wgh_sum or ones that don't change the the wgh_sum
                if new_wgh_sum >= wgh_sum[neighbor]: continue
                # keep track of shortest wgh_sum ! refer to
                # code_breakdown\dijkstra.ipynb for explanations
                wgh_sum[neighbor] = new_wgh_sum
                predecessors[neighbor] = current_node
                push(visit_queue, (new_wgh_sum, neighbor))
                    
        # If the end node wgh_sum ends up to still be INF that
        # indicates there is no path from start to end, how sad
        if wgh_sum[end_node] == self._INF:
            return None, [], f"No path found between {start} and {end}."
        
        # refer to code_breakdown\dijkstra.ipynb for explanations
        path = []
        current = end_node
        # Trace backward until we hit the start node
        while current != -1:
            path.append(current)
            current = predecessors[current]
        
        # Flip it to read from Start -> End
        path.reverse()
        
        return wgh_sum[end_node], path, "Shortest Path Found !"
    # ========================================================================================================
    def routing_engine(self, start, end):
        """
        ## To manage the shortest path function usage
        By Stephen Matthews
        """
        # Conduct the shortest path algortihm
        total_wgh_sum, path_ids, status_str = self.shortest_path(start, end)
        # evaluate results
        if (total_wgh_sum, path_ids) == (None, []): return 1, status_str, None, None
        # display the series of path traversals
        traversal_string = []

        search_edge = self.search_edge # store method to prevent repeated self lookups
        for i in range(1, len(path_ids)):
            src, dst, wgh = search_edge(path_ids[i-1], path_ids[i])
            if (src, dst, wgh) == (None, None, None): continue # skip errors
            traversal_string.append(
                f"{self.id_to_name[src]:<{self.max_str_len}} -> {self.id_to_name[dst]:<{self.max_str_len}} : {wgh}")
        # return results for UI to render
        return 0, status_str, traversal_string, total_wgh_sum
    
    # ========================================================================================================
    def build_MST(self):
        """
        ## build MST out of the adjacency list with Prim's Algorithm
        By Neil Yapson and Joshua Christopher
        """
        if self.nodecount == 0: # Kalau graph kosong MSTnya tidak ada, return set kosong
            return set()

        self.MST_edge_set = set() # Buat set kosong untuk menyimpan edge-edge MST
        visited = [False] * self.nodecount # Buat list visited untuk menandai node yang sudah di visit

        id_to_name = self.id_to_name # Store locally to prevent repeated self lookups

        for start in range(self.nodecount): # Memastikan semua connected components dibuat MST 
            if visited[start]: # Kalau node sudah masuk MST, skip
                continue
            
            visited[start] = True # Node yang belum dikunjungi menjadi node awal
            
            edge_queue = []
            for neighbor, wgh in self.ADJ_list[start]: # Masukkan setiap edge dari node awal ke heap
                # NOTE PENTING : wgh sbagai index 0 dalam 3-tuple krn itu yg dievaluasi sortingnya heap
                push(edge_queue, (wgh, start, neighbor))

            while edge_queue: # Selama masih ada kandidat edge
                wgh, src, dst = pop(edge_queue) # Ambil edge dengan bobot terkecil
                if visited[dst]: # Kalau node tujuan sudah ada di MST, skip supaya tidak siklik
                    continue

                visited[dst] = True # Node baru masuk MST
                self.MST_edge_set.add((id_to_name[src], id_to_name[dst], wgh)) # Simpan edge ke MST 

                for neighbor, next_wgh in self.ADJ_list[dst]: # Eksplor semua edge node baru
                    if visited[neighbor]: # Kalau neighbor sudah ada di MST, skip 
                        continue
                    push(edge_queue, (next_wgh, dst, neighbor)) # Masukkan edge baru ke heap

        return self.MST_edge_set # Return semua edge MST, kalau ada graph disconnected jadi Minimum Spanning Forest