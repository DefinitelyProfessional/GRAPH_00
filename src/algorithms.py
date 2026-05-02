import heapq
INF = float("inf")

def optimized_dijkstra(graph, start_node, end_node):
    """
    The core algorithmic engine. 
    Expects nodes to be integers (0 to N-1).
    graph format: graph[source_id] = [(neighbor_id, weight), ...]
    """
    num_nodes = len(graph)
    
    # Pre-allocated arrays (Lighting fast integer lookups)
    distances = [INF] * num_nodes
    predecessors = [-1] * num_nodes  # -1 means no predecessor yet
    visited = [False] * num_nodes
    
    distances[start_node] = 0
    
    # Priority Queue stores tuples: (current_distance, node_id)
    pq = [(0, start_node)]
    
    while pq:
        # 1. Pop the node with the absolute shortest known distance
        current_distance, current_node = heapq.heappop(pq)
        
        # 2. Early Exit: If we reached the destination, we are done
        if current_node == end_node:
            break
            
        # 3. Skip stale entries (nodes we've already fully processed)
        if visited[current_node]:
            continue
            
        # Mark as permanently settled
        visited[current_node] = True
        
        # 4. Explore all neighbors (Fast iteration over a list of tuples)
        for neighbor, weight in graph[current_node]:
            if visited[neighbor]:
                continue
                
            new_distance = current_distance + weight
            
            # 5. Relaxation Step: Did we find a faster route?
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node  # Record the path step
                heapq.heappush(pq, (new_distance, neighbor))
                
    # --- Path Reconstruction ---
    if distances[end_node] == INF:
        return INF, []  # No path exists
        
    path = []
    current = end_node
    while current != -1:  # Trace backward until we hit the start node
        path.append(current)
        current = predecessors[current]
        
    path.reverse()  # Flip it to read from Start -> End
    
    return distances[end_node], path


# ==========================================
# Translation Layer (For your CSV Data)
# ==========================================

def routing_engine(ADJ_list, name_to_id, id_to_name, start_node, end_node):
    # 3. Check if user input is valid
    if start_node not in name_to_id or end_node not in name_to_id:
        return "Invalid start or end node."
        
    # 4. Run the Engine!
    start_id = name_to_id[start_node]
    end_id = name_to_id[end_node]
    
    total_distance, path_ids = optimized_dijkstra(ADJ_list, start_id, end_id)
    
    # 5. Translate results back to human-readable strings
    if total_distance == INF:
        return f"No path found between {start_node} and {end_node}."
        
    path_names = [id_to_name[node_id] for node_id in path_ids]
    
    return total_distance, path_names

# --- Demo Execution ---
if __name__ == "__main__":
    pass