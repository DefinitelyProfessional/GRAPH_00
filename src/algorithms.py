"""
# CLASS DEFINITIONS FOR THE GRAPH BASED ALGORITHMS
"""
from heapq import heappop as pop, heappush as push # Make use of efficient priority queue

class GRAPHSTRUCTURE:
    def __init__(self, ADJ_list: list, name_to_id: dict, id_to_name: dict, max_str_len: int):
        self.ADJ_list = ADJ_list # Made by the DATALOADER
        self.name_to_id = name_to_id # getfrom DATALOADER
        self.id_to_name = id_to_name # getfrom DATALOADER
        self._INF = float("inf") # a preference to define infinity
        self.num_nodes = len(ADJ_list)
        self.node_names = self.name_to_id.keys()
        self.max_str_len = max_str_len # niche for displays

    # ========================================================================================================
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
        distances = [self._INF] * self.num_nodes
        visited = [False] * self.num_nodes
        predecessors = [-1] * self.num_nodes
        
        distances[start_node] = 0 # trivially we start at the starting node with wgh 0
        
        # Priority Queue of nodes to visit : (current_distance, node_id)
        visit_queue = [(0, start_node)]
        
        # Visit every node that needs to be explored
        while visit_queue:
            # Pop the node with the shortest known distance !
            current_distance, current_node = pop(visit_queue)
            
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
                
                new_distance = current_distance + wgh
                
                # Skip further distances or ones that don't change the the distance
                if new_distance >= distances[neighbor]: continue
                # keep track of shortest distances ! refer to
                # code_breakdown\dijkstra.ipynb for explanations
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                push(visit_queue, (new_distance, neighbor))
                    
        # If the end node distance ends up to still be INF that
        # indicates there is no path from start to end, how sad
        if distances[end_node] == self._INF:
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
        
        return distances[end_node], path
    
    # ========================================================================================================
    def search_edge(self, src, dst):
        """
        ## Something to make life easier, searches for existing edges in O(n)
        """
        try: # let errors occur without causing a full crash
            for destinations, wgh in self.ADJ_list[src]:
                if destinations != dst: continue
                return src, dst, wgh # match found !!
            print(f"{src}, {dst} NOT FOUND")
        except Exception as cursed: print(cursed)
        return None, None, None # false condition if it were to reach here ...

    # ========================================================================================================
    def routing_engine(self, start, end):
        """
        ## To manage the shortest path function usage
        """
        # Conduct the shortest path algortihm
        total_distance, path_ids = self.shortest_path(start, end)
        
        # evaluate results
        if (total_distance, path_ids) == (None, []): return
        
        # display the series of path traversals
        for i in range(1, len(path_ids)):
            src, dst, wgh = self.search_edge(path_ids[i-1], path_ids[i])
            if (src, dst, wgh) == (None, None, None): continue # skip errors
            print(f"{self.id_to_name[src]} -> {self.id_to_name[dst]} : {wgh}")
        
        print(f"Total Distance : {total_distance}")
    
    # ========================================================================================================
    def display_nodes(self, width=20):
        """
        ## To make life easier, uses data from DATALOADER
        """
        for idx, name in enumerate(self.node_names, start=1):
            print(f"{name:<{self.max_str_len}}", end=" | " if idx % width != 0 else "\n")
        print()