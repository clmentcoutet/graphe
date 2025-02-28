import time

import networkx as nx

from collections import deque


def find_paths(graph, start, end, cycles):
    paths = []
    queue = deque([(start, [start], set())])  # (current node, path, used cycles)

    cycle_sets = [set(cycle) for cycle in cycles]  # Convert cycles to sets for quick lookup

    while queue:
        print()
        node, path, used_cycles = queue.popleft()
        print(queue)
        print(f"Node: {node}, Current path: {path}, used cycles: {used_cycles}")  # For debugging purposes

        if node == end:
            print(f"Found a path: {path}")  # For debugging purposes
            paths.append(path)
            continue

        for neighbor in graph.get(node, []):
            print(f"Exploring neighbor: {neighbor}")  # For debugging purposes
            if neighbor in path:
                print(f"Neighbor: {neighbor} is already in the path {path}, skipping")  # For debugging purposes
                continue  # Avoid simple cycles (self-loops)

            new_used_cycles = used_cycles.copy()
            print(f"New used cycles before loop: {new_used_cycles}")  # For debugging purposes

            # Check if adding this node enters a new cycle
            for i, cycle in enumerate(cycle_sets):
                print(f"Checking cycle {cycle} against path {path}")  # For debugging purposes
                if neighbor in cycle and not cycle.isdisjoint(path):
                    print(f"Found cycle {cycle} in path {path}, adding to used cycles")  # For debugging purposes
                    if i in used_cycles:
                        print(f"Cycle {cycle} already used in path {path}, skipping")  # For debugging purposes
                        break  # This cycle was already used, stop
                    new_used_cycles.add(i)
                    print(f"New used cycles in loop: {new_used_cycles}")  # For debugging purposes
            else:
                print(f"No cycles found in path {path}, adding to queue")  # For debugging purposes
                queue.append((neighbor, path + [neighbor], new_used_cycles))

    return paths

def is_contiguous_sublist(main_list, sublist):
    n, m = len(main_list), len(sublist)
    return [main_list[i:i + m] == sublist for i in range(n - m + 1)]

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
        print(current, path, used_cycled)
        #time.sleep(0.1)

        # If we reached the end, add the path to results
        if current == end:
            all_paths.append(path)
            continue

        # Get neighbors
        for neighbor in graph.get(current, []):
            print(f"Exploring neighbor: {neighbor}")  # For debugging purposes

            # Create new state
            new_path = path + [neighbor]
            print(new_path)
            new_used_cycles = used_cycled.copy()

            # iterate over cycles to check if the new path forms a cycle
            for cycle in cycles:
                print(f"Checking cycle {"".join(cycle)} against path {"".join(new_path)}")  # For debugging purposes
                sublist = is_contiguous_sublist(new_path, cycle).count(True)
                print(f"Sublist: {sublist}")  # For debugging purposes
                if sublist == 1:
                    print(f"Found cycle {cycle} in path {new_path}, adding to used cycles")  # For debugging purposes
                    if cycle in new_used_cycles:
                        if neighbor == end:
                            print(f"Found a path from {start} to {end}: {new_path}")  # For debugging purposes
                            all_paths.append(new_path)
                            break  # Stop exploring further paths in this cycle
                        print(f"Cycle {cycle} already used in path {new_path}, skipping")  # For debugging purposes
                        #if there is no more cycle
                        if new_used_cycles == cycles:
                            print(f"No more cycles available")
                            break
                        continue #
                    new_used_cycles.append(cycle)
                elif sublist > 1:
                    break

            else:
                stack.append((neighbor, new_path, new_used_cycles))
                print(stack)

    return all_paths

if __name__ == "__main__":
    ##example:
    graph = {
        '0': ['1', '7'],
        '1': ['2'],
        '2': ['3'],
        '3': ['4', '5'],
        '4': [],
        '5': ['6', '7'],
        '6': ['2'],
        '7': ['1', '6']
    }
    start = '0'
    end = '4'

    G = nx.DiGraph(graph)
    cycles = list(nx.simple_cycles(G))
    print(cycles)

    paths = find_paths_with_cycles(graph, start, end, cycles)
    print(f"Number of paths from {start} to {end}: {len(paths)}")

    # Display results
    for path in paths:
        print(" -> ".join(path))
