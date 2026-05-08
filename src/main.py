'''
THIS IS MAIN TO HANDLE COORDINATION AND PROGRAM FLOW
'''
# setup path connections to required files
from pathlib import Path # This is better than plain path strings
ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
RELATIONS_FILE_PATH = ROOT_DIR / "data" / "relations.csv"

# external py files to decentralize definitions
from csv_handling import DATALOADER
from algorithms import GRAPHLIST

# read the relations file and setup the program
DATA = DATALOADER(RELATIONS_FILE_PATH)
GLIST = GRAPHLIST(DATA.ADJ_list, DATA.name_to_id, DATA.id_to_name, DATA.max_str_len)

# MAIN PROGRAM EXECUTION
if __name__ == "__main__":
    while True:

        match input():
            case "1":
                pass
            case "2":
                pass

    # DATA.display_adjacency_list()
    GLIST.display_nodes()
    start_node = input("Start : ")
    end_node = input("End : ")
    GLIST.routing_engine(start_node, end_node)