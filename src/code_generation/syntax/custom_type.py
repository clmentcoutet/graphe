from enum import Enum


class NodeType(Enum):
    MODULE = 'Module'
    FUNCTION_DEF = 'FunctionDefinition'
    PARAMETERS = 'Parameters'
    PARAMETER = 'Parameter'
    BODY = 'Body'
    STATEMENT = 'Statement'
    EXPRESSION_STATEMENT = 'ExpressionStatement'
    IF_STATEMENT = 'IfStatement'
    RETURN_STATEMENT = 'ReturnStatement'
    EXPRESSION = 'Expression'
    IDENTIFIER_EXPRESSION = 'IdentifierExpression'
    BASE_TYPE_EXPRESSION = 'BaseTypeExpression'
    LITERAL = 'Literal'
    BINARY_OPERATION = 'BinaryOperation'
    UNARY_OPERATION = 'UnaryOperation'
    CALL_EXPRESSION = 'CallExpression'
    DECORATOR = 'Decorator'
    CLASS_DEF = 'ClassDefinition'
    ATTRIBUTE_DEF = 'AttributeDefinition'


class Operator(Enum):
    pass


class BinaryOperator(Enum):
    ADD = '+'
    SUB = '-'
    MUL = '*'
    DIV = '/'
    GT = '>'
    LT = '<'
    POW = '**'

class UnaryOperator(Operator):
    NEG = '-'
    NOT = 'not'


class Modifiers(Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'
