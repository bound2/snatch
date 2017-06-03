import atexit
from InstagramAPI import InstagramAPI


class InstagramProcessor:
    def __init__(self, username, password):
        self._instagramApi = InstagramAPI(username, password)
        self._instagramApi.login()
        atexit.register(self.destroy)

    def destroy(self):
        self._instagramApi.logout()

    def upload_image(self, file_path, caption='', hashtags=None):
        full_caption = self._create_full_caption(caption, hashtags)
        self._instagramApi.uploadPhoto(file_path, caption=full_caption, upload_id=None)

    def _create_full_caption(self, caption, hashtags):
        if hashtags is not None:
            for hashtag in hashtags:
                caption += ' ' + hashtag
        return caption
