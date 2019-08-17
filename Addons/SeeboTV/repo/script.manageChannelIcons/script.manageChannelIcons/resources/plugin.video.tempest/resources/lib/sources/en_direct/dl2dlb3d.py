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
        self.domains = ['dl2.dlb3d.xyz']
        self.base_link = 'http://dl2.dlb3d.xyz/'
        self.search_movie = 'M/%s/'
        self.search_tv = 'S/%s/'

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
            title = cleantitle.get_query(tvshowtitle)
            url = self.base_link + self.search_tv % title
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
            if 'M' in result:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.compile('a href=".+?" title="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url:
                            continue
                        if any(x in url for x in ['Trailer', 'Dubbed', 'rar']):
                            raise Exception()
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                except:
                    return
            else:
                try:
                    r = requests.get(result, timeout=10).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + 'E/2160p.x264.WEBRip/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '4K', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '1080p.x264.BluRay/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '1080p.x264.WEBRip/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + 'E/1080p.x264.WEBRip/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '1080p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '720p.x265.BluRay/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + '720p.x265.WEBRip/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    result2 = result + 'E/720p.x265.WEBRip/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '720p.x264.BluRay/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '720p.x264.WEBRip/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + 'E/720p.x264.WEBRip/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '480p.x264.BluRay/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if not self.se in url: continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    result2 = result + '480p.x264.WEBRip/'
                    r = requests.get(result2, timeout=5).content
                    r = re.findall('a href=".+?" title="(.+?)"', r)
                    for url in r:
                        if self.se not in url:
                            continue
                        url = result2 + url
                        sources.append({'source': 'DL', 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                except:
                    return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
