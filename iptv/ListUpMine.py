# -*- coding: utf-8 -*-
import sys
import os
import re
import chardet


__base_m3u_file__ = "playlist-base.m3u"
###################################################################################################
def usage(msg=None, exit_code=1):
	print_msg = """
usage %s iptv.m3u outfile[...]
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


def UpdateChannelURL(m3u_file, out_file):
	if not os.path.exists(m3u_file):
		sys.stderr.write('Cannot find m3u file <%s>\n' % m3u_file)
		return False

	ifp = open(m3u_file)
	m3u_sgml = ifp.read()
	ifp.close()

	lines = CheckEncode(m3u_sgml)
	if lines < 0:
		return False

	bfp = open(__base_m3u_file__)
	bm3u_sgml = bfp.read()
	bfp.close()

	blines = CheckEncode(bm3u_sgml)
	if blines < 0:
		return False

	newList = []
	lcnt = 0
	for line in lines:
		sndx = line.upper().find('#EXTINF')
		if sndx >= 0:
			m = re.search(r'#EXTINF:-1.*,(.+)', line, flags=re.IGNORECASE)
			channel = m.group(1)
			for bline in blines:
				bndx = bline.upper().find('#EXTINF')
				if bndx >= 0:
					m = re.search(r'#EXTINF:-1\s+.+\s.+,(.+)', bline, flags=re.IGNORECASE)
					if channel == m.group(1):
						newList.append('#EXTINF:-1,'+channel)
						newList.append(lines[lcnt+1])
						break
		lcnt += 1

	ofp = open(out_file+".m3u", 'w')
	ofp.write('#EXTM3U'+'\n')
	for line in newList:
		ofp.write(line+'\n')
	ofp.close()

	return True

###################################################################################################
def doConvert():
	if len(sys.argv) <= 2:
		usage()
	iptv_file = sys.argv[1]
	out_file = sys.argv[2]
	if UpdateChannelURL(iptv_file,out_file):
		print "Updating <%s> OK!" % iptv_file
	else:
		print "Updating <%s> Failture!" % iptv_file
###################################################################################################
if __name__ == '__main__':
	doConvert()
