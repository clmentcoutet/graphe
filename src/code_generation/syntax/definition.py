from abc import ABCMeta

from src.code_generation.syntax.syntax_tree import Node


class Definition(Node, metaclass=ABCMeta):
    pass


class FunctionDefinition(Definition):
    """
    Represents a function definition

    Java attributes:
        - name (IdentifierExpression): The function name
        - return_type (IdentifierExpression): The function return type
        - modifier (Modifier): The function modifier (e.g., 'public', 'private')
        - body (Optional[Body]): The function body
        - parameters (Optional[List[Parameter]]): The function parameters
        - decorators (Optional[List[Decorator]]): The function decorators
    """


class AttributeDefinition(Definition):
    """
    Represents a class attribute

    Java attributes:
        - name (IdentifierExpression): The attribute name
        - type (IdentifierExpression): The attribute type
        - modifier (Modifier): The attribute modifier (e.g., 'public', 'private')
        - initializer (Optional[Expression]): The attribute initializer
    """


class ClassDefinition(Definition):
    """
    Represents a class definition

    Java attributes:
        - name (IdentifierExpression): The class name
        - modifiers (Modifier): The class modifier (e.g., 'public', 'private')
        - attributes (Optional[AttributeDefinition]): attribute of the class
        - methods (Optional[List[FunctionDefinition]]): methods of the class
        - implements (Optional[List[IdentifierExpression]]): The class implements
        - extends (Optional[IdentifierExpression]): The class extends
    """

class ClassTestDefinition(Definition):
    """
    Represents a class test definition

    Common Attributes:
        - name (IdentifierExpression): The class name
        - methods (Optional[List[FunctionTestDefinition]]): methods of the class
    """

class FunctionTestDefinition(Definition):
    """
    Represents a function test definition

    Common Attributes:
        - name (IdentifierExpression): The function name
        - body (Optional[Body]): The function body
        - parameters (Optional[List[IdentifierExpression]]): The function parameters
    """
