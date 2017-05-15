#!/usr/bin/env python
import unittest
import mock
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
        self._meme_dao.insert_many(self._reddit_parser.find_dank_memes_from_new())
        # 10 length due to duplicate objects being returned by find_dank_memes
        assert len(self._meme_dao.find_by_site(Site.REDDIT)) == 10

    def test_unique_index(self):
        self._meme_dao.delete_all()
        #meme = Meme()

if __name__ == '__main__':
    unittest.main()
