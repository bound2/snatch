from pymongo import ASCENDING
from meme import Meme
from util.jsonutils import collection_to_json
from util.jsonutils import to_json
from util.jsonutils import from_json


class MemeDao:
    def __init__(self, config):
        self._client = config.client
        self._db = config.db
        self._table = self._db.meme
        self._table.create_index([("post_id", ASCENDING), ("site", ASCENDING)], unique=True)
        self._table.create_index([("media_url", ASCENDING)], unique=True)

    # -------------------------- CREATE OPERATIONS --------------------------#
    def insert_one(self, data):
        return self._table.insert_one(from_json(to_json(data)))

    def insert_many(self, data):
        return self._table.insert_many(from_json(collection_to_json(data)))

    # -------------------------- READ OPERATIONS --------------------------#
    def find_by_id(self, post_id, site):
        cursor = self._table.find({'post_id': post_id, 'site': site})
        memes = self._parse_find_result(cursor)
        try:
            return memes.pop()
        except Exception:
            return None

    def find_by_site(self, site):
        cursor = self._table.find({'site': site})
        return self._parse_find_result(cursor)

    def find_non_processed(self):
        cursor = self._table.find({'processed': False})
        return self._parse_find_result(cursor)

    def find_processed(self):
        cursor = self._table.find({'processed': True})
        return self._parse_find_result(cursor)

    def _parse_find_result(self, cursor):
        memes = set()
        for record in cursor:
            meme = Meme(record.get('post_id'), record.get('site'),
                        record.get('text'), record.get('media_url'),
                        record.get('processed'))
            memes.add(meme)
        return memes

    # -------------------------- UPDATE OPERATIONS --------------------------#
    def mark_meme_processed(self, post_id):
        self._table.update_one(
            {'post_id': post_id},
            {'$set': {'processed': True}}
        )

    # -------------------------- DELETE OPERATIONS --------------------------#
    def delete_many(self, site):
        return self._table.delete_many({'site': site}).deleted_count

    def delete_all(self):
        return self._table.delete_many({}).deleted_count
