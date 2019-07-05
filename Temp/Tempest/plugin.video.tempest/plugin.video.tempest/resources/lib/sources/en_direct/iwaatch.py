# -*- coding: utf-8 -*-
"""
**Created by Tempest**
"""

import requests

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123movies4u.ch']
        self.base_link = 'https://iwaatch.com'
        self.search_link = '/movie/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '_')
            url = self.base_link + self.search_link % title
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return

            r = requests.get(url).content
            u = client.parseDOM(r, "span", attrs={"class": "download-q"})
            for t in u:
                u = client.parseDOM(t, 'a', ret='href')
                for url in u:
                    quality = source_utils.check_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                return sources
        except:
            return sources

    def resolve(self, url):
        return url
