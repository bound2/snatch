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

    def find_by_id(self, id, site):
        cursor = self.__table.find({'id': id, 'site': site})
        for record in cursor:
            meme = Meme(record.get('id'), record.get('site'), record.get('text'), record.get('media_url'))
            return meme
        return None

    def find_by_site(self, site):
        return self.__table.find({'site': site})
