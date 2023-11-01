import sys
sys.path.append('.')
import unittest
from unittest.mock import Mock
from lib.validator import _get_types, _validate_against_rules, _operation, validate, validator
from lib.exceptions import ValidationError
import json
from typing import Dict, Any


class Response:
    def __init__(self):
        pass
    def text(self, content) -> Any:
        return content
    def json(self, content) -> Any:
        return content


class Request:
    def __init__(self):
        self.body = {
            "q": "educational courses on economics",
            "comment": "Im looking for an online course on economics.",
            "code": 100
        }
        self.query = {}
        self.params = {}


def next(message, status=400) -> None:
    message = {"error": message, "statusCode": status}
    response = json.dumps(message)
    print(response)


class ValidatorTest(unittest.TestCase):
    validation_rules: Dict[str, str] = {
            "q": "string|required|max:100",
            "timestamp": "string|sometimes|max:30",
            "comment": "string|required|min:1|max:3000",
            "code": "integer|required",
            "version": "float|sometimes",
            "metadata": "object|sometimes"
        }
    request_params: Dict[str, Any] = {
        "q": "educational courses on economics",
        "comment": "Im looking for an online course on economics.",
        "code": 100
    }
        
    def test_A_get_types(self) -> None:
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
        with self.assertRaises(ValidationError, msg=f"Unknown type provided: {not_real_type}"):
            _get_types(not_real_type)
    
    def test_B_parse_validation(self) -> None:
        # Test for success
        key = "q"
        rules = self.validation_rules[key]
        self.assertIsNone(_validate_against_rules(key, rules, self.request_params))

        # Test for failure
        request_params_copy = self.request_params.copy()
        request_params_copy["key"] = 100
        
        validation_rules_copy = self.validation_rules.copy()
        validation_rules_copy["key"] = "string|required"

        key, value = 'key', "string|required"
        with self.assertRaises(ValidationError, msg="key is not the expected type. Expected type: string, actual type: <class 'int'>"):
            _validate_against_rules(key, value, request_params_copy)

    def test_C_operation(self) -> None:
        # Create a fail case
        validation_rules_copy = self.validation_rules.copy()
        validation_rules_copy["metadata"] = "object|required"
        error_cb = Mock(return_value=None)
        # Test with callback
        with self.assertRaises(ValidationError, msg="metadata is required, but was not provided."):
            _operation(validation_rules_copy, self.request_params)
            error_cb.assert_not_called()
    
    def test_D_validate_decorator(self) -> None:
        req = Request()
        res = Response()
        @validate
        def test_case(req, res, next, validation_rules, payload_level):
            return "success"
        result = test_case(req=req, res=res, next=next, validation_rules=self.validation_rules, payload_level="query")
        self.assertIsNone(result)

    def test_E_validator(self):
        result = validator(self.validation_rules, self.request_params)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
    
