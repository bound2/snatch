#!/usr/bin/env python
from parser.redditparser import RedditParser

if __name__ == '__main__':
    reddit_parser = RedditParser()

    all_memes = set()
    all_memes.update(reddit_parser.find_dank_memes_from_hot())
    all_memes.update(reddit_parser.find_dank_memes_from_rising())
    all_memes.update(reddit_parser.find_dank_memes_from_new())

    for meme in all_memes:
        print meme


