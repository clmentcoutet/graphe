import time

import networkx as nx

from collections import deque


def generate_rotated_lists(lst):
    n: int = len(lst)
    return [lst[i:] + lst[:i+1] for i in range(n)]

def is_contiguous_sublist(main_list, sublist):
    n, m = len(main_list), len(sublist)
    return [main_list[i:i + m] == sublist for i in range(n - m + 1)].count(True)


def occur_cycle_in_path(path, cycle):
    """Count occurrences of any cyclic rotation of cycle in path as contiguous sublists."""
    rotated_cycles = generate_rotated_lists(cycle)
    return [is_contiguous_sublist(path, rotated) for rotated in rotated_cycles]


def find_paths_with_cycles(graph, start, end, cycles):
    """
    Find all paths from start to end in a directed graph where each path
    can use at most one edge from the special_edges set.
    Cycles can be traversed multiple times, but the path length is limited
    to prevent infinite loops.

    Args:
        graph: A dictionary representing the directed graph {node: [neighbors]}
        start: The starting node
        end: The ending node
        special_edges: A list of tuples (source, target) representing special edges
        max_path_length: Maximum allowed path length to prevent infinite cycles

    Returns:
        A list of paths, where each path is a list of nodes
    """

    # Initialize result list
    all_paths = []

    # Stack-based DFS to avoid recursion issues
    # Each entry is (current_node, path_so_far, used_special_edge)
    stack = [(start, [start], list())]

    cycles = [cycle for cycle in cycles]

    while stack:
        current, path, used_cycled = stack.pop()

        # If we reached the end, add the path to results
        if current == end:

            all_paths.append(path)
            continue

        for neighbor in graph.get(current, []):
            new_path = path + [neighbor]
            new_used_cycles = used_cycled.copy()

            # iterate over cycles to check if the new path forms a cycle
            for cycle in cycles:
                count_cycle = occur_cycle_in_path(new_path, cycle)
                if any(count > 1 for count in count_cycle):
                    break
                elif any(count == 1 for count in count_cycle):
                    if cycle in new_used_cycles:
                        if neighbor == end:
                            all_paths.append(new_path)
                            break
                        #if there is no more cycle
                        if new_used_cycles == cycles:
                            break
                        continue
                    new_used_cycles.append(cycle)

            else:
                stack.append((neighbor, new_path, new_used_cycles))

    return all_paths

if __name__ == "__main__":
    ##example:
    graph = {
        '0': ['1', '4'],
        '1': ['2'],
        '2': ['3'],
        '3': ['4', '5'],
        '4': ['2', '1'],
        '5': [],
    }
    start = '0'
    end = '5'

    G = nx.DiGraph(graph)
    cycles = list(nx.simple_cycles(G))
    print(cycles)

    paths = find_paths_with_cycles(graph, start, end, cycles)
    print(f"Number of paths from {start} to {end}: {len(paths)}")

    # Display results
    for path in paths:
        print(" -> ".join(path))
