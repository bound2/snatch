#!/usr/bin/env python
from parser.redditparser import RedditParser
from database.memedao import MemeDao
from database.meme import Site

if __name__ == '__main__':
    reddit_parser = RedditParser()
    meme_dao = MemeDao()

    all_memes = set()
    all_memes.update(reddit_parser.find_dank_memes_from_hot())
    all_memes.update(reddit_parser.find_dank_memes_from_rising())
    all_memes.update(reddit_parser.find_dank_memes_from_new())

    results = meme_dao.insert_many(all_memes)

    cursor = meme_dao.find_by_site(Site.REDDIT)
    for document in cursor:
        print document