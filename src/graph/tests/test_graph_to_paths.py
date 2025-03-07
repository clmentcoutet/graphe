from unittest.mock import patch

import pytest
import networkx as nx

from src.graph.find_cycles import find_cycles
from src.graph.find_path_with_cycles import find_paths_with_cycles
from src.graph.find_start_end_node import find_start_end_nodes


def _execute_paths_finder(G):
    starts, ends = find_start_end_nodes(G)
    cycles = find_cycles(G)

    return find_paths_with_cycles(G, starts, ends, cycles)


def test_graph_no_ending_node__raise_exception():
    # Arrange
    G = nx.DiGraph()
    G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'B')])

    # Act
    with pytest.raises(ValueError) as e:
        _, ends = find_start_end_nodes(G)

    # Assert
    assert str(e.value) == "The graph does not have an ending node."


def test_graph_multiple_start_node__raise_exception():
    # Arrange
    G = nx.DiGraph()
    G.add_edges_from([('A', 'C'), ('B', 'C'), ('C', 'D')])

    # Act
    with pytest.raises(ValueError) as e:
        starts, _ = find_start_end_nodes(G)

    # Assert
    assert str(e.value) == "Multiple start nodes found in the graph, find the nodes ['A', 'B']"


def test_graph_no_cycle_one_node__return_one_path():
    # Arrange
    G = nx.DiGraph()
    G.add_node("A")

    # Act
    paths = _execute_paths_finder(G)

    # Assert
    assert paths == [["A"]]


def test_graph_one_cycle__return_two_paths():
    # Arrange
    G = nx.DiGraph()
    G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('C', 'B')])

    # Act
    paths = _execute_paths_finder(G)

    # Assert
    assert ["A", "B", "C", "D"] in paths
    assert ["A", "B", "C", "B", "C", "D"] in paths
    assert len(paths) == 2