# -*- coding: utf-8 -*-

import urlparse

from exoscrapers import sources_exoscrapers
from exoscrapers.modules import control

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
action = params.get('action')
mode = params.get('mode')
query = params.get('query')


def ScraperChoice():
    from exoscrapers import providerSources
    sourceList = sorted(providerSources())
    control.idle()
    select = control.selectDialog([i for i in sourceList])
    if select == -1: return
    module_choice = sourceList[select]
    control.setSetting('module.provider', module_choice)
    control.openSettings('0.1')


if action == "ExoscrapersSettings":
    control.openSettings('0.0', 'script.module.exoscrapers')

elif mode == "ExoscrapersSettings":
    control.openSettings('0.0', 'script.module.exoscrapers')


elif action == "ScraperChoice":
    ScraperChoice()


elif action == "toggleAll":
    sourcelist = []
    sourceList = sources_exoscrapers.all_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllHosters":
    sourcelist = []
    sourceList = sources_exoscrapers.hoster_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All Hoster providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllForeign":
    sourcelist = []
    sourceList = sources_exoscrapers.all_foreign_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All Foregin providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllSpanish":
    sourcelist = []
    sourceList = sources_exoscrapers.spanish_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All Spanish providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllGerman":
    sourcelist = []
    sourceList = sources_exoscrapers.german_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All German providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllGreek":
    sourcelist = []
    sourceList = sources_exoscrapers.greek_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All Greek providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllPolish":
    sourcelist = []
    sourceList = sources_exoscrapers.polish_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All Polish providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllPaid":
    sourcelist = []
    sourceList = sources_exoscrapers.all_paid_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All Paid providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllDebrid":
    sourcelist = []
    sourceList = sources_exoscrapers.debrid_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All Debrid providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")


elif action == "toggleAllTorrent":
    sourcelist = []
    sourceList = sources_exoscrapers.torrent_providers
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    #    xbmc.log('All Torrent providers = %s' % sourceList,2)
    control.openSettings(query, "script.module.exoscrapers")

if action == "Defaults":
    sourceList = ['1putlocker', '123movieshubz', '123123movies', 'animetoon', 'azmovie',
                  'cartoonhd', 'cmovieshdbz', 'extramovies', 'fmoviesio', 'freefmovies', 'freeputlockers',
                  'gowatchseries', 'hdbest', 'hdmto', 'hdonline', 'iwaatch', 'iwannawatch',
                  'movie4kis', 'myhdpopcorn', 'mymovie4k', 'mywatchepseries', 'primewire',
                  'projectfreetv', 'putlockeronl', 'reddit', 'seehd', 'seriesonline', 'sezonlukdizi',
                  'sharemovies', 'solarmoviefree', 'streamdreams', 'timewatch', 'toonget',
                  'tvbox', 'wannahd', 'watch32', 'watchepisodes', 'watchserieshd', 'xwatchseries',
                  '0day', '2ddl', '300mbdownload', '300mbfilms', 'ddlspot', 'directdl', 'filmxy',
                  'moviesleak', 'mvrls', 'myvideolink', 'rlsbb', 'scenerls', 'scenerlscom', 'scnsrc',
                  'tvdownload', 'ultrahd', '1337x', 'eztv', 'glodls', 'kickass2', 'limetorrents',
                  'magnetdl', 'mkvcage', 'piratebay', 'torrentapi', 'torrentdownloads', 'yifyddl',
                  'ytsam', 'zoogle']
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    control.openSettings(query, "script.module.exoscrapers")