import pytest
from algorithms.dijkstra import dijkstra

def test_dijkstra_simple_case():
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }
    start_node = 'A'
    end_node = 'D'
    expected_distance = 4
    expected_path = ['A', 'B', 'C', 'D']

    distance, path = dijkstra(graph, start_node, end_node)
    assert distance == expected_distance
    assert path == expected_path

def test_dijkstra_unreachable():
    graph = {
        'A': {'B': 1},
        'B': {'A': 1},
        'C': {}
    }
    start_node = 'A'
    end_node = 'C'
    expected_distance = float('inf')
    expected_path = []

    distance, path = dijkstra(graph, start_node, end_node)
    assert distance == expected_distance
    assert path == expected_path
    
def test_dijkstra_no_edges():
    graph = {'A': {}, 'B': {}}
    start_node = 'A'
    end_node = 'B'
    distance, path = dijkstra(graph, start_node, end_node)
    assert distance == float('inf')
    assert path == []