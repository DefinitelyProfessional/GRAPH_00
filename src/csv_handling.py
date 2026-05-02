"""
# CSV FILE HANDLING AND PREPARING DATA FOR THE PROGRAM
by Stephen Matthews
"""

import csv
import random

# ========================================================================================================
def prepare_adj_list(relations_path: str):
    """
    # Read CSV and prepare the graph environment
    """
    nodes = set()
    edges = set()
    try: # READ   
        with open(relations_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file); next(reader) # unused header
            for src, dst, wgh in reader:
                nodes.add(src); nodes.add(dst) # collect the unique nodes
                edges.add((src, dst, float(wgh))) # store the  unique edges 
    except Exception as cursed: print(cursed)

    # Clever way to map node string names into integer index
    name_to_id = {name: idx for idx, name in enumerate(sorted(nodes))}
    id_to_name = {idx: name for name, idx in name_to_id.items()}

    # Create the graph environment for the sake of dijkstra's efficiency !
    # This will be in the form of an adjacency list !
    # [src0] -> [(dst0, wgh0), (dst1, wgh1), (dst2, wgh2)]
    # [src1] -> [(dst0, wgh0), (dst1, wgh1)]
    ADJ_list = [[] for _ in range(len(nodes))]
    for src, dst, wgh in edges: # note edges is alredy a unique set
        ADJ_list[name_to_id[src]].append((name_to_id[dst], wgh))

    return name_to_id, id_to_name, ADJ_list

# ========================================================================================================
def display_adjacency_list(id_to_name, ADJ_list):
    """
    # a dev tool to help visualize teh adjacency list
    """
    for idx, src in enumerate(ADJ_list):
        print(f"{id_to_name[idx]} : ", end="")
        for dst, wgh in src: print(f"({id_to_name[dst]}, {wgh})", end=", ")
        print()

# ========================================================================================================
def generate_relations_csv(relations_path: str, num_nodes=10, num_edges=20, min_weight=1, max_weight=100):
    """
    # Self explanatory ahh function.
    random and exactly the specified amount of nodes & edges.
    """
    # The max possible edges in a directed graph is V * (V - 1) that "-1" being no self loops allowed
    max_possible_edges = num_nodes * (num_nodes - 1)
    if num_edges > max_possible_edges: num_edges = max_possible_edges

    # Generate the list of nodes name (0='A', 25='Z', 26='AA', ...)
    nodes = []
    for i in range(num_nodes):
        name = ""
        while i >= 0: # from Least Significant
            name = chr(i % 26 + 65) + name
            i = (i // 26) - 1 # greedy ahh
        nodes.append(name)
    
    # Generate unique edges
    edges = set()
    while len(edges) < num_edges:
        src_idx = random.randint(0, num_nodes - 1)
        dst_idx = random.randint(0, num_nodes - 1)
        # Ensure no self loops(!=) and no dupes(not in) // edges first, weights later
        if src_idx != dst_idx and (src_idx, dst_idx) not in edges: edges.add((src_idx, dst_idx))

    try: # WRITE TO CSV WHILE ALSO GENERATING THE WEIGHTS   
        with relations_path.open('w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file) # simple writer
            writer.writerow(["src", "dst", "wgh"]) # the esteemed header
            writer.writerows( # they say this generator is more efficient
                (nodes[src_id], nodes[dst_id], float(random.randint(min_weight, max_weight)))
                for src_id, dst_id in edges
            )
    except Exception as cursed: print(cursed)



# Quick generate relations
if __name__ == "__main__":
    # setup path connections to required files
    from pathlib import Path # This is better than plain path strings
    ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
    RELATIONS_FILE_PATH = ROOT_DIR / "data" / "relations.csv"

    if input("Generate random relations ? (y/n)") in "Yy":
        generate_relations_csv(RELATIONS_FILE_PATH, num_nodes=26**2, num_edges=1000, min_weight=1, max_weight=50)