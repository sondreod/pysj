import pytest
from pysj import paginate



def test_paginated():
    i = 0
    get_url = paginate("lol.lol?offset=OFFSET&pagesize=PAGESIZE", max_num_requests=2)

    data = None
    while url := get_url(data):
        i += 1
        print(url)