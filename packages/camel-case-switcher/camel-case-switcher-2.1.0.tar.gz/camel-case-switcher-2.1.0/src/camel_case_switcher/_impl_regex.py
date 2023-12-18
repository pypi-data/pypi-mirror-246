import regex
from typing import *

import sys
if (sys.version_info < (3, 10)):
    from typing import Match

def camel_case_to_underscore(camel_case_string: str, *, leading_lower_is_private: bool = False, process_acronyms: bool = True) -> str:
    if (not camel_case_string):
        return ''
    
    result = camel_case_string
    
    if (process_acronyms):
        result = regex.sub(r'[[:upper:]]+(?=[[:upper:]]|\b)', lambda m: ('_' + cast(Match, m).group(0)).lower(), result)
    
    result = regex.sub(r'[[:upper:]]', lambda m: '_' + cast(Match[str], m).group(0), result).lower().strip('_')
    
    if (leading_lower_is_private and camel_case_string[0].islower()):
        result = '_' + result
    
    return result


def underscore_to_camel_case(underscore_string: str, leading_upper_if_not_private: bool = False) -> str:
    if (not underscore_string):
        return ''
    
    result = underscore_string
    result = regex.sub(r'[[:letter:]]+(?=_|\b)', lambda m: cast(Match[str], m).group(0).capitalize(), result)
    result = result.replace('_', '')
    
    if (leading_upper_if_not_private and not underscore_string[0].startswith('_')):
        result = result[0].upper() + result[1:]
    else:
        result = result[0].lower() + result[1:]
    
    return result


__all__ = \
[
    'camel_case_to_underscore',
    'underscore_to_camel_case',
]
