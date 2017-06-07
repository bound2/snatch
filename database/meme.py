class Site:
    def __init__(self):
        pass

    REDDIT = 'reddit'
    TELEGRAM = 'telegram'


class Meme:
    def __init__(self, post_id, site, text, media_url, processed=False):
        self.post_id = post_id
        self.site = site
        self.text = text
        self.media_url = media_url
        self.processed = processed

    def __str__(self):
        return "post_id={:s}, site={:s}, text={:s}, media_url={:s}, processed={:s}" \
            .format(self.post_id,
                    str(self.site),
                    self.text,
                    self.media_url,
                    str(self.processed))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.post_id == other.post_id and self.site == other.site
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(self.post_id) + hash(self.site)
