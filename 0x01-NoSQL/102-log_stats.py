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


def print_present_ips(server_collection):
    """
    print the top 10 HTTP IPs in a collection.
    """
    print('IPs:')
    req_logs = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for req_log in req_logs:
        ip = req_log['_id']
        ip_requests_count = req_log['totalRequests']
        print('\t{}: {}'.format(ip, ip_requests_count))


def run():
    """
    provide some stats about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    get_nginx_stats(client.logs.nginx)
    print_present_ips(client.logs.nginx)


if __name__ == '__main__':
    run()
