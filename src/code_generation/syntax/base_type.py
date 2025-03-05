from enum import Enum
from typing import Type


class Language(Enum):
    python = 1
    java = 2
    javascript = 3


class JavaBaseType(Enum):
    DEFAULT = 'Object'
    BOOLEAN = 'boolean'
    CHAR = 'char'
    BYTE = 'byte'
    INTEGER = 'int'
    FLOAT = 'float'
    STRING = 'string'


class PythonBaseType(Enum):
    DEFAULT = 'object'
    BOOLEAN = 'bool'
    CHAR = 'char'
    BYTE = 'byte'
    INTEGER = 'int'
    FLOAT = 'float'
    STRING ='str'


class JavaScriptBaseType(Enum):
    DEFAULT = 'Object'
    BOOLEAN = 'boolean'
    CHAR = 'String'
    BYTE = 'Number'
    INTEGER = 'Number'
    FLOAT = 'Number'
    STRING ='string'


class BaseType:
    def __init__(self, language: Type[Enum]):
        self.language = language

    def __getattr__(self, item):
        if item in self.language.__members__:
            return self.language[item].value
        raise AttributeError(f"{item} is not a valid type in {self.language.__name__}")