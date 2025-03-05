from src.code_generation.generator.CodeGeneratorFactory import CodeGeneratorFactory
from src.code_generation.syntax.base_type import Language
from src.code_generation.tree.adapter.ClassTreeAdapter import ClassTreeAdapter
from src.code_generation.example_tree import tree_two_functions


# Example Usage
if __name__ == "__main__":
    tree = tree_two_functions()
    adapter = ClassTreeAdapter()

    # Generate Python code
    generator = CodeGeneratorFactory.get_generator(Language.python, adapter, tree)
    code = generator.generate()
    print("Python Code:")
    print(code)
    with open('output.py', 'w') as f:
        f.write(code)

    # Generate Java code
    generator = CodeGeneratorFactory.get_generator(Language.java, adapter, tree)
    code = generator.generate()
    print("\nJava Code:")
    print(code)
    with open('output.java', 'w') as f:
        f.write(code)

    # Generate JS code
    generator = CodeGeneratorFactory.get_generator(Language.javascript, adapter, tree)
    code = generator.generate()
    print("\nJS Code:")
    print(code)
    with open('output.js', 'w') as f:
        f.write(code)