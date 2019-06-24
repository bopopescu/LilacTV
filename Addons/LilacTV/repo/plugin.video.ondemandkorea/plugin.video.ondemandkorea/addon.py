# -*- coding: utf-8 -*-
"""
    Ondemand Korea
"""
from xbmcswift2 import Plugin
import os
import re
import time
import xbmc

plugin = Plugin()
_L = plugin.get_string

plugin_path = plugin.addon.getAddonInfo('path')
lib_path = os.path.join(plugin_path, 'resources', 'lib')
sys.path.append(lib_path)
import ondemandkorea as scraper

sys.path.append('/storage/.kodi/addons/service.vpn.manager/')
import vpnBJ as vpn

tPrevPage = u"[B]<<%s[/B]" %_L(30100)
tNextPage = u"[B]%s>>[/B]" %_L(30101)

root_url = "http://www.ondemandkorea.com"

quality_tbl = ['180p', '240p', '300p', '360p', '480p', '720p']

@plugin.route('/')
def main_menu():
    #urls = scraper.parseTop()
    items = [
        {'label':_L(30111), 'path':plugin.url_for('genre_view', genre='drama')},
        {'label':_L(30202), 'path':plugin.url_for('genre_view', genre='drama1')},
        {'label':_L(30112), 'path':plugin.url_for('genre_view', genre='variety')},
        {'label':_L(30203), 'path':plugin.url_for('genre_view', genre='variety1')},
        {'label':_L(30113), 'path':plugin.url_for('genre_view', genre='documentary')},
        {'label':_L(30118), 'path':plugin.url_for('genre_view', genre='korean-news')},
        {'label':_L(30114), 'path':plugin.url_for('genre_view', genre='food')},
        {'label':_L(30115), 'path':plugin.url_for('genre_view', genre='beauty')},
        {'label':_L(30117), 'path':plugin.url_for('genre_view', genre='health')},
        {'label':_L(30120), 'path':plugin.url_for('genre_view', genre='economy')},
        {'label':_L(30125), 'path':plugin.url_for('genre_view', genre='kids')},
        {'label':_L(30119), 'path':plugin.url_for('genre_view', genre='education')},
        {'label':_L(30121), 'path':plugin.url_for('genre_view', genre='religion')},
        {'label':_L(30204), 'path':plugin.url_for('genre_view', genre='baseball')},
        {'label':_L(30205), 'path':plugin.url_for('genre_view', genre='billiards')},
        {'label':_L(30206), 'path':plugin.url_for('genre_view', genre='fishing')},
        {'label':_L(30207), 'path':plugin.url_for('genre_view', genre='golf')},
    ]
    return items

@plugin.route('/genre/<genre>/')
def genre_view(genre):
    plugin.log.debug(genre)
    koPage = plugin.get_setting('koPage', bool)

    sortFlag = False
    if genre == 'drama1':
        sortFlag = True
        genre = 'drama'
    elif genre == 'variety1':
        sortFlag = True
        genre = 'variety'
    elif genre == 'korean-news':
        sortFlag = True
    elif genre == 'documentary':
        sortFlag = True

    info = scraper.parseGenre(genre, sortFlag, koPage=koPage)
    items = [{'label':item['title'], 'path':plugin.url_for('episode_view', url=item['url'], page=1, genre=genre), 'thumbnail':item['thumbnail']} for item in info]
    return plugin.finish(items, view_mode='thumbnail')

@plugin.route('/episode/<genre>/<page>/<url>')
def episode_view(url, page, genre):

    #if not os.path.exists('/storage/FirstRun.flag'):
    #    os.mknod('/storage/FirstRun.flag')
    #    xbmc.executebuiltin("ReloadSkin()")
    #    time.sleep(1)

    plugin.log.debug(url)
    koPage = plugin.get_setting('koPage', bool)
    info = scraper.parseEpisodePage2(url, page=int(page), koPage=koPage)
    items = [{'label':item['title'], 'label2':item['broad_date'], 'path':plugin.url_for('play_episode', url=item['url'], genre=genre), 'thumbnail':item['thumbnail']} for item in info['episode']]
    # navigation
    if 'prevpage' in info:
        items.append({'label':tPrevPage, 'path':plugin.url_for('episode_view', url=url, page=info['prevpage'], genre=genre)})
    if 'nextpage' in info:
        items.append({'label':tNextPage, 'path':plugin.url_for('episode_view', url=url, page=info['nextpage'], genre=genre)})
    return plugin.finish(items, update_listing=False)

def CheckDNS():
    OpenDNS = "/storage/.config/resolv.conf"
    DefaDNS = "/run/connman/resolv.conf"
    if not (os.path.exists(OpenDNS)) or not (os.path.exists(DefaDNS)):
        return False

    with open(OpenDNS, 'r') as f:
        OpenDNS_IP = re.search("(\d+[.]+\d+[.]+\d+[.]+\d+)",f.read(),flags=re.IGNORECASE).group(1)

    with open(DefaDNS, 'r') as f:
        DefaDNS_IP = re.search("(\d+[.]+\d+[.]+\d+[.]+\d+)",f.read(),flags=re.IGNORECASE).group(1)

    if OpenDNS_IP == DefaDNS_IP:
        return True

    return False


@plugin.route('/play/<genre>/<url>')
def play_episode(url, genre):
    Flag = CheckDNS()
    if Flag == False:
        vpn.changeConnection()

    global quality_tbl
    plugin.log.debug(url)
    resolution = quality_tbl[ plugin.get_setting('quality', int) ]
    use_mp4_url = plugin.get_setting('mp4_url', bool)

    if use_mp4_url:
        info = scraper.extractVideoUrl(url, referer=url)
        if info is None:
            info = scraper.guessVideoUrl(url, genre=genre)
            plugin.log.info("use guessed url")
    else:
        info = scraper.extractStreamUrl(url, referer=url)

    if info is None:
        xbmc.executebuiltin( "Notification(영상 소스를 찾을 수 없습니다, 잠시 후 다시 시도해 보세요.,10000)" )
        vpn.disconnect()
        return plugin.finish(None, succeeded=False)

    plugin.log.debug("resolution: "+resolution)
    avail_resolutions = info['videos'].keys()
    if not resolution in avail_resolutions:
        resolution = avail_resolutions[0]
    video = info['videos'][resolution]

    if re.search('1080',video['url']):
        new_video=re.sub('1080','480', video['url'])
    else:
        new_video=video['url']

    #if info is not None:
    if Flag == False:
        vpn.disconnect()

    plugin.play_video( {'label':info['title'], 'path':new_video} )

    return plugin.finish(None, succeeded=False)

def is_connected():
    pingOutput = os.system("ping -c 1 " + "google.com")
    if pingOutput == 0:
        return True
    else:
        time.sleep(2)
        pingOutput = os.system("ping -c 1 " + "google.com")
        if pingOutput == 0:
            return True
        else:
            return False

if __name__ == "__main__":
    if is_connected():
        vpn.disconnect()
        plugin.run()

# vim:sw=4:sts=4:et
