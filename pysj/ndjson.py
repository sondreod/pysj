import json
from functools import partial

from pysj import NDJSONDecoder, NDJSONEncoder

dump = partial(json.dump, cls=NDJSONEncoder)
dumps = partial(json.dumps, cls=NDJSONEncoder)

load = partial(json.load, cls=NDJSONDecoder)
loads = partial(json.loads, cls=NDJSONDecoder)
