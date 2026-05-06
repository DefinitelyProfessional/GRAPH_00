"""
# CSV FILE HANDLING AND PREPARING DATA FOR THE PROGRAM
by Stephen Matthews
"""

import csv
import random

class DATALOADER:
    def __init__(self, relations_path):
        self.relations_path = relations_path
        self.generate_relations_path = relations_path
        self.max_str_len, self.name_to_id, self.id_to_name, self.ADJ_list, self.ADJ_mtrx = self.prepare_adj_list()

    # ========================================================================================================
    def prepare_adj_list(self):
        """
        ## Read CSV and prepare the graph environment
        """
        nodes = set()
        edges = set()
        # READ THE CSV, Intentionally no try except is used here because any error would
        # make the program unable to continue run anyways, so let it be a blocking error
        with open(self.relations_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file); next(reader) # unused header
            for src, dst, wgh in reader:
                nodes.add(src); nodes.add(dst) # collect the unique nodes
                edges.add((src, dst, float(wgh))) # store the  unique edges

        # Clever way to map node string names into integer index
        name_to_id = {name: idx for idx, name in enumerate(sorted(nodes))}
        id_to_name = {idx: name for name, idx in name_to_id.items()}

        # Create the graph environment as an adjacency list for the sake of dijkstra's efficiency
        # Explanation for how this ADJ_list works is documented in code_breakdown\csv_handling.md
        nodecount = len(nodes)
        ADJ_list = [[] for _ in range(nodecount)]
        ADJ_mtrx = [[float("inf")]*nodecount for _ in range(nodecount)]
        for src, dst, wgh in edges: # note edges is alredy a unique set
            ADJ_list[name_to_id[src]].append((name_to_id[dst], wgh))
            ADJ_mtrx[name_to_id[src]][name_to_id[dst]] = wgh
        
        # get the max length of node strings, niche for displays
        max_str_len = max(len(s) for s in nodes)

        return max_str_len, name_to_id, id_to_name, ADJ_list, ADJ_mtrx
        
    # ========================================================================================================
    def display_adjacency_list(self):
        """
        ## a dev tool to help visualize teh adjacency list
        """
        map_ = self.id_to_name
        for src, relations in enumerate(self.ADJ_list):
            print(f"{map_[src]} : ", end="")
            for dst, wgh in relations: print(f"({map_[dst]}, {wgh})", end=", ")
            print()

    # ========================================================================================================
    def generate_relations_csv(self, directional=True, nodecount=10, num_edges=20, min_weight=1, max_weight=100):
        """
        ## Self explanatory ahh function.
        random and exactly the specified amount of nodes & edges.
        """
        # The max possible edges in a directed graph is V * (V - 1) that "-1" being no self loops allowed
        # As for a bidirectional graph it would be half of a directional graph cuz of going in 2 ways.
        max_possible_edges = nodecount * (nodecount - 1) if directional else (nodecount * (nodecount - 1)) // 2
        if num_edges > max_possible_edges: num_edges = max_possible_edges

        # Generate the list of nodes name (0='A', 25='Z', 26='AA', ...)
        nodes = []
        for i in range(nodecount):
            name = ""
            while i >= 0: # from Least Significant
                name = chr(i % 26 + 65) + name
                i = (i // 26) - 1 # greedy ahh
            nodes.append(name)
        
        # Generate unique edges
        edges = set()
        while len(edges) < num_edges:
            src_idx = random.randint(0, nodecount - 1)
            dst_idx = random.randint(0, nodecount - 1)
            if src_idx == dst_idx: continue # Skip self-loops
            # For bidirectional, (A, B) is the same as (B, A)
            # A clever way to go around that is to ensure A n B is sorted
            # edges being a set already ensures no dupes exist
            edges.add((src_idx, dst_idx) if directional else tuple(sorted((src_idx, dst_idx))))

        try: # WRITE TO CSV WHILE ALSO GENERATING THE WEIGHTS   
            with self.generate_relations_path.open('w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file) # simple writer
                writer.writerow(["src", "dst", "wgh"]) # the esteemed header
                if directional:
                    writer.writerows( # they say this generator is more efficient
                        (nodes[src_id], nodes[dst_id], float(random.randint(min_weight, max_weight)))
                        for src_id, dst_id in edges
                    )
                else:
                    for src_id, dst_id in edges:
                        wgh = float(random.randint(min_weight, max_weight))
                        writer.writerow((nodes[src_id], nodes[dst_id], wgh))
                        writer.writerow((nodes[dst_id], nodes[src_id], wgh))
        except Exception as cursed: print(cursed)

# Quick generate relations
if __name__ == "__main__":
    # setup path connections to required files
    from pathlib import Path # This is better than plain path strings
    ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
    RELATIONS_FILE_PATH = ROOT_DIR / "data" / "relations.csv"

    if input("Generate random relations ? (y/n)") in "Yy":
        LOADER = DATALOADER(RELATIONS_FILE_PATH)
        LOADER.generate_relations_csv(directional=True, nodecount=26**2, num_edges=10000, min_weight=1, max_weight=50)