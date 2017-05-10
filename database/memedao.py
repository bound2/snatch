#!/usr/bin/env python

from pymongo import MongoClient
from meme import Meme
from util.jsonutils import collection_to_json
from util.jsonutils import to_json
from util.jsonutils import from_json


class MemeDao:
    def __init__(self):
        self.__client = MongoClient()
        self.__db = self.__client.test
        self.__table = self.__db.meme

    def insert_one(self, data):
        return self.__table.insert_one(from_json(to_json(data)))

    def insert_many(self, data):
        return self.__table.insert_many(from_json(collection_to_json(data)))

    def find(self, id, site):
        result = self.__table.find({'id': id, 'site': site})
        meme = Meme(result.id, result.site, result.text, result.media_url)
        return meme

    def find_by_site(self, site):
        return self.__table.find({'site': site})
