#!/usr/bin/python

import httplib, json, time

conn = httplib.HTTPSConnection('api.coinmarketcap.com')

conn.request('GET', '/v1/ticker/?limit=100')

r = conn.getresponse()

if r.status != 200:
    raise 'http returned: ' + r.status + ', ' + r.reason

data = r.read()

js = json.loads(data)


while True:
    t = int(time.time())
    print 'data update started (' + time.ctime(t) + ')'
    for curr in js:
        name, value = curr['id'], curr['price_usd']

        f = open('data/' + name, 'a')
        f.write(str(t) + ':' + value + '\n')
        f.close()

    t = time.ctime()
    print 'data update finished (' + t + ')'

    time.sleep (600)





