__all__ = (
    'ast_to_data',
    'convert_file',
    'data_to_text',
    'parse',
    'text_to_data',
)


import os
from ast import AST, Module
from os import PathLike

from .compiler import Compiler
from .lexer import Lexer
from .parser import RecursiveDescentParser, FileParser, PyParser


type FileContents = str
type PythonData = str


def parse(file: PathLike = None, *, string: FileContents = None) -> Module:
    '''
    Parse a config file and return its AST.

    :param file: The file to parse
    :type file: :class:`PathLike`
    '''
    if string is None:
        return FileParser(file).parse()
    if file is None:
        return RecursiveDescentParser(string=string)).parse()
    raise ValueError(
        "A `file` argument is required when `string` is not given or None."
    )


def ast_to_data(node: AST) -> PythonData:
    '''
    Convert an AST to Python data.

    :param node: The AST to convert
    :type node: :class:`AST`
    '''
    return Compiler().compile(node)


def data_to_text(data: PythonData) -> FileContents:
    '''
    Convert Python data to config file text.

    :param data: The data to convert
    :type data: :class:`PythonData`
    '''
    return PyParser.to_scuff(data)


def text_to_data(string: FileContents) -> PythonData:
    '''
    Convert config file text to Python data.

    :param string: The text to parse
    :type string: :class:`FileContents`
    '''
    module = RecursiveDescentParser(string=string).parse()
    return Compiler().compile(module)


def convert_file(file: PathLike) -> PythonData:
    '''
    Read a config file, parse its contents and return the encoded data.

    :param file: The file to parse
    '''
    absolute = os.path.abspath(os.path.expanduser(file))
    module = FileParser(absolute).parse()
    return Compiler().compile(module)

