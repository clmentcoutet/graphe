import pytest

from src.code_generation.generator.JavaCodeGenerator import JavaCodeGenerator
from src.code_generation.syntax.base_type import Language
from src.code_generation.syntax.custom_type import (
    UnaryOperator,
    BinaryOperator,
    Modifier,
)
from src.code_generation.syntax.definition import (
    AttributeDefinition,
    FunctionDefinition,
    ClassDefinition, FunctionTestDefinition, ClassTestDefinition,
)
from src.code_generation.syntax.expression import (
    IdentifierExpression,
    Literal,
    BaseTypeExpression,
    CallExpression,
    UnaryOperation,
    BinaryOperation,
)
from src.code_generation.syntax.statement import (
    ReturnStatement,
    ExpressionStatement,
    IfStatement, CommentStatement,
)
from src.code_generation.syntax.syntax_tree import Parameter, Decorator, Body
from src.code_generation.tree.adapter.ClassTreeAdapter import ClassTreeAdapter


@pytest.fixture
def adapter():
    return ClassTreeAdapter()


@pytest.fixture
def language():
    return Language.java


def test_node_BaseTypeExpression_no_name__raise_AttributeError(adapter, language):
    # Arrange
    expression = BaseTypeExpression()
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'name' is not defined but required for class 'BaseTypeExpression'"
    )


def test_node_BaseTypeExpression_name__return_name(adapter, language):
    # Arrange
    expression = BaseTypeExpression(name="int")
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    code = generator.generate()

    # Assert
    assert code == "int"


def test_node_Literal_no_value__raise_AttributeError(adapter, language):
    # Arrange
    expression = Literal()
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'value' is not defined but required for class 'Literal'"
    )


def test_node_Literal_value__return_value(adapter, language):
    # Arrange
    expression = Literal(value="123")
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    code = generator.generate()

    # Assert
    assert code == "123"


def test_node_IdentifierExpression_no_name__raise_AttributeError(adapter, language):
    # Arrange
    expression = IdentifierExpression()
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'name' is not defined but required for class 'IdentifierExpression'"
    )


def test_node_IdentifierExpression_name_no_super_class__return_name(adapter, language):
    # Arrange
    expression = IdentifierExpression(name="myVariable")
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    code = generator.generate()

    # Assert
    assert code == "myVariable"


def test_node_IdentifierExpression_name_super_class__return_super_class_name(
    adapter, language
):
    # Arrange
    expression = IdentifierExpression(
        name="myVariable", super_class=IdentifierExpression(name="MySuperClass")
    )
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    code = generator.generate()

    # Assert
    assert code == "MySuperClass.myVariable"


def test_node_Parameter_no_type__raise_AttributeError(adapter, language):
    # Arrange
    parameter = Parameter()
    generator = JavaCodeGenerator(adapter, parameter)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'type' is not defined but required for class 'Parameter'"
    )


def test_node_Parameter_no_name__raise_AttributeError(adapter, language):
    # Arrange
    parameter = Parameter(type=BaseTypeExpression(name="int"))
    generator = JavaCodeGenerator(adapter, parameter)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'name' is not defined but required for class 'Parameter'"
    )


def test_node_Parameter_name_type__return_parameter_string(adapter, language):
    # Arrange
    parameter = Parameter(
        type=BaseTypeExpression(name="int"),
        name=IdentifierExpression(name="myVariable"),
    )
    generator = JavaCodeGenerator(adapter, parameter)

    # Act
    code = generator.generate()

    # Assert
    assert code == "int myVariable"


def test_node_Decorator_no_name__raise_AttributeError(adapter, language):
    # Arrange
    decorator = Decorator()
    generator = JavaCodeGenerator(adapter, decorator)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'name' is not defined but required for class 'Decorator'"
    )


def test_node_Decorator_name_no_arguments__return_decorator_string(adapter, language):
    # Arrange
    decorator = Decorator(name=IdentifierExpression(name="myDecorator"))
    generator = JavaCodeGenerator(adapter, decorator)

    # Act
    code = generator.generate()

    # Assert
    assert code == "@myDecorator"


def test_node_Decorator_name_arguments__return_decorator_string(adapter, language):
    # Arrange
    decorator = Decorator(
        name=IdentifierExpression(name="myDecorator"),
        arguments=[
            IdentifierExpression(name="arg1"),
            IdentifierExpression(name="arg2"),
        ],
    )
    generator = JavaCodeGenerator(adapter, decorator)

    # Act
    code = generator.generate()

    # Assert
    assert code == "@myDecorator(arg1, arg2)"


def test_node_CallExpression_no_callee__raise_AttributeError(adapter, language):
    # Arrange
    expression = CallExpression()
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'callee' is not defined but required for class 'CallExpression'"
    )


def test_no_CallExpression_callee_no_arguments_return_call_string(adapter, language):
    # Arrange
    expression = CallExpression(
        callee=IdentifierExpression(name="myFunction"),
    )
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    code = generator.generate()

    # Assert
    assert code == "myFunction()"


def test_no_CallExpression_callee_arguments__return_call_string(adapter, language):
    # Arrange
    expression = CallExpression(
        callee=IdentifierExpression(name="myFunction"),
        arguments=[
            IdentifierExpression(name="arg1"),
            IdentifierExpression(name="arg2"),
        ],
    )
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    code = generator.generate()

    # Assert
    assert code == "myFunction(arg1, arg2)"


def test_node_UnaryOperation_no_operand__raise_AttributeError(adapter, language):
    # Arrange
    expression = UnaryOperation()
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'operand' is not defined but required for class 'UnaryOperation'"
    )


def test_node_UnaryOperation_no_operator__raise_AttributeError(adapter, language):
    # Arrange
    expression = UnaryOperation(operand=IdentifierExpression(name="myVariable"))
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'operator' is not defined but required for class 'UnaryOperation'"
    )


def test_node_UnaryOperation_operand_operator__return_unary_operation_string(
    adapter, language
):
    # Arrange
    expression = UnaryOperation(
        operand=IdentifierExpression(name="myVariable"), operator=UnaryOperator.NEG
    )
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    code = generator.generate()

    # Assert
    assert code == "-myVariable"


def test_node_BinaryOperation_no_left_operand__raise_AttributeError(adapter, language):
    # Arrange
    expression = BinaryOperation()
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'left' is not defined but required for class 'BinaryOperation'"
    )


def test_node_BinaryOperation_no_right_operand__raise_AttributeError(adapter, language):
    # Arrange
    expression = BinaryOperation(left=IdentifierExpression(name="myLeftVariable"))
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'right' is not defined but required for class 'BinaryOperation'"
    )


def test_node_BinaryOperation_no_operator__raise_AttributeError(adapter, language):
    # Arrange
    expression = BinaryOperation(
        left=IdentifierExpression(name="myLeftVariable"),
        right=IdentifierExpression(name="myRightVariable"),
    )
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'operator' is not defined but required for class 'BinaryOperation'"
    )


def test_node_BinaryOperation_left_right_operator__return_binary_operation_string(
    adapter, language
):
    # Arrange
    expression = BinaryOperation(
        left=IdentifierExpression(name="myLeftVariable"),
        right=IdentifierExpression(name="myRightVariable"),
        operator=BinaryOperator.ADD,
    )
    generator = JavaCodeGenerator(adapter, expression)

    # Act
    code = generator.generate()

    # Assert
    assert code == "myLeftVariable + myRightVariable"


def test_node_ReturnStatement_no_expression__raise_AttributeError(adapter, language):
    # Arrange
    statement = ReturnStatement()
    generator = JavaCodeGenerator(adapter, statement)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'expression' is not defined but required for class 'ReturnStatement'"
    )


def test_node_ReturnStatement_expression__return_return_string(adapter, language):
    # Arrange
    statement = ReturnStatement(expression=IdentifierExpression(name="myVariable"))
    generator = JavaCodeGenerator(adapter, statement)

    # Act
    code = generator.generate()

    # Assert
    assert code == "return myVariable;"


def test_node_ExpressionStatement_no_expression__raise_AttributeError(
    adapter, language
):
    # Arrange
    statement = ExpressionStatement()
    generator = JavaCodeGenerator(adapter, statement)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'expression' is not defined but required for class 'ExpressionStatement'"
    )


def test_node_ExpressionStatement_expression__return_expression_statement_string(
    adapter, language
):
    # Arrange
    statement = ExpressionStatement(expression=IdentifierExpression(name="myVariable"))
    generator = JavaCodeGenerator(adapter, statement)

    # Act
    code = generator.generate()

    # Assert
    assert code == "myVariable;"


def test_node_IfStatement_no_condition__raise_AttributeError(adapter, language):
    # Arrange
    statement = IfStatement()
    generator = JavaCodeGenerator(adapter, statement)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'condition' is not defined but required for class 'IfStatement'"
    )


def test_node_IfStatement_condition_no_then__raise_AttributeError(adapter, language):
    # Arrange
    statement = IfStatement(condition=IdentifierExpression(name="myCondition"))
    generator = JavaCodeGenerator(adapter, statement)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'then' is not defined but required for class 'IfStatement'"
    )


def test_node_IfStatement_condition_then_no_else__return_if_statement_string(
    adapter, language
):
    # Arrange
    statement = IfStatement(
        condition=IdentifierExpression(name="myCondition"),
        then=Body(
            statements=[
                ReturnStatement(
                    expression=IdentifierExpression(name="myReturnVariable")
                )
            ]
        ),
    )
    generator = JavaCodeGenerator(adapter, statement)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == """if (myCondition) {
    return myReturnVariable;\n}"""
    )


def test_node_IfStatement_condition_then_else__return_if_statement_string(
    adapter, language
):
    # Arrange
    statement = IfStatement(
        condition=IdentifierExpression(name="myCondition"),
        then=Body(
            statements=[
                ReturnStatement(
                    expression=IdentifierExpression(name="myReturnVariable")
                )
            ]
        ),
        _else=Body(
            statements=[
                ReturnStatement(
                    expression=IdentifierExpression(name="myDefaultReturnVariable")
                )
            ]
        ),
    )
    generator = JavaCodeGenerator(adapter, statement)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == """if (myCondition) {
    return myReturnVariable;\n} else {
    return myDefaultReturnVariable;\n}"""
    )


def test_node_Body_no_statements__raise_AttributeError(adapter, language):
    # Arrange
    body = Body()
    generator = JavaCodeGenerator(adapter, body)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'statements' is not defined but required for class 'Body'"
    )


def test_node_Body_two_statements__return_body_string(adapter, language):
    # Arrange
    body = Body(
        statements=[
            ExpressionStatement(expression=IdentifierExpression(name="myVariable1")),
            ReturnStatement(expression=IdentifierExpression(name="myVariable2")),
        ]
    )
    generator = JavaCodeGenerator(adapter, body)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == """myVariable1;
return myVariable2;"""
    )


def test_node_AttributeDefinition_no_name__raise_AttributeError(adapter, language):
    # Arrange
    definition = AttributeDefinition()
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'name' is not defined but required for class 'AttributeDefinition'"
    )


def test_node_AttributeDefinition_name_no_modifier__raise_AttributeError(
    adapter, language
):
    # Arrange
    definition = AttributeDefinition(name=IdentifierExpression(name="MyVariable"))
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'modifier' is not defined but required for class 'AttributeDefinition'"
    )


def test_node_AttributeDefinition_name_modifier_no_type__raise_AttributeError(
    adapter, language
):
    # Arrange
    definition = AttributeDefinition(
        name=IdentifierExpression(name="myVariable"), modifier=Modifier.PUBLIC
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'type' is not defined but required for class 'AttributeDefinition'"
    )


def test_node_AttributeDefinition_name_modifier_type_no_initializer__return_attribute_definition_string(
    adapter, language
):
    # Arrange
    definition = AttributeDefinition(
        name=IdentifierExpression(name="myVariable"),
        modifier=Modifier.PUBLIC,
        type=IdentifierExpression(name="int"),
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == "public int myVariable;"


def test_node_AttributeDefinition_name_modifier_type_initializer__return_attribute_definition_string(
    adapter, language
):
    # Arrange
    definition = AttributeDefinition(
        name=IdentifierExpression(name="myVariable"),
        modifier=Modifier.PUBLIC,
        type=IdentifierExpression(name="int"),
        initializer=Literal(value=0),
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == "public int myVariable = 0;"


def test_node_FunctionDefinition_no_name__raise_AttributeError(adapter, language):
    # Arrange
    definition = FunctionDefinition()
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'name' is not defined but required for class 'FunctionDefinition'"
    )


def test_node_FunctionDefinition_name_no_modifier__raise_AttributeError(
    adapter, language
):
    # Arrange
    definition = FunctionDefinition(name=IdentifierExpression(name="myFunction"))
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'modifier' is not defined but required for class 'FunctionDefinition'"
    )


def test_node_FunctionDefinition_name_modifier_no_return_type__raise_AttributeError(
    adapter, language
):
    # Arrange
    definition = FunctionDefinition(
        name=IdentifierExpression(name="myFunction"), modifier=Modifier.PUBLIC
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'return_type' is not defined but required for class 'FunctionDefinition'"
    )


def test_node_FunctionDefinition_name_modifier_return_type_no_body__return_function_definition_string(
    adapter, language
):
    # Arrange
    definition = FunctionDefinition(
        name=IdentifierExpression(name="myFunction"),
        modifier=Modifier.PUBLIC,
        return_type=IdentifierExpression(name="void"),
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == """public void myFunction() {\n}"""


def test_node_FunctionDefinition_name_modifier_return_type_parameter_no_body__return_function_definition_string(
    adapter, language
):
    # Arrange
    definition = FunctionDefinition(
        name=IdentifierExpression(name="myFunction"),
        modifier=Modifier.PUBLIC,
        return_type=IdentifierExpression(name="void"),
        parameters=[
            Parameter(
                type=IdentifierExpression(name="int"),
                name=IdentifierExpression(name="myParameter"),
            )
        ],
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == """public void myFunction(int myParameter) {\n}"""


def test_node_FunctionDefinition_name_modifier_return_type_parameter_body__return_function_definition_string(
    adapter, language
):
    # Arrange
    definition = FunctionDefinition(
        name=IdentifierExpression(name="myFunction"),
        modifier=Modifier.PUBLIC,
        return_type=IdentifierExpression(name="void"),
        parameters=[
            Parameter(
                type=IdentifierExpression(name="int"),
                name=IdentifierExpression(name="myParameter"),
            )
        ],
        body=Body(
            statements=[
                ReturnStatement(expression=IdentifierExpression(name="myReturnValue"))
            ]
        ),
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == """public void myFunction(int myParameter) {\n    return myReturnValue;\n}"""
    )


def test_node_FunctionDefinition_name_modifier_return_type_parameter_body_decorator__return_function_definition_string(
    adapter, language
):
    # Arrange
    definition = FunctionDefinition(
        name=IdentifierExpression(name="myFunction"),
        modifier=Modifier.PUBLIC,
        return_type=IdentifierExpression(name="void"),
        parameters=[
            Parameter(
                type=IdentifierExpression(name="int"),
                name=IdentifierExpression(name="myParameter"),
            )
        ],
        body=Body(
            statements=[
                ReturnStatement(expression=IdentifierExpression(name="myReturnValue"))
            ]
        ),
        decorators=[Decorator(name=IdentifierExpression(name="myDecorator"))],
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == """@myDecorator\npublic void myFunction(int myParameter) {\n    return myReturnValue;\n}"""
    )


def test_node_ClassDefinition_no_name__raise_AttributeError(adapter, language):
    # Arrange
    definition = ClassDefinition()
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'name' is not defined but required for class 'ClassDefinition'"
    )


def test_node_ClassDefinition_no_modifier__raise_AttributeError(adapter, language):
    # Arrange
    definition = ClassDefinition(name=IdentifierExpression(name="MyClass"))
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'modifier' is not defined but required for class 'ClassDefinition'"
    )


def test_node_ClassDefinition_name_modifier__return_class_definition_string(
    adapter, language
):
    # Arrange
    definition = ClassDefinition(
        name=IdentifierExpression(name="MyClass"), modifier=Modifier.PUBLIC
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == "public class MyClass {\n}"


def test_node_ClassDefinition_name_modifier_extends__return_class_definition_string(
    adapter, language
):
    # Arrange
    definition = ClassDefinition(
        name=IdentifierExpression(name="MyClass"),
        modifier=Modifier.PUBLIC,
        extends=IdentifierExpression(name="MyBaseClass"),
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == "public class MyClass extends MyBaseClass {\n}"


def test_node_ClassDefinition_name_modifier_extends_implements__return_class_definition_string(
    adapter, language
):
    # Arrange
    definition = ClassDefinition(
        name=IdentifierExpression(name="MyClass"),
        modifier=Modifier.PUBLIC,
        extends=IdentifierExpression(name="MyBaseClass"),
        implements=[
            IdentifierExpression(name="MyInterface1"),
            IdentifierExpression(name="MyInterface2"),
        ],
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == "public class MyClass extends MyBaseClass implements MyInterface1, MyInterface2 {\n}"
    )


def test_node_ClassDefinition_name_modifier_extends_implements_attributes__return_class_definition_string(
    adapter, language
):
    # Arrange
    definition = ClassDefinition(
        name=IdentifierExpression(name="MyClass"),
        modifier=Modifier.PUBLIC,
        extends=IdentifierExpression(name="MyBaseClass"),
        implements=[
            IdentifierExpression(name="MyInterface1"),
            IdentifierExpression(name="MyInterface2"),
        ],
        attributes=[
            AttributeDefinition(
                name=IdentifierExpression(name="myAttribute"),
                modifier=Modifier.PUBLIC,
                type=IdentifierExpression(name="String"),
            ),
            AttributeDefinition(
                name=IdentifierExpression(name="myOtherAttribute"),
                modifier=Modifier.PROTECTED,
                type=IdentifierExpression(name="int"),
            ),
        ],
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == """public class MyClass extends MyBaseClass implements MyInterface1, MyInterface2 {
    public String myAttribute;
    protected int myOtherAttribute;\n}"""
    )


def test_node_ClassDefinition_name_modifier_extends_implements_attributes_methods__return_class_definition_string(
    adapter, language
):
    # Arrange
    definition = ClassDefinition(
        name=IdentifierExpression(name="MyClass"),
        modifier=Modifier.PUBLIC,
        extends=IdentifierExpression(name="MyBaseClass"),
        implements=[
            IdentifierExpression(name="MyInterface1"),
            IdentifierExpression(name="MyInterface2"),
        ],
        attributes=[
            AttributeDefinition(
                name=IdentifierExpression(name="myAttribute"),
                modifier=Modifier.PUBLIC,
                type=IdentifierExpression(name="String"),
            ),
            AttributeDefinition(
                name=IdentifierExpression(name="myOtherAttribute"),
                modifier=Modifier.PROTECTED,
                type=IdentifierExpression(name="int"),
            ),
        ],
        methods=[
            FunctionDefinition(
                name=IdentifierExpression(name="myMethod"),
                modifier=Modifier.PUBLIC,
                return_type=IdentifierExpression(name="void"),
                parameters=[
                    Parameter(
                        type=IdentifierExpression(name="int"),
                        name=IdentifierExpression(name="myParameter"),
                    )
                ],
                body=Body(
                    statements=[
                        ReturnStatement(
                            expression=IdentifierExpression(name="myReturnValue")
                        )
                    ]
                ),
            ),
            FunctionDefinition(
                name=IdentifierExpression(name="myOtherMethod"),
                modifier=Modifier.PROTECTED,
                return_type=IdentifierExpression(name="String"),
                parameters=[],
                body=Body(
                    statements=[
                        ReturnStatement(expression=Literal(value='"Hello, World!"'))
                    ]
                ),
            ),
        ],
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == """public class MyClass extends MyBaseClass implements MyInterface1, MyInterface2 {
    public String myAttribute;
    protected int myOtherAttribute;

    public void myMethod(int myParameter) {
        return myReturnValue;
    }

    protected String myOtherMethod() {
        return "Hello, World!";
    }\n}"""
    )


def test_node_Comment_no_comment__raise_AttributeError(adapter, language):
    # Arrange
    comment = CommentStatement()
    generator = JavaCodeGenerator(adapter, comment)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert str(e.value) == "Attribute 'comment' is not defined but required for class 'CommentStatement'"


def test_node_Comment_comment__return_comment_string(adapter, language):
    # Arrange
    comment = CommentStatement(comment="This is a test comment")
    generator = JavaCodeGenerator(adapter, comment)

    # Act
    code = generator.generate()

    # Assert
    assert code == "// This is a test comment"


def test_node_FunctionTestDefinition_no_name__raise_AttributeError(adapter, language):
    # Arrange
    definition = FunctionTestDefinition()
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert (
        str(e.value)
        == "Attribute 'name' is not defined but required for class 'FunctionTestDefinition'"
    )

def test_node_FunctionTestDefinition_name_no_body_no_parameters__return_function_definition_string(adapter, language):
    # Arrange
    definition = FunctionTestDefinition(name=IdentifierExpression(name="myFunctionTest"))
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == "@Test\npublic void myFunctionTest() {\n}"


def test_node_FunctionTestDefinition_name_body_no_parameters__return_function_definition_string(adapter, language):
    # Arrange
    definition = FunctionTestDefinition(
        name=IdentifierExpression(name="myFunctionTest"),
        body=Body(
            statements=[
                ReturnStatement(expression=IdentifierExpression(name="myReturnValue"))
            ]
        )
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == "@Test\npublic void myFunctionTest() {\n    return myReturnValue;\n}"


def test_node_FunctionTestDefinition_name_body_parameters__return_function_definition_string(adapter, language):
    # Arrange
    definition = FunctionTestDefinition(
        name=IdentifierExpression(name="myFunctionTest"),
        body=Body(
            statements=[
                ReturnStatement(expression=IdentifierExpression(name="myReturnValue"))
            ]
        ),
        parameters=[
            Parameter(
                type=IdentifierExpression(name="int"),
                name=IdentifierExpression(name="param1"),
            ),
            Parameter(
                type=IdentifierExpression(name="String"),
                name=IdentifierExpression(name="param2"),
            ),
        ],
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == "@Test\npublic void myFunctionTest(int param1, String param2) {\n    return myReturnValue;\n}"
    )


def test_node_ClassTestDefinition_no_name__raise_AttributeError(adapter, language):
    # Arrange
    definition = ClassTestDefinition()
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    with pytest.raises(AttributeError) as e:
        generator.generate()

    # Assert
    assert str(e.value) == "Attribute 'name' is not defined but required for class 'ClassTestDefinition'"


def test_node_ClassTestDefinition_name_no_method__return_class_definition_string(adapter, language):
    # Arrange
    definition = ClassTestDefinition(name=IdentifierExpression(name="MyClassTest"))
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert code == "public class MyClassTest {\n}"


def test_node_ClassTestDefinition_name_method__return_class_definition_string(adapter, language):
    # Arrange
    definition = ClassTestDefinition(
        name=IdentifierExpression(name="MyClassTest"),
        methods=[
            FunctionTestDefinition(
                name=IdentifierExpression(name="myMethodTest"),
                body=Body(
                    statements=[
                        ReturnStatement(expression=IdentifierExpression(name="myReturnValue"))
                    ]
                ),
            )
        ]
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    assert (
        code
        == """public class MyClassTest {\n
    @Test
    public void myMethodTest() {
        return myReturnValue;
    }\n}"""
    )

def test_large_class_definition(adapter, language):
    # Arrange
    definition = ClassDefinition(
        name=IdentifierExpression(name="ComplexClass"),
        modifier=Modifier.PUBLIC,
        extends=IdentifierExpression(name="BaseClass"),
        implements=[
            IdentifierExpression(name="Interface1"),
            IdentifierExpression(name="Interface2"),
        ],
        attributes=[
            AttributeDefinition(
                name=IdentifierExpression(name="attribute1"),
                modifier=Modifier.PRIVATE,
                type=IdentifierExpression(name="String"),
            ),
            AttributeDefinition(
                name=IdentifierExpression(name="attribute2"),
                modifier=Modifier.PROTECTED,
                type=IdentifierExpression(name="int"),
            ),
        ],
        methods=[
            FunctionDefinition(
                name=IdentifierExpression(name="method1"),
                modifier=Modifier.PUBLIC,
                return_type=IdentifierExpression(name="void"),
                parameters=[
                    Parameter(
                        type=IdentifierExpression(name="int"),
                        name=IdentifierExpression(name="param1"),
                    )
                ],
                body=Body(
                    statements=[
                        ExpressionStatement(
                            expression=IdentifierExpression(name="attribute2")
                        ),
                        ReturnStatement(expression=Literal(value="42")),
                    ]
                ),
            ),
            FunctionDefinition(
                name=IdentifierExpression(name="method2"),
                modifier=Modifier.PUBLIC,
                return_type=IdentifierExpression(name="String"),
                parameters=[],
                decorators=[
                    Decorator(name=IdentifierExpression(name="CustomAnnotation"))
                ],
                body=Body(
                    statements=[ReturnStatement(expression=Literal(value='"Hello"'))]
                ),
            ),
        ],
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    expected_code = """public class ComplexClass extends BaseClass implements Interface1, Interface2 {
    private String attribute1;
    protected int attribute2;

    public void method1(int param1) {
        attribute2;
        return 42;
    }

    @CustomAnnotation
    public String method2() {
        return "Hello";
    }
}"""
    assert code == expected_code


def test_mega_class_definition(adapter, language):
    # Arrange
    definition = ClassDefinition(
        name=IdentifierExpression(name="MegaClass"),
        modifier=Modifier.PUBLIC,
        extends=IdentifierExpression(name="SuperClass"),
        implements=[
            IdentifierExpression(name="InterfaceA"),
            IdentifierExpression(name="InterfaceB"),
            IdentifierExpression(name="InterfaceC"),
        ],
        attributes=[
            AttributeDefinition(
                name=IdentifierExpression(name="id"),
                modifier=Modifier.PRIVATE,
                type=IdentifierExpression(name="int"),
                initializer=Literal(value="0"),
            ),
            AttributeDefinition(
                name=IdentifierExpression(name="name"),
                modifier=Modifier.PUBLIC,
                type=IdentifierExpression(name="String"),
            ),
            AttributeDefinition(
                name=IdentifierExpression(name="active"),
                modifier=Modifier.PROTECTED,
                type=IdentifierExpression(name="boolean"),
                initializer=Literal(value="true"),
            ),
        ],
        methods=[
            # Méthode conditionnelle qui retourne le maximum de deux valeurs
            FunctionDefinition(
                name=IdentifierExpression(name="computeValue"),
                modifier=Modifier.PUBLIC,
                return_type=IdentifierExpression(name="int"),
                parameters=[
                    Parameter(
                        type=IdentifierExpression(name="int"),
                        name=IdentifierExpression(name="a"),
                    ),
                    Parameter(
                        type=IdentifierExpression(name="int"),
                        name=IdentifierExpression(name="b"),
                    ),
                ],
                body=Body(
                    statements=[
                        IfStatement(
                            condition=BinaryOperation(
                                left=IdentifierExpression(name="a"),
                                right=IdentifierExpression(name="b"),
                                operator=BinaryOperator.GT,
                            ),
                            then=Body(
                                statements=[
                                    ReturnStatement(
                                        expression=IdentifierExpression(name="a")
                                    )
                                ]
                            ),
                            _else=Body(
                                statements=[
                                    ReturnStatement(
                                        expression=IdentifierExpression(name="b")
                                    )
                                ]
                            ),
                        )
                    ]
                ),
            ),
            # Méthode avec annotation qui met à jour le nom
            FunctionDefinition(
                name=IdentifierExpression(name="updateName"),
                modifier=Modifier.PUBLIC,
                return_type=IdentifierExpression(name="void"),
                parameters=[
                    Parameter(
                        type=IdentifierExpression(name="String"),
                        name=IdentifierExpression(name="newName"),
                    )
                ],
                decorators=[
                    Decorator(
                        name=IdentifierExpression(name="Logger"),
                        arguments=[Literal(value='"updateName called"')],
                    )
                ],
                body=Body(
                    statements=[
                        ExpressionStatement(
                            expression=BinaryOperation(
                                left=IdentifierExpression(name="this.name"),
                                right=IdentifierExpression(name="newName"),
                                operator=BinaryOperator.EQ,
                            )
                        )
                    ]
                ),
            ),
            # Méthode qui inverse l'état d'un booléen et le retourne
            FunctionDefinition(
                name=IdentifierExpression(name="toggleActive"),
                modifier=Modifier.PUBLIC,
                return_type=IdentifierExpression(name="boolean"),
                parameters=[],
                body=Body(
                    statements=[
                        CommentStatement(comment="toggle active"),
                        ExpressionStatement(
                            expression=UnaryOperation(
                                operand=IdentifierExpression(name="active"),
                                operator=UnaryOperator.NOT,
                            )
                        ),
                        ReturnStatement(expression=IdentifierExpression(name="active")),
                    ]
                ),
            ),
        ],
    )
    generator = JavaCodeGenerator(adapter, definition)

    # Act
    code = generator.generate()

    # Assert
    expected_code = """public class MegaClass extends SuperClass implements InterfaceA, InterfaceB, InterfaceC {
    private int id = 0;
    public String name;
    protected boolean active = true;

    public int computeValue(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }

    @Logger("updateName called")
    public void updateName(String newName) {
        this.name = newName;
    }

    public boolean toggleActive() {
        // toggle active
        !active;
        return active;
    }
}"""
    assert code == expected_code
