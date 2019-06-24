# -*- coding: utf-8 -*-
"""
**Created by Tempest**
"""

import re, requests

from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['ns502618.ip-192-99-8.net']
        self.base_link = 'http://ns502618.ip-192-99-8.net/library/movieland/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            title = '%s.%s' % (title, year)
            i = requests.get(self.base_link, timeout=10).content
            i = re.compile('a href="(.+?)"').findall(i)
            for url in i:
                if not title in url: continue
                return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return

            url = self.base_link + url
            quality = source_utils.check_sd_url(url)
            sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
