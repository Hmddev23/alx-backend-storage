#!/usr/bin/env python3
"""
list all documents in a MongoDB collection.
"""


def list_all(mongo_collection):
    """
    retrieve all documents from the collection.
    Parameters:
    - mongo_collection: The MongoDB collection.

    Returns:
    - list: list containing all documents from the collection.
    """
    return list(mongo_collection.find())
