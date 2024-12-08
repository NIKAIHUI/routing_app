import pytest
import pandas as pd
from algorithms.clark_wright import clark_wright

def test_clark_wright_basic_case():
    """
    Test the basic functionality of the Clark-Wright Savings Algorithm.
    """
    distance_matrix = pd.DataFrame([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    demands = [5, 5, 5]
    max_capacity = 30
    expected_routes = [[2, 0, 1]]

    routes = clark_wright(distance_matrix, demands, max_capacity)
    assert sorted(routes) == sorted(expected_routes)

def test_clark_wright_exceed_capacity():
    """
    Test that the algorithm does not merge routes exceeding max capacity.
    """
    distance_matrix = pd.DataFrame([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    demands = [7, 7, 7]  # Customer demands
    max_capacity = 5  # Maximum capacity of the vehicle

    # Expected routes where no merging happens due to capacity constraints
    expected_routes = [[0], [1], [2]]

    routes = clark_wright(distance_matrix, demands, max_capacity)
    assert sorted(routes) == sorted(expected_routes)

def test_clark_wright_empty_demands():
    """
    Test the behavior with no demands (edge case).
    """
    distance_matrix = pd.DataFrame([
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ])
    demands = []
    max_capacity = 10
    expected_routes = []

    routes = clark_wright(distance_matrix, demands, max_capacity)
    assert routes == expected_routes