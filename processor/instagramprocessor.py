import atexit
import os
from util import fileutils
from InstagramAPI import InstagramAPI


class InstagramProcessor:

    DOWNLOAD_DIR = "..{:s}downloads".format(os.sep)

    def __init__(self):
        self._instagramApi = InstagramAPI('user', 'password')
        self._instagramApi.login()
        atexit.register(self.destroy)

    def destroy(self):
        self._instagramApi.logout()

    def upload_image(self, image_url, caption='', hashtags=None):
        full_caption = self._create_full_caption(caption, hashtags)
        file_name = fileutils.download_file(url=image_url, destination_folder=InstagramProcessor.DOWNLOAD_DIR)
        file_path = InstagramProcessor.DOWNLOAD_DIR + os.sep + file_name
        try:
            self._instagramApi.uploadPhoto(file_path, caption=full_caption, upload_id=None)
        finally:
            fileutils.delete_file(InstagramProcessor.DOWNLOAD_DIR, file_name)


    def _create_full_caption(self, caption, hashtags):
        if hashtags is not None:
            for hashtag in hashtags:
                caption += ' ' + hashtag
        return caption

