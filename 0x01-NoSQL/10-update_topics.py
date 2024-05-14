#!/usr/bin/env python3
"""
update topics for a document in a MongoDB collection.
"""

def update_topics(mongo_collection, name, topics):
    """
    Update the topics for a document with the given
    name in the specified MongoDB collection.
    Parameters:
    - mongo_collection: The MongoDB collection.
    - name (str): The name of the document to update.
    - topics (list): The list of topics to set for the document.
    Returns:
    - None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
