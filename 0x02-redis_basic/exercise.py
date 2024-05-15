#!/usr/bin/env python3
"""
a module for a Redis-based cache system
with call counting and history tracking.
"""

import uuid
from typing import Union, Callable, Optional
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """
    decorator to count the number of times a method is called.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The wrapped method with call count functionality.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function to increment the call
        count in Redis and call the original method.
        Args:
            self: The instance the method is bound to.
            *args: Positional arguments to the method.
            **kwargs: Keyword arguments to the method.
        Returns:
            The result of the original method call.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    decorator to store the history of inputs
    and outputs of method calls in Redis.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The wrapped method with call history functionality.
    """
    inkey = method.__qualname__ + ":inputs"
    outkey = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function to store inputs and outputs
        of the method in Redis and call the original method.
        Args:
            self: The instance the method is bound to.
            *args: Positional arguments to the method.
            **kwargs: Keyword arguments to the method.
        Returns:
            The result of the original method call.
        """
        self._redis.rpush(inkey, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(outkey, str(res))
        return res

    return wrapper


def replay(method: Callable) -> None:
    """
    function to display the history of calls to a decorated method.
    Args:
        method (Callable): The method that displays the history.
    """
    in_key = "{}:inputs".format(method.__qualname__)
    out_key = "{}:outputs".format(method.__qualname__)

    inputs = method.__self__._redis.lrange(in_key, 0, -1)
    outputs = method.__self__._redis.lrange(out_key, 0, -1)

    print("{} was called {} times:".format(method.__qualname__, len(inputs)))
    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                method.__qualname__, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


class Cache:
    """
    cache class to interact with a Redis
    database for storing and retrieving data.
    Methods:
        store: Stores data in the cache and returns a unique key.
        get: Retrieves data from the cache using a key.
        get_str: Retrieves data as a string.
        get_int: Retrieves data as an integer.
    """

    def __init__(self):
        """
        initialize the Cache instance and clear the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data in the cache and return a unique key.
        Args:
            data (Union[str, bytes, int, float]): the cache stored data.
        Returns:
            str: The unique key associated with the stored data.
        """
        keyx = str(uuid.uuid4())
        self._redis.set(keyx, data)
        return keyx

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        retrieve data from the cache using a key, optionally
        applying a transformation function.
        Args:
            key (str): The key to look up in the cache.
            fn (Optional[Callable]): a function to apply to the retrieved data.
        Returns:
            Union[str, bytes, int, float]: The retrieved data.
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        retrieve data from the cache as a string.
        Args:
            key (str): The key to look up in the cache.
        Returns:
            str: The retrieved data as a string.
        """
        return self.get(key, fn=str)

    def get_int(self, key: str) -> int:
        """
        retrieve data from the cache as an integer.
        Args:
            key (str): The key to look up in the cache.
        Returns:
            int: The retrieved data as an integer.
        """
        return self.get(key, fn=int)
