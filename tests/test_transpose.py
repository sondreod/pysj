from pysj import transpose

test_data = [
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6],
]


def test_transpose():
    assert transpose(test_data) == list(
        map(lambda x: [x] * len(test_data[0]), range(1, len(test_data) + 1))
    )
