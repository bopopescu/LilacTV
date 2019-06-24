# -*- coding: utf-8 -*-


import re

from resources.lib.modules import source_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['openloadmovie.org']
        self.base_link = 'https://openloadmovie.org'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + '/movies/%s-%s' % (title, year)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostprDict + hostDict
            sources = []
            r = client.request(url)
            match = re.compile('<iframe class="metaframe rptss" src="(.+?)"').findall(r)
            for url in match:
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': url, 'direct': False,
                                    'debridonly': False})
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url
