#!/usr/bin/env python

from enum import Enum


class Site(Enum):
    REDDIT = 1


class Meme:
    def __init__(self, id, site, text, media_url):
        self.id = id
        self.site = site
        self.text = text
        self.media_url = media_url

    def __str__(self):
        return "id={:s}\nsite={:s}\ntext={:s}\nmedia_url={:s}\n".format(self.id, str(self.site), self.text, self
                                                                        .media_url)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.site == other.site
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(self.id) + hash(self.site)
