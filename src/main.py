'''
THIS IS MAIN TO HANDLE COORDINATION AND PROGRAM FLOW
'''
# setup path connections to required files
from pathlib import Path # This is better than plain path strings
ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
RELATIONS_FILE_PATH = ROOT_DIR / "data" / "relations.csv"

# external py files to decentralize definitions
from csv_handling import GRAPHLOADER
from algorithms import routing_engine

# read the relations and initialize the ADJ_list
GRAPH = GRAPHLOADER(RELATIONS_FILE_PATH)

# --- Demo Execution ---
if __name__ == "__main__":
    print(GRAPH.name_to_id.keys())
    start_node = input("Start : ")
    end_node = input("End : ")
    total_distance, path_names = routing_engine(GRAPH.ADJ_list, GRAPH.name_to_id, GRAPH.id_to_name, start_node, end_node)
    
    for i in range(1, len(path_names)):
        src, dst = GRAPH.name_to_id[path_names[i-1]], GRAPH.name_to_id[path_names[i]]
        src, dst, wgh = GRAPH.search_edge(src, dst)
        print(f"{src} -> {dst} : {wgh}")
    print("total distance :",  total_distance)