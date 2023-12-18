from typing import Optional

from camel_case_switcher import dict_keys_camel_case_to_underscore, dict_keys_underscore_to_camel_case
from tests.abstract import BaseTestCase


class DictProcessorTests(BaseTestCase):
    def check_processing(self, obj_snake_case, obj_camel_case, recursive: Optional[bool], **kwargs):
        params = dict(snake_case=obj_snake_case, camel_case=obj_camel_case, recursive=recursive, **kwargs)
        if (recursive is not None):
            kwargs['recursive'] = recursive
        with self.subTest("snake case => camel case", **params):
            self.assertEqual(obj_camel_case, dict_keys_underscore_to_camel_case(obj_snake_case, **kwargs))
        with self.subTest("camel case => snake case", **params):
            self.assertEqual(obj_snake_case, dict_keys_camel_case_to_underscore(obj_camel_case, **kwargs))
    
    def test_dict_non_recursive(self):
        obj_snake_case = dict(some_field=44, some_other_field='apple', list_items=[dict(do_not_touch_me=True)])
        obj_camel_case = dict(someField=44, someOtherField='apple', listItems=[dict(do_not_touch_me=True)])
        
        self.check_processing(obj_snake_case, obj_camel_case, recursive=None)
        self.check_processing(obj_snake_case, obj_camel_case, recursive=False)
    
    def test_dict_recursive(self):
        obj_snake_case = dict(some_field=44, some_other_field='apple', list_items=[dict(please_touch_me=True)])
        obj_camel_case = dict(someField=44, someOtherField='apple', listItems=[dict(pleaseTouchMe=True)])
        
        self.check_processing(obj_snake_case, obj_camel_case, recursive=True)
    
    def test_list_non_recursive(self):
        obj_snake_case = [ dict(some_field=44, some_other_field='apple', list_items=[dict(do_not_touch_me=True)]) ]
        obj_camel_case = [ dict(someField=44, someOtherField='apple', listItems=[dict(do_not_touch_me=True)]) ]
        
        # Important: SAME arguments
        self.check_processing(obj_snake_case, obj_snake_case, recursive=None)
        self.check_processing(obj_camel_case, obj_camel_case, recursive=False)
    
    def test_list_recursive(self):
        obj_snake_case = [ dict(some_field=44, some_other_field='apple', list_items=[dict(please_touch_me=True)]) ]
        obj_camel_case = [ dict(someField=44, someOtherField='apple', listItems=[dict(pleaseTouchMe=True)]) ]
        
        self.check_processing(obj_snake_case, obj_camel_case, recursive=True)


__all__ = \
[
    'DictProcessorTests',
]


if (__name__ == '__main__'):
    from unittest import main as unittest_main
    unittest_main()
