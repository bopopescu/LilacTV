# -*- coding: utf-8 -*-

"""
    **Created by Tempest**

"""

import re
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['alluc.xyz']
        self.base_link = 'https://www1.alluc.xyz'
        self.search_link = '/?s=%s+%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            url = self.base_link + self.search_link % (title, year)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            r = self.scraper.get(url).content
            u = client.parseDOM(r, "div", attrs={"class": "item"})
            for i in u:
                t = re.compile('<a href="(.+?)"').findall(i)
                for r in t:
                    t = self.scraper.get(url).content
                    r = re.compile('<a href="(.+?)"').findall(t)
                    for url in r:
                        quality, info = source_utils.get_release_quality(url)
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            return sources

    def resolve(self, url):
        return url
