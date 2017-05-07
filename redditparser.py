#!/usr/bin/env python

import praw
import economyutils


class RedditParser:
    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        self.memeeconomy = self.reddit.subreddit('MemeEconomy')

    def find_dank_memes_from_hot(self):
        memes = []

        for submission in self.memeeconomy.hot(limit = 50):
            url_allowed = Rules.url_allowed(submission.url)
            if not url_allowed:
                continue

            should_copy = Rules.should_be_copied(submission.title, submission.score)
            if not should_copy:
                continue

            memes.append(MemeDTO(submission.id, submission.title, submission.score, submission.url))

        return memes


class MemeDTO:
    def __init__(self, id, title, score, url):
        self.id = id
        self.title = title
        self.score = score
        self.url = url

    def __str__(self):
        return "id={:s}\ntitle={:s}\nscore={:s}\nurl={:s}\n".format(self.id, self.title, str(self.score), self.url)

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
    for meme in reddit_parser.find_dank_memes_from_hot():
        print str(meme)
