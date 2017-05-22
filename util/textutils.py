import re


def extract_url(text):
    return re.search("(?P<url>https?://[^\s]+)", text).group("url")
