import typing

from core.engine.base import SearchResult
from core.engine.bing import Bing
from core.engine.google import Google


class Tinksp:

    def search(self, keywords, e="bing") -> typing.List[SearchResult]:
        if e == "bing":
            engine = Bing()
        elif e == "google":
            engine = Google()
        else:
            raise ValueError("Invalid engine: %s" % e)
        return engine.search(keywords, site="tinksp.com")[:5]
