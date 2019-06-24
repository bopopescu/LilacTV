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
        self.domains = ['dl.sitemovie.ir']
        self.base_link_movie = 'http://dl.sitemovie.ir/movie/'
        self.base_link_tv = 'http://dl.sitemovie.ir/serial/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s' % (title, year)
            url = self.base_link_movie
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
            self.season = int(season)
            if not url: return
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
            if 'serial' in result:
                try:
                    result2 = result + 'S%02d/' % self.season
                    r = requests.get(result2, timeout=10)
                    if not r.ok:
                        result2 = result + 's%02d/' % self.season
                        r = requests.get(result2, timeout=10)
                    if not r.ok:
                        return
                    r = r.content
                    r = re.findall('a href="(.+?)"',r)
                    for url in r:
                        if self.se not in url:
                            continue
                        if any(x in url for x in ['Dubbed']):
                            continue
                        url = result2 + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    return
            else:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if self.title not in url:
                            continue
                        if any(x in url for x in ['Trailer', 'Dubbed', 'rar']):
                            continue
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    r = requests.get(result, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        title = self.title.replace('.', '_')
                        if title not in url:
                            continue
                        if any(x in url for x in ['Trailer', 'Dubbed', 'rar']):
                            continue
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
