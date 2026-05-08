# Preview on `graphdataclass.py` and how it serves as a data structure to store graph data

## `GRAPHDATA` base class
This class serves as a data structure to store graph data and make data transfers easier between different functions and classes. It contains the following attributes :
```python
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
```
## `AUTOLOADGRAPHDATA` class
```python
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
```
This is a rather peculiar way of using python classes, but I find it to be a useful way to enable passing the `graphdata` object enough to transfer all of the packaged data into the classes that need them. Inheritance is used over and over again to make use of this somewhat modular structure I made.

### `display_adjacency_list()` debug tool to display adjacency list in a readable format

### `display_nodes()` function to display all nodes in the graph in an arguably readable format