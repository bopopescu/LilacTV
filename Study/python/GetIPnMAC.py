# -*- coding: utf-8 -*-
import socket
import urllib
import re
import uuid

wan = re.search(re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),urllib.urlopen('http://checkip.dyndns.org').read()).group()
print ('WAN  : ' + wan)
print ('MAC  : ' + hex(uuid.getnode()))

#tail -n 10000 /opt/lampstack-5.6.24-0/apache2/logs/access_log | cut -d\  -f 1 | sort | uniq -c | sort -k 1 -rn | more
