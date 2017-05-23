import time

from pymongo.errors import DuplicateKeyError
from telepot import DelegatorBot
from telepot.helper import ChatHandler
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

from redditparser import Rules
from database.config import TestConfiguration
from database.memedao import MemeDao
from database.meme import Meme
from database.meme import Site

from util import idutils
from util import textutils


class TelegramParser(ChatHandler):
    def __init__(self, *args, **kwargs):
        super(TelegramParser, self).__init__(*args, **kwargs)
        self._meme_dao = MemeDao(config=TestConfiguration())

    def on_chat_message(self, msg):
        raw_text = msg.get('text')
        if Rules.url_allowed(raw_text):
            try:
                self._save_potential_meme(url=textutils.extract_url(text=raw_text))
                current_count = len(self._meme_dao.find_by_site(Site.TELEGRAM))
                self.sender.sendMessage("Memebot found a potential image. Total images found %s" % current_count)
            except DuplicateKeyError:
                self.sender.sendMessage("Memebot found a duplicate image. Bad bad bad!!!")

    def _save_potential_meme(self, url):
        id = idutils.generate_id()
        meme = Meme(post_id=id, site=Site.TELEGRAM, text='', media_url=url)
        self._meme_dao.insert_one(data=meme)


if __name__ == '__main__':
    TOKEN = ''

    bot = DelegatorBot(TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, TelegramParser, timeout=10
        ),
    ])
    MessageLoop(bot).run_as_thread()
    print('Listening ...')

    while 1:
        time.sleep(10)
