#!/usr/bin/env python

import praw
import economyutils


class RedditParser:
    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        self.memeeconomy = self.reddit.subreddit('MemeEconomy')


class Rules:
    KEYWORDS = [
        list(['buy', 'buy', 'buy']),
        list(['buy', 'buy', 'buy!!!']),
        list(['invest', 'invest', 'invest']),
        list(['high profit']),
        list(['buy quick', 'sell quick']),
        list(['great potential', 'buy'])
    ]

    BAD_KEYWORDS = [
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
            good_keywords = Rules.match_to_keywords(words, Rules.KEYWORDS)
            bad_keywords = Rules.match_to_keywords(words, Rules.BAD_KEYWORDS)
            return good_keywords and not bad_keywords

    @staticmethod
    def match_to_keywords(words, validation_keywords):
        for keywords in validation_keywords:
            if economyutils.sublist(keywords, words):
                return True

        return False

    @staticmethod
    def url_allowed(url):
        if 'i.redd.it' in url:
            return True
        elif 'i.imgur.com' in url:
            return True
        return False


if __name__ == '__main__':
    reddit_parser = RedditParser()
    for submission in reddit_parser.memeeconomy.hot(limit=50):
        copy = Rules.should_be_copied(submission.title, submission.score)
        print('Title: ', submission.title)
        print('Score: ', submission.score)
        print('Copy: ', copy)
        print('Url: ', submission.url)
        print('Url allowed: ', Rules.url_allowed(submission.url))
        print('---------------------------------\n')
