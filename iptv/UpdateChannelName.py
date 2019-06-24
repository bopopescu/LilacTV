# -*- coding: utf-8 -*-
import sys
import os
import re
import chardet


#__base_m3u_file__ = "playlist-base.m3u"
#__base_m3u_file__ = "playlist-lilactvHD2.m3u"
__out_m3u_file__ = "playlist-test.m3u"

ChannelIndex = [["SBS", "sbs"],
				["SBS funE", "SBS fun E"],
				["KBS1", "kbs1"],
				["KBS2", "kbs2"],
				["KBS JOY", "KBS Joy"],
				["MBC", "mbc"],
				["MBC Every1","MBC every1"],
				["EBS", "EBS1"],
				["EBS2", "ebs2"],
				["JTBC", "jtbc"],
				["MBN", "mbn"],
				["tvN", "TVN"],
				["채널A", "Channel A"],
				["TV조선", "TV Chosun"],
				["Mnet", "MNET"],
				["연합뉴스TV", "newsy"],
				["YTN", "ytn"],
				["JTBC Golf", "JTBC GOLF"],
				["SBS GOLF", "sbs golf"],
				["SBS Sports", "SBS스포츠"],
				["KBS N Sports", "KBSN스포츠"],
				["MBC SPORTS+", "MBC스포츠+"],
				["SPOTV", "spotv"],
				["SPOTV+", "spotv+"],
				["SPOTV2","spotv2"],
				["SkySports", "sky Sports"],
				["JTBC3", "JTBC3 FOXSPORTS"],
				["OGN", "ogn"],
				["SPOTV Games", "SPOTV GAMES"],
				["OCN", "ocn"],
				["스크린", "Screen"],
				["채널CGV", "Ch CGV"],
				["슈퍼액션", "Super Action"],
				["mplex", "Mplex"],
				["FOX", "Fox"],
				["AXN", "Axn"],
				["XtvN", "XTM"],
				["O tvN", "OTVN"],
				["온스타일", "On Style"],
				["올리브", "Olive"],
				["FISHING TV", "Fishing TV"],
				["FTV", "Ftv"],
				["바둑TV", "바둑 TV"],
				["마운틴TV", "Moutain TV"],
				["SkyTravel", "sky Travel"],
				["NGC", "내셔널지오그래프"],
				["디스커버리채널", "Discovery Channel"],
				["History", "히스토리"],
				["JEI 재능TV", "JEI재능TV"],
				["Tooniverse", "투니버스"],
				["Disney Channel", "디즈니채널"],
				["디즈니주니어", "Disney Juior"]]	

###################################################################################################
def usage(msg=None, exit_code=1):
	print_msg = """
usage %s iptv.m3u [...]
	Update channel's url into your m3u file with same channel name.
	By Jin Kim <railrac23@gmail.com>
""" % os.path.basename(sys.argv[0])
	if msg:
		print_msg += '%s\n' % msg
	print print_msg
	sys.exit(exit_code)
###################################################################################################

def CheckEncode(sgml):
	chdt = chardet.detect(sgml)
	if chdt['encoding'] != 'UTF-8':
		sgml = unicode(sgml, chdt['encoding'].lower()).encode('utf-8')

	try:
		fndx = sgml.find('#EXTINF')
	except Exception, e:
		print chdt
		raise e

	if fndx < 0:
		return fndx

	sgml = sgml[fndx:]
	lines = sgml.split('\n')

	return lines


def FindChannelName(channel, name):
	index = ChannelIndex.index(channel)
	for i in range(len(ChannelIndex[index])):
		if ChannelIndex[index][i] == name:
			return True
	return False


def UpdateChannelURL(m3u_file):
	if not os.path.exists(m3u_file):
		sys.stderr.write('Cannot find m3u file <%s>\n' % m3u_file)
		return False	

	ifp = open(m3u_file)
	m3u_sgml = ifp.read()
	ifp.close()	

	lines = CheckEncode(m3u_sgml)
	if lines < 0:
		return False

	newList = []
	for line in lines:
		sndx = line.upper().find('#EXTINF')
		if sndx >= 0:
			m = re.search(r'#EXTINF:-1.*,\d+_(.+)', line, flags=re.IGNORECASE)
			channel = m.group(1)
			newList.append('#EXTINF:-1,'+channel)
			print channel
		else:
			newList.append(line)
	
	ofp = open(__out_m3u_file__, 'w')
	ofp.write('#EXTM3U'+'\n')
	for line in newList:
		ofp.write(line+'\n')
	ofp.close()

	return True

###################################################################################################
def doConvert():
	if len(sys.argv) <= 1:
		usage()
	for iptv_file in sys.argv[1:]:
		if UpdateChannelURL(iptv_file):
			print "Updating <%s> OK!" % iptv_file
		else:
			print "Updating <%s> Failture!" % iptv_file
###################################################################################################
if __name__ == '__main__':
	doConvert()

