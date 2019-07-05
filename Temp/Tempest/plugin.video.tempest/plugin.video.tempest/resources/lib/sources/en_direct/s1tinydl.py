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
        self.domains = ['s1.tinydl.info']
        self.base_link = 'http://s1.tinydl.info/Movies/'
        self.base_link2 = 'http://s1.tinydl.info/Movies2/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s/' % (title, year)
            return
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            try:
                result = self.base_link + self.title.replace('.', '%20')
                r = requests.get(result).content
                r = re.compile('a href="(.+?)" title=".+?"').findall(r)
                for url in r:
                    if any(x in url for x in ['Trailer', 'AUDIO']): continue
                    url = result + url
                    quality = source_utils.check_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            except:
                return

            try:
                result = self.base_link2 + self.title.replace('.', '%20')
                r = requests.get(result).content
                r = re.compile('a href="(.+?)" title=".+?"').findall(r)
                for url in r:
                    if any(x in url for x in ['Trailer', 'AUDIO']): continue
                    url = result + url
                    quality = source_utils.check_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            except:
                return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
