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
        self.domains = ['dl3.dlb3d.xyz']
        self.base_link = 'http://dl3.dlb3d.xyz/'
        self.search_movie = 'Movies/%s/'
        self.search_tv = 'Tv.Shows/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s' % (title, year)
            self.year = year
            url = self.base_link + self.search_movie % self.title
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.tvtitle = cleantitle.get_query(tvshowtitle)
            url = self.base_link + self.search_tv % self.tvtitle
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.se = 'S%02dE%02d' % (int(season), int(episode))
            season = 'S%02d/' % int(season)
            if url is None:
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
            if 'Movies' in result:
                r = requests.get(result, timeout=10).content
                r = re.compile('a href="(.+?)" title=".+?"').findall(r)
                for url in r:
                    if self.title not in url: continue
                    if any(x in url for x in ['Trailer', 'Dubbed', 'rar']): continue
                    url = result + url
                    quality = source_utils.check_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            else:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if self.se not in url:
                            continue
                        if any(x in url for x in ['Dubbed']):
                            raise Exception()
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    i = self.base_link + self.search_tv % self.tvtitle
                    r = requests.get(i, timeout=10).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if self.se not in url:
                            continue
                        if any(x in url for x in ['Dubbed']):
                            raise Exception()
                        url = i + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
