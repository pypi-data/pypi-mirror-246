'''
Scuff:
    A config file format and transpiler suite written in Python.
'''


__title__ = 'scuff'
__description__ = "A config file format and transpiler suite written in Python."
__url__ = "https://github.com/akyuute/scuff"
__version__ = '0.1'
__author__ = "akyuute"
__license__ = 'MIT'
__copyright__ = "Copyright (c) 2023-present akyuute"


from .tools import (
    ast_to_data,
    convert_file,
    data_to_text,
    parse,
    text_to_data,
)
from .parser import (
    FileParser,
    RecursiveDescentParser,
    PyParser,
    Unparser,
)
from .compiler import Compiler

