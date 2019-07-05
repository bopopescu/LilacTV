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
        self.domains = ['pz10028.parspack.net']
        self.base_link_movie = 'http://pz10028.parspack.net/F/%s/'
        self.base_link_tv = 'http://pz10028.parspack.net/S/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_url(title)
            title = '%s.%s' % (title, year)
            self.title = title.replace('.', '%20')
            url = self.base_link_movie % self.title
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.get_query(tvshowtitle)
            title = '%s' % title
            url = self.base_link_tv % title
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
            if 'F' in result:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        title = self.title.replace('%20', '.')
                        if not title in url: continue
                        if any(x in url for x in ['Trailer', 'Dubbed', 'rar', 'EXTRAS']): continue
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    return

            else:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.findall('a href="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + 'E/'
                    r = requests.get(result2, timeout=10).content
                    r = re.findall('a href="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '720p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.findall('a href="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '480p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.findall('a href="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': 'SD', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
