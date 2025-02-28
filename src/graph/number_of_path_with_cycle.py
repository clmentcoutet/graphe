def find_paths_with_limited_special_edges(graph, start, end, special_edges):
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
    # Convert special edges to a set for O(1) lookup
    special_edges_set = set(special_edges)

    # Initialize result list
    all_paths = []

    # Stack-based DFS to avoid recursion issues
    # Each entry is (current_node, path_so_far, used_special_edge)
    stack = [(start, [start], set())]

    while stack:
        current, path, used_special_edges = stack.pop()

        # If we reached the end, add the path to results
        if current == end:
            all_paths.append(path)
            continue

        # Get neighbors
        for neighbor in graph.get(current, []):
            edge = (current, neighbor)

            # Skip if this edge is already used and it's special
            if edge in special_edges_set and edge in used_special_edges:
                continue

            # Create new state
            new_path = path + [neighbor]
            new_used_special_edges = used_special_edges.copy()

            # If this is a special edge, mark it as used
            if edge in special_edges_set:
                new_used_special_edges.add(edge)

            stack.append((neighbor, new_path, new_used_special_edges))

    return all_paths


def find_cycles_edges(graph):
    """
    Find all backward edges in a directed graph.
    A backward edge is one that points back to a node already visited in the current DFS path.

    Args:
        graph: A dictionary representing the directed graph {node: [neighbors]}

    Returns:
        A list of backward edges represented as 'source->target'
    """
    backward_edges = set()

    def dfs(node, path_set, full_path):
        # Add current node to the path
        path_set.add(node)
        full_path.append(node)

        # Explore neighbors
        for neighbor in graph.get(node, []):
            # If neighbor is already in our path, it's a backward edge
            if neighbor in path_set:
                if node > neighbor:
                    backward_edges.add((node, neighbor))
            else:
                # Continue DFS with a new copy of the path set and full path
                dfs(neighbor, path_set.copy(), full_path.copy())

    # Start DFS from each node to find all backward edges
    for start_node in graph:
        dfs(start_node, set(), [])

    return sorted(backward_edges)


def find_all_paths(graph, start, end):
    """
    Find all paths from start to end in a directed graph.

    Args:
        graph: A dictionary representing the directed graph {node: [neighbors]}
        start: The starting node
        end: The ending node

    Returns:
        A list of paths, where each path is a list of nodes
    """
    special_edges = find_cycles_edges(graph)
    return find_paths_with_limited_special_edges(graph, start, end, [])


# Example usage
if __name__ == "__main__":
    # Example graph
    graph = {
        '1': ['2'],
        '2': ['1', '3'],
        '3': ['4', '2'],
        '4': [''],
    }
    start = '1'
    end = '4'

    # Special edges that can be used at most once per path
    special_edges = find_cycles_edges(graph)

    # Find all paths from '1' to '5'
    paths = find_paths_with_limited_special_edges(graph, start, end, special_edges)

    print(f"Found {len(paths)} paths from 1 to 5:")
    for i, path in enumerate(paths, 1):

        # Check which special edges were used
        used_special = []
        for j in range(len(path) - 1):
            edge = (path[j], path[j + 1])
            if edge in special_edges:
                used_special.append((edge[0], edge[1]))
        if len(used_special) >= 0:
            print(f"Path {i}: {' -> '.join(path)}")
            print(used_special)