# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 02-08-2019 by JewBMX in Scrubs.

import re,urlparse
from resources.lib.modules import client,cleantitle,source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviescouch.pro']
        self.base_link = 'https://moviescouch.pw'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            search_id = cleantitle.getsearch(title)
            url = urlparse.urljoin(self.base_link, self.search_link)
            url = url  % (search_id.replace(':', ' ').replace(' ', '+'))
            search_results = client.request(url)
            match = re.compile('<article id=.+?href="(.+?)" title="(.+?)"',re.DOTALL).findall(search_results)
            for row_url, row_title in match:
                if cleantitle.get(title) in cleantitle.get(row_title):
                    if year in str(row_title):
                        return row_url
            return
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            html = client.request(url)
            links = re.compile('<iframe src="(.+?)"',re.DOTALL).findall(html)
            for link in links:
                quality, info = source_utils.get_release_quality(link, url)
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].split('.')[0].title()
                valid, host = source_utils.is_host_valid(host, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url

