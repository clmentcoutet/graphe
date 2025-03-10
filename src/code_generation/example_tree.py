from src.code_generation.syntax.custom_type import BinaryOperator, UnaryOperator
from src.code_generation.syntax.definition import (
    FunctionDefinition,
    ClassDefinition,
    AttributeDefinition,
)
from src.code_generation.syntax.expression import (
    IdentifierExpression,
    Literal,
    BinaryOperation,
    UnaryOperation,
    CallExpression,
    BaseTypeExpression,
)
from src.code_generation.syntax.statement import IfStatement, ReturnStatement
from src.code_generation.syntax.syntax_tree import *


def tree_two_functions():
    return Module(
        classes=[
            ClassDefinition(
                name=IdentifierExpression("MathUtils"),
                attributes=[
                    AttributeDefinition(
                        name=IdentifierExpression("count"),
                        type=BaseTypeExpression("INTEGER"),
                        initializer=Literal(0),
                    ),
                    AttributeDefinition(
                        name=IdentifierExpression("name"),
                        type=BaseTypeExpression("STRING"),
                        initializer=Literal(2),
                    ),
                    AttributeDefinition(
                        name=IdentifierExpression("base"),
                        type=BaseTypeExpression("INTEGER"),
                    ),
                ],
                methods=[
                    FunctionDefinition(
                        name=IdentifierExpression("factorial"),
                        parameters=Parameters(
                            [
                                Parameter(name=IdentifierExpression("self")),
                                Parameter(name=IdentifierExpression("n")),
                            ]
                        ),
                        body=Body(
                            statements=[
                                IfStatement(
                                    condition=BinaryOperation(
                                        left=IdentifierExpression("n"),
                                        operator=BinaryOperator.GT,
                                        right=Literal(0),
                                    ),
                                    then_branch=Body(
                                        statements=[
                                            ReturnStatement(
                                                expression=BinaryOperation(
                                                    left=IdentifierExpression("n"),
                                                    operator=BinaryOperator.MUL,
                                                    right=CallExpression(
                                                        callee=IdentifierExpression(
                                                            "factorial",
                                                            super_class=IdentifierExpression(
                                                                "self"
                                                            ),
                                                        ),
                                                        arguments=[
                                                            BinaryOperation(
                                                                left=IdentifierExpression(
                                                                    "n"
                                                                ),
                                                                operator=BinaryOperator.SUB,
                                                                right=Literal(1),
                                                            )
                                                        ],
                                                    ),
                                                )
                                            )
                                        ]
                                    ),
                                    else_branch=Body(
                                        statements=[
                                            ReturnStatement(expression=Literal(1))
                                        ]
                                    ),
                                )
                            ]
                        ),
                        return_type=BaseTypeExpression("INTEGER"),
                    )
                ],
            )
        ]
    )


BinaryOperation(
    left=IdentifierExpression("n"),
    operator=BinaryOperator.SUB,
    right=Literal(1),
)
