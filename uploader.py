import os
import random
import ConfigParser

from argparse import ArgumentParser
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


def parse_hashtags(config):
    hashtags = set()
    sections = config.sections()
    for section in sections:
        tag_group = set()
        for option in config.options(section):
            option = option.strip()
            if len(option) > 0:
                tag = "#{:s}".format(option)
                tag_group.add(tag)
        hashtags.add(frozenset(tag_group))
    return hashtags


DOWNLOAD_DIR = "resources{:s}downloads".format(os.sep)

if __name__ == '__main__':

    argument_parser = ArgumentParser()
    argument_parser.add_argument('--count', default=1, help='how many memes should be uploaded per user')
    args = argument_parser.parse_args()
    max_upload_count = args.count

    meme_dao = MemeDao(ProductionConfiguration())
    uploadable_memes = meme_dao.find_non_processed()

    if len(uploadable_memes) > 0:
        user_config = ConfigParser.ConfigParser()
        tag_config = ConfigParser.ConfigParser(allow_no_value=True)

        user_config.read("insta.ini")
        tag_config.read("hashtags.ini")

        insta_users = parse_users(user_config)
        hashtags = parse_hashtags(tag_config)

        for user in insta_users:
            insta_processor = InstagramProcessor(user.username, user.password)
            current_upload_count = 0
            for meme in uploadable_memes:
                raw_file_path = fileutils.download_file(url=meme.media_url, destination_folder=DOWNLOAD_DIR)
                file_path = fileutils.convert_to_jpeg(raw_file_path)
                fileutils.fix_aspect_ratio(file_path)
                try:
                    insta_processor.upload_image(file_path=file_path, hashtags=random.sample(hashtags, 1)[0])
                    meme_dao.mark_meme_processed(meme.post_id)
                    current_upload_count += 1
                finally:
                    fileutils.delete_file(file_path)
                # Break early if limit is hit
                if current_upload_count == max_upload_count:
                    break
