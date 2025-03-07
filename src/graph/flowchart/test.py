import networkx as nx
from itertools import combinations

from src.graph.find_path_with_cycles import find_paths_with_cycles


def minimal_path_cover(all_paths, all_edges):
    """
    Find minimal set of paths that cover all edges in the graph.

    Parameters:
    G (nx.DiGraph): The directed graph
    all_paths (list): List of lists, where each inner list is a path (sequence of nodes)

    Returns:
    list: Minimal list of paths that cover all edges
    """

    # Convert paths to edge sets
    path_edge_sets = []
    for path in all_paths:
        edges = set()
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            if edge in all_edges:  # Only include valid edges
                edges.add(edge)
        if edges:  # Only add paths that contain valid edges
            path_edge_sets.append((path, edges))

    if not path_edge_sets:
        return []

    # Find minimal combination of paths that covers all edges
    min_paths = None
    min_path_count = float('inf')

    # Try all possible combinations of paths
    for r in range(1, len(path_edge_sets) + 1):
        for combo in combinations(path_edge_sets, r):
            # Combine all edges from this combination of paths
            combined_edges = set()
            selected_paths = []
            for path, edges in combo:
                combined_edges.update(edges)
                selected_paths.append(path)

            # Check if this combination covers all edges
            if combined_edges == all_edges:
                if len(selected_paths) < min_path_count:
                    min_paths = selected_paths
                    min_path_count = len(selected_paths)
                break  # Found a solution with r paths, no need to check more in this size

    return min_paths if min_paths is not None else []


# Example usage
def main():
    # Create a sample directed graph
    graph = {
        '0': ['1'],
        '1': ['2', "6"],
        '2': ['3', "PA"],
        '3': ['5', '4'],
        '4': ['PC', '5'],
        '5': ["PC", "EXIT"],
        '6': ['7', "PB"],
        '7': ['PC', "EXIT"],
        'PA': ["4"],
        'PB': ["7"],
        'PC': ["EXIT"],
        'EXIT': [],

    }
    start = '0'
    end = 'EXIT'
    G = nx.DiGraph(graph)
    cycles = list(nx.simple_cycles(G))
    all_paths = find_paths_with_cycles(G, start, end, cycles)

    # Find minimal covering paths
    result = minimal_path_cover(all_paths, set(G.edges()))

    # Print results
    print("Minimal paths to cover all edges:")
    for i, path in enumerate(result):
        print(f"Path {i + 1}: {path}")

    # Verify coverage
    covered_edges = set()
    for path in result:
        for i in range(len(path) - 1):
            covered_edges.add((path[i], path[i + 1]))
    print(f"\nCovered edges: {covered_edges}")
    print(f"All graph edges: {set(G.edges())}")
    print(f"Complete coverage: {covered_edges == set(G.edges())}")


if __name__ == "__main__":
    main()