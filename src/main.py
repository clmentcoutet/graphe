import logging
import time
from pathlib import Path
from typing import List, Dict

from src.code_generation.syntax_tree_to_java_code import syntax_tree_to_java_code
from src.graph.find_cycles import find_cycles
from src.graph.find_path_with_cycles import find_paths_with_cycles
from src.graph.find_start_end_node import find_start_end_nodes
from src.graph.flowchart.display import InteractiveGraph
from src.graph.flowchart.highlight import highlight_path_in_drawio
from src.graph.flowchart.parse import parse_drawio
from src.graph_to_syntax_tree.paths_to_syntax_tree import paths_to_syntax_tree

logger = logging.getLogger(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)


EXAMPLE_FOLDER = "drawio_examples"
EXAMPLE_NAME = 'addDemo'
XML_FILE = Path.cwd().parent / EXAMPLE_FOLDER / f"{EXAMPLE_NAME}.drawio"


def highlight():
    if paths:
        first_path = paths[0]  # Select the first path
        highlight_path_in_drawio(str(XML_FILE), [first_path])

def _formate_paths(paths, graph) -> List[List[Dict]]:
    formatted_paths = []
    for path in paths:
        formatted_path = [
            {
                "id": node,
                "label": graph.nodes[node].get("label", ""),
                "type": graph.nodes[node].get("type")
            } for node in path
        ]
        formatted_paths.append(formatted_path)
    return formatted_paths



if __name__ == "__main__":
    # create networkx graph
    logger.info("Creating networkx graph")
    graph = parse_drawio(XML_FILE)
    logger.info(f"Graph created with {len(graph.nodes)} nodes and {len(graph.edges)} edges")

    # display graph
    interactive_graph = InteractiveGraph(graph)
    #plt.show()

    # find start and ends nodes
    logger.info("Finding start and end nodes")
    start_node, end_nodes = find_start_end_nodes(graph)
    #end_nodes = [end_nodes[0]]
    logger.info(f"Start node: {start_node}, End nodes: {end_nodes}")

    # find cycles lists
    logger.info("Finding cycles")
    start = time.time()
    cycles = find_cycles(graph)
    end = time.time()
    logger.info(f"Number of cycles: {len(cycles)}")
    logger.info(f"Time taken to find cycles: {end - start} seconds")

    # find all paths
    logger.info("Finding all paths" if cycles else "No cycles found")  # If no cycles, no paths to find)
    start = time.time()
    paths = find_paths_with_cycles(graph, start_node, end_nodes, cycles)
    end = time.time()
    logger.info(f"Number of paths from {start_node} to {end_nodes}: {len(paths)}")
    logger.info(f"Time taken to find paths: {end - start} seconds")

    # format and display paths
    formatted_paths = _formate_paths(paths, graph)
    logger.info("Paths:")
    for path in formatted_paths:
        logger.info(path)

    # get merged syntax tree
    logger.info("Merging syntax tree")
    merged_syntax_tree = paths_to_syntax_tree(formatted_paths)
    logger.info("Syntax tree merged successfully")

    # convert syntax tree to Java code
    logger.info("Converting merged syntax tree to Java code")
    start = time.time()
    syntax_tree_to_java_code(merged_syntax_tree)
    end = time.time()
    logger.info(f"Time taken to convert syntax tree to Java code: {end - start} seconds")
    logger.info("Java code generated successfully")

    # highlight the first path
    #highlight()
