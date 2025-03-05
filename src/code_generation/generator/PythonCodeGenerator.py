from src.code_generation.generator.CodeGenerator import CodeGenerator
from src.code_generation.syntax.syntax_tree import Node


class PythonCodeGenerator(CodeGenerator):

    def visit_parameter(self, node: Node, indent: int):
        return super().visit_parameter(node, indent)

    def visit_identifier_expression(self, node: Node, indent: int):
        return super().visit_identifier_expression(node, indent)

    def visit_literal(self, node: Node, indent: int):
        return super().visit_literal(node, indent)

    def visit_body(self, node, indent):
        code = []
        for child in self.tree_adapter.get_children(node):
            code.append(self.visit(child, indent))
        return "\n".join(code)

    def visit_expression_statement(self, node, indent):
         raise NotImplementedError("visit_expression_statement not implemented")

    def visit_return_statement(self, node, indent):
        children = self.tree_adapter.get_children(node)
        code = self.visit(children[0], indent)  # Expression
        indent_str = "    " * indent
        return f"{indent_str}return {code}"

    def visit_module(self, node, indent):
        code = []
        for child in self.tree_adapter.get_children(node):
            code.append(self.visit(child, indent))
        return "\n\n".join(code)

    def visit_function_def(self, node, indent):
        name = self.tree_adapter.get_property(node, 'name')
        decorators = self.tree_adapter.get_property(node, 'decorators')
        children = self.tree_adapter.get_children(node)
        params = self.visit(children[0], indent)  # Parameters
        body = self.visit(children[1], indent + 1)  # Body
        indent_str = "    " * indent
        code = []
        for decorator in decorators:
            code.append(self.visit(decorator, indent))
        return f"{"\n".join(code)}\n{indent_str}def {name}({params}):\n{body}"

    def visit_parameters(self, node, indent):
        params = [self.visit(child, indent) for child in self.tree_adapter.get_children(node)]
        return ", ".join(params)

    def visit_binary_operation(self, node, indent):
        children = self.tree_adapter.get_children(node)
        left = self.visit(children[0], indent)
        right = self.visit(children[1], indent)
        op = self.tree_adapter.get_property(node, 'operator').value
        return f"{left} {op} {right}"


    def visit_unary_operation(self, node, indent):
        children = self.tree_adapter.get_children(node)
        op = self.tree_adapter.get_property(node, 'operator').value
        operand = self.visit(children[0], indent)
        return f"{op}{operand}"

    def visit_call_expression(self, node, indent):
        call = self.visit(self.tree_adapter.get_property(node, 'callee'))
        arguments = [self.visit(child, indent) for child in self.tree_adapter.get_children(node)]
        return f"{call}({', '.join(arguments)})"

    def visit_if_statement(self, node, indent):
        indent_str = "    " * indent
        children = self.tree_adapter.get_children(node)
        condition = self.visit(children[0], indent)
        then_branch = self.visit(children[1], indent + 1)
        code = f"{indent_str}if {condition}:\n{then_branch}"
        if len(children) > 2:  # Else branch exists
            else_branch = self.visit(children[2], indent + 1)
            code += f"\n{indent_str}else:\n{else_branch}"
        return code

    def visit_decorator(self, node, indent):
        name = self.visit(self.tree_adapter.get_property(node, 'expression'))
        parameters = self.tree_adapter.get_children(node)
        if len(parameters) > 0:
            params = self.visit(parameters[0], indent)
            return f"@{name}({params})"
        else:
            return f"@{name}"

