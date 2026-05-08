"""
# CLASS DEFINITIONS FOR THE GRAPH BASED ALGORITHMS
"""
from heapq import heappop as pop, heappush as push # Make use of efficient priority queue

class GRAPHSTRUCTURE:
    def __init__(self, name_to_id: dict, id_to_name: dict, max_str_len: int, nodecount: int):
        self.name_to_id = name_to_id # get from DATALOADER
        self.id_to_name = id_to_name # get from DATALOADER
        self._INF = float("inf") # a preference to define infinity
        self.node_names = self.name_to_id.keys()
        self.nodecount = nodecount
        self.max_str_len = max_str_len # niche for displays
    # ========================================================================================================
    def display_nodes(self, width=20):
        """
        ## To make life easier, uses data from DATALOADER
        """
        for idx, name in enumerate(self.node_names, start=1):
            print(f"{name:<{self.max_str_len}}", end=" | " if idx % width != 0 else "\n")
        print()
    # ========================================================================================================
    def get_neighbors(self, current_node: int): raise NotImplementedError # LIST MTRX implementation differ
    def shortest_path(self, start: str, end: str):
        """
        ## The simplest most efficient dijkstra implemntation in python
        """
        if start not in self.name_to_id or end not in self.name_to_id:
            print("Non-Existant Nodes !!!"); return None, []
            
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
            for neighbor, wgh in self.get_neighbors(current_node):
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
            print(f"No path found between {start} and {end}."); return None, []
        
        # refer to code_breakdown\dijkstra.ipynb for explanations
        path = []
        current = end_node
        # Trace backward until we hit the start node
        while current != -1:
            path.append(current)
            current = predecessors[current]
        
        # Flip it to read from Start -> End
        path.reverse()
        
        return wgh_sum[end_node], path
    # ========================================================================================================
    def search_edge(self, src, dst): raise NotImplementedError # LIST MTRX implementation differ
    def routing_engine(self, start, end):
        """
        ## To manage the shortest path function usage
        """
        # Conduct the shortest path algortihm
        total_wgh_sum, path_ids = self.shortest_path(start, end)
        # evaluate results
        if (total_wgh_sum, path_ids) == (None, []): return
        # display the series of path traversals
        for i in range(1, len(path_ids)):
            src, dst, wgh = self.search_edge(path_ids[i-1], path_ids[i])
            if (src, dst, wgh) == (None, None, None): continue # skip errors
            print(f"{self.id_to_name[src]} -> {self.id_to_name[dst]} : {wgh}")
        # finally, show results
        print(f"Total Distance : {total_wgh_sum}")
    



class GRAPHLIST(GRAPHSTRUCTURE):
    """
    class optimized for sparse graphs
    """
    def __init__(self, ADJ_list: list, name_to_id: dict, id_to_name: dict, max_str_len: int):
        super().__init__(name_to_id, id_to_name, max_str_len, len(ADJ_list))
        self.ADJ_list = ADJ_list # Made by the DATALOADER
    # ========================================================================================================     
    def get_neighbors(self, current_node: int): # optimized for shortest_path that works with ADJ_list
        return self.ADJ_list[current_node]
    # ========================================================================================================
    def search_edge(self, src, dst):
        """
        ## Something to make life easier, searches for existing edges in O(n) for ADJ_list
        """
        try: # let errors occur without causing a full crash
            for destinations, wgh in self.ADJ_list[src]:
                if destinations != dst: continue
                return src, dst, wgh # match found !!
            print(f"{src}, {dst} NOT FOUND")
        except Exception as cursed: print(cursed)
        return None, None, None # false condition if it were to reach here ...



class GRAPHMTRX(GRAPHSTRUCTURE):
    """
    class optimized for dense graphs
    """
    def __init__(self, ADJ_mtrx: list, name_to_id: dict, id_to_name: dict, max_str_len: int):
        super().__init__(name_to_id, id_to_name, max_str_len, len(ADJ_mtrx))
        self.ADJ_mtrx = ADJ_mtrx # Made by the DATALOADER
    # ========================================================================================================
    def get_neighbors(self, current_node: int): # optimized for shortest_path that works with ADJ_mtrx
        return [(neighbor, weight) for neighbor, weight in enumerate(self.ADJ_mtrx[current_node]) if weight != self._INF]
    # ========================================================================================================
    def search_edge(self, src, dst):
        """
        ## Something to make life easier, searches for existing edges in O(1) for ADJ_mtrx
        """
        try: # let errors occur without causing a full crash
            wgh = self.ADJ_mtrx[src][dst]
            if wgh != self._INF:
                return src, dst, wgh # match found !!
            else: print(f"{src}, {dst} NOT FOUND")
        except Exception as cursed: print(cursed)
        return None, None, None # false condition if it were to reach here ...