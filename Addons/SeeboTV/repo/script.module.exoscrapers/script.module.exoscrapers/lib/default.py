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
    sourceList = ['1putlocker', '123movieshubz', 'animetoon', 'azmovie', 'bnwmovies',
                  'cartoonhd', 'cmovieshd', 'coolmoviezone', 'deepmovie', 'divxcrawler', 'extramovies', 'fmoviesio',
                  'freefmovies',
                  'gomoviesink', 'gowatchseries', 'hdmto', 'hdpopcorneu', 'iwaatch', 'iwannawatch',
                  'library', 'movie4kis', 'mycouchtuner', 'myhdpopcorn', 'onlineseries', 'primewire',
                  'projectfreetv', 'putlockerfree', 'putlockeronl', 'seehd', 'series9', 'seriesonline', 'sezonlukdizi',
                  'sharemovies', 'solarmoviefree', 'streamdreams', 'swatchseries', 'timewatch', 'toonget',
                  'tvbox', 'watchepisodes', 'watchserieshd', 'wnmnt', 'xwatchseries', 'yesmoviesgg',
                  '2ddl', '300mbdownload', '300mbfilms', 'ddlspot', 'directdl', 'ganool',
                  'maxrls', 'moviesleak', 'mvrls', 'myvideolink', 'rapidmoviez', 'rlsbb', 'sceneddl', 'scenerls',
                  'scenerlscom', 'ultrahd',
                  'warezmovies', '1337x', 'btdb', 'btscene', 'digbt', 'doublr', 'eztv', 'glodls', 'kickass2',
                  'limetorrents',
                  'magnetdl', 'mkvcage', 'piratebay', 'torrentapi', 'torrentdownloads', 'yify',
                  'yifyddl',
                  'ytsam', 'zoogle']
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, params['setting'])
    control.openSettings(query, "script.module.exoscrapers")
