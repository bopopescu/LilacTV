"""
    Kodi resolveurl plugin
    Copyright (C) 2019 script.module.resolveurl

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
from urllib2 import HTTPError
from urlparse import urlparse

from lib import cfsolver, helpers, jsunpack
from urlresolver.common import Net, RAND_UA
from urlresolver.lib.net import HttpResponse
from urlresolver.resolver import UrlResolver, ResolverError


class SpeedVidResolver(UrlResolver):
    name = "SpeedVid"
    domains = ['speedvid.net']
    pattern = '(?://|\.)(speedvid\.net)/(?:embed-|p-)?(\w+)'
    
    def __init__(self):
        self.net = Net()
        self.desktopHeaders = {
            'User-Agent': RAND_UA,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1'
        }

    
    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)

        try:
            r = self.net.http_GET(web_url, headers=self.desktopHeaders)
            content = r.content
        except HTTPError as e:
            r = HttpResponse(e)
            content = r.content
            if cfsolver.test_cloudflare(r, content): # Test if there's a Cloudflare challenge.
                submitURL = cfsolver.solve_cf_challenge(r, content) # Get the solution URL.
                if not submitURL:
                    return None
                # Get redirected to the proper page.
                self.desktopHeaders['Referer'] = r.get_url() + '/'
                r = self.net.http_GET(submitURL, headers=self.desktopHeaders)
                content = r.content

        if r._response.code == 200:
            source = None
            pattern = re.compile('(eval\(function\(p,a,c,k.*?)\s*?</script>', re.DOTALL)
            for match in pattern.finditer(content):
                unpackedData = jsunpack.unpack(match.group(1)).replace("\\\'", "'")
                tempURL = re.search('''(?:file|src):.*?['"](?P<url>.*?)['"]''', unpackedData, re.DOTALL).group(1)
                # Some of the links might be broken, so only use working ones.
                try:
                    if self.net.http_HEAD(tempURL, headers=self.desktopHeaders)._response.code < 400:
                        source = tempURL
                        break
                except:
                    pass # HTTPError caused by a broken link.

            if source:
                # Headers for requesting media (copied from Firefox).
                parsedUrl = urlparse(r.get_url())
                kodiHeaders = {
                    'User-Agent': self.net.get_user_agent(),
                    'Accept': 'video/webm,video/ogg,video/*;q=0.9,application/ogg;q=0.7,audio/*;q=0.6,*/*;q=0.5',
                    'Referer': '%s://%s/' % (parsedUrl.scheme, parsedUrl.netloc),
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Cookie': '; '.join(cookie.name+'='+cookie.value for cookie in self.net._cj)
                }
                return source + helpers.append_headers(kodiHeaders)
        raise ResolverError('Unable to locate video')

        
    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='http://www.{host}/{media_id}')