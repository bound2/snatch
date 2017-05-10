#!/usr/bin/env python
import unittest
import mock
from testhelper import mock_reddit_data
from parser.redditparser import RedditParser


class RedditTest(unittest.TestCase):

    @mock.patch('__main__.RedditParser.find_dank_memes', return_value=mock_reddit_data())
    def test_parser(self, meme_mock):
        reddit_parser = RedditParser()
        # Test filteration of the memes
        assert len(reddit_parser.find_dank_memes_from_hot()) == 10
        assert len(reddit_parser.find_dank_memes_from_new()) == 10
        assert len(reddit_parser.find_dank_memes_from_rising()) == 10
        assert len(mock_reddit_data()) == 40


if __name__ == '__main__':
    unittest.main()
