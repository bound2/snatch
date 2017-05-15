#!/usr/bin/env python
import unittest
import mock
from pymongo.errors import DuplicateKeyError
from reddittest import mock_reddit_data
from parser.redditparser import RedditParser
from parser.redditparser import Site
from database.memedao import MemeDao
from database.meme import Meme


class DaoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._reddit_parser = RedditParser()
        cls._meme_dao = MemeDao()

    @classmethod
    def tearDownClass(cls):
        cls._meme_dao.delete_all()

    @mock.patch('__main__.RedditParser.find_dank_memes', return_value=mock_reddit_data())
    def test_insert_many_delete_many(self, meme_mock):
        self._meme_dao.delete_all()
        memes = self._reddit_parser.find_dank_memes_from_hot()
        ids = self._meme_dao.insert_many(memes).inserted_ids
        assert len(ids) == 10
        assert self._meme_dao.delete_all() == 10

    @mock.patch('__main__.RedditParser.find_dank_memes', return_value=mock_reddit_data())
    def test_insert_one_read_one(self, meme_mock):
        self._meme_dao.delete_all()
        meme_to_save = self._reddit_parser.find_dank_memes_from_hot().pop()
        result = self._meme_dao.insert_one(meme_to_save)
        assert result.inserted_id is not None

        # check that it was saved and is accessible from database
        meme_loaded = self._meme_dao.find_by_id(meme_to_save.post_id, 'reddit')
        assert meme_loaded.post_id == meme_to_save.post_id
        assert meme_loaded.site == meme_to_save.site
        assert meme_loaded.media_url == meme_to_save.media_url
        assert meme_loaded.text == meme_to_save.text

    @mock.patch('__main__.RedditParser.find_dank_memes', return_value=mock_reddit_data())
    def test_find_by_site(self, meme_mock):
        self._meme_dao.delete_all()
        self._meme_dao.insert_many(self._reddit_parser.find_dank_memes_from_hot())
        assert len(self._meme_dao.find_by_site(Site.REDDIT)) == 10

    def test_unique_index_success(self):
        self._meme_dao.delete_all()
        # same post_id, same site
        meme1 = Meme(post_id='berlin55', site=Site.REDDIT, text='Crossover fidget memes on the rise! BUY BUY BUY',
                     media_url='https://i.redd.it/xi7s8hwcsowy.jpg')
        meme2 = Meme(post_id='berlin55', site=Site.REDDIT, text='POPE MEMES ON THE RISE!!! BUY BUY BUY NOW',
                     media_url='https://i.redd.it/lkgqkz3etkwy.jpg')
        self._meme_dao.insert_one(meme1)
        with self.assertRaises(DuplicateKeyError) as context:
            self._meme_dao.insert_one(meme2)
        assert 'duplicate key error collection: test.meme index: post_id_1_site_1 dup key: { : "berlin55", : "reddit" }' in str(context.exception)
        assert len(self._meme_dao.find_by_site(Site.REDDIT)) == 1

    def test_unique_index_not_used(self):
        self._meme_dao.delete_all()
        # same post_id, different site
        meme1 = Meme(post_id='paris47', site='reddit', text='Crossover fidget memes on the rise! BUY BUY BUY',
                     media_url='https://i.redd.it/xi7s8hwcsowy.jpg')
        meme2 = Meme(post_id='paris47', site='lulztech', text='POPE MEMES ON THE RISE!!! BUY BUY BUY NOW',
                     media_url='https://i.redd.it/lkgqkz3etkwy.jpg')
        self._meme_dao.insert_one(meme1)
        self._meme_dao.insert_one(meme2)
        assert len(self._meme_dao.find_by_site('reddit')) == 1
        assert len(self._meme_dao.find_by_site('lulztech')) == 1


if __name__ == '__main__':
    unittest.main()
