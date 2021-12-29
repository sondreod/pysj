# Pysj

This package contains utils, classes and helper functions I find myself reimplementing in several projects. As of now all functions are importable from the top level module.

The name is a commonly used shortened version of the Norwegian word "pysjamas" (in english: pajamas/pyjamas).
Coding in your pysjamas/pajamas/pyjamas is comfortable. This package is an attempt to make Python development a bit more comfortable as well.

This is an ongoing project and so far just a few functions are implemented. Most time  have been spent on project structure, tests and packaging.


### Installation
```bash
pip install pysj
```
### Usage
```python
from pysj import sha256, ExtendedJSONEncoder

# Simple hashing
print(sha256("test"))

# JSON Encoder converting datetime to ISO format
json.dumps(
    {
        "timestamp": datetime.datetime.fromisoformat("2021-12-01T04:50:00.123456")
    },
    cls=ExtendedJSONEncoder,
)
```

### API Overview
Public classes and functions are importable from the top level package.

## Classes
__`ExtendedJSONEncoder`__
Subclass for `json.JSONEncoder` making encoding of datetime and numpy arrays work.

__`ExtendedJSONDecoder`__
Not finished: Subclass for `json.JSONDecoder` making decoding of datetime and work.


## Functions
__`flatten`__
Recursively flattens an iterable (depth first)

__`seconds`__
Returns the number of seconds in the given time intervals combined, rounded down to nearest integer.

__`sha256`__
Returns the hexdigest representation of the sha256 hash from the plaintext input

__`sha1`__
Returns the hexdigest representation of the sha1 hash from the plaintext input

__`md5`__
Returns the hexdigest representation of the md5 hash from the plaintext input

__`uuid`__
Returns the hex representation of a uuid4 as string