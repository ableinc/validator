# Validator

This is a request handler validation tool for RESTful API endpoints.

## How To Use

```python
from validator import validator, ValidationError

def request_handler(req, res, next):
    # If you're familiar with Express.js req, res, next should be understood
    validation_rules = get_validation_rules()
    request_parameters = req.query
    validation_rules = {
        "q": "string|required|max:100",
        "timestamp": "string|sometimes|max:30",
        "comment": "string|required|min:10",
        "code": "integer|required|"
    }
    try:
        validator(validation_rules, request_parameters)
    except ValidationError:
        return next({ "message": "The request parameters are not valid."})
    res.json({"message": "Validation successful."})
```
Refer to the ```demo.py``` file for further implementations.

## How to Instal

As of now the validator tool is not in the Python Package repository (PyPi). You can still pip install the git repo.

```bash
python -m pip install git+https://github.com/ableinc/validator.git
```

## Contributions

This library was designed and inspired by [Jacob Lucas](gitlab.com/Jlucas87). Validator is a python rewrite of the original nodeJS library.
