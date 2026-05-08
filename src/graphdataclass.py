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
                 ADJ_type: str,
                 ADJ_obj: list,
                 max_str_len: int):
        self.name_to_id = name_to_id # to translate name strings to node_id/indeces
        self.id_to_name = id_to_name # to translate node_id/indeces to name strings
        self.nodecount = nodecount # store how many nodes
        self.nodenames = nodenames # store names of nodes
        self.ADJ_type = ADJ_type # store the type of ADJ_obj : LIST xor MTRX
        self.ADJ_obj = ADJ_obj # can be adjacency LIST xor MTRX
        self.max_str_len = max_str_len # for display
    # ========================================================================================================
    def display_adjacency_list(self):
        """
        ## a dev tool to help visualize the adjacency list
        """
        if self.ADJ_type != "LIST": return # this is an adj list specific debug tool
        map_ = self.id_to_name # prevent repeated self lookups
        for src, relations in enumerate(self.ADJ_obj):
            print(f"{map_[src]} : ", end="")
            for dst, wgh in relations: print(f"({map_[dst]}, {wgh})", end=", ")
            print()
    # ========================================================================================================
    def display_nodes(self, width=20):
        """
        ## To make life easier, uses data from DATALOADER
        """
        for idx, name in enumerate(self.nodenames, start=1):
            print(f"{name:<{self.max_str_len}}", end=" | " if idx % width != 0 else "\n")
        print()

class AUTOLOADGRAPHDATA(GRAPHDATA):
    def __init__(self, graphdata: GRAPHDATA):
        super().__init__(
            graphdata.name_to_id,
            graphdata.id_to_name,
            graphdata.nodecount,
            graphdata.nodenames,
            graphdata.ADJ_type,
            graphdata.ADJ_obj,
            graphdata.max_str_len)