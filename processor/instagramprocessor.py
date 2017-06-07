import atexit

from util import logger
from InstagramAPI import InstagramAPI


class InstagramProcessor:
    def __init__(self, username, password):
        logger.log('instagramprocessor.py', 'creating processor for user: {:s}'.format(username))
        self._instagramApi = InstagramAPI(username, password)
        self._instagramApi.login()
        atexit.register(self.destroy)

    def destroy(self):
        logger.log('instagramprocessor.py', 'killing off processor for user: {:s}'.format(self._instagramApi.username))
        self._instagramApi.logout()

    def upload_image(self, file_path, caption='', hashtags=None):
        full_caption = self._create_full_caption(caption, hashtags)
        self._instagramApi.uploadPhoto(file_path, caption=full_caption, upload_id=None)
        logger.log('instagramprocessor.py', 'Uploading picture: {:s}'.format(file_path))
        logger.log('instagramprocessor.py', 'Response: {:s}'.format(self._instagramApi.LastResponse.text))

    def _create_full_caption(self, caption, hashtags):
        if hashtags is not None:
            for hashtag in hashtags:
                caption += ' ' + hashtag
        return caption
