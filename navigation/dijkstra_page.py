import streamlit as st
import json
from algorithms.dijkstra import dijkstra

def dijkstra_page():
    st.title("Dijkstra's Algorithm")
    st.markdown("##### Solve single-source shortest path problems with non-negative edge weights.")

    # Initialize session state
    if "graph" not in st.session_state:
        st.session_state["graph"] = {}
    if "node_names" not in st.session_state:
        st.session_state["node_names"] = []
    if "confirm_reset" not in st.session_state:
        st.session_state["confirm_reset"] = False

    # Function to reset session state
    def reset_state():
        st.session_state["graph"] = {}
        st.session_state["node_names"] = []
        st.session_state["uploaded_file"] = None
        st.session_state["confirm_reset"] = False

    MAX_NODES = 30  # Maximum allowable nodes

    # Function to process JSON data
    def process_graph(graph_data):
        processed_graph = {}
        processed_edges = set()

        for node, connections in graph_data.items():
            if node not in processed_graph:
                processed_graph[node] = {}
            for neighbor, distance in connections.items():
                if (neighbor, node) in processed_edges:
                    continue
                processed_graph.setdefault(node, {})[neighbor] = distance
                processed_edges.add((node, neighbor))
        return processed_graph

    # Sidebar: Upload JSON File
    uploaded_file = st.sidebar.file_uploader("Upload a JSON file of the graph (max 30 nodes)", type=["json"])
    if uploaded_file:
        try:
            graph_data = json.load(uploaded_file)
            if len(graph_data) > MAX_NODES:
                st.error(f"Graph exceeds the maximum allowed {MAX_NODES} nodes.")
            else:
                st.session_state["graph"] = process_graph(graph_data)
                st.session_state["node_names"] = list(st.session_state["graph"].keys())
                st.success("Graph uploaded and processed successfully!")
        except Exception as e:
            st.error(f"Error processing the uploaded JSON file: {e}")

    # Sidebar: Define Nodes Manually
    if not uploaded_file:
        num_nodes = st.sidebar.number_input("Number of nodes:", min_value=2, max_value=MAX_NODES, value=3, step=1)
        node_names_input = st.sidebar.text_area(
            "Enter node names (comma-separated):", value=",".join(st.session_state["node_names"])
        )
        if st.sidebar.button("Set Node Names"):
            node_names = [name.strip() for name in node_names_input.split(",") if name.strip()]
            if len(node_names) != len(set(node_names)):
                st.sidebar.error("Duplicate node names found. Ensure all node names are unique.")
            elif len(node_names) != num_nodes:
                st.sidebar.error("Number of node names doesn't match the specified number of nodes.")
            else:
                st.session_state["node_names"] = node_names
                st.session_state["graph"] = {node: {} for node in node_names}
                st.sidebar.success("Node names set successfully!")

    # Sidebar: Define Connections
    node_names = st.session_state.get("node_names", [])
    if node_names:
        for node in node_names:
            neighbors = st.sidebar.multiselect(
                f"Neighbors for {node}:", options=[n for n in node_names if n != node],
                default=list(st.session_state["graph"].get(node, {}).keys()),
                key=f"neighbors_{node}",
            )
            for neighbor in neighbors:
                distance = st.sidebar.number_input(
                    f"Distance from {node} to {neighbor}:", min_value=1, step=1,
                    value=st.session_state["graph"].get(node, {}).get(neighbor, 1),
                    key=f"distance_{node}_{neighbor}",
                )
                st.session_state["graph"].setdefault(node, {})[neighbor] = distance

    # Display Graph
    if st.session_state["graph"]:
        filtered_graph = {k: v for k, v in st.session_state["graph"].items() if v}
        if filtered_graph:
            st.markdown("### Graph Representation")
            st.json(filtered_graph)
            st.download_button(
                label="Download Graph as JSON",
                data=json.dumps(filtered_graph, indent=2),
                file_name="graph.json",
                mime="application/json",
            )
        else:
            st.warning("The graph is empty. Add connections to build the graph.")

    # Select Start and End Nodes
    if node_names and st.session_state["graph"]:
        st.markdown("### Find Shortest Path")
        start_node = st.selectbox("Start Node:", options=[""] + node_names, key="start_node")
        end_node = st.selectbox(
            "End Node:", options=[""] + [node for node in node_names if node != start_node], key="end_node"
        )
        if st.button("Calculate Shortest Path"):
            if not start_node or not end_node:
                st.error("Please select both a start and end node.")
            else:
                graph = st.session_state["graph"]
                if start_node not in graph or end_node not in graph:
                    st.error("Start or end node not found in the graph.")
                else:
                    try:
                        distance, shortest_path = dijkstra(graph, start_node, end_node)
                        st.success(f"Shortest Path: {' → '.join(shortest_path)} (Distance: {distance})")
                    except Exception as e:
                        st.error(f"Error calculating shortest path: {e}")
            
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
