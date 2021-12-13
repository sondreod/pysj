# Pysj

Pysj makes Python development more comfortable.

This package contains utils, classes and helper
functions I find myself reimplementing in several projects.

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