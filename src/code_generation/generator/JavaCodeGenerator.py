from src.code_generation.generator.CodeGenerator import CodeGenerator
from src.code_generation.syntax.custom_type import Modifier
from src.code_generation.syntax.definition import (
    ClassDefinition,
    AttributeDefinition,
    FunctionDefinition, FunctionTestDefinition, ClassTestDefinition,
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
    ExpressionStatement, CommentStatement,
)
from src.code_generation.syntax.syntax_tree import (
    Module,
    Parameter,
    Body,
    Decorator,
    Node,
)
from src.code_generation.tree.adapter.TreePort import TreePort


class JavaCodeGenerator(CodeGenerator):
    INDENT = "    "

    def __init__(self, tree_adapter: TreePort, root: Node):
        super().__init__(tree_adapter, root)

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
        res = f"{self.get_indent_str(indent)}@{self.visit(name, indent)}"
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
        return (
            f"{self.visit(left, indent)} {operator.value} {self.visit(right, indent)}"
        )

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
        res += f"\n{self.get_indent_str(indent)}}}"
        return res

    def visit_body(self, node: Body, indent: int):
        statements = self.get_property(node, "statements")
        return "\n".join([self.visit(statement, indent) for statement in statements])

    def visit_attribute_def(self, node: AttributeDefinition, indent: int):
        name = self.get_property(node, "name")
        modifier = self.get_property(node, "modifier")
        _type = self.get_property(node, "type")
        initializer = self.get_property(node, "initializer", is_require=False)
        res = f"{self.get_indent_str(indent)}{modifier.value} {self.visit(_type, indent)} {self.visit(name, indent)}"
        if initializer:
            res += f" = {self.visit(initializer, indent)}"
        res += ";"
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
            decorators_str = ", ".join(
                [self.visit(decorator, indent) for decorator in decorators]
            )
            res += f"{decorators_str}\n"
        res += f"{self.get_indent_str(indent)}{modifier.value} {self.visit(return_type, indent)} {self.visit(name, indent)}("
        if parameters:
            parameters_str = ", ".join(
                [self.visit(param, indent) for param in parameters]
            )
            res += f"{parameters_str}"
        res += ") {"
        if body:
            res += "\n"
            res += self.visit(body, indent + 1)
        res += f"\n{self.get_indent_str(indent)}}}"
        return res

    def visit_class_def(self, node: ClassDefinition, indent: int):
        name = self.get_property(node, "name")
        modifier = self.get_property(node, "modifier")
        extends = self.get_property(node, "extends", is_require=False)
        implements = self.get_property(node, "implements", is_require=False)
        attributes = self.get_property(node, "attributes", is_require=False)
        methods = self.get_property(node, "methods", is_require=False)
        res = f"{modifier.value} class {self.visit(name, indent)}"
        if extends:
            res += f" extends {self.visit(extends, indent)}"
        if implements:
            res += f" implements {', '.join([self.visit(impl, indent) for impl in implements])}"
        res += " {"
        if attributes:
            res += "\n"
            res += "\n".join(
                [self.visit(attribute, indent + 1) for attribute in attributes]
            )
        if methods:
            res += "\n\n"
            res += "\n\n".join([self.visit(method, indent + 1) for method in methods])
        res += "\n}"
        return res

    def visit_comment_statement(self, node: CommentStatement, indent: int):
        comment = self.get_property(node, "comment")
        return f"{self.get_indent_str(indent)}// {comment}"

    def _function_test_def_to_function_def_instance(self, function_test_def: FunctionTestDefinition):
        name = self.get_property(function_test_def, "name")
        body = self.get_property(function_test_def, "body", is_require=False)
        parameters = self.get_property(function_test_def, "parameters", is_require=False)
        return FunctionDefinition(
            name=name,
            modifier=Modifier.PUBLIC,
            return_type=IdentifierExpression(name="void"),
            decorators=[Decorator(name=IdentifierExpression(name="Test"))],
            body=body,
            parameters=parameters,
        )

    def visit_function_test_def(self, node: FunctionTestDefinition, indent: int):
        function_def_instance = self._function_test_def_to_function_def_instance(node)
        return self.visit(function_def_instance, indent)

    def visit_class_test_def(self, node: ClassTestDefinition, indent: int):
        name = self.get_property(node, "name")
        methods = self.get_property(node, "methods", is_require=False)
        class_definition_instance = ClassDefinition(
            name=name,
            modifier=Modifier.PUBLIC,
        )
        if methods:
            class_definition_instance.add_kwargs(
                methods=[self._function_test_def_to_function_def_instance(method) for method in methods]
            )
        return self.visit(class_definition_instance, indent)