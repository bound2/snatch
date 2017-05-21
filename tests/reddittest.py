#!/usr/bin/env python
import unittest
import mock
from testhelper import mock_reddit_data
from parser.redditparser import RedditParser
from parser.redditparser import Rules


class RedditTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._reddit_parser = RedditParser()

    @mock.patch('__main__.RedditParser._parse_dank_memes', return_value=mock_reddit_data())
    def test_parser_filtering(self, meme_mock):
        assert len(self._reddit_parser.find_dank_memes_hot()) == 10
        assert len(self._reddit_parser.find_dank_memes_new()) == 10
        assert len(self._reddit_parser.find_dank_memes_rising()) == 10
        assert len(mock_reddit_data()) == 40

    @mock.patch('__main__.Rules.url_allowed', return_value=True)
    @mock.patch('__main__.Rules.should_be_copied', return_value=True)
    def test_pagination(self, url_mock, copy_mock):
        self._reddit_parser.fetch_limit = 10
        self._reddit_parser.max_fetch_count = 30
        assert len(self._reddit_parser.find_dank_memes_hot()) == 30
        self._reddit_parser.fetch_limit = 10
        self._reddit_parser.max_fetch_count = 20
        assert len(self._reddit_parser.find_dank_memes_new()) == 20


if __name__ == '__main__':
    unittest.main()
