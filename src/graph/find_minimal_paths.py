from typing import overload, Any

import networkx as nx

from src.graph.find_cycles import find_cycles
from src.graph.find_path_with_cycles import find_paths_with_cycles
from src.graph.find_start_end_node import find_start_end_nodes



def minimum_path_cover_paths(paths: list[list[Any]]) -> list[list[Any]]:
    paths.sort(key=len)

    visited_node = set()
    path_cover = []

    for path in paths:
        if not all(node in visited_node for node in path):
            visited_node.update(path)
            path_cover.append(path)

    return path_cover


def minimum_path_cover_graph(graph: nx.DiGraph):
    start, end_nodes = find_start_end_nodes(graph)
    cycles = find_cycles(graph)

    paths = find_paths_with_cycles(graph, start, end_nodes, cycles)

    return minimum_path_cover_paths(paths)




if __name__ == "__main__":
    graph = {
        '1': ['2'],
        '2': ['3'],
        '3': ['7', '4'],
        '4': ['6', '5'],
        '5': [],
        '6': ['3'],
        '7': ['2'],
    }

    G = nx.DiGraph(graph)

    paths = minimum_path_cover_graph(G)
    print("Paths:")
    for path in paths:
        print(path)
