#!/usr/bin/env python3
"""
print all students in a collection sorted by average score.
"""

def top_students(mongo_collection):
    """
    print all students in a collection sorted by average score.
    Parameters:
    - mongo_collection: The MongoDB collection containing student data.

    Returns:
    - pymongo.cursor.Cursor: the sorted list of students by average score.
    """
    students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return students
