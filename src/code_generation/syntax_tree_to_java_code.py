from src.code_generation.generator.CodeGeneratorFactory import CodeGeneratorFactory
from src.code_generation.syntax.base_type import Language
from src.code_generation.tree.adapter.ClassTreeAdapter import ClassTreeAdapter


def syntax_tree_to_java_code(tree):
    adapter = ClassTreeAdapter()

    generator = CodeGeneratorFactory.get_generator(Language.java, adapter, tree)
    code = generator.generate()
    print("\nJava Code:")
    print(code)
    with open("output.java", "w") as f:
        f.write(code)