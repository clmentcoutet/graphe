from src.code_generation.syntax.definition import FunctionTestDefinition
from src.code_generation.syntax.expression import IdentifierExpression
from src.code_generation.syntax.statement import CommentStatement
from src.code_generation.syntax.syntax_tree import Body


def generate_syntax_tree_skeleton_from_test_name(test_name: str) -> FunctionTestDefinition:
    body = Body(
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
    return FunctionTestDefinition(
        name=IdentifierExpression(name=test_name),
        body=body
    )