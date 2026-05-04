'''
THIS IS MAIN TO HANDLE COORDINATION AND PROGRAM FLOW
'''
# setup path connections to required files
from pathlib import Path # This is better than plain path strings
ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
RELATIONS_FILE_PATH = ROOT_DIR / "data" / "relations.csv"

# external py files to decentralize definitions
from csv_handling import DATALOADER
from algorithms import GRAPHSTRUCTURE

# read the relations file and setup the program
DATA = DATALOADER(RELATIONS_FILE_PATH)
GRAPH = GRAPHSTRUCTURE(DATA.ADJ_list, DATA.name_to_id, DATA.id_to_name)

# --- Demo Execution ---
if __name__ == "__main__":
    DATA.display_adjacency_list()
    start_node = input("Start : ")
    end_node = input("End : ")
    GRAPH.routing_engine(start_node, end_node)