import streamlit as st
import os
from collections import deque
import json

def bfs(adj_matrix, start, end):
    n = len(adj_matrix)
    visited = [False] * n
    prev = [-1] * n
    queue = deque([start])
    visited[start] = True

    while queue:
        node = queue.popleft()
        if node == end:
            break

        for neighbor, is_connected in enumerate(adj_matrix[node]):
            if is_connected and not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True
                prev[neighbor] = node

    # Reconstruct the path
    path = []
    at = end
    while at != -1:
        path.append(at)
        at = prev[at]
    path.reverse()

    if path[0] == start:
        return path
    else:
        return []

# Streamlit Interface
st.title("BFS Path Visualization")

# Large Text Area Input
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
            
            # Extract the node values (if necessary for future use)
            node_values = list(map(int, input_lines[2 + n].split()))
            
            # Run BFS to get the path
            path = bfs(adj_matrix, start, end)
            
            # Serve the BFS visualization HTML in an iframe
            st.write("### BFS Path Visualization")
            with open(os.path.join('static', 'index.html'), 'r') as f:
                html_template = f.read()
            
            # Format the HTML template with BFS data
            html_content = html_template.replace("{{ n }}", json.dumps(n))\
                                        .replace("{{ start }}", json.dumps(start))\
                                        .replace("{{ end }}", json.dumps(end))\
                                        .replace("{{ adj_matrix }}", json.dumps(adj_matrix))\
                                        .replace("{{ path }}", json.dumps(path))

            # Display the HTML in an iframe
            st.components.v1.html(html_content, height=600)

        except Exception as e:
            st.error(f"Error parsing input data: {e}")
    else:
        st.error("Please enter input data.")
