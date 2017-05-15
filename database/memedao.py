#!/usr/bin/env python

from pymongo import MongoClient
from meme import Meme
from util.jsonutils import collection_to_json
from util.jsonutils import to_json
from util.jsonutils import from_json


class MemeDao:
    def __init__(self):
        self._client = MongoClient()
        self._db = self._client.test
        self._table = self._db.meme

    def insert_one(self, data):
        return self._table.insert_one(from_json(to_json(data)))

    def insert_many(self, data):
        return self._table.insert_many(from_json(collection_to_json(data)))

    def find_by_id(self, id, site):
        cursor = self._table.find({'id': id, 'site': site})
        for record in cursor:
            meme = Meme(record.get('id'), record.get('site'), record.get('text'), record.get('media_url'))
            return meme
        return None

    def find_by_site(self, site):
        cursor = self._table.find({'site': site})
        memes = set()
        for record in cursor:
            meme = Meme(record.get('id'), record.get('site'), record.get('text'), record.get('media_url'))
            memes.add(meme)
        return memes

    def delete_many(self, site):
        return self._table.delete_many({'site': site}).deleted_count

    def delete_all(self):
        return self._table.delete_many({}).deleted_count
