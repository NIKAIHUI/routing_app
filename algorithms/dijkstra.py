import streamlit as st
import heapq

def dijkstra(graph, start_node, end_node):
    """
    Calculate the shortest path between start and end nodes.
    """
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    path = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end_node:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, distance in graph[current_node].items():
            new_distance = current_distance + distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                path[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    shortest_path = []
    current = end_node
    while current:
        shortest_path.insert(0, current)
        current = path[current]

    return distances[end_node], shortest_path
