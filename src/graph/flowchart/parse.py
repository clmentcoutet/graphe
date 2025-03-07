import os
import re
from pathlib import Path
import xml.etree.ElementTree as ET

import networkx as nx
from matplotlib import pyplot as plt

from src.graph.flowchart.display import InteractiveGraph


def _clean_graph(G: nx.DiGraph) -> nx.DiGraph:
    G.remove_nodes_from(list(nx.isolates(G)))  # remove isolated nodes
    return G


def _parse_usergroup(user_object):
    html = user_object.get("label", "")
    pattern = r'<font(?: style="[^"]*")?>([^<]*)</font>'
    match = re.search(pattern, html)
    label = match.group(1) if match else None
    id = user_object.get("id")
    return id, label

def _parse_mxcell(cell):
    id = cell.get("id")
    parent = cell.get("parent")
    label = cell.get("value", "").strip()
    label = label if label else None  # node without label
    source = cell.get("source")
    target = cell.get("target")
    return id, label, parent, source, target


def parse_drawio(file_path: str | Path) -> nx.DiGraph:
    if not file_path.endswith(".drawio"):
        raise ValueError("Invalid file extension. Expected .drawio")
    # check if the file exists
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File '{file_path}' not found")

    tree = ET.parse(file_path)
    root = tree.getroot()

    G = nx.DiGraph()

    for user_object in root.findall(".//UserObject"):
        id, label = _parse_usergroup(user_object)
        mx_cell = user_object.findall(".//mxCell")[0]
        _, _, parent, _, _ = _parse_mxcell(mx_cell)
        if parent and id and id not in G.nodes:
            G.add_node(id, label=label)

    for cell in root.findall(".//mxCell"):
        id, label, parent, source, target = _parse_mxcell(cell)
        if source and target:
            G.add_edge(source, target, label=label)
        elif parent and id and id not in G.nodes:
            G.add_node(id, label=label)
    return _clean_graph(G)

if __name__ == "__main__":
    file_path = Path(r"/drawio_examples/testChartwithLoop.drawio")
    graph = parse_drawio(file_path)

    interactive_graph = InteractiveGraph(graph)
    plt.show()


