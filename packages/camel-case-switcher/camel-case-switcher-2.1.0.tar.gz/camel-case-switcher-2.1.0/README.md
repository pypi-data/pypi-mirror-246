# Camel Case and Underscore Style Switcher
Changes style of input string from CamelCase to the underscore_style, and vice versa.

### Installation
Install via pip: `pip install camel-case-switcher`


### Usage
```python
import camel_case_switcher
camel_case_switcher.camel_case_to_underscore('myCamelCaseString')    # =>  'my_camel_case_string'
camel_case_switcher.underscore_to_camel_case('my_underscore_string') # =>  'myUnderscoreString'
```

This library also provides a number of aliases for the very same methods.


### Features
#### Abbreviations Handling:
```python
import camel_case_switcher
camel_case_switcher.camel2snake('OSIApprovedMITLicense') # => 'osi_approved_mit_license'
```

This behaviour is enabled by default and can be disabled by providing a flag `process_acronyms=False`.


#### Unicode Support:
```python
import camel_case_switcher
camel_case_switcher.camel2snake('мояПрекраснаяПрограмма') # => 'моя_прекрасная_программа'
```

This behaviour is always on.

#### Private Members Processing:
```python
import camel_case_switcher

camel_case_switcher.camel2snake('privateField',   leading_lower_is_private=True)        # => '_private_field' <<<
camel_case_switcher.camel2snake('privateField',   leading_lower_is_private=False)       # => 'private_field'  <<<
camel_case_switcher.camel2snake('PublicField',    leading_lower_is_private=True)        # => 'public_field'
camel_case_switcher.camel2snake('PublicField',    leading_lower_is_private=False)       # => 'public_field'

camel_case_switcher.snake2camel('_private_field', leading_upper_if_not_private=True)    # => 'privateField'
camel_case_switcher.snake2camel('_private_field', leading_upper_if_not_private=False)   # => 'privateField'
camel_case_switcher.snake2camel('public_field',   leading_upper_if_not_private=True)    # => 'PublicField' <<<
camel_case_switcher.snake2camel('public_field',   leading_upper_if_not_private=False)   # => 'publicField' <<<
```

This behaviour is disabled by default.

#### Dictionaries Keys Mapping
This library can provide a copy of a given dictionary with all their keys being replaced.
```python
import camel_case_switcher
camel_case_switcher.dict_keys_camel_case_to_underscore({ 'firstName': "Alex", 'lastName': "Smith", 'age': 25 })
# => {'first_name': 'Alex', 'last_name': 'Smith', 'age': 25}
```

Very useful when importing API data structures from JavaScript or other camelCase-respecting languages.
Supports both non-recursive and recursive options, default is non-recursive.


### Alternatives
Alternatively to [stringcase](https://pypi.org/project/stringcase/),
works only with `snake_case` and `camelCase`, but works slightly better with them (see [Features](#Features) for details)

```python
import camel_case_switcher, stringcase

camel_case_switcher.camel2snake('OSIApprovedMITLicense') # => 'osi_approved_mit_license'
stringcase.snakecase('OSIApprovedMITLicense')            # => 'o_s_i_approved_m_i_t_license'
```
