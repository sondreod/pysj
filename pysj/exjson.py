import json
from functools import partial

from pysj import ExtendedJSONDecoder, ExtendedJSONEncoder

dump = partial(json.dump, cls=ExtendedJSONEncoder)
dumps = partial(json.dumps, cls=ExtendedJSONEncoder)

load = partial(json.load, cls=ExtendedJSONDecoder)
loads = partial(json.loads, cls=ExtendedJSONDecoder)
