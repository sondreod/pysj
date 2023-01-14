# Pysj

This package contains utils, classes and helper functions I find myself reimplementing in several projects. As of now all functions are importable from the top level module.

The name is a commonly used shortened version of the Norwegian word "pysjamas" (in english: pajamas/pyjamas).
Coding in your pysjamas/pajamas/pyjamas is comfortable. This package is an attempt to make Python development a bit more comfortable as well.

This is an ongoing project and so far just a few functions are implemented. Most time  have been spent on project structure, tests and packaging.


## Installation
```bash
pip install pysj
```

## Usage

### Importing
```python
# We import everything here for all of the examples
from pysj import (
    md5, 
    sha256,
    ExtendedJSONDecoder,
    ExtendedJSONEncoder,
    Timer,
    chunk,
    first,
    flatten,
    isotime,
    moving_average,
    n_wise,
    paginate,
    seconds,
    take,
    transpose
)
```


### Extended JSON encoding / decoding
```python
# Serializing to json with datetime objects
json.dumps(
    {
        "timestamp": datetime.datetime.fromisoformat("2021-12-01T04:50:00.123456")
    },
    cls=ExtendedJSONEncoder,
)

# and back again
json.loads('{"timestamp": "2021-12-01T04:50:00"}',
    cls=ExtendedJSONDecoder,
)
```

### Some functional stuff
#### Flatten
Flattens an iterable, depth first.
```python
>>> flatten([range(10), (1,2,3), "HELLO", [[["42"]], []], ["y0l0"]])
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 'HELLO', '42', 'y0l0']
```

#### First
Get first element of an iterable
```python
>>> first([1, 2, 3])
1
```

#### Take
Get first *n* elements from an iterable
```python
data = range(100)
>>> list(take(4, ))
[0, 1, 2, 3]
```

#### Chunk
Chunks an iterable into an iterable yield a list with *n* items at a time.

Takes an optional *fillvalue*, defaults to **None**,
```python
data = range(10)
>>> list(chunk(take(4, data, fillvalue=":D")))
[
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [9, 10, ":D", ":D"],
]
```

#### Transpose

```python
>>> transpose(
    [
        [1,2,3],
        [1,2,3],
        [1,2,3],
    ]
)
[
    [1, 1, 1],
    [2, 2, 2],
    [3, 3, 3]
]
```

#### N wise
Yields *n* items from data like a gliding window, as long as there is enough elements in data to yield the full window.

Like itertools.pairwise, but generalized to *n* items. (New in Python 3.10)
```python
>>> list(n_wise(3, [1,2,3,4,5]))
[(1,2,3), (2,3,4), (3,4,5)]
```


#### Moving average
```python
>>> list(moving_average(3, (1,2,3,4,5)))
[2.0, 3.0, 4.0]
```

### Other

#### Isotime
Returns an isoformated string of the current time (or supplied datetime *dt*) to the given *precision*, defaults to 'd' (day).

```python
>>>isotime()
'2023-01-01'

>>>isotime('s')
'2023-01-01T00:00:00'

>>>isotime('m', datetime(2022, 2, 2, 2, 2))
'2022-02-02T02:02'

# Only the first character of *precision* is used, so for readability you can write it out fully.
>>>isotime('minutes', datetime(2022, 2, 2, 2, 2))
'2022-02-02T02:02'
```

#### Stopwatch
```python
>>> with Timer():
>>>     # Do stuff
>>>     sleep(1)
Starting timer
Elapsed time 1.0007134879997466 s.
```

#### Simple hashing
```python
>>> print(sha256("test"))
9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
>>> print(md5("test"))
098f6bcd4621d373cade4e832627b4f6
```