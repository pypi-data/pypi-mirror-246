"""
.. include:: ../../README.md
"""

from collections import namedtuple

__title__ = 'camel-case-switcher'
__author__ = 'Peter Zaitcev / USSX Hares'
__license__ = 'MIT Licence'
__copyright__ = 'Copyright 2017,2023 Peter Zaitcev'
__version__ = '2.1.0'

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(*__version__.split('.'), releaselevel='stable', serial=0)

__all__ = \
[
    'version_info',
    '__title__',
    '__author__',
    '__license__',
    '__copyright__',
    '__version__',
]

from .string_processor import camel_case_to_underscore, underscore_to_camel_case
from .dict_processor import dict_keys_camel_case_to_underscore, dict_keys_underscore_to_camel_case


# Aliases
CamelCaseToUnderscore = camel_case_to_underscore
camelCaseToUnderscore = camel_case_to_underscore
camel2snake = camel_case_to_underscore

underscoreToCamelCase = underscore_to_camel_case
UnderscoreToCamelCase = underscore_to_camel_case
snake2camel = underscore_to_camel_case

# Deprecated imports
from .deprecated import camel_case_to_underscope, CamelCaseToUnderscope, camelCaseToUnderscope
from .deprecated import underscope_to_camel_case, underscopeToCamelCase, UnderscopeToCamelCase
from .deprecated import dict_keys_underscope_to_camel_case, dict_keys_camel_case_to_underscope

__all__.extend \
([
    'dict_keys_camel_case_to_underscore',
    'dict_keys_underscore_to_camel_case',
    'camel_case_to_underscore',
    'CamelCaseToUnderscore',
    'camelCaseToUnderscore',
    'camel2snake',
    'underscore_to_camel_case',
    'underscoreToCamelCase',
    'UnderscoreToCamelCase',
    'snake2camel',
])
