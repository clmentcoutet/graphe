import pytest

from src.code_generation.syntax.definition import FunctionTestDefinition, ClassTestDefinition
from src.code_generation.syntax.statement import CommentStatement
from src.code_generation.syntax.syntax_tree import Body
from src.graph_to_syntax_tree.generate_syntax_tree_skeleton import generate_syntax_tree_skeleton_from_test_name
from src.graph_to_syntax_tree.merge_syntax_tree import merge_syntax_tree
from src.graph_to_syntax_tree.path_to_syntax import get_test_name_path_using_node_label


@pytest.fixture
def path():
    return [
        {'id': 1, 'label': 'node', 'type': 'start_end'},
        {'id': 2, 'label': 'lowercase_node_label', 'type': 'internal_call'},
        {'id': 3, 'label': 'look for label', 'type': 'external_call'},
        {'id': 4, 'label': 'check if label is correct', 'type': 'external_call'},
        {'id': 5, 'label': 'return_string', 'type': 'start_end'},
    ]


def test_get_test_name_from_path_using_node_label__return_test_name_string(path):
    # Arrange

    # Act
    test_name = get_test_name_path_using_node_label(path)

    # Assert
    assert test_name == "test_node__look_for_label_check_if_label_is_correct__return_string"


def test_generate_syntax_tree_skeleton_from_test_name__return_function_test_definition():
    # Arrange
    test_name = "test_node__look_for_label_check_if_label_is_correct__return_string"
    function_test_definition_test = FunctionTestDefinition(
        name="test_node__look_for_label_check_if_label_is_correct__return_string",
        body=Body(
            statements=[
                CommentStatement(
                    comment=f"Arrange"
                ),
                CommentStatement(
                    comment=f"Act"
                ),
                CommentStatement(
                    comment=f"Assert"
                ),
            ],
        )
    )

    # Act
    syntax_tree = generate_syntax_tree_skeleton_from_test_name(test_name)

    # Assert
    assert syntax_tree == function_test_definition_test


def test_merge_syntax_tree__return_merged_syntax_tree():
    # Arrange
    syntax_tree1 = FunctionTestDefinition(
        name="test_1",
        body=Body(
            statements=[
                CommentStatement(
                    comment=f"Arrange"
                ),
                CommentStatement(
                    comment=f"Act"
                ),
                CommentStatement(
                    comment=f"Assert"
                ),
            ],
        )
    )
    syntax_tree2 = FunctionTestDefinition(
        name="test_2",
        body=Body(
            statements=[
                CommentStatement(
                    comment=f"Arrange"
                ),
                CommentStatement(
                    comment=f"Act"
                ),
                CommentStatement(
                    comment=f"Assert"
                ),
            ],
        )
    )
    merged_syntax_tree_test = ClassTestDefinition(
        name="test_class",
        methods= [
            syntax_tree1,
            syntax_tree2,
            ],
        )

    # Act
    merged_syntax_tree = merge_syntax_tree("test_class", [syntax_tree1, syntax_tree2])

    # Assert
    assert merged_syntax_tree == merged_syntax_tree_test
