import random

def generate_ascii_maze(width, height):
    # A perfect maze of N cells requires (2N+1) characters.
    # To get ~30x30 characters, we target 15x15 cells,
    # which gives a (2*15+1) x (2*15+1) = 31x31 grid.
    
    char_width = 31
    char_height = 31
    
    # Initialize grid with all walls '#'
    grid = [['###' for _ in range(char_width)] for _ in range(char_height)]
    
    # Define cells (odd coordinates in the 31x31 grid)
    cells_x = char_width // 2
    cells_y = char_height // 2
    
    # Start the DFS iterative traversal at (1, 1)
    # The cells are at indices like (1,1), (1,3), (3,1), (3,3)...
    # up to (29, 29).
    start_cell = (1, 1)
    stack = [start_cell]
    grid[start_cell[1]][start_cell[0]] = '   '  # Path
    
    # Directions: (dx, dy) for moving 2 cells away
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
    
    while stack:
        x, y = stack[-1]
        
        # Get unvisited neighbors (still walls)
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check boundaries of cell space
            if 1 <= nx < char_width and 1 <= ny < char_height:
                if grid[ny][nx] == '###':
                    neighbors.append((nx, ny))
                    
        if neighbors:
            # Choose a random unvisited neighbor
            nx, ny = random.choice(neighbors)
            
            # Carve the path between current and neighbor
            # and mark neighbor as a path
            # Wall coordinate is ((x+nx)//2, (y+ny)//2)
            wall_x = (x + nx) // 2
            wall_y = (y + ny) // 2
            grid[wall_y][wall_x] = '   '
            grid[ny][nx] = '   '
            
            # Push neighbor to stack to continue traversal
            stack.append((nx, ny))
        else:
            # Backtrack when at a dead end
            stack.pop()

    # Place Start 'S' and End 'E' points
    # Start: Top-left cell (1, 1)
    # End: Bottom-right cell (29, 29)
    
    # Ensure they are placed at cells, not walls.
    grid[1][1] = ' S '
    grid[char_height - 2][char_width - 2] = ' E '
    
    # Convert grid to string
    maze_string = "\n".join("".join(row) for row in grid)
    return maze_string

# Generate the 30x30 character-size perfect maze
final_maze = generate_ascii_maze(30, 30)
print(final_maze)