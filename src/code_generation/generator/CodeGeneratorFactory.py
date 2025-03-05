from src.code_generation.generator.JavascriptCodeGenerator import JavascriptCodeGenerator
from src.code_generation.generator.PythonCodeGenerator import PythonCodeGenerator


class CodeGeneratorFactory:
    """Factory to create the appropriate CodeGenerator based on language."""
    generators = {
        'python': PythonCodeGenerator,
        'javascript': JavascriptCodeGenerator,
        # Add 'java': JavaCodeGenerator when implemented
    }

    @classmethod
    def get_generator(cls, language, tree_adapter, root):
        if language in cls.generators:
            return cls.generators[language](tree_adapter, root)
        raise ValueError(f"Unsupported language: {language}")