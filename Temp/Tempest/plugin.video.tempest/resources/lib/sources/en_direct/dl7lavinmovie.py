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
        self.domains = ['dl7.lavinmovie.net']
        self.base_link_movie = 'http://dl7.lavinmovie.net/Movies/%s/'
        self.base_link_tv = 'http://dl7.lavinmovie.net/Series/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s' % (title, year)
            year = year
            url = self.base_link_movie % year
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.get_query(tvshowtitle)
            url = self.base_link_tv % title.replace('.', '%20')
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
            if 'Series' in result:
                try:
                    result2 = result + '1080p%20x265/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + 'FULL%20HD/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + 'FULL%20HD%201080p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '1080p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '720p%20x265/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '720p%20x265%20PSA/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '720p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + 'HD%20720p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '480p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': 'SD', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    return
            else:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        if any(x in url for x in ['zip']): raise Exception()
                        url = result + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
