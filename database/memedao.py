#!/usr/bin/env python

from pymongo import MongoClient


class MemeDao:
    def __init__(self):
        self.__client = MongoClient()
        self.__db = self.__client.test
        self.__table = self.__db.meme

    def insert_one(self, data):
        return self.__table.insert_one(data)
