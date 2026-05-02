'''
THIS IS MAIN TO HANDLE COORDINATION AND PROGRAM FLOW
'''
# setup path connections to required files
from pathlib import Path # This is better than plain path strings
ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
RELATIONS_FILE_PATH = ROOT_DIR / "data" / "relations.csv"

# external py files to decentralize definitions
from csv_handling import read_relations
from algorithms import optimized_dijkstra

# read the relations and initialize teh graph_environment
graph_environment = read_relations(RELATIONS_FILE_PATH)

# --- Demo Execution ---
if __name__ == "__main__":
    pass
    # # Your mock CSV data (src, dst, weight)
    # edges = [
    #     ("Jakarta", "Bekasi", 20),
    #     ("Jakarta", "Depok", 15),
    #     ("Bekasi", "Cikarang", 25),
    #     ("Depok", "Cikarang", 30),
    #     ("Cikarang", "Bandung", 60),
    #     ("Bekasi", "Bogor", 40) # A dead end for fun
    # ]
    
    # dist, route = run_routing_engine(edges, "Jakarta", "Bandung")
    # print(f"Total Distance: {dist}")
    # print(f"Optimal Route: {' -> '.join(route)}")