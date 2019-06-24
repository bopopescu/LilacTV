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
        self.domains = ['dl.updlf.com']
        self.base_link_movie = 'http://dl.updlf.com/files/Film/%s/'
        self.base_link_tv = 'http://dl.updlf.com/files/Series/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            title = '%s.%s' % (title, year)
            self.title = title.replace('.', '%20')
            year = year
            url = self.base_link_movie % year
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.title = cleantitle.get_query(tvshowtitle)
            url = self.base_link_tv % self.title.replace('.', '%20')
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
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append(
                            {'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': True,
                             'debridonly': False})

                    result2 = result + '1080p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append(
                            {'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': True,
                             'debridonly': False})

                    result2 = result + '720p%20x265%2010bit/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True,
                                        'debridonly': False})

                    result2 = result + '720p%20x265/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True,
                                        'debridonly': False})

                    result2 = result + '720p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True,
                                        'debridonly': False})

                    result2 = result + '480p/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': 'SD', 'language': 'en', 'url': url, 'direct': True,
                                        'debridonly': False})

                    r = requests.get(result, timeout=10).content
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append(
                            {'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True,
                             'debridonly': False})

                    result2 = self.base_link_tv % self.title
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_url(url)
                        sources.append(
                            {'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True,
                             'debridonly': False})
                except:
                    return
            else:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.compile('a href="(.+?)">.+?<').findall(r)
                    for i in r:
                        if self.title not in i:
                            continue
                        i = result + i
                        r = requests.get(i, timeout=10).content
                        r = re.compile('a href="(.+?)">.+?<').findall(r)
                        for url in r:
                            title = self.title.replace('%20', '.')
                            if title not in url:
                                continue
                            if any(x in url for x in ['jpg']):
                                continue
                            url = i + url
                            quality = source_utils.check_url(url)
                            sources.append(
                                {'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True,
                                 'debridonly': False})
                except:
                    return

            return sources
        except:
            return sources

    def resolve(self, url):
        return url
