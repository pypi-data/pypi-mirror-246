import pytest


def obj_max(objs, attr):
    assert isinstance(objs, list)
    return max(objs, key=lambda x: getattr(x, attr))


def obj_min(objs, attr):
    assert isinstance(objs, list)
    return min(objs, key=lambda x: getattr(x, attr))


def delete_keys_from_dict(d, to_delete):
    if isinstance(to_delete, str):
        to_delete = [to_delete]
    if isinstance(d, dict):
        for single_to_delete in set(to_delete):
            if single_to_delete in d:
                del d[single_to_delete]
        for _, v in d.items():
            delete_keys_from_dict(v, to_delete)
    elif isinstance(d, list):
        for i in d:
            delete_keys_from_dict(i, to_delete)


################################################################################
# TESTS
################################################################################


class Dummy:
    def __init__(self, attr):
        self.attr = attr


def test_obj_max():
    objs = [
        Dummy(i) for i in range(10)
    ]  # Creates a list of Dummy objects with attrs 0 through 9.
    assert (
        obj_max(objs, "attr").attr == 9
    )  # The maximum should be the last object, with attr == 9.


def test_obj_min():
    objs = [
        Dummy(i) for i in range(10)
    ]  # Creates a list of Dummy objects with attrs 0 through 9.
    assert (
        obj_min(objs, "attr").attr == 0
    )  # The minimum should be the first object, with attr == 0.


def test_obj_max_empty():
    objs = []  # An empty list.
    with pytest.raises(ValueError):
        obj_max(objs, "attr")


def test_obj_min_empty():
    objs = []  # An empty list.
    with pytest.raises(ValueError):
        obj_min(objs, "attr")


@pytest.mark.parametrize(
    "input_dict,keys_to_delete,expected_output",
    [
        ({"a": 1, "b": 2, "c": 3}, "a", {"b": 2, "c": 3}),
        ({"a": 1, "b": 2, "c": 3}, ["a", "b"], {"c": 3}),
        ({"a": 1, "b": {"c": 2, "d": 3}}, "c", {"a": 1, "b": {"d": 3}}),
        ({"a": 1, "b": {"c": 2, "d": 3}}, ["c", "d"], {"a": 1, "b": {}}),
        ({"a": 1, "b": [{"c": 2}, {"d": 3}]}, "c", {"a": 1, "b": [{}, {"d": 3}]}),
    ],
)
def test_delete_keys_from_dict(input_dict, keys_to_delete, expected_output):
    delete_keys_from_dict(input_dict, keys_to_delete)
    assert input_dict == expected_output
