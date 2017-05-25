from pymongo.errors import DuplicateKeyError

from database.config import ProductionConfiguration
from parser.redditparser import RedditParser
from database.memedao import MemeDao

if __name__ == '__main__':
    reddit_parser = RedditParser()
    meme_dao = MemeDao(ProductionConfiguration())

    all_memes = set()
    all_memes.update(reddit_parser.find_dank_memes_hot())
    all_memes.update(reddit_parser.find_dank_memes_rising())
    all_memes.update(reddit_parser.find_dank_memes_new())

    for meme in all_memes:
        try:
            meme_dao.insert_one(meme)
        except DuplicateKeyError:
            print "Unable to save a duplicate meme: %s" % str(meme)
            pass
