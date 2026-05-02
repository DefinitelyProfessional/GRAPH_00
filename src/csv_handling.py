import csv
import random

# 
def prepare_graph(relations_path: str):
    return

# ===================================================================================================
def generate_relations_csv(relations_path: str, num_nodes=10, num_edges=20, min_weight=1, max_weight=100):
    """
    # Self explanatory ahh function.
    random and exactly the specified amount of nodes & edges.
    """
    # The max possible edges in a directed graph is V * (V - 1) that "-1" being no self loops allowed
    max_possible_edges = num_nodes * (num_nodes - 1)
    if num_edges > max_possible_edges: num_edges = max_possible_edges

    # Generate the list of node_names (0='A', 25='Z', 26='AA', ...)
    node_names = []
    for i in range(num_nodes):
        name = ""
        while i >= 0: # from Least Significant
            name = chr(i % 26 + 65) + name
            i = (i // 26) - 1 # greedy ahh
        node_names.append(name)
    
    # Generate unique edges
    edges = set()
    while len(edges) < num_edges:
        src_idx = random.randint(0, num_nodes - 1)
        dst_idx = random.randint(0, num_nodes - 1)
        # Ensure no self loops(!=) and no dupes(not in) // edges first, weights later
        if src_idx != dst_idx and (src_idx, dst_idx) not in edges: edges.add((src_idx, dst_idx))

    try: # WRITE TO CSV WHILE ALSO GENERATING THE WEIGHTS   
        with open(relations_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f) # We love CSV
            writer.writerow(["src", "dst", "wgh"]) # The esteemed Header
            for src_id, dst_id in edges: # THIS IS WHERE THE WEIGHT IS GENERATED
                weight = random.randint(min_weight, max_weight) 
                writer.writerow([node_names[src_id], node_names[dst_id], weight])
    except Exception as cursed: print(cursed)

# Quick generate relations
if __name__ == "__main__":
    # setup path connections to required files
    from pathlib import Path # This is better than plain path strings
    ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
    RELATIONS_FILE_PATH = ROOT_DIR / "data" / "relations.csv"

    generate_relations_csv(RELATIONS_FILE_PATH, num_nodes=10, num_edges=30, min_weight=1, max_weight=50)