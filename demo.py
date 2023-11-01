import sys
sys.path.append('.')
from lib import validate, validator, ValidationError
import json
from typing import Dict, Any, Callable
from datetime import datetime


class Response:
    def __init__(self):
        self.status_code = 200
    def status(self, status_code: int):
        self.status_code = status_code
        return self
    def send(self, content):
        return content
    def json(self, content: Dict[str, Any]):
        return json.dumps(content)
    
    
class Request:
    def __init__(self):
        self.body = {
            "q": "educational courses on economics",
            "timestamp": datetime.now().timestamp(),  # this will be 16 digits long
            "comment": "Im looking for an online course on economics.",
            "code": 100,
            "metadata": { "username": "JohnDoe", "is_active": True },
            "timeSince": datetime.now().timestamp()
        }
        self.query = {}
        self.params = {}


def get_validation_rules():
    return {
        "q": "string|required|max:100",
        "timestamp": "float|sometimes|min:1|max:13",
        "comment": "string|required|min:10",
        "code": "integer|required",
        "version": "float|sometimes",
        "metadata": "dict|required",
        "timeSince": "number|required"
    }


@validate
def request_with_decorator(request: Request, response: Response, validation_rules: Dict[str, Any], next: Callable, payload_level: str):
    return response.status(200).send("Validation successful.")


def request_with_method(request: Request, response: Response, next: Callable):
    validation_rules = get_validation_rules()
    request_parameters = request.body
    try:
        validator(validation_rules, request_parameters)
        return response.status(200).send("Validation successful.")
    except ValidationError as e:
        return next({ "message": e })
    except Exception:
        return next({ "message": "Something else went wrong." })


def next(message, status=400):
    message["statusCode"] = status
    response = json.dumps(message)
    print('Error occurred:', response)


if __name__ == "__main__":
    # Example using the validate decorator
    # next is your error handler callback (similar to Express.js)
    response = request_with_decorator(request=Request(), response=Response(), next=next, validation_rules=get_validation_rules(), payload_level="body")
    print('Decorator response:', response)
    # Example using the validator function
    response = request_with_method(request=Request(), response=Response(), next=next)
    print('Request handler response:', response)
