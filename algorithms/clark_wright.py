import streamlit as st

def calculate_savings(distance_matrix):
    """
    Calculate the savings for each pair of nodes.
    """
    savings = []
    n = len(distance_matrix)
    depot = n - 1  # Depot is the last node in the matrix

    for i in range(n - 1):  # Exclude depot itself
        for j in range(i + 1, n - 1):
            saving = distance_matrix.iloc[i, depot] + distance_matrix.iloc[j, depot] - distance_matrix.iloc[i, j]
            savings.append((i, j, saving))

    # Sort by savings in descending order
    savings.sort(key=lambda x: x[2], reverse=True)
    return savings

def clark_wright(distance_matrix, demands, max_capacity):
    """
    Implement the Clark-Wright Savings Algorithm to calculate routes.
    """
    if not demands:
        return []
    
    savings = calculate_savings(distance_matrix)
    n = len(distance_matrix)
    routes = {i: [i] for i in range(n - 1)}  # Exclude depot from individual routes
    route_map = {i: i for i in range(n - 1)}
    capacities = {i: demands[i] for i in range(n - 1)}

    for i, j, saving in savings:
        route_i = route_map[i]
        route_j = route_map[j]

        if route_i != route_j:
            if (capacities[route_i] + capacities[route_j]) <= max_capacity:
                if routes[route_i][-1] == i and routes[route_j][0] == j:
                    routes[route_i].extend(routes[route_j])
                    capacities[route_i] += capacities[route_j]
                    for node in routes[route_j]:
                        route_map[node] = route_i
                    del routes[route_j]
                elif routes[route_j][-1] == j and routes[route_i][0] == i:
                    routes[route_j].extend(routes[route_i])
                    capacities[route_j] += capacities[route_i]
                    for node in routes[route_i]:
                        route_map[node] = route_j
                    del routes[route_i]

    return list(routes.values())
