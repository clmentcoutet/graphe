import logging

import networkx as nx

logger = logging.getLogger(__name__)

def _generate_rotated_lists(lst):
    n: int = len(lst)
    return [lst[i:] + lst[:i+1] for i in range(n)]

def _is_contiguous_sublist(main_list, sublist):
    n, m = len(main_list), len(sublist)
    return [main_list[i:i + m] == sublist for i in range(n - m + 1)].count(True)


def _occur_cycle_in_path(path, cycle):
    """Count occurrences of any cyclic rotation of cycle in path as contiguous sublists."""
    rotated_cycles = _generate_rotated_lists(cycle)
    return [_is_contiguous_sublist(path, rotated) for rotated in rotated_cycles]


def find_paths_with_cycles(graph: nx.DiGraph, start: str, end: str | list[str], cycles: list) -> list[list[str]]:
    """
    Find all paths from start to end in a directed graph where each path
    can use each cycles at most once.

    Args:
        graph: A dictionary representing the directed graph {node: [neighbors]}
        start: The starting node
        end: The ending node
        cycles: A list of cycles, where each cycle is a list of nodes

    Returns:
        A list of paths, where each path is a list of nodes
    """
    if not isinstance(end, list):
        end = [end]

    # Initialize result list
    all_paths = []

    # Stack-based DFS to avoid recursion issues
    # Each entry is (current_node, path_so_far, used_special_edge)
    stack = [(start, [start], list())]

    cycles = [cycle for cycle in cycles]

    while stack:
        current, path, used_cycled = stack.pop()

        # If we reached the end, add the path to results
        if current in end:
            logger.info(f"Found path: {path}")
            if path in all_paths:
                logger.info(f"Path already exists: {path}")
                continue
            all_paths.append(path)
            continue

        for neighbor in graph[current]:
            new_path = path + [neighbor]
            new_used_cycles = used_cycled.copy()

            # iterate over cycles to check if the new path forms a cycle
            for cycle in cycles:
                count_cycle = _occur_cycle_in_path(new_path, cycle)
                if any(count > 1 for count in count_cycle):
                    break
                elif any(count == 1 for count in count_cycle):
                    if cycle in new_used_cycles:
                        if neighbor in end:
                            logger.info(f"Found path: {path}")
                            if path in all_paths:
                                logger.info(f"Path already exists: {path}")
                                continue
                            all_paths.append(new_path)
                            break
                        continue
                    new_used_cycles.append(cycle)

            else:
                stack.append((neighbor, new_path, new_used_cycles))

    return all_paths

if __name__ == "__main__":
    ##example:
    graph = {
        '0': ['1'],
        '1': ['2', "8"],
        '2': ['3'],
        '3': ['4', "10"],
        '4': ['5'],
        '5': ["6"],
        '6': ["3", "7"],
        '7': [],
        '8': ["9"],
        '9': ["10", "11"],
        '10': [],
        '11': [],
    }
    start = '0'
    end = '11'
    graph = {
        '0': ['1'],
        '1': ['2'],
        '2': ['3', "6"],
        '3': ['4', '5'],
        '4': [],
        '5': ['2'],
        '6': ['1'],
    }
    start = '0'
    end = '4'

    G = nx.DiGraph(graph)
    cycles = list(nx.simple_cycles(G))
    print(cycles)

    paths = find_paths_with_cycles(G, start, end, cycles)
    print(f"Number of paths from {start} to {end}: {len(paths)}")

    # Display results
    for path in paths:
        print(" -> ".join(path))
