"""
# STORE CLASSES TO ENCAPSULATE DATA FOR TRANSFERS
By Stephen Matthews
"""
class GRAPHDATA:
    def __init__(self,
                 name_to_id: dict,
                 id_to_name: dict,
                 nodecount: int,
                 nodenames: set,
                 ADJ_list: list,
                 max_str_len: int):
        self.name_to_id = name_to_id # to translate name strings to node_id/indeces
        self.id_to_name = id_to_name # to translate node_id/indeces to name strings
        self.nodecount = nodecount # store how many nodes
        self.nodenames = nodenames # store names of nodes
        self.ADJ_list = ADJ_list # adjacency list
        self.max_str_len = max_str_len # for display

class AUTOLOADGRAPHDATA(GRAPHDATA):
    def __init__(self, graphdata: GRAPHDATA):
        super().__init__(
            graphdata.name_to_id,
            graphdata.id_to_name,
            graphdata.nodecount,
            graphdata.nodenames,
            graphdata.ADJ_list,
            graphdata.max_str_len)
    # ========================================================================================================
    def display_adjacency_list(self):
        """
        ## a dev tool to help visualize the adjacency list, if the program decided to use MTRX its already too big to visualize in the terminal.
        """
        map_ = self.id_to_name # prevent repeated self lookups
        for src, relations in enumerate(self.ADJ_list):
            print(f"{map_[src]} : ", end="")
            for dst, wgh in relations: print(f"({map_[dst]}, {wgh})", end=", ")
            print()
    # ========================================================================================================
    def display_nodes(self, width=20):
        """
        ## To make life easier, uses data from CSVLOADER
        """
        for idx, name in enumerate(self.nodenames, start=1):
            print(f"{name:<{self.max_str_len}}", end=" | " if idx % width != 0 else "\n")
        print()
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