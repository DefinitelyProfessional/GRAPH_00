'''
THIS IS MAIN TO HANDLE COORDINATION AND PROGRAM FLOW
'''
# setup path connections to required files
from pathlib import Path # This is better than plain path strings
ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
DATA_DIRECTORY = ROOT_DIR / "data" # Define the data directory where INPUT_FILE_NAME is located
# INPUT_FILE_NAME = "relations.csv" # Specify the exact file name of the input relations
INPUT_FILE_NAME = "directed_relations.csv" # Specify the exact file name of the input relations
# INPUT_FILE_NAME = "undirected_relations.csv" # Specify the exact file name of the input relations

# external py files to decentralize definitions
from csv_handling import CSVHANDLER
from algorithms import GRAPHSTRUCTURE

# read the relations file and setup the program
DATA = CSVHANDLER(DATA_DIRECTORY, INPUT_FILE_NAME)
GRAPH = GRAPHSTRUCTURE(DATA.graphdata)

# MAIN PROGRAM EXECUTION
if __name__ == "__main__":

    # TODO PROGRAM CONTROL WOY
    # while True:

    #     match input():
    #         case "1":
    #             pass
    #         case "2":
    #             pass

    # GRAPH.display_adjacency_list()
    GRAPH.display_nodes()
    start_node = input("Start : ")
    end_node = input("End : ")
    GRAPH.routing_engine(start_node, end_node)