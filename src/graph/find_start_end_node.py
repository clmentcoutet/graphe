import networkx as nx


def find_start_end_nodes(graph: nx.DiGraph) -> tuple[str, list[str]]:
    start_nodes = [n for n, d in graph.in_degree() if d == 0]
    end_nodes = [n for n, d in graph.out_degree() if d == 0]

    if len(start_nodes) == 0 or len(end_nodes) == 0:
        raise ValueError("No start or end nodes found in the graph")

    if len(start_nodes) > 1:
        start_nodes_labels = [f"{n} ({graph.in_degree(n)})" for n in start_nodes]
        raise ValueError(f"Multiple start nodes found in the graph, find the nodes {start_nodes_labels}")

    return start_nodes[0], end_nodes
