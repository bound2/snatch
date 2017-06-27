import praw
import re

from database.meme import Meme
from database.meme import Site
from util import collectionutils
from enum import Enum


class Popularity(Enum):
    HOT = 1
    RISING = 2
    NEW = 3


class RedditParser:
    def __init__(self, fetch_limit=25, max_fetch_count=250):
        self.reddit = praw.Reddit('bot1')
        self.memeeconomy = self.reddit.subreddit('MemeEconomy')
        self.fetch_limit = fetch_limit
        self.max_fetch_count = max_fetch_count

    def find_dank_memes_hot(self):
        return self._get_dank_memes(Popularity.HOT)

    def find_dank_memes_rising(self):
        return self._get_dank_memes(Popularity.RISING)

    def find_dank_memes_new(self):
        return self._get_dank_memes(Popularity.NEW)

    def _get_dank_memes(self, popularity, memes=None, last_submission=None):
        if memes is None:
            memes = dict()
        if last_submission is None:
            submissions = self._get_submission_by_popularity(popularity)
        else:
            page = len(memes) / self.fetch_limit
            params = {"count": self.fetch_limit * page, "after": last_submission.fullname}
            submissions = self._get_submission_by_popularity(popularity, params)

        memes.update(self._parse_dank_memes(submissions))
        current_count = len(memes)
        if current_count < self.max_fetch_count and current_count % self.fetch_limit == 0:
            return self._get_dank_memes(popularity, memes, self._get_last_submission(submissions))
        else:
            return self._apply_filter(memes)

    def _get_submission_by_popularity(self, popularity, pagination_params=None):
        if popularity is Popularity.HOT:
            return self.memeeconomy.hot(limit=self.fetch_limit, params=pagination_params)
        elif popularity is Popularity.RISING:
            return self.memeeconomy.rising(limit=self.fetch_limit, params=pagination_params)
        elif popularity is Popularity.NEW:
            return self.memeeconomy.new(limit=self.fetch_limit, params=pagination_params)
        else:
            raise TypeError("Expected type Popularity, but found: %s" % popularity.whoami())

    def _get_last_submission(self, submissions):
        last_submission = None
        for submission in submissions._listing.children:
            last_submission = submission
        return last_submission

    def _parse_dank_memes(self, listing):
        meme_map = dict()

        for submission in listing:
            meme = Meme(post_id=submission.id, site=Site.REDDIT, text=submission.title, media_url=submission.url)
            meme_map.update({meme: submission.score})

        return meme_map

    def _apply_filter(self, meme_map):
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

    _KEYWORDS = [
        list(['buy', 'buy', 'buy']),
        list(['invest', 'invest', 'invest']),
        list(['high profit']),
        list(['buy quick', 'sell quick']),
        list(['great potential', 'buy'])
    ]

    _BAD_KEYWORDS = [
        list(['sell', 'sell', 'sell']),
        list(['sell', 'now']),
        list(['time', 'to', 'sell']),
        list(['normie', 'sell']),
        list(['9gag']),
        list(['ifunny']),
        list(['buzzfeed']),
        list(['spotify']),
        list(['porn'])
    ]

    @staticmethod
    def should_be_copied(title, score):
        cleaned_title = re.sub(r"(!)|(\?)|(-)|(\+)", "", title)
        words = list(cleaned_title.lower().split(' '))
        good_keywords = Rules._match_to_keywords(words, Rules._KEYWORDS)
        bad_keywords = Rules._match_to_keywords(words, Rules._BAD_KEYWORDS)
        if not bad_keywords:
            if score >= 500 or good_keywords:
                return True
        return False

    @staticmethod
    def _match_to_keywords(words, validation_keywords):
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
