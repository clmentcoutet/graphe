from src.code_generation.generator.JavaCodeGenerator import JavaCodeGenerator
from src.code_generation.generator.JavaScriptCodeGenerator import JavaScriptCodeGenerator
from src.code_generation.generator.PythonCodeGenerator import PythonCodeGenerator
from src.code_generation.syntax.base_type import Language


class CodeGeneratorFactory:
    """Factory to create the appropriate CodeGenerator based on language."""
    generators = {
        Language.python: PythonCodeGenerator,
        Language.java: JavaCodeGenerator,
        Language.javascript: JavaScriptCodeGenerator
    }

    @classmethod
    def get_generator(cls, language: Language, tree_adapter, root):
        if language in cls.generators:
            return cls.generators[language](tree_adapter, root)
        raise ValueError(f"Unsupported language: {language}")