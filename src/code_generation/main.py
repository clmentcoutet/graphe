from src.code_generation.generator.CodeGeneratorFactory import CodeGeneratorFactory
from src.code_generation.syntax.syntax_tree import *
from src.code_generation.tree.ClassTreeAdapter import ClassTreeAdapter

# Example Usage
if __name__ == "__main__":
    # Example dictionary-based syntax tree
    tree = Module(functions=[
        # Function: @staticmethod factorial(n)
        FunctionDefinition(
            name="factorial",
            parameters=Parameters(parameters=[Parameter(name="n")]),
            body=Body(statements=[
                # if n > 0:
                #     return n * factorial(n - 1)
                # else:
                #     return 1
                IfStatement(
                    condition=BinaryOperation(
                        left=IdentifierExpression("n"),
                        operator=BinaryOperator.GT,
                        right=Literal(0)
                    ),
                    then_branch=Body(statements=[
                        ReturnStatement(
                            expression=BinaryOperation(
                                left=IdentifierExpression("n"),
                                operator=BinaryOperator.MUL,
                                right=CallExpression(
                                    callee=IdentifierExpression("factorial"),
                                    arguments=[
                                        BinaryOperation(
                                            left=IdentifierExpression("n"),
                                            operator=BinaryOperator.SUB,
                                            right=Literal(1)
                                        )
                                    ]
                                )
                            )
                        )
                    ]),
                    else_branch=Body(statements=[
                        ReturnStatement(expression=Literal(1))
                    ])
                )
            ]),
            decorators=[Decorator(
                expression=IdentifierExpression("staticmethod"),
            parameters=Parameters(parameters=[Parameter(name="n")]))]
        ),
        # Function: is_positive(x)
        FunctionDefinition(
            name="is_positive",
            parameters=Parameters(parameters=[Parameter(name="x")]),
            body=Body(statements=[
                # if x > 0:
                #     return True
                # else:
                #     return not (-x < 0)
                IfStatement(
                    condition=BinaryOperation(
                        left=IdentifierExpression("x"),
                        operator=BinaryOperator.GT,
                        right=Literal(0)
                    ),
                    then_branch=Body(statements=[
                        ReturnStatement(expression=Literal(True))
                    ]),
                    else_branch=Body(statements=[
                        ReturnStatement(
                            expression=UnaryOperation(
                                operator=UnaryOperator.NOT,
                                operand=BinaryOperation(
                                    left=UnaryOperation(
                                        operator=UnaryOperator.NEG,
                                        operand=IdentifierExpression("x")
                                    ),
                                    operator=BinaryOperator.GT,
                                    right=Literal(0)
                                )
                            )
                        )
                    ])
                )
            ])
        )
    ])

    # Generate Python code
    adapter = ClassTreeAdapter()
    generator = CodeGeneratorFactory.get_generator('python', adapter, tree)
    code = generator.generate()
    print("Python Code:")
    print(code)
    with open('output.py', 'w') as f:
        f.write(code)
