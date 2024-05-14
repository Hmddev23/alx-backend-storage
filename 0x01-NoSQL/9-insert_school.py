#!/usr/bin/env python3
"""
insert a school document into a MongoDB collection.
"""

def insert_school(mongo_collection, **kwargs):
    """
    insert a school document into MongoDB collection.
    Parameters:
    - mongo_collection: The MongoDB collection.
    - **kwargs: the fields and values of the school document.
    Returns:
    - ObjectId: The ObjectId of the inserted document.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
