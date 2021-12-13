from pysj import flatten


def test_basic_nested_list():

    assert flatten([[1, 2, 3], [4, 5, 6]]) == [1, 2, 3, 4, 5, 6]


def test_nested_list_with_different_types():

    assert flatten(
        [[(1.3, 3.0), "string", "another string"], [4, 5e2, sorted({"a", "b", "c"})]]
    ) == [1.3, 3.0, "string", "another string", 4, 5e2, "a", "b", "c"]


def test_already_flat_input():

    flat_input = [8, 7, 6, 5, 4, 3, 2, 1]
    assert flatten(flat_input) == flat_input
