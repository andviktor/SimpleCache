import pytest
import time
from cache import Cache


def test_cache_add_str_value():
    cache = Cache()
    cache["test"] = "string"
    assert cache["test"] == "string"


def test_cache_add_int_value():
    cache = Cache()
    cache["test"] = 1
    assert cache["test"] == 1


def test_cache_add_object_value():
    cache = Cache()
    test_object = [1, 2, 3, 4, 5]
    cache["test"] = test_object
    assert cache["test"] == [1, 2, 3, 4, 5]


def test_cache_add_multiple_values():
    cache = Cache()
    for i in range(10):
        value = "value #{}".format(i)
        cache[i] = value
        assert cache[i] == value


def test_cache_add_and_get_single_value():
    cache = Cache()
    cache["test"] = "test"
    assert cache["test"] == "test"


def test_cache_size():
    cache = Cache()
    for i in range(10):
        cache[i] = 0
    assert cache.size() == 10


def test_cache_clean_by_ttl_expired():
    cache = Cache(ttl=1)
    cache["test"] = "test"
    assert cache["test"] == "test"
    time.sleep(2)
    with pytest.raises(KeyError) as excinfo:
        _ = cache["test"]
    assert str(excinfo.value) == "'Data with key \"test\" has expired.'"


def test_cache_clean_by_clean_timeout():
    cache = Cache(ttl=5, clean_timeout=2)

    # time 0s: add first value, check size == 1
    cache["one"] = 1
    assert cache.size() == 1

    # time 1s: add second value, check size == 2
    time.sleep(2)
    cache["two"] = 2
    assert cache.size() == 2

    # time 2s: first value has expired, check size == 1
    time.sleep(3)
    try:
        _ = cache[0]
    except Exception:
        pass
    assert cache.size() == 1

    # time 3s: all values expired, check size == 0
    time.sleep(3)
    try:
        _ = cache[0]
    except Exception:
        pass
    assert cache.size() == 0


def test_cache_print(capfd):
    cache = Cache()
    for i in range(4):
        value = "value #{}".format(i)
        cache[i] = value
    cache.print(width=80)
    out, err = capfd.readouterr()
    assert out == "{0: 'value #0', 1: 'value #1', 2: 'value #2', 3: 'value #3'}\n"
