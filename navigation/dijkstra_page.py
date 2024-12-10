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
    
    # Function to compute the bidirectional graph dynamically
    def compute_bidirectional_graph(graph):
        """
        Ensures the graph is bidirectional by adding reverse connections
        for each edge defined in the graph.
        """
        bidirectional_graph = {}
        for node, neighbors in graph.items():
            for neighbor, distance in neighbors.items():
                bidirectional_graph.setdefault(node, {})[neighbor] = distance
                bidirectional_graph.setdefault(neighbor, {})[node] = distance
        return bidirectional_graph

    # Function to synchronize the graph when neighbors are selected/removed
    def update_graph(node):
        """
        Updates the graph dynamically based on neighbors selected for a node.
        """
        selected_neighbors = st.session_state[f"neighbors_{node}"]

        # Add or retain neighbors in the graph
        for neighbor in selected_neighbors:
            if neighbor not in st.session_state["graph"].get(node, {}):
                # Ensure neighbor is initialized with a default distance
                st.session_state["graph"].setdefault(node, {})[neighbor] = 1
                st.session_state["graph"].setdefault(neighbor, {})[node] = 1

        # Remove neighbors that are no longer selected
        current_neighbors = list(st.session_state["graph"].get(node, {}).keys())
        for old_neighbor in current_neighbors:
            if old_neighbor not in selected_neighbors:
                # Remove connection in both directions
                st.session_state["graph"][node].pop(old_neighbor, None)
                st.session_state["graph"][old_neighbor].pop(node, None)

    # Upload JSON file
    uploaded_file = st.sidebar.file_uploader("Upload Graph JSON", type=["json"])
    if uploaded_file:
        try:
            uploaded_data = json.load(uploaded_file)

            # Initialize the graph with uploaded data (one-time operation)
            if not st.session_state["graph"]:
                st.session_state["graph"] = uploaded_data
                st.session_state["node_names"] = list(uploaded_data.keys())

            st.sidebar.success("JSON file loaded! You can now edit the graph dynamically.")
        except Exception as e:
            st.sidebar.error(f"Error reading JSON file: {e}")

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
    
    # Main UI for defining nodes and connections
    node_names = st.session_state["node_names"]
    if node_names:
        for node in node_names:
            st.sidebar.markdown(f"### Define connections for {node}")

            # Available neighbors are all nodes except the current node
            available_neighbors = [n for n in node_names if n != node]

            # Get default neighbors from the graph
            default_neighbors = list(st.session_state["graph"].get(node, {}).keys())

            # Multiselect for neighbors
            neighbors = st.sidebar.multiselect(
                f"Select neighbors for {node}:",
                options=available_neighbors,
                default=default_neighbors,
                key=f"neighbors_{node}",
                on_change=update_graph,
                args=(node,),
            )

            # Input distances for each selected neighbor
            for neighbor in neighbors:
                distance_key = f"distance_{node}_{neighbor}"

                # Ensure distance entry exists before accessing it
                st.session_state["graph"].setdefault(node, {})[neighbor] = st.session_state["graph"].get(node, {}).get(
                    neighbor, 1
                )
                st.session_state["graph"].setdefault(neighbor, {})[node] = st.session_state["graph"][node][neighbor]

                # Number input for distance
                distance = st.sidebar.number_input(
                    f"Distance from {node} to {neighbor}:",
                    min_value=1,
                    value=st.session_state["graph"][node][neighbor],
                    key=distance_key,
                )

                # Update the graph dynamically with the new distance
                st.session_state["graph"][node][neighbor] = distance
                st.session_state["graph"][neighbor][node] = distance  # Ensure bidirectional consistency


    # Display the graph dynamically
    if st.session_state["graph"]:
        # Compute the bidirectional graph dynamically
        bidirectional_graph = compute_bidirectional_graph(st.session_state["graph"])
        st.markdown("### Graph Representation (Bidirectional)")
        st.json(bidirectional_graph)

        # Download button for graph JSON
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
