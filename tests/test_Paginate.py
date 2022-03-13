from pysj import paginate


def test_paginated():
    i = 0
    get_url = paginate(
        "lol.lol?offset=OFFSET&pagesize=PAGESIZE", max_num_requests=20, start_one=False
    )

    data = None
    while url := get_url(data):
        i += 1
        if i < 10:
            data = {"valid": i}
        print(url)
