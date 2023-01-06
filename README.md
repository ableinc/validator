# Validrequest

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
        "names": "list|required|min:3",
        "code": "integer|required|"
    }
    try:
        validator(validation_rules, request_parameters)
    except ValidationError:
        return next({ "message": "The request parameters are not valid."})
    res.json({"message": "Validation successful."})
```
Refer to the ```demo.py``` file for further implementations.

## How to Install


```bash
python -m pip install validrequest
```
or

```bash
python -m pip install git+https://github.com/ableinc/validrequest.git
```

## Contributions

This library was designed and inspired by [Jacob Lucas](https://gitlab.com/Jlucas87). Validator is a python rewrite of the original nodeJS library.
