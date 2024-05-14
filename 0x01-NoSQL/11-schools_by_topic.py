#!/usr/bin/env python3
"""
retrieve data from a MongoDB collection.
"""

def schools_by_topic(mongo_collection, topic):
    """
    retrieve data from a collection.
    Parameters:
    - mongo_collection: The MongoDB collection.
    - topic (str): The topic to filter schools by.
    Returns:
    - pymongo.cursor.Cursor: A cursor containing data.
    """
    return mongo_collection.find({"topics": topic})
