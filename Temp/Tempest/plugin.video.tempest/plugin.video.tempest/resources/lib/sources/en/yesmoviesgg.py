# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 05-06-2019 by JewBMX in Scrubs.

import re
from resources.lib.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['yesmovies.gg']
        self.base_link = 'https://yesmovies.gg'
        self.search_link = '/film/%s/watching.html?ep=0'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('--', '-')
            url = self.base_link + self.search_link % title
            return url
        except:
            return

# https://www3.yesmovies.gg/film/the-code-season-1/watching.html
# https://www3.yesmovies.gg/film/the-code-season-1/watching.html?ep=5

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostprDict + hostDict
            r = client.request(url)
            qual = re.compile('class="quality">(.+?)<').findall(r)
            for i in qual:
                quality = source_utils.check_url(i)
                info = i
            u = client.parseDOM(r, "div", attrs={"class": "pa-main anime_muti_link"})
            for t in u:
                u = re.findall('data-video="(.+?)"', t)
                for url in u:
                    if 'vidcloud' in url:
                        continue
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
                return sources
        except:
            return

    def resolve(self, url):
        return url
