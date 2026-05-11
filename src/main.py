'''
THIS IS MAIN TO HANDLE COORDINATION AND PROGRAM FLOW
'''
# setup path connections to required files
from pathlib import Path # This is better than plain path strings
ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00 
DATA_DIRECTORY = ROOT_DIR / "data" # Define the data directory where INPUT_FILE_NAME is located
INPUT_FILE_NAME = "relations.csv" # Specify the exact file name of the input relations
# INPUT_FILE_NAME = "directed_relations.csv" # Specify the exact file name of the input relations
# INPUT_FILE_NAME = "undirected_relations.csv" # Specify the exact file name of the input relations

# external py files to decentralize definitions
from csv_handling import CSVHANDLER
from algorithms import GRAPHSTRUCTURE
from rich_ui import UI_MANAGER

# read the relations file and setup the program
HANDLER = CSVHANDLER(DATA_DIRECTORY, INPUT_FILE_NAME)
GRAPH = GRAPHSTRUCTURE(HANDLER.graphdata)
UI = UI_MANAGER()
# MAIN PROGRAM EXECUTION
if __name__ == "__main__":
    UI.show_title() # only once in the beginning
    # show menu once and only display when the user pressed invalid action choices
    UI.show_main_menu() 

    while True:
        match UI.get_choice():
            # EXIT PROGRAM
            case "0": break
            # Display the main menu again
            case "1": UI.show_main_menu()
            # Display all nodes
            case "2":
                UI.show_section("List of ALL available nodes")
                # TODO display nodes should be handled by UI instead, Not by GRAPH
            # Run Shortest Path
            case "3":
                UI.show_section("Finding Shortest Path", "green")
                start_node, end_node = UI.ask_shortest_path_nodes()
                # TODO the display part of the routing engine should be done by UI
                GRAPH.routing_engine(start_node, end_node)
            # Generate MST
            case "4":
                UI.show_section("Generating MST Relations", "yellow")
                MST_EDGE_SET = GRAPH.build_MST()
                UI.show_mst_preview(MST_EDGE_SET)
                output_file = UI.ask_mst_output_file()
                HANDLER.write_new_relations(output_file, payload_edges=MST_EDGE_SET)
            # Change Input
            case "5":
                UI.show_section("Ganti File Input CSV", "cyan")
                current_input_file = UI.choose_input_file()
                # New file path handling is already done by the prepare_graph 
                HANDLER.graphdata = HANDLER.prepare_graph(current_input_file)
                GRAPH = GRAPHSTRUCTURE(HANDLER.graphdata)
                UI.show_success(f"Berhasil berpindah ke file: {current_input_file}")
    UI.show_goodbye()