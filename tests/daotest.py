#!/usr/bin/env python
import unittest
import mock
from reddittest import mock_reddit_data
from parser.redditparser import RedditParser
from database.memedao import MemeDao


class DaoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._reddit_parser = RedditParser()
        cls._meme_dao = MemeDao()

    @mock.patch('__main__.RedditParser.find_dank_memes', return_value=mock_reddit_data())
    def test_insert_many(self, meme_mock):
        memes = self._reddit_parser.find_dank_memes_from_hot()
        ids = self._meme_dao.insert_many(memes).inserted_ids
        assert len(ids) == 10

    @mock.patch('__main__.RedditParser.find_dank_memes', return_value=mock_reddit_data())
    def test_insert_one_read_one(self, meme_mock):
        meme_to_save = self._reddit_parser.find_dank_memes_from_hot().pop()
        result = self._meme_dao.insert_one(meme_to_save)
        assert result.inserted_id is not None

        # check that it was saved and is accessible from database
        meme_loaded = self._meme_dao.find_by_id(meme_to_save.id, 'reddit')
        assert meme_loaded.id == meme_to_save.id
        assert meme_loaded.site == meme_to_save.site
        assert meme_loaded.media_url == meme_to_save.media_url
        assert meme_loaded.text == meme_to_save.text

    #TODO index duplicate test



if __name__ == '__main__':
    unittest.main()
