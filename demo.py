from lib import validate, validator, ValidationError
import json

def get_validation_rules():
    return {
        "q": "string|required|max:100",
        "timestamp": "string|sometimes|max:30",
        "comment": "string|required|min:10",
        "code": "integer|required|",
        "version": "float|sometimes|"
    }


@validate
def request(req, res, next, validation_rules, parse_level, strict=False):
    print('Validation successful.')


def request_two(req, res, next):
    validation_rules = get_validation_rules()
    request_parameters = req.query
    try:
        validator(validation_rules, request_parameters, strict=False)
    except ValidationError:
        return next({ "message": "The request parameters are not valid."})
    print("Validation successful.")



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


if __name__ == "__main__":
    # Example using the validate decorator
    # next is your error handler callback (similar to Express.js)
    request(req=Request(), res=Response(), next=next, validation_rules=get_validation_rules(), parse_level="query")

    # Example using the validator function
    request_two(req=Request(), res=Response(), next=next)

    # Note: strict=True will test against required and sometimes fields. By default strict is False.

