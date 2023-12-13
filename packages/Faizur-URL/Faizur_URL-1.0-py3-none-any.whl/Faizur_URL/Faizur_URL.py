from pyshorteners import Shortener

class FaizurURL:
    def __init__(self, api_key=None):
        self.shortener = Shortener(api_key=api_key)

    def shorten_url(self, url, **kwargs):
        return self.shortener.tinyurl.short(url, **kwargs)

    def expand_url(self, short_url, **kwargs):
        return self.shortener.tinyurl.expand(short_url, **kwargs)

    # Additional features from pyshorteners
    def adfly(self, url, **kwargs):
        return self.shortener.adfly.short(url, **kwargs)

    def bitly(self, url, **kwargs):
        return self.shortener.bitly.short(url, **kwargs)

    def chilpit(self, url, **kwargs):
        return self.shortener.chilpit.short(url, **kwargs)

    def clkim(self, url, **kwargs):
        return self.shortener.clkim.short(url, **kwargs)

    def isgd(self, url, **kwargs):
        return self.shortener.isgd.short(url, **kwargs)

    def osdb(self, url, **kwargs):
        return self.shortener.osdb.short(url, **kwargs)

    # Additional services
    def tinycc(self, url, **kwargs):
        return self.shortener.tinycc.short(url, **kwargs)

    def tinyurl_com(self, url, **kwargs):
        return self.shortener.tinyurl_com.short(url, **kwargs)

    def tnyim(self, url, **kwargs):
        return self.shortener.tnyim.short(url, **kwargs)

    # More services
    def dagd(self, url, **kwargs):
        return self.shortener.dagd.short(url, **kwargs)

    def ow_ly(self, url, **kwargs):
        return self.shortener.ow_ly.short(url, **kwargs)

    def git_io(self, url, **kwargs):
        return self.shortener.git_io.short(url, **kwargs)

    def qr_code(self, url, **kwargs):
        return self.shortener.qr_code.short(url, **kwargs)

    # Add more methods for other supported services as needed