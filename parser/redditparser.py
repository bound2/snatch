#!/usr/bin/env python

import praw

from database.meme import Meme
from database.meme import Site
from util import collectionutils


class RedditParser:
    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        self.memeeconomy = self.reddit.subreddit('MemeEconomy')

    def find_dank_memes_from_hot(self):
        return RedditParser.__find_dank_memes(self.memeeconomy.hot(limit=50))

    def find_dank_memes_from_rising(self):
        return RedditParser.__find_dank_memes(self.memeeconomy.rising(limit=50))

    def find_dank_memes_from_new(self):
        return RedditParser.__find_dank_memes(self.memeeconomy.new(limit=50))

    @staticmethod
    def __find_dank_memes(listing):
        memes = set()

        for submission in listing:
            url_allowed = Rules.url_allowed(submission.url)
            if not url_allowed:
                continue

            should_copy = Rules.should_be_copied(submission.title, submission.score)
            if not should_copy:
                continue

            memes.add(Meme(id=submission.id, site=Site.REDDIT, text=submission.title, media_url=submission.url))

        return memes


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
