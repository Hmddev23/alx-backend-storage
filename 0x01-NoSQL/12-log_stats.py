#!/usr/bin/env python3
"""
provide some stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def get_nginx_stats(collection):
    """
    print stats about Nginx request logs.
    """
    print('{} logs'.format(collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_count))
    status_counter = len(list(
        collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_counter))


def run():
    """
    provide some stats about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    get_nginx_stats(client.logs.nginx)


if __name__ == '__main__':
    run()
