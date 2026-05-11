"""
# CSV FILE HANDLING AND PREPARING DATA FOR THE PROGRAM
by Stephen Matthews
"""
from graphdataclass import GRAPHDATA
from pathlib import Path
import csv
import random

class CSVHANDLER:
    def __init__(self, data_directory:Path, input_file:str, output_file:str=None):
        self.data_directory = Path(data_directory) # Ensure data_directory is a Path object
        self.input_path = self.data_directory / input_file # setup the input file path

        # Verify the input file exists before processing
        if not self.input_path.exists():
            raise FileNotFoundError(f"Missing relations file at: {self.input_path}")

        if output_file: self.output_path = self.data_directory / output_file # setup output
        else: self.output_path = self.input_path.with_stem(f"{self.input_path.stem}_new")

        print(f"Input  Filepath at {self.input_path}")
        print(f"Output Filepath at {self.output_path}")
        
        self.graphdata = self.prepare_graph() # for storing data read by prepare_graph

    # ========================================================================================================
    def prepare_graph(self):
        """
        ## Read CSV and prepare the graph environment
        """
        nodes = set()
        edges = set()
        # READ THE CSV, Intentionally no try except is used here because any error would
        # make the program unable to continue run anyways, so let it be a blocking error
        with open(self.input_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file); next(reader) # unused header
            for src, dst, wgh in reader:
                nodes.add(src); nodes.add(dst) # collect the unique nodes
                edges.add((src, dst, float(wgh))) # store the unique edges

        # Clever way to map node string names into integer index
        name_to_id = {name: idx for idx, name in enumerate(sorted(nodes))}
        id_to_name = {idx: name for name, idx in name_to_id.items()}

        # get the max length of node strings, niche for displays
        max_str_len = max(len(s) for s in nodes)

        # Create the graph environment as an adjacency list for the sake of dijkstra's efficiency
        # Explanation for how this ADJ_list works is documented in code_breakdown\csv_handling.md
        nodecount = len(nodes)

        # Generate the Adjacency List the program will use for data processing
        ADJ_list = [[] for _ in range(nodecount)]
        for src, dst, wgh in edges: # note edges is alredy a unique set
            ADJ_list[name_to_id[src]].append((name_to_id[dst], wgh))
        return GRAPHDATA(name_to_id, id_to_name, nodecount, name_to_id.keys(), ADJ_list, max_str_len)

    # ========================================================================================================
    def write_new_relations(self, new_path="", payload_edges=set()):
        """
        ## Write a new edge set to self.output_path,
        i.e. used by MST to print the new generated MST relations
        """
        # if a relations_path is specified it will write into the specified new relations path
        if new_path : self.output_path = self.data_directory / new_path
        # there must be a non empty set of new edges to be written
        if not payload_edges: print("Empty Edge set, write cancelled."); return
        # write the new edges set into the new relations file path
        with open(self.output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, ); writer.writerow(['src', 'dst', 'wgh']) # write csv header
            writer.writerows(payload_edges)
        print(f"Specified edge set successfuly writen to :\n{self.output_path}")

    # ========================================================================================================
    def generate_relations_csv(self, new_file_path='', directional=True, nodecount=26**2+26, num_edges=100000, min_weight=1, max_weight=1000):
        """
        ## Self explanatory ahh function.
        random and exactly the specified amount of nodes & edges.
        """
        # Setup the new_relations_path
        if new_file_path: self.output_path = self.data_directory / new_file_path

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
            with open(self.output_path, 'w', newline='', encoding='utf-8') as file:
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
    DATA_DIRECTORY = ROOT_DIR / "data"

    if input("Generate random relations ? (y/n)") in "Yy":
        LOADER = CSVHANDLER(DATA_DIRECTORY, "relations.csv")
        LOADER.generate_relations_csv(new_file_path="relations.csv",directional=True)
        # LOADER.generate_relations_csv(new_file_path="directed_relations.csv",directional=True)
        # LOADER.generate_relations_csv(new_file_path="undirected_relations.csv",directional=False)