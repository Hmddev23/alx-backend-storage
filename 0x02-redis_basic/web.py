#!/usr/bin/env python3
"""
a module for fetching web pages with request
counting and caching using Redis.
"""

import requests
from functools import wraps
from typing import Callable
import redis

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    decorator to count the number of requests
    made to a URL and cache the response.
    Args:
        method (Callable): The method to be decorated.
    Returns:
        Callable: The wrapped method with request counting.
    """
    @wraps(method)
    def wrapper(url):
        """
        wrapper function to increment the request
        count, check cache, and fetch the page if not cached.
        Args:
            url (str): The URL of the page to fetch.
        Returns:
            str: The HTML content of the page.
        """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html

        return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    fetch the HTML content of a page from the specified URL.
    Args:
        url (str): The URL of the page to fetch.
    Returns:
        str: The HTML content of the page.
    """
    req = requests.get(url)
    return req.text
