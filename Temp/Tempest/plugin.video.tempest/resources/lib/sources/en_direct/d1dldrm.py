# -*- coding: utf-8 -*-
"""
**Created by Tempest**
"""

import re
import requests
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['d1.dldrm.ir']
        self.base_link = 'http://d1.dldrm.ir/Serial/'
        self.search_link = '%s/'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.get_query(tvshowtitle)
            title = '%s' % title
            url = self.base_link + self.search_link % title
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.se = 'S%02dE%02d' % (int(season), int(episode))
            if url is None:
                return
            url = url
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return

            result = url
            r = requests.get(result, timeout=10).content
            r = re.findall('A HREF=".+?">(.+?)<', r)
            for r in r:
                if not self.se in r: continue
                url = result + r
                quality = source_utils.check_url(url)
                sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
