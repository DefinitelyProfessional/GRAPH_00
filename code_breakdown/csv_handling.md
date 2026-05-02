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

Note that negative weights are allowed but not accounted for in the current implementation of our Dijkstra's algorithm. So unpredictable results may occur if done so, therefore it is recommended to only use non-negative weights.

## `prepare_adj_list(relations_path: str)` returns `name_to_id`, `id_to_name`, and `ADJ_list`
The `prepare_adj_list` function takes the path to the `relations.csv` file as input and returns three things taht are used for the program :
1. `name_to_id`: a dictionary that maps node names (strings) to their corresponding integer index.
2. `id_to_name`: a dictionary that maps node integer index back to their corresponding names.
3. `ADJ_list`: an adjacency list representation of the graph.

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
    0: [(1, 10.1), (2, 20.2), ...],
    1: [(3, 30.3), ...],
    2: [(3, 40.4), (4, 50.5), ...],
    ...
]
```

# Dev Tools
## `generate_relations_csv(relations_path: str, directional=True, num_nodes=10, num_edges=20, min_weight=1, max_weight=100)`
generates a random `relations.csv` file with the specified parameters.

## `display_adjacency_list(id_to_name, ADJ_list)`
displays the adjacency list in a readable format using the `id_to_name` dictionary to convert node indices back to their names.

## Run the csv file to run the main function and see the results