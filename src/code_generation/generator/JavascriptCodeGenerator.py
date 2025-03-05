from src.code_generation.generator.CodeGenerator import CodeGenerator


class JavascriptCodeGenerator(CodeGenerator):
    """Generates JavaScript source code from a syntax tree."""

    def visit_variable(self, node, indent):
        """Generate code for a variable node."""
        name = self.tree_adapter.get_property(node, 'name')
        return name

    def visit_literal(self, node, indent):
        """Generate code for a literal node."""
        value = self.tree_adapter.get_property(node, 'value')
        return str(value)

    def visit_return_statement(self, node, indent):
        """Generate code for a return statement."""
        expr_node = self.tree_adapter.get_children(node)[0]
        expr_code = self.visit(expr_node, indent)
        indent_str = ' ' * (indent * 4)
        return f"{indent_str}return {expr_code};"

    def visit_module(self, node, indent):
        statements = self.tree_adapter.get_children(node)
        return '\n\n'.join([self.visit(stmt, indent) for stmt in statements])

    def visit_function_def(self, node, indent):
        name = self.tree_adapter.get_property(node, 'name')
        children = self.tree_adapter.get_children(node)
        params_node = children[0]
        body_node = children[1]
        params_code = ', '.join([self.visit(param, indent) for param in self.tree_adapter.get_children(params_node)])
        body_code = '\n'.join([self.visit(stmt, indent + 1) for stmt in self.tree_adapter.get_children(body_node)])
        indent_str = ' ' * (indent * 4)
        return f"{indent_str}function {name}({params_code}) {{\n{body_code}\n{indent_str}}}"

    def visit_parameter(self, node, indent):
        return self.tree_adapter.get_property(node, 'name')

    def visit_assignment(self, node, indent):
        var = self.tree_adapter.get_property(node, 'variable')
        expr_node = self.tree_adapter.get_children(node)[0]
        expr_code = self.visit(expr_node, indent)
        indent_str = ' ' * (indent * 4)
        return f"{indent_str}{var} = {expr_code};"

    def visit_binary_op(self, node, indent):
        left = self.visit(self.tree_adapter.get_children(node)[0], indent)
        op = self.tree_adapter.get_property(node, 'operator')
        right = self.visit(self.tree_adapter.get_children(node)[1], indent)
        return f"{left} {op} {right}"
