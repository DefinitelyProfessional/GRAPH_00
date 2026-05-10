# Preview on `csv_handling.py` and how to use the `relations.csv`

## Defining the relations in a graph world with `relations.csv`

For the sake of versatility, the relations for the graph are defined in a CSV file as a directed graph. There are 3 predefined entries to represent every edge in the graph :
```csv
src,dst,wgh
src0,dst0,wgh0
src1,dst1,wgh1
src2,dst2,wgh2
```
> `src` a string as the **source** node, `dst` a string as the **destination** node, and `wgh` a float as the **weight** of the edge between them.  

> **An edge goes from `src` to `dst` with a weight of `wgh`**. The graph is directed, so the edge only goes one way.  

> bidirectional edges can be represented by having two entries in the CSV file, one for each direction.  

Note that negative wgh_sum are allowed but not accounted for in the current implementation of our Dijkstra's algorithm. So unpredictable results may occur if done so, therefore it is recommended to only use non-negative wgh_sum.
## `CSVHANDLER class` handles automatic csv loading and store important data structures
```python
class CSVHANDLER:
    def __init__(self, relations_path):
        self.relations_path = relations_path
        self.generate_relations_path = relations_path
        self.graphdata = self.prepare_graph()
```
The following are methods callable within the `CSVHANDLER` class :

## `prepare_adj_list(relations_path: str)` returns `name_to_id`, `id_to_name`, and `ADJ_list`
The `prepare_adj_list` function takes the path to the `relations.csv` file as input and returns `GRAPHDATA` as a package to contain the following data structures :
1. `name_to_id`: a dictionary that maps node names (strings) to their corresponding integer index.
2. `id_to_name`: a dictionary that maps node integer index back to their corresponding names.
3. `nodecount`: an integer of the total number of unique nodes in the graph. 
4. `nodenames`: a list of strings of the unique node names in the graph.
5. `ADJ_list`: a list of list of tuples for the adjacency list the program will use.
6. `max_str_len`: an integer of the maximum string length of the node names in the graph, used for formatting the output.

## The design choice to settle on using adjacency lists over adjacency matrices
A final verdict is made to primarily work with adjacency lists because the dijkstra algorithm implemented in this project is ultimately more efficient with adjacency lists regardless a sparse or dense graph. **A legacy version where there are separate implementations of the program working with either list or matrices is available in the `legacy_list_matrix` branch in this github repository**

## `ADJ_list` visualization not indexed
```python
ADJ_list = [
    "src0": [("src1", 10.1), ("src2", 20.2), ...],
    "src1": [("src3", 30.3), ...],
    "src2": [("src3", 40.4), ("src4", 50.5), ...],
    ...
]
```

## `ADJ_list` visualization actual indexed
```python
ADJ_list = [
    [(1, 10.1), (2, 20.2), ...], # 0
    [(3, 30.3), ...],            # 1
    [(3, 40.4), (4, 50.5), ...], # 2
    ...
]
```

# Dev Tools
## `generate_relations_csv(relations_path: str, directional=True, nodecount=10, num_edges=20, min_weight=1, max_weight=100)`
generates a random `relations.csv` file with the specified parameters.

## Run the csv file to run the main function and see the results