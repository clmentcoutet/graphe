from pathlib import Path
import xml.etree.ElementTree as ET

import networkx as nx
from matplotlib import pyplot as plt

from src.flowchart.display import InteractiveGraph


def _clean_graph(G: nx.DiGraph) -> nx.DiGraph:
    G.remove_nodes_from(list(nx.isolates(G)))  # remove isolated nodes
    return G

def parse_drawio(file_path: str | Path) -> nx.DiGraph:
    tree = ET.parse(file_path)
    root = tree.getroot()

    G = nx.DiGraph()

    for cell in root.findall(".//mxCell"):
        cell_id = cell.get("id")
        parent = cell.get("parent")
        value = cell.get("value", "").strip()
        value = value if value else None  # node without label
        source = cell.get("source")
        target = cell.get("target")

        if source and target:
            G.add_edge(source, target, label=value)
        elif parent and cell_id:
            G.add_node(cell_id, label=value)

    return _clean_graph(G)

if __name__ == "__main__":
    file_path = Path(r"E:\stage\sujet\python\drawio_examples\testChartwithLoop.drawio")
    graph = parse_drawio(file_path)

    interactive_graph = InteractiveGraph(graph)
    plt.show()


