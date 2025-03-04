import sys
import xml.etree.ElementTree as ET
import re

HIGHLIGHT_NODE_COLOR = "#FF0000"  # Red
HIGHLIGHT_EDGE_COLOR = "#FF0000"  # Red
HIGHLIGHT_EDGE_WIDTH = "4"  # Increase stroke width


def highlight_path_in_drawio(xml_file_path: str, paths: list[list], checked: bool = True):
    """
    Modifies the .drawio XML file to highlight the given path by changing node and edge colors,
    and increasing stroke width.

    Args:
        xml_file_path: Path to the .drawio XML file.
        path: List of node IDs representing the path to highlight.
        checked: If True, use the default highlight colors. If False, use the existing colors
                or remove stroke if no existing color is found.
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    diagram = root.find(".//diagram")
    if diagram is None:
        print("No diagram found in the XML file.")
        return

    if not (isinstance(paths, list) and all(isinstance(sublist, list) for sublist in paths)):
        print("Invalid input: paths should be a list of lists.")
        return

    for path in paths:
        print(path)
        for cell in diagram.iter("mxCell"):
            style = cell.get("style", "")
            cell_id = cell.get("id")
            source, target = cell.get("source"), cell.get("target")

            if cell_id in path:
                # Handle nodes in the path
                if checked:
                    # Use default highlight color
                    if "strokeColor=" in style:
                        style = re.sub(r"strokeColor=[^;]+", f"strokeColor={HIGHLIGHT_NODE_COLOR}", style)
                    else:
                        style += f"strokeColor={HIGHLIGHT_NODE_COLOR};"

                    # Set stroke width
                    if "strokeWidth=" in style:
                        style = re.sub(r"strokeWidth=[^;]+", f"strokeWidth={HIGHLIGHT_EDGE_WIDTH}", style)
                    else:
                        style += f"strokeWidth={HIGHLIGHT_EDGE_WIDTH};"
                else:
                    # When checked is False
                    stroke_match = re.search(r"strokeColor=[^;]+", style)
                    if not stroke_match:
                        # Remove stroke if no existing stroke color
                        style = re.sub(r"strokeColor=[^;]+;", "", style)  # Remove any existing stroke color
                        style = re.sub(r"strokeWidth=[^;]+;", "", style)  # Remove any existing stroke width
                    else:
                        # Keep existing stroke color but update width
                        if "strokeWidth=" in style:
                            style = re.sub(r"strokeWidth=[^;]+", f"strokeWidth={HIGHLIGHT_EDGE_WIDTH}", style)
                        else:
                            style += f"strokeWidth={HIGHLIGHT_EDGE_WIDTH};"

            # Check if the edge connects sequential nodes in the path
            if source is not None and target is not None and source in path and target in path:
                # Find the indices of source and target in the path
                source_indexes = [index for index, element in enumerate(path) if element == source]
                target_indexes = [index for index, element in enumerate(path) if element == target]

                # Check if an edge connecting sequential nodes exists in the style attribute
                if any(source_index + 1 in target_indexes for source_index in source_indexes):
                    if checked:
                        # Use default highlight color for edges
                        if "strokeColor=" in style:
                            style = re.sub(r"strokeColor=[^;]+", f"strokeColor={HIGHLIGHT_EDGE_COLOR}", style)
                        else:
                            style += f"strokeColor={HIGHLIGHT_EDGE_COLOR};"

                        # Set stroke width
                        if "strokeWidth=" in style:
                            style = re.sub(r"strokeWidth=[^;]+", f"strokeWidth={HIGHLIGHT_EDGE_WIDTH}", style)
                        else:
                            style += f"strokeWidth={HIGHLIGHT_EDGE_WIDTH};"
                    else:
                        # When checked is False
                        stroke_match = re.search(r"strokeColor=[^;]+", style)
                        if not stroke_match:
                            # Remove stroke if no existing stroke color
                            style = re.sub(r"strokeColor=[^;]+;", "", style)  # Remove any existing stroke color
                            style = re.sub(r"strokeWidth=[^;]+;", "", style)  # Remove any existing stroke width
                        else:
                            # Keep existing stroke color but update width
                            if "strokeWidth=" in style:
                                style = re.sub(r"strokeWidth=[^;]+", f"strokeWidth={HIGHLIGHT_EDGE_WIDTH}",
                                               style)
                            else:
                                style += f"strokeWidth={HIGHLIGHT_EDGE_WIDTH};"

            cell.set("style", style)

    # Save the modified XML to a new file
    modified_file_path = xml_file_path.replace('.drawio', '_highlighted.drawio')
    tree.write(modified_file_path, encoding="utf-8", xml_declaration=True)
    print(f"Modified file saved as: {modified_file_path}")
    return modified_file_path


if __name__ == "__main__":
    xml_file_path = sys.argv[1]  # Path to the XML file
    path_to_highlight = sys.argv[2].split(',')  # Path to highlight (comma-separated list)

    # Add optional checked parameter (default to True if not provided)
    checked = True
    if len(sys.argv) > 3:
        checked = sys.argv[3].lower() == 'true'

    highlight_path_in_drawio(xml_file_path, [path_to_highlight], checked)