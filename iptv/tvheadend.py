# -*- coding: utf-8 -*-
import sys
import os
import re
import chardet


__base_m3u_file__ = "playlist-base.m3u"
__out_m3u_file__ = "update/playlist-tvheadend"

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

	temp = "imsi.m3u"
	os.system("cp "+m3u_file+" "+temp)

	# list = ["List1.m3u", "List2.m3u", "List3.m3u"]
	# tFp = open(temp, "a+")
	# for n in range(0,3):
	# 	lFp = open(list[n])
	# 	List = lFp.read()
	# 	lFp.close()
	# 	tFp.write(List)
	# tFp.close()

	bfp = open(__base_m3u_file__)
	bm3u_sgml = bfp.read()
	bfp.close()

	blines = CheckEncode(bm3u_sgml)
	if blines < 0:
		return False

	for n in range(1,11):
		ifp = open(temp)
		m3u_sgml = ifp.read()
		ifp.close()
		lines = CheckEncode(m3u_sgml)
		if lines < 0:
			return False

		newList = []
		blcnt = 0
		blines = CheckEncode(bm3u_sgml)
		for bline in blines:
			sndx = bline.upper().find('#EXTINF')
			if sndx >= 0 and blines[blcnt+1].find('http://') < 0:
				m = re.search(r'#EXTINF:-1\s+.+\s.+,(.+)', bline, flags=re.IGNORECASE)
				channel = m.group(1)
				lcnt = 0
				for line in lines:
					tndx = line.upper().find('#EXTINF')
					if tndx >= 0:
						m = re.search('#EXTINF:-1,*(.+)', line, flags=re.IGNORECASE)
						if channel == m.group(1) and lines[lcnt+1].find('http://') >= 0:
							blines[blcnt+1] = lines[lcnt+1]
							lines[lcnt+1] = ""
							#print m.group(1) + " " + blines[blcnt+1]
							break
					lcnt += 1
			blcnt += 1
			newList.append(bline)

		ofp = open(__out_m3u_file__+str(n)+".m3u", 'w')
		ofp.write('#EXTM3U'+'\n')
		for line in newList:
			ofp.write(line+'\n')
		ofp.close()

		ofp = open(temp, 'w')
		for line in lines:
			ofp.write(line+'\n')
		ofp.close()

	os.system("rm "+temp)

	return True

###################################################################################################
def doConvert():
	if len(sys.argv) <= 1:
		usage()
	for iptv_file in sys.argv[1:]:
		if UpdateChannelURL(iptv_file):
			os.system("./UploadM3U")
			print "Updating <%s> OK!" % iptv_file
		else:
			print "Updating <%s> Failture!" % iptv_file
###################################################################################################
if __name__ == '__main__':
	doConvert()
