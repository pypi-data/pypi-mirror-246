try:
    from ._impl_regex import *
except ImportError:
    from ._impl_fallback import *

__all__ = \
[
    'camel_case_to_underscore',
    'underscore_to_camel_case',
]
