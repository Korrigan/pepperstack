"""
Interface for mongodb using pymongo
Provides a simple function get_connection() which rely on different settings

"""

import pymongo


def get_connection():
    """
    Returns a pymongo.Database object representing the mongodb connection

    """
    c = pymongo.MongoClient('127.0.0.1')
    return c['si']
