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
