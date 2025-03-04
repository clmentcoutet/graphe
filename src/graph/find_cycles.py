import networkx as nx

def find_cycles(graph: nx.Graph) -> list:
    cycles = list(nx.simple_cycles(graph))
    return cycles


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

    print(f"cycles: {find_cycles(G)}")