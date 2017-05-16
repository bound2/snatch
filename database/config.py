from pymongo import MongoClient


class _Configuration:
    def __init__(self, client, db):
        self.client = client
        self.db = db


class TestConfiguration(_Configuration):
    def __init__(self):
        client = MongoClient()
        db = client.test
        _Configuration.__init__(self, client, db)


class ProductionConfiguration(_Configuration):
    def __init__(self):
        client = MongoClient()
        db = client.production
        _Configuration.__init__(self, client, db)
