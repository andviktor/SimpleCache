import datetime
import time
from pprint import pprint
from typing import Any


class CacheValue:

    def __init__(self, value) -> None:
        self._value: Any = value
        self._created_at: datetime = datetime.datetime.now()


class Cache:
    """
    Cache of values in a hash table style.

    Raises a KeyError if attempting to retrieve data that does not exist in the cache.
    """

    def __init__(self, ttl: int = 3600, clean_timeout: int = 60) -> None:
        self.__ttl = ttl
        self.__values = dict()
        self.__last_clean = datetime.datetime.now()
        self.__clean_timeout = clean_timeout

    def __getitem__(self, name: str) -> Any:

        if datetime.datetime.now() > (
            self.__last_clean + datetime.timedelta(seconds=self.__clean_timeout)
        ):
            self.__clean_by_timeout()

        if name in self.__values:
            if datetime.datetime.now() >= (
                self.__values[name]._created_at + datetime.timedelta(seconds=self.__ttl)
            ):
                self.__values.pop(name)
                raise KeyError('Data with key "{}" has expired.'.format(name))
            else:
                return self.__values[name]._value
        else:
            raise KeyError('No data with key "{}" in the cache.'.format(name))

    def __setitem__(self, name: str, value: Any):
        self.__values[name] = CacheValue(value)

    def __clean_by_timeout(self) -> None:
        for key in list(self.__values.keys()):
            if datetime.datetime.now() >= (
                self.__values[key]._created_at + datetime.timedelta(seconds=self.__ttl)
            ):
                del self.__values[key]

    def print(self, width: int = 1) -> None:
        values = {key: self.__values[key]._value for key in self.__values}
        pprint(values, width=width)

    def size(self) -> int:
        return len(self.__values)


# Self-testing if the module lauched directly
if __name__ == "__main__":
    print("CACHE SELF-TESTING:")
    print("=== 1 step: creating new Cache object with TTL 5 seconds ===")
    try:
        cache = Cache(ttl=5, clean_timeout=1)
    except Exception as e:
        print("Error on 1 step: {}".format(e))

    print("=== 2 step: storing first value and waiting 2 seconds ===")
    try:
        cache["one"] = 1
        cache.print()
    except Exception as e:
        print("Error on 2 step: {}".format(e))

    print("=== 3 step: storing second value ===")
    time.sleep(2)
    try:
        cache["two"] = 2
        cache.print()
    except Exception as e:
        print("Error on 3 step: {}".format(e))

    print(
        '=== 4 step: first value has expired, check that the cache contains only value "two" ==='
    )
    time.sleep(3)
    try:
        _ = cache[0]
    except Exception:
        pass
    cache.print()
    assert cache.size() == 1, "TEST failed: Cache size must be 1"

    print("=== 4 step: second value has expired, check that the cache is empty ===")
    time.sleep(3)
    try:
        _ = cache[0]
    except Exception:
        pass
    cache.print()
    assert cache.size() == 0, "TEST failed: Cache size must be 0"

    print("SELF TESTING COMPLETED.")
