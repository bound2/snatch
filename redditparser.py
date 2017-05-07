#!/usr/bin/env python

import praw

class RedditParser:

    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        self.memeeconomy = self.reddit.subreddit('MemeEconomy')


if __name__ == '__main__':
    reddit_parser = RedditParser()
    print reddit_parser.reddit.user.me()

