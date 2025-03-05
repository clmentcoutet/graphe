from abc import ABC, abstractmethod, ABCMeta
from typing import List, Optional, Any

from src.code_generation.syntax.custom_type import NodeType, BinaryOperator, UnaryOperator



class Node(ABC):
    TYPE_MAPPING = {
        'Module': NodeType.MODULE,
        'FunctionDefinition': NodeType.FUNCTION_DEF,
        'Parameters': NodeType.PARAMETERS,
        'Parameter': NodeType.PARAMETER,
        'Body': NodeType.BODY,
        'Statement': NodeType.STATEMENT,
        'ExpressionStatement': NodeType.EXPRESSION_STATEMENT,
        'IfStatement': NodeType.IF_STATEMENT,
        'ReturnStatement': NodeType.RETURN_STATEMENT,
        'Expression': NodeType.EXPRESSION,
        'IdentifierExpression': NodeType.IDENTIFIER_EXPRESSION,
        'Literal': NodeType.LITERAL,
        'BinaryOperation': NodeType.BINARY_OPERATION,
        'UnaryOperation': NodeType.UNARY_OPERATION,
        'CallExpression': NodeType.CALL_EXPRESSION,
        'Decorator': NodeType.DECORATOR
    }

    def get_type(self):
        class_name = self.__class__.__name__
        return self.TYPE_MAPPING[class_name]

    @property
    @abstractmethod
    def children(self) -> List[Any] | Any:
        raise NotImplementedError('Subclasses must implement this method')


class Module(Node):
    def __init__(self, functions: List['FunctionDefinition']):
        self.functions = functions

    @property
    def children(self):
        return self.functions


class Expression(Node, metaclass=ABCMeta):
    pass

class Statement(Node, metaclass=ABCMeta):
    pass


class Parameter(Node):
    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return []


class Parameters(Node):
    def __init__(self, parameters: List[Parameter]):
        self.parameters = parameters

    @property
    def children(self):
        return self.parameters


class Body(Node):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    @property
    def children(self):
        return self.statements


class Decorator(Node):
    def __init__(self, expression: 'IdentifierExpression', parameters: Optional[Parameters] = None):
        self.expression = expression
        self.parameters = parameters or []

    @property
    def children(self):
        return self.parameters


class FunctionDefinition(Node):
    def __init__(
            self,
            name: str,
            parameters: Parameters,
            body: Body,
            decorators: Optional[List[Decorator]] = None,
    ):
        self.name = name
        self.decorators = decorators or []
        self.parameters = parameters
        self.body = body

    @property
    def children(self):
        return [self.parameters, self.body]


class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    @property
    def children(self):
        return []


class IfStatement(Statement):
    def __init__(self, condition: Expression, then_branch: Body, else_branch: Optional[Body] = None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    @property
    def children(self):
        children = [self.condition, self.then_branch]
        if self.else_branch is not None:
            children.append(self.else_branch)
        return children


class ReturnStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

    @property
    def children(self):
        return [self.expression]


class IdentifierExpression(Expression):
    def __init__(self, name: str):
        self.name = name

    @property
    def children(self):
        return []


class Literal(Expression):
    def __init__(self, value: Any):
        self.value = value

    @property
    def children(self):
        return []


class BinaryOperation(Expression):
    def __init__(self, left: Expression, operator: BinaryOperator, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    @property
    def children(self):
        return [self.left, self.right]


class UnaryOperation(Expression):
    def __init__(self, operator: UnaryOperator, operand: Expression):
        self.operator = operator
        self.operand = operand

    @property
    def children(self):
        return [self.operand]


class CallExpression(Expression):
    def __init__(self, callee: IdentifierExpression, arguments: List[Expression]):
        self.callee = callee
        self.arguments = arguments  # List of expressions as arguments

    @property
    def children(self):
        return self.arguments