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
        self.domains = ['stg.pz10139.parspack.net']
        self.base_link_movie = 'http://stg.pz10139.parspack.net/Films/%s/'
        self.base_link_tv = 'http://stg.pz10139.parspack.net/Tv%20Shows/'
        self.search_link = ''

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s' % (title, year)
            url = self.base_link_movie % self.title
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.get_query(tvshowtitle)
            title = '%s/' % title
            url = self.base_link_tv + title
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.se = 'S%02dE%02d' % (int(season), int(episode))
            season = 'S%02d/' % int(season)
            if not url: return
            url = url + season
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url in None: return

            result = url
            if 'Tv' in result:
                r = requests.get(result, timeout=10).content
                r = re.findall('a href="(.+?)"', r)
                for url in r:
                    if not self.se in url: continue
                    url = result + url
                    quality = source_utils.check_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            else:
                r = requests.get(result, timeout=10).content
                r = re.compile('a href="(.+?)"').findall(r)
                for url in r:
                    if not self.title in url: continue
                    if any(x in url for x in ['Trailer', 'Dubbed', 'rar', 'EXTRAS']): continue
                    url = result + url
                    quality = source_utils.check_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
