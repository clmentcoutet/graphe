from src.code_generation.generator.CodeGenerator import CodeGenerator
from src.code_generation.syntax.base_type import JavaBaseType, BaseType
from src.code_generation.syntax.definition import (
    ClassDefinition,
    AttributeDefinition,
    FunctionDefinition,
)
from src.code_generation.syntax.expression import (
    BaseTypeExpression,
    BinaryOperation,
    UnaryOperation,
    CallExpression,
    Literal,
    IdentifierExpression,
)
from src.code_generation.syntax.statement import (
    ReturnStatement,
    IfStatement,
    ExpressionStatement,
)
from src.code_generation.syntax.syntax_tree import (
    Module,
    Parameters,
    Parameter,
    Body,
    Decorator,
)
from src.code_generation.tree.adapter.TreePort import TreePort


class JavaCodeGenerator(CodeGenerator):
    INDENT = "    "

    def __init__(self, tree_adapter: TreePort, root: Module):
        super().__init__(tree_adapter, root)
        self.base_type = BaseType(JavaBaseType)

    def visit_module(self, node: Module, indent: int) -> str:
        classes = self.get_property(node, "classes", is_require=False)
        if not classes:
            return ""
        return "\n".join([self.visit(child, indent) for child in classes])

    def visit_base_type_expression(self, node: BaseTypeExpression, indent: int):
        name = self.get_property(node, "name")
        return name

    def visit_literal(self, node: Literal, indent: int):
        value = self.get_property(node, "value")
        return f"{value}"

    def visit_identifier_expression(self, node: IdentifierExpression, indent: int):
        name = self.get_property(node, "name")
        super_class = self.get_property(node, "super_class", is_require=False)
        if super_class:
            return f"{self.visit(super_class, indent)}.{name}"
        return name

    def visit_parameter(self, node: Parameter, indent: int):
        _type = self.get_property(node, "type")
        name = self.get_property(node, "name")
        return f"{self.visit(_type, indent)} {self.visit(name, indent)}"

    def visit_decorator(self, node: Decorator, indent: int):
        name = self.get_property(node, "name")
        arguments = self.get_property(node, "arguments", is_require=False)
        res = f"@{self.visit(name, indent)}"
        if arguments:
            arguments_str = ", ".join([self.visit(arg, indent) for arg in arguments])
            res += f"({arguments_str})"
        return res

    def visit_call_expression(self, node: CallExpression, indent: int):
        name = self.get_property(node, "callee")
        arguments = self.get_property(node, "arguments", is_require=False)
        res = f"{self.visit(name, indent)}("
        if arguments:
            arguments_str = ", ".join([self.visit(arg, indent) for arg in arguments])
            res += f"{arguments_str}"
        return f"{res})"

    def visit_unary_operation(self, node: UnaryOperation, indent: int):
        operand = self.get_property(node, "operand")
        operator = self.get_property(node, "operator")
        return f"{operator.value}{self.visit(operand, indent)}"

    def visit_binary_operation(self, node: BinaryOperation, indent: int):
        left = self.get_property(node, "left")
        right = self.get_property(node, "right")
        operator = self.get_property(node, "operator")
        return f"{self.visit(left, indent)} {operator.value} {self.visit(right, indent)}"

    def visit_return_statement(self, node: ReturnStatement, indent: int):
        expression = self.get_property(node, "expression")
        return f"{self.get_indent_str(indent)}return {self.visit(expression, indent)};"

    def visit_expression_statement(self, node: ExpressionStatement, indent: int):
        expression = self.get_property(node, "expression")
        return f"{self.get_indent_str(indent)}{self.visit(expression, indent)};"

    def visit_if_statement(self, node: IfStatement, indent: int):
        condition = self.get_property(node, "condition")
        then_branch = self.get_property(node, "then")
        else_branch = self.get_property(node, "_else", is_require=False)
        res = f"{self.get_indent_str(indent)}if ({self.visit(condition, indent)}) {{\n"
        res += f"{self.visit(then_branch, indent + 1)}"
        if else_branch:
            res += f"\n{self.get_indent_str(indent)}}} else {{\n"
            res += self.visit(else_branch, indent + 1)
        res += f"{self.get_indent_str(indent)}\n}}"
        return res

    def visit_body(self, node: Body, indent: int):
        statements = self.get_property(node, "statements")
        return "\n".join([self.visit(statement, indent) for statement in statements])

    def visit_attribute_def(self, node: AttributeDefinition, indent: int):
        name = self.get_property(node, "name")
        modifier = self.get_property(node, "modifier")
        _type = self.get_property(node, "type")
        initializer = self.get_property(node, "initializer", is_require=False)
        res = f"{modifier.value} {self.visit(_type, indent)} {self.visit(name, indent)}"
        if initializer:
            res += f" = {self.visit(initializer, indent)}"
        return res

    def visit_function_def(self, node: FunctionDefinition, indent: int):
        name = self.get_property(node, "name")
        modifier = self.get_property(node, "modifier")
        return_type = self.get_property(node, "return_type")
        decorators = self.get_property(node, "decorators", is_require=False)
        parameters = self.get_property(node, "parameters", is_require=False)
        body = self.get_property(node, "body", is_require=False)
        res = ""
        if decorators:
            decorators_str = ", ".join([self.visit(decorator, indent) for decorator in decorators])
            res += f"{decorators_str}\n"
        res += f"{modifier.value} {self.visit(return_type, indent)} {self.visit(name, indent)}("
        if parameters:
            parameters_str = ", ".join([self.visit(param, indent) for param in parameters])
            res += f"{parameters_str}"
        res += ") {"
        if body:
            res += "\n"
            res += self.visit(body, indent + 1)
        res += "\n}"
        return res