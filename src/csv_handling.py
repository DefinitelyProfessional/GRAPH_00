"""
# CSV FILE HANDLING AND PREPARING DATA FOR THE PROGRAM
by Stephen Matthews
"""

import csv
import random

class GRAPHLOADER:
    def __init__(self, relations_path):
        self.relations_path = relations_path
        self.generate_relations_path = relations_path
        self.name_to_id, self.id_to_name, self.ADJ_list = self.prepare_adj_list()

    # ========================================================================================================
    def prepare_adj_list(self):
        """
        # Read CSV and prepare the graph environment
        """
        nodes = set()
        edges = set()
        try: # READ THE CSV
            with open(self.relations_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file); next(reader) # unused header
                for src, dst, wgh in reader:
                    nodes.add(src); nodes.add(dst) # collect the unique nodes
                    edges.add((src, dst, float(wgh))) # store the  unique edges 
        except Exception as cursed: print(cursed)

        # Clever way to map node string names into integer index
        name_to_id = {name: idx for idx, name in enumerate(sorted(nodes))}
        id_to_name = {idx: name for name, idx in name_to_id.items()}

        # Create the graph environment for the sake of dijkstra's efficiency !
        # This will be in the form of an adjacency list ! REFER TO code_breakdown\csv_handling.md
        ADJ_list = [[] for _ in range(len(nodes))]
        for src, dst, wgh in edges: # note edges is alredy a unique set
            ADJ_list[name_to_id[src]].append((name_to_id[dst], wgh))

        return name_to_id, id_to_name, ADJ_list

    # ========================================================================================================
    def search_edge(self, src, dst):
        try:
            if src is str: src = self.name_to_id[src]
            if dst is str: dst = self.name_to_id[dst]
            for destinations, wgh in self.ADJ_list[src]:
                if destinations != dst: continue
                return self.id_to_name[src], self.id_to_name[dst], wgh
            print(f"{src}, {dst} NOT FOUND")
        except: print("Searching Error... likely indexing error... maybe")
        
    # ========================================================================================================
    def display_adjacency_list(self):
        """
        # a dev tool to help visualize teh adjacency list
        """
        map_ = self.id_to_name
        for src, relations in enumerate(self.ADJ_list):
            print(f"{map_[src]} : ", end="")
            for dst, wgh in relations: print(f"({map_[dst]}, {wgh})", end=", ")
            print()

    # ========================================================================================================
    def generate_relations_csv(self, directional=True, num_nodes=10, num_edges=20, min_weight=1, max_weight=100):
        """
        # Self explanatory ahh function.
        random and exactly the specified amount of nodes & edges.
        """
        # The max possible edges in a directed graph is V * (V - 1) that "-1" being no self loops allowed
        # As for a bidirectional graph it would be half of a directional graph cuz of going in 2 ways.
        max_possible_edges = num_nodes * (num_nodes - 1) if directional else (num_nodes * (num_nodes - 1)) // 2
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
            if src_idx == dst_idx: continue # Skip self-loops
            # For bidirectional, (A, B) is the same as (B, A)
            # A clever way to go around that is to ensure A n B is sorted
            if not directional: edge_key = tuple(sorted((src_idx, dst_idx)))
            else: edge_key = (src_idx, dst_idx)
            # Ensure no dupes exist
            if edge_key not in edges: edges.add(edge_key)

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
        LOADER = GRAPHLOADER(RELATIONS_FILE_PATH)
        LOADER.generate_relations_csv(directional=False, num_nodes=26**2, num_edges=1000, min_weight=1, max_weight=50)