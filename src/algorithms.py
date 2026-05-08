"""
# CLASS DEFINITIONS FOR THE GRAPH BASED ALGORITHMS
"""
from graphdataclass import GRAPHDATA, AUTOLOADGRAPHDATA
from heapq import heappop as pop, heappush as push # Make use of efficient priority queue

class GRAPHSTRUCTURE(AUTOLOADGRAPHDATA):
    def __init__(self, graphdata: GRAPHDATA):
        super().__init__(graphdata)
        self._INF = float("inf") # a preference to define infinity
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
        # store a defined method from the child node
        # this prevents repeated self method lookups
        get_neighbors = self.get_neighbors
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
            for neighbor, wgh in get_neighbors(current_node):
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
        search_edge = self.search_edge # store method to prevent repeated self lookups
        for i in range(1, len(path_ids)):
            src, dst, wgh = search_edge(path_ids[i-1], path_ids[i])
            if (src, dst, wgh) == (None, None, None): continue # skip errors
            print(f"{self.id_to_name[src]:<{self.max_str_len}} -> {self.id_to_name[dst]:<{self.max_str_len}} : {wgh}")
        # finally, show results
        print(f"Total Distance : {total_wgh_sum}")
    


class GRAPHLIST(GRAPHSTRUCTURE):
    """
    ## class optimized for sparse graphs
    """
    def __init__(self, graphdata: GRAPHDATA): super().__init__(graphdata)
    # ========================================================================================================     
    def get_neighbors(self, current_node: int): # optimized for shortest_path that works with ADJ_list
        return self.ADJ_obj[current_node] # notice how it is more simple with ADJ_list objects
    # ========================================================================================================
    def search_edge(self, src, dst):
        """
        ## Something to make life easier, searches for existing edges in O(n) for ADJ_list
        """
        try: # let errors occur without causing a full crash
            for destinations, wgh in self.ADJ_obj[src]:
                if destinations != dst: continue
                return src, dst, wgh # match found !!
            print(f"{src}, {dst} NOT FOUND")
        except Exception as cursed: print(cursed)
        return None, None, None # false condition if it were to reach here ...
    # ========================================================================================================
    def build_MST():
        # TODO woy implement MST with ADJ_list
        return



class GRAPHMTRX(GRAPHSTRUCTURE):
    """
    ## class optimized for dense graphs
    """
    def __init__(self, graphdata: GRAPHDATA): super().__init__(graphdata)
    # ========================================================================================================
    def get_neighbors(self, current_node: int): # optimized for shortest_path that works with ADJ_mtrx
        return [(neighbor, weight) for neighbor, weight in enumerate(self.ADJ_obj[current_node]) if weight != self._INF]
    # ========================================================================================================
    def search_edge(self, src, dst):
        """
        ## Something to make life easier, searches for existing edges in O(1) for ADJ_mtrx
        """
        try: # let errors occur without causing a full crash
            wgh = self.ADJ_obj[src][dst]
            if wgh != self._INF:
                return src, dst, wgh # match found !!
            else: print(f"{src}, {dst} NOT FOUND")
        except Exception as cursed: print(cursed)
        return None, None, None # false condition if it were to reach here ...
    # ========================================================================================================
    def build_MST():
        # TODO woy implement MST with ADJ_mtrx
        return