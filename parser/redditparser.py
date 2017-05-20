#!/usr/bin/env python

import praw

from database.meme import Meme
from database.meme import Site
from util import collectionutils


class RedditParser:
    # TODO use single configuration for test and production?
    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        self.memeeconomy = self.reddit.subreddit('MemeEconomy')

    def find_dank_memes_from_hot(self):
        return self.apply_filter(self.parse_dank_memes(self.memeeconomy.hot(limit=50)))

    def find_dank_memes_from_rising(self):
        return self.apply_filter(self.parse_dank_memes(self.memeeconomy.rising(limit=50)))

    def find_dank_memes_from_new(self):
        return self.apply_filter(self.parse_dank_memes(self.memeeconomy.new(limit=50)))

    def parse_dank_memes(self, listing):
        meme_map = dict()

        for submission in listing:
            meme = Meme(post_id=submission.id, site=Site.REDDIT, text=submission.title, media_url=submission.url)
            meme_map.update({meme: submission.score})

        return meme_map

    def apply_filter(self, meme_map):
        filtered_memes = set()
        for key, value in meme_map.iteritems():

            url_allowed = Rules.url_allowed(key.media_url)
            if not url_allowed:
                continue

            should_copy = Rules.should_be_copied(key.text, value)
            if not should_copy:
                continue

            filtered_memes.add(key)

        return filtered_memes


class Rules:
    def __init__(self):
        pass

    __KEYWORDS = [
        list(['buy', 'buy', 'buy']),
        list(['buy', 'buy', 'buy!!!']),
        list(['invest', 'invest', 'invest']),
        list(['high profit']),
        list(['buy quick', 'sell quick']),
        list(['great potential', 'buy'])
    ]

    __BAD_KEYWORDS = [
        list(['sell', 'sell', 'sell']),
        list(['invest', 'worthy', '?']),
        list(['should', 'i', 'invest']),
        list(['could', 'i', 'get']),
        list(['what', 'do', 'you']),
        list(['is', 'worth', 'anything']),
        list(['safe', 'investment', '?'])
    ]

    @staticmethod
    def should_be_copied(title, score):
        if score >= 500:
            return True
        else:
            words = list(title.lower().split(' '))
            good_keywords = Rules.__match_to_keywords(words, Rules.__KEYWORDS)
            bad_keywords = Rules.__match_to_keywords(words, Rules.__BAD_KEYWORDS)
            return good_keywords and not bad_keywords

    @staticmethod
    def __match_to_keywords(words, validation_keywords):
        for keywords in validation_keywords:
            if collectionutils.sublist(keywords, words):
                return True

        return False

    @staticmethod
    def url_allowed(url):
        if 'i.redd.it' in url:
            return True
        elif 'i.imgur.com' in url:
            return True
        return False
