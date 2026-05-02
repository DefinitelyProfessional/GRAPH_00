'''
THIS IS MAIN TO HANDLE COORDINATION AND PROGRAM FLOW
'''
# setup path connections to required files
from pathlib import Path # This is better than plain path strings
ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
RELATIONS_FILE_PATH = ROOT_DIR / "data" / "relations.csv"

# external py files to decentralize definitions
from csv_handling import prepare_adj_list
from algorithms import routing_engine

# read the relations and initialize the ADJ_list
name_to_id, id_to_name, ADJ_list = prepare_adj_list(RELATIONS_FILE_PATH)

# --- Demo Execution ---
if __name__ == "__main__":
    print(name_to_id.keys())
    start_node = input("Start : ")
    end_node = input("End : ")
    routing_engine(ADJ_list, name_to_id, id_to_name, start_node, end_node)