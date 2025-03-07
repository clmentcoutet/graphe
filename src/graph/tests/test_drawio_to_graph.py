import networkx as nx
import pytest

from src.graph.flowchart.parse import parse_drawio


DRAWIO_NO_MXCELL_NO_USEROBJECT = r"xml_testing_files/no_mxcell_userobject.drawio"
DRAWIO_MXCELL_NO_USEROBJECT_ISOLATE_NODE = r"xml_testing_files/mxcell_no_userobject_isolate.drawio"
DRAWIO_MXCELL_NO_USEROBJECT_NO_ISOLATE_NODE = r"xml_testing_files/mxcell_no_userobject_no_isolate.drawio"
DRAWIO_MXCELL_USEROBJECT_NO_ISOLATE_NODE = r"xml_testing_files/mxcell_userobject_no_isolate.drawio"

TXT_FILE_PATH = r"E:\stage\sujet\python\src\graph\tests\xml_testing_files\test.txt"


def test_file_not_found__raise_FileNotFoundError():
    # Act
    with pytest.raises(FileNotFoundError) as e:
        file_extension = "non_existent_file.drawio"
        parse_drawio(file_extension)

    # Assert
    assert str(e.value) == "File 'non_existent_file.drawio' not found"


def test_file_extension_not_correct__raise_ValueError():
    # Act
    with pytest.raises(ValueError) as e:
        file_extension = TXT_FILE_PATH
        parse_drawio(file_extension)

    # Assert
    assert str(e.value) == "Invalid file extension. Expected .drawio"


def test_drawiofile_no_mxCell_no_UserObject_no_isolate_node__return_empty_graph():
    # Act
    graph: nx.DiGraph = parse_drawio(DRAWIO_NO_MXCELL_NO_USEROBJECT)

    # Assert
    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0


def test_drawiofile_mxCell_no_UserObject_no_isolate_node__return_two_node_one_edge_graph():
    # Act
    graph: nx.DiGraph = parse_drawio(DRAWIO_MXCELL_NO_USEROBJECT_NO_ISOLATE_NODE)

    # Assert
    assert len(graph.nodes) == 2
    assert graph.has_node("node-1")
    assert graph.has_node("node-2")
    assert len(graph.edges) == 1
    assert graph.has_edge("node-1", "node-2")


def test_drawiofile_mxCell_no_UserObject_isolate_node__return_two_node_one_edge_graph(mocker):
    # Arrange
    mock_isolates = mocker.patch("networkx.isolates", return_value=iter(["1"]))

    # Act
    graph: nx.DiGraph = parse_drawio(DRAWIO_MXCELL_NO_USEROBJECT_ISOLATE_NODE)

    # Assert
    assert len(graph.nodes) == 2
    assert graph.has_node("node-1")
    assert graph.has_node("node-2")
    assert len(graph.edges) == 1
    assert graph.has_edge("node-1", "node-2")
    assert mock_isolates.call_count == 1


def test_drawiofile_mxCell_UserObject_no_isolate_node__return_two_node_one_edge_graph():
    # Act
    graph: nx.DiGraph = parse_drawio(DRAWIO_MXCELL_USEROBJECT_NO_ISOLATE_NODE)
    # Assert
    assert len(graph.nodes) == 2
    assert graph.has_node("node-1")
    assert graph.has_node("node-2")
    assert len(graph.edges) == 1
    assert graph.has_edge("node-1", "node-2")
    assert graph.nodes["node-1"]["label"] == "1"
    assert graph.nodes["node-2"]["label"] == "2"