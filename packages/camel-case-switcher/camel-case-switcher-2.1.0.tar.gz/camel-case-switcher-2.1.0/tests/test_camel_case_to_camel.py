from camel_case_switcher import camel_case_to_underscore, camelCaseToUnderscore, CamelCaseToUnderscore
from tests.abstract import BaseTestCase


class Camel2SnakeCamelCaseToUnderscoreTestCase(BaseTestCase):
    def test_normal(self):
        # print("Testing 'Camel case to underscore' - no additional options")
        result = camel_case_to_underscore('camelCaseToUnderscore')
        expected = 'camel_case_to_underscore'
        self.assertEqual(result, expected)
    
    def test_no_lower_is_private(self):
        # print("Testing 'Camel case to underscore': leading_lower_is_private=False")
        result = camel_case_to_underscore('camelCaseToUnderscore', leading_lower_is_private=False)
        expected = 'camel_case_to_underscore'
        self.assertEqual(result, expected)
    
    def test_lower_is_private(self):
        # print("Testing 'Camel case to underscore': leading_lower_is_private=True")
        result = camel_case_to_underscore('CamelCaseToUnderscore', leading_lower_is_private=True)
        expected = 'camel_case_to_underscore'
        self.assertEqual(result, expected)
    
    def test_lower_is_private_leading_lowercase(self):
        # print("Testing 'Camel case to underscore': leading_lower_is_private=True; leading lowercase")
        result = camel_case_to_underscore('camelCaseToUnderscore', leading_lower_is_private=False)
        expected = 'camel_case_to_underscore'
        self.assertEqual(result, expected)
    
    def test_no_lower_is_private_leading_lowercase(self):
        # print("Testing 'Camel case to underscore': leading_lower_is_private=True; leading lowercase")
        result = camel_case_to_underscore('camelCaseToUnderscore', leading_lower_is_private=True)
        expected = '_camel_case_to_underscore'
        self.assertEqual(result, expected)

class Camel2SnakeAcronymProcessingTestCase(BaseTestCase):
    def test_enabled_leading_acronym(self):
        # print("Testing 'Acronym processing': process_acronyms=True; leading acronym")
        result = camel_case_to_underscore('ABCObject', process_acronyms=True)
        expected = 'abc_object'
        self.assertEqual(result, expected)
    
    def test_enabled_middle_acronym(self):
        # print("Testing 'Acronym processing': process_acronyms=True; middle acronym")
        result = camel_case_to_underscore('ObjectABCInstance', process_acronyms=True)
        expected = 'object_abc_instance'
        self.assertEqual(result, expected)
    
    def test_enabled_trailing_acronym(self):
        # print("Testing 'Acronym processing': process_acronyms=True; trailing acronym")
        result = camel_case_to_underscore('ObjectABC', process_acronyms=True)
        expected = 'object_abc'
        self.assertEqual(result, expected)
    
    def test_disabled_leading_acronym(self):
        # print("Testing 'Acronym processing': process_acronyms=False; leading acronym")
        result = camel_case_to_underscore('ABCObject', process_acronyms=False)
        expected = 'a_b_c_object'
        self.assertEqual(result, expected)
    
    def test_disabled_middle_acronym(self):
        # print("Testing 'Acronym processing': process_acronyms=False; middle acronym")
        result = camel_case_to_underscore('ObjectABCInstance', process_acronyms=False)
        expected = 'object_a_b_c_instance'
        self.assertEqual(result, expected)
    
    def test_disabled_trailing_acronym(self):
        # print("Testing 'Acronym processing': process_acronyms=False; trailing acronym")
        result = camel_case_to_underscore('ObjectABC', process_acronyms=False)
        expected = 'object_a_b_c'
        self.assertEqual(result, expected)

class Camel2SnakeDifferentStyleNamesTestCase(BaseTestCase):
    def test_camel_case_to_underscore_1(self):
        # print("Testing 'Different Style Names': camelCase and CamelCase")
        result = camelCaseToUnderscore
        expected = CamelCaseToUnderscore
        self.assertEqual(result, expected)
    def test_camel_case_to_underscore_2(self):
        # print("Testing 'Different Style Names': camelCase and camel_case")
        result = camelCaseToUnderscore
        expected = camel_case_to_underscore
        self.assertEqual(result, expected)


__all__ = \
[
    'Camel2SnakeAcronymProcessingTestCase',
    'Camel2SnakeCamelCaseToUnderscoreTestCase',
    'Camel2SnakeDifferentStyleNamesTestCase',
]


if (__name__ == '__main__'):
    from unittest import main as unittest_main
    unittest_main()
