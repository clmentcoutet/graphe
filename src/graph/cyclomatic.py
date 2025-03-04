import networkx as nx


def compute_cyclomatic_number(graph):
    nb_edges = graph.number_of_edges()
    nb_nodes = graph.number_of_nodes()
    nb_connected_components = len(list(nx.strongly_connected_components(graph)))

    return nb_edges - nb_nodes + 2*nb_connected_components
