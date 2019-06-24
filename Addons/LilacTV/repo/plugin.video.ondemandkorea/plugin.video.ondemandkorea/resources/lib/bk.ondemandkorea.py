# -*- coding: utf-8 -*-
"""
    ondemandkorea.com

    /includes/latest.php?cat=<name>
    /includes/episode_page.php?cat=<name>&id=<num>&page=<num>
"""
import urllib, urllib2
import re
import json
from bs4 import BeautifulSoup
import time
import random

root_url = "http://www.ondemandkorea.com"
#cat_json_url = root_url+"/includes15/categories/{genre:s}_{language:s}.json?cb={timestamp:d}"
cat_json_url = root_url+"/includes15/categories/{genre:s}_{language:s}.json"
mp4_url = "http://{hostname:s}.ondemandkorea.com/{genre:s}/{program:s}/{program:s}_{date:s}.{resolution:s}.{bitrate:s}.mp4"
img_base = "http://max.ondemandkorea.com/includes/timthumb.php?w=175&h=100&src="
# mimic iPad
default_hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Connection': 'keep-alive'}
tablet_UA = 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Safari/535.19'

#eplist_url = "/includes/episode_page.php?cat={program:s}&id={videoid:s}&page={page:d}"
eplist_url = "/includes15/episode_page/"

bitrate2resolution = {
    196:'180',
    396:'240',
    796:'300',
    1296:'360',
    1596:'480',
    2296:'720'
}

def parseTop(koPage=True):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    items = []
    for node in soup.find('div', {'id':'menu-category'}).findAll(lambda tag: tag.name=='a' and '.html' in tag['href']):
        items.append(node['href'])
    return items

def DebugbyBJ(text):
  fo=open("/storage/DebubyBJ.txt","w")
  fo.write(text)
  fo.close()


def GetTITLE(filename):
    fi=open(filename)
    lines=fi.readlines()
    fi.close()  

    for line in lines:
      if "\"title_kr\": \"" in line:
        item=line.split("\"")
        result=item[3]
        return result

    return "Title"

def GetItemTitle(item_html):
  url = root_url+item_html
  req = urllib2.Request(url, headers=default_hdr)  
  html = urllib2.urlopen(req).read().decode('utf-8')
  #title = re.compile('<title>(.*?)</title>', re.S).search(html).group(1).strip()
  #title = re.compile('^\"title_kr\":',re.M).search(html)

  f = open("/storage/html1.txt","w")
  f.write(html.encode('utf-8'))
  f.close()

  title = GetTITLE("/storage/html1.txt")

  return title

def parseGenre(genre, sortFlag, koPage=True):
    #ts = int(time.mktime(time.gmtime()) / 1000 / 60 / 5)
    lang = "kr" if koPage else "en"    
    url = cat_json_url.format(genre=genre, language=lang)    
    req  = urllib2.Request(url, headers=default_hdr)
    jstr = urllib2.urlopen(req).read()
    obj = json.loads(jstr)    

    if sortFlag:
        sorted_obj = sorted(obj, key=lambda x : x['latest'], reverse=True)
    else:
        sorted_obj = sorted(obj, key=lambda x : x['popular'], reverse=True)
    items = []
    flag1 = False
    for item in sorted_obj:
        if sortFlag:
            if item['onAir'] == 1:
                #Title = item['title']
                #if not flag1:
                #    Title = GetItemTitle(item['postName'])
                #    flag1 = True
                items.append({'title':item['title'], 'url':item['postName'], 'thumbnail':item['img']})
                #DebugbyBJ(str(item['postName']))
        else:
            items.append({'title':item['title'], 'url':item['postName'], 'thumbnail':item['img']})            
        
    return items

def parseEpisodePage(page_url, page=1, koPage=True):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    result = {'episode':[]}
    for node in soup.findAll('div', {'class':re.compile('^(?:ep|ep_last)$')}):
        if not node.b:
            continue
        title = node.b.string.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
        thumb = node.find('img', {'title':True})['src']
        dt = node.b.findNextSibling(text=True)
        bdate = dt.string.split(':',1)[1].strip() if dt else ''
        result['episode'].append({'title':title, 'broad_date':bdate, 'url':root_url+node.a['href'], 'thumbnail':thumb})
    # no page navigation
    return result

def GetEpisode():
    fi=open("/storage/html.txt")
    lines=fi.readlines()
    fi.close()  

    for line in lines:
      if "includes15/episode_page" in line:
        item=line.split("/")
        result=item[3]
        return result

    return "error"

def parseEpisodePage2(page_url, page=1, koPage=True):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read().decode('utf-8')
    # 1. 
    #   $.getJSON( "/includes/episode_page.php", {cat: '<program>',id: <videoid>,page : pg)
    # 2. 
    #   "program" : "<program>",
    #   "videoid" : "<videoid>",

    f = open("/storage/html.txt","w")
    f.write(html.encode('utf-8'))
    f.close()

    pagedata = GetEpisode()

    pagedata_url = pagedata.replace("9999", str(page));
    list_url = root_url+eplist_url+pagedata_url

    #match = re.compile("getJSON\( *\"/[^\"]*\", *{ *cat: *'([^']*)', *id: *(\d+)"). search(html)
    #if match:
    #    program, videoid = match.group(1,2)
    #else:
    #    program = re.compile('"program" *: *"(.*?)"').search(html).group(1)
    #    videoid = re.compile('"videoid" *: *(\d+)').search(html).group(1)
    #list_url = root_url+eplist_url.format(program=program, videoid=videoid, page=page)

    req  = urllib2.Request(list_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    req.add_header('Referer', page_url)
    jstr = urllib2.urlopen(req).read()
    obj = json.loads(jstr)

    result = {'episode':[]}
    for item in obj['list']:
        result['episode'].append({'title':item['title'], 'broad_date':item['onAirDate'], 'url':root_url+"/"+item['url'], 'thumbnail':img_base+item["thumbnail"]})
    if obj['curPage'] > 1:
        result['prevpage'] = page-1
    if obj['curPage'] < obj['numPages']:
        result['nextpage'] = page+1
    return result

# m3u8
def extractStreamUrl(page_url, koPage=True, referer=None):
    req  = urllib2.Request(page_url, headers=default_hdr)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    if referer:
        req.add_header('Referer', referer)
    html = urllib2.urlopen(req).read().decode('utf-8')
    vid_title = re.compile('<title>(.*?)</title>', re.S).search(html).group(1).strip()
    match = re.compile("""(http[^'"]*m3u8)""").search(html, re.I|re.U)
    if not match:
        return None
    
    vid_url = match.group(1)
    title=GetTITLE("/storage/html.txt")
    #title = vid_title.split('-')[0]

    videos = dict()
    for bitrate, resolution in bitrate2resolution.iteritems():
        videos[resolution] = {'url':vid_url}
    return {'title':title, 'videos':videos}

# mp4
def extractVideoUrl(page_url, koPage=True, referer=None):
    req  = urllib2.Request(page_url)
    req.add_header('User-Agent', tablet_UA)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    if referer:
        req.add_header('Referer', referer)
    html = urllib2.urlopen(req).read().decode('utf-8')
    vid_title = re.compile('<div id="title">(.*?)</div>', re.S).search(html).group(1).strip()
    match = re.compile("""(http[^'"]*mp4)""").search(html)
    if not match:
        return None
    vid_url = match.group(1)
    videos = dict()
    for bitrate, resolution in bitrate2resolution.iteritems():
        videos[resolution] = {'url':vid_url.replace('360p', resolution)}
    return {'title':vid_title, 'videos':videos}

def guessVideoUrl(page_url, genre='drama', koPage=True):
    hostname = "lime%02d" % random.randint(1,8)
    if genre == "variety":
        genre = "variety2"

    req = urllib2.Request(page_url)
    req.add_header('User-Agent', tablet_UA)
    if koPage:
        req.add_header('Accept-Langauge', 'ko')
        req.add_header('Cookie', 'language=kr')
    html = urllib2.urlopen(req).read().decode('utf-8')
    vid_title = re.compile('<div id="title">(.*?)</div>', re.S).search(html).group(1).strip()
    thumb = re.compile('<link rel="image_src" href="([^"]*)"').search(html).group(1)
    program, date = re.compile("/([^/_]*)_(\d+)").search(thumb).group(1,2)

    videos = dict()
    for bitrate, resolution in bitrate2resolution.iteritems():
        vid_url = mp4_url.format(hostname=hostname, program=program, date=date, resolution=resolution, bitrate=str(bitrate)+'k', genre=genre)
        videos[resolution] = {'url':vid_url}
    return {'title':vid_title, 'videos':videos}

if __name__ == "__main__":
    #print parseTop()
    print parseGenre( "variety" )
    #print parseEpisodePage( root_url+"/infinite-challenge-e452.html" )
    print parseEpisodePage2( root_url+"/infinite-challenge-e452.html", page=2 )
    #print extractStreamUrl( root_url+"/infinite-challenge-e452.html" )
    #print extractVideoUrl( root_url+"/infinite-challenge-e452.html" )
    print parseEpisodePage2( root_url+"/mystery-music-show-mask-king-e31.html" )
    print extractVideoUrl( root_url+"/mystery-music-show-mask-king-e31.html" )
    print guessVideoUrl( root_url+"/mystery-music-show-mask-king-e31.html", genre='variety' )

# vim:sw=4:sts=4:et
