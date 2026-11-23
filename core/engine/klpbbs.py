import typing

from core.engine.base import SearchResult
from core.engine.bing import Bing
from core.engine.google import Google


class Klpbbs:

    def search(self, keywords, e="bing") -> typing.List[SearchResult]:
        if e == "bing":
            engine = Bing()
        elif e == "google":
            engine = Google()
        return engine.search(keywords, site="klpbbs.com")[:3]  # 一般来将,前五个才有价值 # 更加fw,3个