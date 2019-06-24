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
        self.domains = ['dl.dlb3d.xyz']
        self.base_link_movie = 'http://dl.dlb3d.xyz/M/%s/'
        self.base_link_tv = 'http://dl.dlb3d.xyz/S/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s' % (title, year)
            self.year = year
            url = self.base_link_movie % self.title
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.get_query(tvshowtitle)
            url = self.base_link_tv % title
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.se = 'S%02dE%02d' % (int(season), int(episode))
            season = 'S%02d/' % int(season)
            if not url:
                return
            url = url + season
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return

            result = url
            if 'M' in result:
                r = requests.get(result, timeout=10).content
                r = re.findall('a href=".+?" title="(.+?)"', r)
                for url in r:
                    if any(x in url for x in ['Trailer', 'Dubbed', 'rar']): continue
                    url = result + url
                    quality = source_utils.check_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            else:
                r = requests.get(result, timeout=10).content
                r = re.findall('a href=".+?" title="(.+?)"', r)
                for url in r:
                    if not self.se in url: continue
                    if any(x in url for x in ['Trailer']): continue
                    url = result + url
                    quality = source_utils.check_direct_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
