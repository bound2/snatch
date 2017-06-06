import os
import ConfigParser

from util import fileutils
from database.memedao import MemeDao
from database.config import ProductionConfiguration
from processor.instagramprocessor import InstagramProcessor


class BasicUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return "(username={:s}, password={:s})".format(self.username, self.password)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.username == other.username and self.password == other.password
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(self.username) + hash(self.password)


def parse_users(config):
    users = set()
    sections = config.sections()
    for section in sections:
        user = BasicUser(
            config.get(section, "username"),
            config.get(section, "password")
        )
        users.add(user)
    return users


DOWNLOAD_DIR = "resources{:s}downloads".format(os.sep)
BASIC_HASHTAGS = ["#dank", "#meme", "#funny", "#joke",
                  "#topkek", "#economy", "#grills",
                  "#100", "#lit", "#dankmeme", "#memegram",
                  "#polonium", "#detox"]

if __name__ == '__main__':
    meme_dao = MemeDao(ProductionConfiguration())
    uploadable_memes = meme_dao.find_non_processed()

    if len(uploadable_memes) > 0:
        config = ConfigParser.ConfigParser()
        config.read("insta.ini")
        insta_users = parse_users(config)

        for user in insta_users:
            insta_processor = InstagramProcessor(user.username, user.password)
            for meme in uploadable_memes:
                raw_file_path = fileutils.download_file(url=meme.media_url, destination_folder=DOWNLOAD_DIR)
                file_path = fileutils.convert_to_jpeg(raw_file_path)
                fileutils.fix_aspect_ratio(file_path)
                try:
                    insta_processor.upload_image(file_path=file_path, hashtags=BASIC_HASHTAGS)
                    meme_dao.mark_meme_processed(meme.post_id)
                finally:
                    fileutils.delete_file(file_path)
