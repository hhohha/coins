#!/usr/bin/python

import httplib, time, sys
from history_parser import CryptoHistoryParser

if len(sys.argv) < 2:
    print 'args needed'
    sys.exit()

currency_name = sys.argv[1]
today = time.strftime('%Y%m%d', time.gmtime())

conn = httplib.HTTPSConnection('coinmarketcap.com')

conn.request('GET', '/currencies/' + currency_name + '/historical-data/?start=20130428&end=' + today)

r = conn.getresponse()

if r.status != 200:
    raise 'http returned: ' + r.status + ', ' + r.reason

data = r.read()


myParser = CryptoHistoryParser()

output = myParser.feed(data)

f = open('output', 'w')

f.write(output)
f.close()

