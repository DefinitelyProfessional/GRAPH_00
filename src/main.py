'''
THIS IS MAIN TO HANDLE COORDINATION AND PROGRAM FLOW
'''
from pathlib import Path
from rich.text import Text

from csv_handling import CSVHANDLER
from algorithms import GRAPHSTRUCTURE
from rich_ui import UI_MANAGER

ROOT_DIR = Path(__file__).resolve().parents[1] # 0:src, 1:GRAPH_00
DATA_DIRECTORY = ROOT_DIR / "data" # MUST BE DEFINED
INPUT_FILE_NAME = "" # to be defined by program 

# Initialize UI manager
UI = UI_MANAGER()

def update_graph_session(ui_, directory):
    """Handle file selection and object re-initialization."""
    selected_file = ui_.select_file_from_directory(directory)
    # if 
    if selected_file:
        # Re-initialize the handler and graph with the new file
        new_handler = CSVHANDLER(directory, selected_file)
        new_graph = GRAPHSTRUCTURE(new_handler.graphdata)
        
        ui_.set_content("FILE LOADED !", f"Active File in use : [bold cyan]{selected_file}[/]", color="green")
        ui_.set_status(f"Loaded {selected_file} successfully.", "green")
        
        return new_handler, new_graph, selected_file
    # indicate a failed update
    return None, None, None

if __name__ == "__main__":
    # Initial file loading
    HANDLER, GRAPH, INPUT_FILE_NAME = update_graph_session(UI, DATA_DIRECTORY)
    # Safety check if no files were found or selected
    if not HANDLER:
        UI.console.print("[bold red]System could not start without a data file. Exiting...[/]")
        exit()
    
    while True:
        # Render the current UI state and wait for a command        
        match UI.prompt("SELECT ACTION", choices=["0", "1", "2", "3", "4", "5"], default="1"):
            case "0": # EXIT PROGRAM
                UI.clear_terminal() # Clear screen one last time and exit cleanly
                UI.console.print("[bold cyan]End of Session. Thank you, goodbye![/bold cyan]")
                break
                
            case "1": # WINDOW RESET usually to fix inherent terminal display limitations
                UI.set_content("Content", Text("Cleared. Waiting for command.", style="dim"))
                UI.set_status("Ready.", "green")
                
            case "2": # SHOW ALL NODES
                UI.display_nodes(GRAPH.nodenames)
                UI.set_status("Take a look. Take your time.", "green")
                
            case "3": # SHORTEST PATH
                UI.display_nodes(GRAPH.nodenames)
                UI.set_status("Waiting for Start & End nodes ...", "yellow")
                
                # Prompt for parameters.
                start_node = UI.prompt("Enter Start node")
                UI.set_status(f"Start at Node {start_node} to ?", "yellow")
                end_node = UI.prompt("Enter End node")

                error_occured, status_str, traversal_paths, total_wgh_sum = GRAPH.routing_engine(start_node, end_node) 
                if error_occured:
                    UI.set_content("Shortest Path (Dijkstra)", "No traversal path was returned ...", color="red")
                    UI.set_status(f"ERROR : {status_str}", "red")
                else:
                    UI.display_traversal(traversal_paths, total_wgh_sum)
                    UI.set_status(f"Path calculated from {start_node} to {end_node} with a TOTAL WEIGHT of {total_wgh_sum}", "green")
                
            case "4": # GENERATE MST
                UI.set_status("Generating MST...", "yellow")
                MST_EDGE_SET = GRAPH.build_MST()
                
                # Use the UI to build the table renderable, then set it as the content
                mst_table = UI.generate_mst_table(MST_EDGE_SET)
                UI.set_content("Preview of the Minimum Spanning Tree", mst_table, color="magenta")
                
                # Ask for output file
                output_file = UI.prompt("Enter MST output file name (Empty to Cancel)", default="")
                if output_file: 
                    HANDLER.write_new_relations(output_file, payload_edges=MST_EDGE_SET)
                    UI.set_status(f"MST saved to {output_file}", "green")
                else: UI.set_status(f"Empty file, save cancelled.", "yellow")
                
            case "5": # CHANGE FILE
                NEW_H, NEW_G, NEW_NAME = update_graph_session(UI, DATA_DIRECTORY)
                # Only reset the handler and graph if it's a successful update
                if NEW_H: HANDLER, GRAPH, INPUT_FILE_NAME = NEW_H, NEW_G, NEW_NAME