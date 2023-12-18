from camel_case_switcher import underscore_to_camel_case, underscoreToCamelCase, UnderscoreToCamelCase
from tests.abstract import BaseTestCase


class Snake2CamelUnderscoreToCamelCaseTestCase(BaseTestCase):
    def test_normal(self):
        # print("Testing 'Underscore to camel case' - no additional options")
        result = underscore_to_camel_case('underscore_to_camel_case')
        expected = 'underscoreToCamelCase'
        self.assertEqual(result, expected)
    
    def test_normal_leading_underscore(self):
        # print("Testing 'Underscore to camel case' - no additional options; leading underscore")
        result = underscore_to_camel_case('_underscore_to_camel_case')
        expected = 'underscoreToCamelCase'
        self.assertEqual(result, expected)
    
    def test_no_upper_if_not_private(self):
        # print("Testing 'Underscore to camel case': leading_upper_if_not_private=False")
        result = underscore_to_camel_case('underscore_to_camel_case', leading_upper_if_not_private=False)
        expected = 'underscoreToCamelCase'
        self.assertEqual(result, expected)
    
    def test_upper_if_not_private(self):
        # print("Testing 'Underscore to camel case': leading_upper_if_not_private=True")
        result = underscore_to_camel_case('underscore_to_camel_case', leading_upper_if_not_private=True)
        expected = 'UnderscoreToCamelCase'
        self.assertEqual(result, expected)
    
    def test_upper_if_not_private_leading_underscore(self):
        # print("Testing 'Underscore to camel case': leading_upper_if_not_private=True; leading underscore")
        result = underscore_to_camel_case('_underscore_to_camel_case', leading_upper_if_not_private=False)
        expected = 'underscoreToCamelCase'
        self.assertEqual(result, expected)
    
    def test_no_upper_if_not_private_leading_underscore(self):
        # print("Testing 'Underscore to camel case': leading_upper_if_not_private=True; leading underscore")
        result = underscore_to_camel_case('_underscore_to_camel_case', leading_upper_if_not_private=True)
        expected = 'underscoreToCamelCase'
        self.assertEqual(result, expected)

class Snake2CamelDifferentStyleNamesTestCase(BaseTestCase):
    def test_underscore_to_camel_case_1(self):
        # print("Testing 'Different Style Names': underscoreStyle and UnderscoreStyle")
        result = underscoreToCamelCase
        expected = UnderscoreToCamelCase
        self.assertEqual(result, expected)
    def test_underscore_to_camel_case_2(self):
        # print("Testing 'Different Style Names': underscoreStyle and underscore_style")
        result = underscoreToCamelCase
        expected = underscore_to_camel_case
        self.assertEqual(result, expected)


__all__ = \
[
    'Snake2CamelDifferentStyleNamesTestCase',
    'Snake2CamelUnderscoreToCamelCaseTestCase',
]


if (__name__ == '__main__'):
    from unittest import main as unittest_main
    unittest_main()
