import networkx as nx


def find_start_end_nodes(graph: nx.DiGraph) -> tuple[str, list[str]]:
    start_nodes = [n for n, d in graph.in_degree() if d == 0]
    end_nodes = [n for n, d in graph.out_degree() if d == 0]

    if len(end_nodes) == 0:
        raise ValueError("The graph does not have an ending node.")



    if len(start_nodes) != 1:
        raise ValueError(f"Multiple start nodes found in the graph, find the nodes {start_nodes}")

    return start_nodes[0], end_nodes
