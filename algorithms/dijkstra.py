import streamlit as st
import heapq

def dijkstra(graph, start_node, end_node):
    """
    Calculate the shortest path between start and end nodes.
    """
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    path = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Stop searching if we reach the end_node
        if current_node == end_node:
            break

        # Skip processing if this distance is not optimal
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                path[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    # Backtrack to find the path, if reachable
    shortest_path = []
    current = end_node
    while current and distances[current] != float('inf'):
        shortest_path.insert(0, current)
        current = path[current]

    # If the end_node is unreachable, return an empty path
    if distances[end_node] == float('inf'):
        return float('inf'), []

    return distances[end_node], shortest_path