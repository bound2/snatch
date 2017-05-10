#!/usr/bin/env python
import unittest
import mock
from mock import MagicMock
from mock import patch
from database.meme import Meme
from database.meme import Site
from parser.redditparser import RedditParser

def mock_reddit_data():
    return {
        Meme(id='6ad955', site=Site.REDDIT, text='Crossover fidget memes on the rise! BUY BUY BUY', media_url='https://i.redd.it/xi7s8hwcsowy.jpg'),
        Meme(id='6a9sod', site=Site.REDDIT, text='POPE MEMES ON THE RISE!!! BUY BUY BUY NOW', media_url='https://i.redd.it/lkgqkz3etkwy.jpg'),
        Meme(id='6ac9cf', site=Site.REDDIT, text='INVEST NOW', media_url='https://i.redd.it/kuwbty37vnwy.jpg'),
        Meme(id='6a5fzv', site=Site.REDDIT, text='Muslim Noises memes on the rise!BUY BUY BUY', media_url='https://i.redd.it/yu3jsdyw9hwy.jpg'),
        Meme(id='6a2z8d', site=Site.REDDIT, text='thos Beans are a high-risk, high-reward commodity', media_url='http://i.imgur.com/lYRoiWg.jpg'),
        Meme(id='6a6s68', site=Site.REDDIT, text='Condescending Spongebob memes on the rise! BUY BUY BUY', media_url='https://i.redd.it/991iipqxbiwy.png'),
        Meme(id='6ad955', site=Site.REDDIT, text='Crossover fidget memes on the rise! BUY BUY BUY', media_url='https://i.redd.it/xi7s8hwcsowy.jpg'),
        Meme(id='6aedlg', site=Site.REDDIT, text='Meta', media_url='https://i.redd.it/nw8sevggnpwy.jpg'),
        Meme(id='6acb23', site=Site.REDDIT, text='Chuck E. Cheese meme rising in popularity!!! Good short term investment before taken by normies?', media_url='https://i.redd.it/mbs2soz6xnwy.jpg'),
        Meme(id='6ac087', site=Site.REDDIT, text='Completely nuts, should I invest?', media_url='https://i.redd.it/lwco5wgvjnwy.jpg'),
        Meme(id='6ac7q5', site=Site.REDDIT, text='Can I get an Evaluation on this Template/Meme', media_url='https://i.redd.it/ov1jmpm9tnwy.jpg'),
        Meme(id='6ab2ps', site=Site.REDDIT, text='CONDESCENDING SPONGEBOB MEMES POSTED BY COLLEGE TWITTER! SELL SELL SELL!!!', media_url='https://i.redd.it/uqrnytca7mwy.png'),
        Meme(id='6adbfq', site=Site.REDDIT, text='Historical Spongebob memes are making a comeback!!! Buy Now!!!', media_url='http://i.imgur.com/kFuayKT.png'),
        Meme(id='6ae78p', site=Site.REDDIT, text="Pepe's death makes it to Snapchat! Sell! Sell! Invest in Pepe's ghost meme's and short Blepe.", media_url='https://i.redd.it/63eklzjlipwy.jpg'),
        Meme(id='6ae23m', site=Site.REDDIT, text="Any potential?", media_url='https://i.redd.it/o6zpjujrepwy.jpg'),
        Meme(id='6af1ab', site=Site.REDDIT, text="Can I get an appraisal?", media_url='https://i.redd.it/b1e7723u5qwy.jpg'),
        Meme(id='6aegzc', site=Site.REDDIT, text="Buy or Sell fidget spinner lightsabers?", media_url='https://i.redd.it/4wn6yt12qpwy.jpg'),
        Meme(id='6aax81', site=Site.REDDIT, text="Colorized Minecraft memes: BUY WHILE YOU CAN STILL AFFORD!", media_url='http://i.imgur.com/DChzMus.png'),
        Meme(id='6ade1n', site=Site.REDDIT, text="Potential ?", media_url='https://i.redd.it/p4l46jv1wowy.jpg'),
        Meme(id='6adsdi', site=Site.REDDIT, text="Value of this Pepe? Go ahead and steal it, it can't be worth more than a few dat bois without a watermark", media_url='https://i.redd.it/njytn2v87pwy.jpg'),
        Meme(id='6acfxd', site=Site.REDDIT, text="possible meme format? any potential?", media_url='https://i.redd.it/uirf7cla2owy.jpg'),
        Meme(id='6aeguh', site=Site.REDDIT, text="Has anyone ever done any trading here?", media_url='https://i.redd.it/0r4v4olyppwy.jpg'),
        Meme(id='6adpr8', site=Site.REDDIT, text="BOW WOW CHALLENGE MEMES ARE BORN! GET THEM EARLY! BUY NOW!", media_url='https://i.redd.it/mmpyf5r35pwy.jpg'),
        Meme(id='6a90jg', site=Site.REDDIT, text="QUICK BUY AP CALC BC POTATO MEMES BEFORE ITS TOO LATE!!!", media_url='https://i.redd.it/bvzpr1rz2kwy.jpg'),
        Meme(id='6adk91', site=Site.REDDIT, text='Small capped centipede meme stock: any future value with Comey Termination and Trumpies calling themselves "Centipedes"?', media_url='https://i.redd.it/zszs21pj0pwy.png'),
        Meme(id='6a9idt', site=Site.REDDIT, text='More investors needed', media_url='https://i.redd.it/itnfuldnjkwy.jpg'),
        Meme(id='6a7946', site=Site.REDDIT, text='Rare trading card meme seeking appraisal', media_url='http://i.imgur.com/YZ3lGqA.png'),
        Meme(id='6adxzl', site=Site.REDDIT, text='Warning! Condescending Spongebob already adopted by twitter users', media_url='http://i.imgur.com/g5fw8Qc.jpg'),
        Meme(id='6aew8m', site=Site.REDDIT, text='any potential for this format?', media_url='https://i.redd.it/mt9drzrx1qwy.jpg'),
        Meme(id='6aepk0', site=Site.REDDIT, text='Meta-Memes without actual content on the rise!!!', media_url='https://i.redd.it/24fw1fqnwpwy.jpg'),
        Meme(id='6aejj0', site=Site.REDDIT, text='What is the estimated value of this maymay', media_url='https://i.redd.it/dwchudyzrpwy.jpg'),
        Meme(id='6ad83u', site=Site.REDDIT, text='BAKED BEANS MEMES ARE ON THE RISE, BUY BUY BUY!!', media_url='https://i.redd.it/zl81sinirowy.jpg'),
        Meme(id='6adznn', site=Site.REDDIT, text='CRASH IN T-MINUS 2 DAYS. BUY BEFORE THE GREAT FACEBOOK CRASH FOR MASSIVE PROFITS.', media_url='https://i.redd.it/8yqpc8bxcpwy.jpg'),
        Meme(id='6ady38', site=Site.REDDIT, text="Smoking messages memes are on the rise. BUY BUY BUY! (Here's a template)", media_url='https://i.redd.it/imtfgpfobpwy.jpg'),
        Meme(id='6adswa', site=Site.REDDIT, text="Fake google results memes? Can I get an appraisal", media_url='https://i.redd.it/8kpugbdn7pwy.jpg'),
        Meme(id='6acee0', site=Site.REDDIT, text="SCINECE MEMES ON THE RISE! BUY!", media_url='https://i.redd.it/5wa0r3wp0owy.jpg'),
        Meme(id='6abj56', site=Site.REDDIT, text="seen 'livin in the future' memes lately. may be a good invesment.", media_url='https://i.redd.it/oxh8316evmwy.jpg'),
        Meme(id='6aejfp', site=Site.REDDIT, text="BEAR MARKET: TRUMP NEXT TO BE FIRED. SELL SELL SELL", media_url='https://i.redd.it/0jh3mvbfrpwy.png'),
        Meme(id='6abdo5', site=Site.REDDIT, text="This meme of any value? Found it in an old meme warehouse. Is it worthwhile?", media_url='https://i.redd.it/rl4gdrwzmmwy.jpg'),
        Meme(id='6ae073', site=Site.REDDIT, text="Bae Come over intelligent memes are on the rise. Guaranteed normie-proof.", media_url='https://i.redd.it/m8gwnpkbdpwy.jpg'),
        Meme(id='6a9tt7', site=Site.REDDIT, text='This got deleted because I titled it "take a look at this meme', media_url='https://i.redd.it/bdi96zi7ukwy.jpg')
    }

class RedditTest(unittest.TestCase):

    @mock.patch('__main__.RedditParser.find_dank_memes_from_hot', return_value=mock_reddit_data())
    @mock.patch('__main__.RedditParser.find_dank_memes_from_new', return_value=mock_reddit_data())
    @mock.patch('__main__.RedditParser.find_dank_memes_from_rising', return_value=mock_reddit_data())
    def test_parser(self, hot_mock, new_mock, rising_mock):
        reddit_parser = RedditParser()
        assert len(reddit_parser.find_dank_memes_from_hot()) == 40
        assert len(reddit_parser.find_dank_memes_from_new()) == 40
        assert len(reddit_parser.find_dank_memes_from_rising()) == 40


if __name__ == '__main__':
    unittest.main()
