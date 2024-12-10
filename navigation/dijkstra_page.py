import streamlit as st
import json
from algorithms.dijkstra import dijkstra

def dijkstra_page():
    MAX_NODES = 30  # Maximum allowable nodes for performance efficiency

    st.title("Dijkstra's Algorithm")
    st.markdown("##### Solve single-source shortest path problems with non-negative edge weights.")

    # Initialize session state
    if "graph" not in st.session_state:
        st.session_state["graph"] = {}
    if "node_names" not in st.session_state:
        st.session_state["node_names"] = []
    if "confirm_reset" not in st.session_state:
        st.session_state["confirm_reset"] = False

    # Reset session state
    def reset_state():
        st.session_state.update({
            "graph": {},
            "node_names": [],
            "uploaded_file": None,
            "confirm_reset": False,
        })
        
    # Compute bidirectional graph for output
    def compute_bidirectional_graph(graph):
        bidirectional_graph = {}
        for node, neighbors in graph.items():
            for neighbor, distance in neighbors.items():
                bidirectional_graph.setdefault(node, {})[neighbor] = distance
                bidirectional_graph.setdefault(neighbor, {})[node] = distance
        return bidirectional_graph
    
    # Handle file upload and process graph data
    uploaded_file = st.sidebar.file_uploader("Upload a JSON file of the graph (max 30 nodes)", type=["json"])

    if uploaded_file:
        try:
            graph_data = json.load(uploaded_file)
            if len(graph_data) > MAX_NODES:
                st.error(f"Graph exceeds the maximum allowed {MAX_NODES} nodes.")
            else:
                st.session_state["graph"] = graph_data
                st.session_state["node_names"] = list(graph_data.keys())
                st.success("Graph JSON uploaded successfully!")
        except Exception as e:
            st.error(f"Error loading Graph JSON: {e}")

    # Manual input for nodes and connections
    if not uploaded_file:
        num_nodes = st.sidebar.number_input(
            "How many nodes are in the graph?", min_value=2, max_value=MAX_NODES, step=1, value=3
        )
        node_names_input = st.sidebar.text_area(
            "Enter the names of the nodes (comma-separated, e.g., A,B,C):",
            value=",".join(st.session_state["node_names"]),
        )

        if st.sidebar.button("Add Nodes"):
            node_names = [name.strip() for name in node_names_input.split(",") if name.strip()]
            if len(node_names) != len(set(node_names)):
                st.sidebar.error("Duplicate node names found. Ensure all node names are unique.")
            elif len(node_names) != num_nodes:
                st.sidebar.error("Number of node names entered doesn't match the specified number of nodes.")
            else:
                st.session_state["node_names"] = node_names
                st.session_state["graph"] = {node: {} for node in node_names}
                st.sidebar.success("Node names added!")

    # Define a callback to update the graph when the user selects neighbors
    def update_graph(node):
        selected_neighbors = st.session_state[f"neighbors_{node}"]
        st.session_state["graph"][node] = {
            neighbor: st.session_state["graph"].get(node, {}).get(neighbor, 1)
            for neighbor in selected_neighbors
        }

    # Define connections
    node_names = st.session_state.get("node_names", [])
    if node_names:
        defined_edges = set()  # Track already-defined edges
        for node in node_names:
            st.sidebar.markdown(f"### Define connections for {node}")
            available_neighbors = [
                n for n in node_names if n != node and (n, node) not in defined_edges
            ]
            
            # Filter default values to ensure they exist in available options
            default_neighbors = [
                neighbor for neighbor in st.session_state["graph"].get(node, {}).keys()
                if neighbor in available_neighbors
            ]

            neighbors = st.sidebar.multiselect(
                f"Select neighbors for {node}:",
                options=available_neighbors,
                default=default_neighbors,
                key=f"neighbors_{node}",
                on_change=update_graph,
                args=(node,),  # Pass the current node to the callback
            )

            # Add distances for each neighbor
            for neighbor in neighbors:
                distance = st.sidebar.number_input(
                    f"Distance from {node} to {neighbor}:", 
                    min_value=1, step=1,
                    value=st.session_state["graph"].get(node, {}).get(neighbor, 1),
                    key=f"distance_{node}_{neighbor}",
                )
                st.session_state["graph"].setdefault(node, {})[neighbor] = distance

            # Track edges to avoid redundant entries
            for neighbor in neighbors:
                defined_edges.add((node, neighbor))
                defined_edges.add((neighbor, node)) 
                
    # Display and download the graph
    if st.session_state["graph"]:
        bidirectional_graph = compute_bidirectional_graph(st.session_state["graph"])
        st.markdown("### Graph Representation (Bidirectional)")
        st.json(bidirectional_graph)
        st.download_button(
            label="Download Graph as JSON",
            data=json.dumps(bidirectional_graph, indent=2),
            file_name="graph.json",
            mime="application/json",
        )
    # Shortest path calculation
    if node_names and st.session_state["graph"]:
        st.markdown("### Shortest Path Calculation")
        start_node = st.selectbox("Select the start node:", [""] + node_names)
        end_node = st.selectbox(
            "Select the end node:", [""] + [node for node in node_names if node != start_node]
        )

        if st.button("Calculate Shortest Path"):
            if not start_node or not end_node:
                st.error("Please select both a start and end node.")
            else:
                # Use the bidirectional graph for the calculation
                bidirectional_graph = compute_bidirectional_graph(st.session_state["graph"])

                # Check if start and end nodes are connected
                if start_node not in bidirectional_graph or end_node not in bidirectional_graph:
                    st.error("Start or end node not found in the graph!")
                elif not bidirectional_graph[start_node]:
                    st.error(f"The start node '{start_node}' has no neighbors.")
                elif not bidirectional_graph[end_node]:
                    st.error(f"The end node '{end_node}' has no neighbors.")
                else:
                    try:
                        # Calculate shortest path
                        distance, shortest_path = dijkstra(bidirectional_graph, start_node, end_node)
                        
                        # Handle unreachable nodes
                        if distance == float('infinity'):
                            st.error(f"No path exists between {start_node} and {end_node}.")
                        else:
                            st.success(f"Shortest Path: {' → '.join(shortest_path)} (Distance: {distance})")
                    except Exception as e:
                        st.error(f"Error during shortest path calculation: {e}")
                
    # Reset Button Logic
    if st.button("Reset"):
        if uploaded_file:
            st.warning("Remove the uploaded file to reset.")
        else:
            st.session_state["confirm_reset"] = True

    if st.session_state["confirm_reset"] and not uploaded_file:
        confirm_reset = st.checkbox("I confirm the reset action")

        if confirm_reset:
            reset_state()
            st.success("Reset successfully!")
