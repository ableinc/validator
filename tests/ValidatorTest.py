import unittest
from unittest.mock import Mock
from lib.validator import _get_types, _parse_validation_rule, _operation, validate, validator
from lib.exceptions import ValidationError
import json

class Response:
    def __init__(self):
        pass
    def text(self, content):
        return content
    def json(self, content):
        return content
    
class Request:
    def __init__(self):
        self.query = {
            "q": "educational courses on economics",
            "comment": "Im looking for an online course on economics.",
            "code": 100
        }
        self.params = {}


def next(message, status=400):
    message["statusCode"] = status
    response = json.dumps(message)
    print(response)


class ValidatorTest(unittest.TestCase):
    validation_rules = {
            "q": "string|required|max:100",
            "timestamp": "string|sometimes|max:30",
            "comment": "string|required|min:10",
            "code": "integer|required|",
            "version": "float|sometimes|",
            "metadata": "object|sometimes|"
        }
    request_params = {
        "q": "educational courses on economics",
        "comment": "Im looking for an online course on economics.",
        "code": 100
    }
        
    def test_A_get_types(self):
        q = self.validation_rules["q"]
        q_type = q.split('|')[0]
        result = _get_types(q_type)
        self.assertEqual(result, str)

        code = self.validation_rules["code"]
        code_type = code.split('|')[0]
        result = _get_types(code_type)
        self.assertEqual(result, int)

        version = self.validation_rules["version"]
        version_type = version.split('|')[0]
        result = _get_types(version_type)
        self.assertEqual(result, float)

        metadata = self.validation_rules["metadata"]
        metadata_type = metadata.split('|')[0]
        result = _get_types(metadata_type)
        self.assertEqual(result, dict)

        not_real_type = "blah"
        result = _get_types(not_real_type)
        self.assertEqual(result, str)
    
    def test_B_parse_validation(self):
        # Test for success
        key = "q"
        value = self.validation_rules[key]
        result = _parse_validation_rule(key, value, self.request_params)
        self.assertTrue(result)

        # Test for failure
        request_params_copy = self.request_params.copy()
        request_params_copy["key"] = 100
        
        validation_rules_copy = self.validation_rules.copy()
        validation_rules_copy["key"] = "string|required|"

        key, value = 'key', "string|required|"
        with self.assertRaises(ValidationError, msg="key is not the expected type. Expected type: string, actual type: <class 'int'>"):
            _parse_validation_rule(key, value, request_params_copy)

    def test_C_operation(self):
        # Create a fail case
        request_params_copy = self.request_params.copy()
        request_params_copy["key"] = "string|required|"
        validation_rules_copy = self.validation_rules.copy()
        validation_rules_copy["key"] = 100
        # Test with callback without strict
        error_cb = Mock(return_value={ "message": "Error" })
        _operation(validation_rules_copy, request_params_copy, error_cb)
        error_cb.assert_called()
        # Test with callback with strict
        with self.assertRaises(ValidationError):
            _operation(validation_rules_copy, request_params_copy, None, True)
            error_cb.assert_not_called()
    
    def test_D_validate_decorator(self):
        req = Request()
        res = Response()
        @validate
        def test_case(req, res, next, validation_rules, parse_level):
            return "success"
        result = test_case(req=req, res=res, next=next, validation_rules=self.validation_rules, parse_level="query")
        self.assertIsNone(result)


    def test_E_validator(self):
        result = validator(self.validation_rules, self.request_params)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
    
