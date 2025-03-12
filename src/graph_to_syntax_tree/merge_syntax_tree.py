from typing import List

from src.code_generation.syntax.definition import FunctionTestDefinition, ClassTestDefinition
from src.code_generation.syntax.expression import IdentifierExpression


def merge_syntax_tree(name: str, list_syntax_tree: List[FunctionTestDefinition]) -> ClassTestDefinition:
    """
    Merges a list of FunctionTestDefinition objects into a single ClassTestDefinition object.

    Args:
        name (str): The name of the class.
        list_syntax_tree (List[FunctionTestDefinition]): A list of FunctionTestDefinition objects.

    Returns:
        ClassTestDefinition: A ClassTestDefinition object containing all the FunctionTestDefinition objects.
    """
    return ClassTestDefinition(
        name=IdentifierExpression(name=name),
        methods=list_syntax_tree
    )
