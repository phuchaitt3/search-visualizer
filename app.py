import streamlit as st
import os
from collections import deque
import json

# Import your search algorithms
from sortedcontainers import SortedDict
import random

# Include all your previously implemented algorithms here
def bfs(arr, source, destination):
    if source == destination:
        return {}, [source]

    frontier = deque([(source, [source])])
    frontier_set = {source}
    explored = set()

    while frontier:
        node, path = frontier.popleft()
        frontier_set.remove(node)
        
        explored.add(node)
        for neighbor, cost in enumerate(arr[node]):
            if cost > 0 and neighbor not in explored and neighbor not in frontier_set:
                if neighbor == destination:
                    return explored, path + [neighbor]
                frontier.append((neighbor, path + [neighbor]))
                frontier_set.add(neighbor)

    return explored, []
    pass

# 1.2. Depth-first search (DFS)
def dfs(arr, source, destination):
    if source == destination:
        return {}, [source]
    
    frontier = [(source, [source])]
    frontier_set = {source}
    explored = set()

    while frontier:
        node, path = frontier.pop()
        frontier_set.remove(node)
        
        explored.add(node)
        for neighbor, cost in enumerate(arr[node]):
            if cost > 0 and neighbor not in explored and neighbor not in frontier_set:
                if neighbor == destination:
                    return explored, path + [neighbor]
                frontier.append((neighbor, path + [neighbor]))
                frontier_set.add(neighbor)
                
    return explored, []
    pass

# 1.3. Uniform-cost search (UCS)
def ucs(arr, source, destination):
    frontier = SortedDict()
    frontier[(0, source)] = [source]
    frontier_set = {source}
    explored = set()
    node_cost = {source: 0}

    while frontier:
        (cost, node), path = frontier.popitem(0)
        frontier_set.remove(node)
        
        if node == destination:
            return explored, path
        
        explored.add(node)
        for neighbor, edge_cost in enumerate(arr[node]):
            if edge_cost > 0:
                new_cost = cost + edge_cost
                
                if neighbor not in explored and neighbor not in frontier_set:
                    frontier[(new_cost, neighbor)] = path + [neighbor]
                    frontier_set.add(neighbor)
                    node_cost[neighbor] = new_cost
                    
                elif neighbor in frontier_set and new_cost < node_cost[neighbor]:
                    del frontier[(node_cost[neighbor], neighbor)]
                    frontier[(new_cost, neighbor)] = path + [neighbor]
                    node_cost[neighbor] = new_cost
                
    return explored, []
    pass

# 1.4. Iterative deepening search (IDS)
# 1.4.a. Depth-limited search
def dls(arr, source, destination, depth_limit):
    if depth_limit < 0:
        return {}, []
    
    if depth_limit == 0:
        if source == destination:
            return {}, [source]
        return {}, []
    
    frontier = [(source, [source], depth_limit)]
    frontier_set = {source}
    explored = set()

    while frontier:
        node, path, depth = frontier.pop()
        frontier_set.remove(node)

        explored.add(node)
        for neighbor, cost in enumerate(arr[node]):
            if cost > 0 and neighbor not in explored and neighbor not in frontier_set:
                if neighbor == destination:
                    return explored, path + [neighbor]
                if depth - 1 == 0:
                    continue
                frontier.append((neighbor, path + [neighbor], depth - 1))
                frontier_set.add(neighbor)

    return {}, []
    pass

# 1.4.b. IDS
def ids(arr, source, destination):
    for depth in range(len(arr)):
        explored, path = dls(arr, source, destination, depth)
        if path:
            return explored, path
    return {}, []
    pass

# 1.5. Greedy best first search (GBFS)
def gbfs(arr, source, destination, heuristic):
    frontier = SortedDict()
    frontier[(heuristic[source], source)] = [source]
    frontier_set = {source}
    explored = set()

    while frontier:
        (_, node), path = frontier.popitem(0)
        frontier_set.remove(node)
        
        explored.add(node)
        for neighbor, cost in enumerate(arr[node]):
            if cost > 0 and neighbor not in explored and neighbor not in frontier_set:
                if neighbor == destination:
                    return explored, path + [neighbor]
                frontier[(heuristic[neighbor], neighbor)] = path + [neighbor]
                frontier_set.add(neighbor)
                
    return explored, []
    pass

# 1.6. Graph-search A* (AStar)
def astar(arr, source, destination, heuristic):
    frontier = SortedDict()
    frontier[(0 + heuristic[source], source)] = (0, [source])
    frontier_set = {source}
    explored = set()
    node_cost = {source: 0}

    while frontier:
        (f_cost, node), (g_cost, path) = frontier.popitem(0)
        frontier_set.remove(node)
        
        if node == destination:
            return explored, path
        
        explored.add(node)
        for neighbor, edge_cost in enumerate(arr[node]):
            if edge_cost > 0:
                new_g_cost = g_cost + edge_cost
                new_f_cost = new_g_cost + heuristic[neighbor]
                
                if neighbor not in explored and neighbor not in frontier_set:
                    frontier[(new_f_cost, neighbor)] = (new_g_cost, path + [neighbor])
                    frontier_set.add(neighbor)
                    node_cost[neighbor] = new_g_cost

                elif neighbor in frontier_set and new_g_cost < node_cost[neighbor]:
                    del frontier[(node_cost[neighbor] + heuristic[neighbor], neighbor)]
                    frontier[(new_f_cost, neighbor)] = (new_g_cost, path + [neighbor])
                    node_cost[neighbor] = new_g_cost
                
    return explored, []
    pass

# 1.7. Hill-climbing First-choice (HC)
def hc(arr, source, destination, heuristic):
    visited = {}
    node = source
    path = [source]

    while node != destination:
        neighbors = [(heuristic[neighbor], neighbor) for neighbor, cost in enumerate(arr[node]) if cost > 0]
        if not neighbors:
            return visited, []
        
        random.shuffle(neighbors)
        
        for _, next_node in neighbors:
            if heuristic[next_node] < heuristic[node]:
                visited[next_node] = node
                path.append(next_node)
                node = next_node
                break
        else:
            return visited, []

    return visited, path
    pass

# Streamlit Interface
st.title("Search Algorithms Visualization")

# Algorithm selection
algorithm = st.selectbox(
    "Choose an algorithm",
    ["BFS", "DFS", "UCS", "IDS", "GBFS", "A*", "Hill-Climbing"]
)

# Text input for graph data
input_data = st.text_area("Paste the input data (number of nodes, start/end nodes, adjacency matrix, and node values):", 
                          height=200, 
                          placeholder="Example:\n5\n0 4\n0 1 0 0 0\n1 0 1 0 0\n0 1 0 1 0\n0 0 1 0 1\n0 0 0 1 0\n7 6 5 4 3")

if st.button("Visualize Path"):
    if input_data:
        try:
            # Parse the input data
            input_lines = input_data.strip().split('\n')
            n = int(input_lines[0])  # Number of nodes
            start, end = map(int, input_lines[1].split())  # Start and End nodes
            
            # Extract the adjacency matrix
            adj_matrix = []
            for i in range(2, 2 + n):
                adj_matrix.append(list(map(int, input_lines[i].split())))
            
            # Extract the heuristic for specific algorithms
            heuristic = None
            if algorithm in ["GBFS", "A*", "Hill-Climbing"]:
                heuristic = list(map(int, input_lines[2 + n].split()))
            
            # Run the selected algorithm
            explored, path = [], []
            if algorithm == "BFS":
                explored, path = bfs(adj_matrix, start, end)
            elif algorithm == "DFS":
                explored, path = dfs(adj_matrix, start, end)
            elif algorithm == "UCS":
                explored, path = ucs(adj_matrix, start, end)
            elif algorithm == "IDS":
                explored, path = ids(adj_matrix, start, end)
            elif algorithm == "GBFS":
                explored, path = gbfs(adj_matrix, start, end, heuristic)
            elif algorithm == "A*":
                explored, path = astar(adj_matrix, start, end, heuristic)
            elif algorithm == "Hill-Climbing":
                explored, path = hc(adj_matrix, start, end, heuristic)
            else:
                st.error("Invalid algorithm selection.")
                path = []

            # Visualization using HTML + D3.js
            if path:
                st.write("### Path:", path)
                
                # Read HTML template
                with open(os.path.join('static', 'index.html'), 'r') as f:
                    html_template = f.read()
                
                # Inject the values into the HTML template
                html_content = html_template.replace("{{ algorithm }}", algorithm)\
                                            .replace("{{ n }}", json.dumps(n))\
                                            .replace("{{ start }}", json.dumps(start))\
                                            .replace("{{ end }}", json.dumps(end))\
                                            .replace("{{ adj_matrix }}", json.dumps(adj_matrix))\
                                            .replace("{{ path }}", json.dumps(path))

                # Display the HTML with D3.js visualizing the path
                st.components.v1.html(html_content, height=600)
            else:
                st.error("No path found.")
            
        except Exception as e:
            st.error(f"Error parsing input data: {e}")
    else:
        st.error("Please enter input data.")