#!/usr/bin/python

import httplib, time, sys
from history_parser import CryptoHistoryParser


# if len(sys.argv) < 2:
#    print 'args needed'
#    sys.exit()
 
#currency_name = sys.argv[1]

currencies_list = ['bitcoin']

today = time.strftime('%Y%m%d', time.gmtime())
  
conn = httplib.HTTPSConnection('coinmarketcap.com')
  
for currency_name in currencies_list:

    print currency_name + ' requesting history...      ',

    conn.request('GET', '/currencies/' + currency_name + '/historical-data/?start=20130428&end=' + today)
    
    r = conn.getresponse()
    
    if r.status != 200:
        print 'ERR: could not get history of ' + currency_name + '(' + str(r.status) + ')\n'
        conn = httplib.HTTPSConnection('coinmarketcap.com')
        continue
        #raise 'http returned: ' + r.status + ', ' + r.reason
    
    data = r.read()
    
    myParser = CryptoHistoryParser()
    
    output = myParser.feed(data)
    
    f = open('all_history/' + currency_name, 'w')
    
    f.write(output)
    f.close()
    print 'DONE\n'
    time.sleep(10)
