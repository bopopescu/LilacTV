# -*- coding: utf-8 -*-
# -Cleaned and Checked on 05-06-2019 by JewBMX in Scrubs.

import re, urllib, urlparse
from resources.lib.modules import client, cleantitle, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['filmxy.me', 'filmxy.one']
        self.base_link = 'https://www.filmxy.one/'
        self.search_link = 'search/%s/feed/rss2/'
        self.post = 'https://cdn.filmxy.one/asset/json/posts.json'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return
            hostDict = hostprDict + hostDict
            data = urlparse.parse_qs(url)
            data = dict((i, data[i][0]) for i in data)
            title = data['title']
            year = data['year']
            tit = cleantitle.geturl(title + ' ' + year)
            query = urlparse.urljoin(self.base_link, tit)
            r = client.request(query, referer=self.base_link, redirect=True)
            if not data['imdb'] in r:
                return sources
            links = []
            try:
                down = client.parseDOM(r, 'div', attrs={'id': 'tab-download'})[0]
                down = client.parseDOM(down, 'a', ret='href')[0]
                data = client.request(down)
                frames = client.parseDOM(data, 'div', attrs={'class': 'single-link'})
                frames = [client.parseDOM(i, 'a', ret='href')[0] for i in frames if i]
                for i in frames:
                    links.append(i)
            except Exception:
                pass
            try:
                streams = client.parseDOM(r, 'div', attrs={'id': 'tab-stream'})[0]
                streams = re.findall('''iframe src=(.+?) frameborder''', streams.replace('&quot;', ''), re.I | re.DOTALL)
                for i in streams:
                    links.append(i)
            except Exception:
                pass
            for url in links:
                try:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    info = source_utils.get_release_quality(url)
                    host = client.replaceHTMLCodes(host)
                    host = host.encode('utf-8')
                    if valid:
                        sources.append({'source': host, 'quality': '1080p', 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
                except Exception:
                    pass
            return sources
        except Exception:
            return sources

    def resolve(self, url):
        return url
