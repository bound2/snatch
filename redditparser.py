#!/usr/bin/env python

import praw

class RedditParser:

    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        self.memeeconomy = self.reddit.subreddit('MemeEconomy')

class Rules:

    KEYWORDS = [
        ["buy", "buy", "buy"],
        ["invest", "invest", "invest"],
        ["high profit"],
        ["buy quick", "sell quick"],
        ["great potential", "buy"]
    ]

    BAD_KEYWORDS = [
        ["sell", "sell", "sell"],
        ["invest", "worthy", "?"],
        ["should", "i", "invest"],
        ["could", "i", "get"],
        ["what", "do", "you"],
        ["is", "worth", "anything"]
    ]

    @staticmethod
    def should_be_copied(title, score):
        if score >= 500:
            return True
        else:
            #tite has dank words
            return False

if __name__ == '__main__':
    reddit_parser = RedditParser()
    #print reddit_parser.reddit.user.me()
    for submission in reddit_parser.memeeconomy.hot(limit = 50):
        print("Title: ", submission.title)
        print("Text: ", submission.selftext)
        print("Score: ", submission.score)
        print("---------------------------------\n")

