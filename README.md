# GRAPH_00
TUI based, interactive Dijkstra's Shortest Path Demo and Minimum Spanning Tree Generator made in python with `rich` UI.  
This is a university issued final semester project under the theme "Graphs".
---


# Dependencies
The program uses the `rich` library for the TUI interface. One will have to install it using `pip install rich` before running the program.
---


# Project Structure
1. `GRAPH_00/src` holds all of the source code for the project.
2. `GRAPH_00/data` to store the graph data files that can be used as input for the program.
3. `GRAPH_00/code_breakdown` contains explanations of the source code files and their functionalities.
Note the UI of this project will not be documented as much as it is trivial compared to the main focus being graphs.

# Usage
Simply put `.csv` files containing 3 entry relations data, being `src,dst,wgh` in the `data` directory and run the `main.py` file in the `src` folder. The program should be self explanatory enough to navigate through the TUI interface and use the features of the program. There are default graph data files provided in the `data` directory that can be used to test the program.