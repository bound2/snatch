#!/usr/bin/env python
import unittest
import mock
from testhelper import mock_reddit_data
from parser.redditparser import RedditParser


class RedditTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._reddit_parser = RedditParser()

    @mock.patch('__main__.RedditParser._parse_dank_memes', return_value=mock_reddit_data())
    def test_parser(self, meme_mock):
        # Test filteration of the memes
        assert len(self._reddit_parser.find_dank_memes_hot()) == 10
        assert len(self._reddit_parser.find_dank_memes_new()) == 10
        assert len(self._reddit_parser.find_dank_memes_rising()) == 10
        assert len(mock_reddit_data()) == 40


if __name__ == '__main__':
    unittest.main()
