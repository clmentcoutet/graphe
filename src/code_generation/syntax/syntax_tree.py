from abc import ABC, abstractmethod
from typing import List, Optional, Any

from src.code_generation.syntax.custom_type import NodeType

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
        'BaseTypeExpression': NodeType.BASE_TYPE_EXPRESSION,
        'Literal': NodeType.LITERAL,
        'BinaryOperation': NodeType.BINARY_OPERATION,
        'UnaryOperation': NodeType.UNARY_OPERATION,
        'CallExpression': NodeType.CALL_EXPRESSION,
        'Decorator': NodeType.DECORATOR,
        "ClassDefinition": NodeType.CLASS_DEF,
        'AttributeDefinition': NodeType.ATTRIBUTE_DEF,
    }

    def get_type(self):
        class_name = self.__class__.__name__
        return self.TYPE_MAPPING[class_name]

    @property
    @abstractmethod
    def children(self) -> List[Any] | Any:
        raise NotImplementedError('Subclasses must implement this method')


class Module(Node):
    def __init__(
            self,
            classes: Optional[List['ClassDefinition']] = None,
            functions: Optional[List['FunctionDefinition']] = None,
            attributes: Optional[List['AttributeDefinition']] = None,
    ):
        self.classes = classes or []
        self.functions = functions or []
        self.attributes = attributes or []

    @property
    def children(self):
        return self.classes + self.functions + self.attributes


class Parameter(Node):
    """
    Represents a function parameter.

    Attributes:
        name (IdentifierExpression): The parameter's name.
        _type (IdentifierExpression): The parameter's type.'
        default_value (Optional[Literal]): The parameter's default value.'
    """
    def __init__(
            self,
            name: 'IdentifierExpression',
            *,
            _type: Optional['IdentifierExpression'] = None,
            default_value: Optional['Literal'] = None):
        self.name = name
        self._type = _type
        self.default_value = default_value

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
    def __init__(self, statements: List['Statement']):
        self.statements = statements

    @property
    def children(self):
        return self.statements


class Decorator(Node):
    def __init__(self, expression: 'IdentifierExpression', parameters: Optional[Parameters] = None):
        self.expression = expression
        self.parameters = parameters or []

    @property
    def children(self) -> List[Node]:
        return self.parameters


