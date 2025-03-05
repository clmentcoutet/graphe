import logging
import time
from pathlib import Path


from src.flowchart.display import InteractiveGraph
from src.flowchart.highlight import highlight_path_in_drawio
from src.flowchart.parse import parse_drawio
from src.graph.find_cycles import find_cycles
from src.graph.find_path_with_cycles import find_paths_with_cycles, logger as path_logger
from src.graph.find_start_end_node import find_start_end_nodes


logger = logging.getLogger(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)



EXAMPLE_FOLDER = "drawio_examples"
EXAMPLE_NAME = 'Algo-Migration-hypersimplify'
XML_FILE = Path.cwd().parent / EXAMPLE_FOLDER / f"{EXAMPLE_NAME}.drawio"


def _display_paths(paths, graph):
    labeled_paths = []
    for i, path in enumerate(paths):
        labeled_paths.append([graph.nodes[node].get('label') if graph.nodes[node].get('label', False) else "None" for node in path])  # Convert node IDs to labels
        print(f"Path {i+1}: {" -> ".join(labeled_paths[i])}")
    return labeled_paths

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
    _display_paths(paths, graph)

    # highlight the first path
    def highlight():
        if paths:
            first_path = paths[0]  # Select the first path
            highlight_path_in_drawio(str(XML_FILE), [first_path])
    highlight()
