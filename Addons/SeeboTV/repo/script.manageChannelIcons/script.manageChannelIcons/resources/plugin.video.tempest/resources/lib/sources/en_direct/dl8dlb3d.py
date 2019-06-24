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
        self.domains = ['dl7.dlb3d.xyz']
        self.base_link_movie = 'http://dl8.dlb3d.xyz/Films/%s/'
        self.base_link_tv = 'http://dl8.dlb3d.xyz/Tv.Shows/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            title = '%s.%s' % (title, year)
            title = title.replace('-', '.')
            self.year = year
            url = self.base_link_movie % title
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.tvtitle = cleantitle.get_query(tvshowtitle)
            url = self.base_link_tv % self.tvtitle
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
            if url is None:
                return

            result = url
            if 'Films' in url:
                r = requests.get(result, timeout=10).content
                r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                for url in r:
                    if any(x in url for x in ['Trailer', 'Dubbed', 'rar']): continue
                    url = result + url
                    quality = source_utils.check_url(url)
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            else:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if self.se not in url: continue
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + 'E/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
