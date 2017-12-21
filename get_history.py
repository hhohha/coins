#!/usr/bin/python

import httplib, time, sys
from history_parser import CryptoHistoryParser


# if len(sys.argv) < 2:
#    print 'args needed'
#    sys.exit()
 
#currency_name = sys.argv[1]

currencies_list = [
'0x',
'aeternity',
'aion',
'ardor',
'ark',
'augur',
'bancor',
'basic-attention-token',
'binance-coin',
'bitcoin',
'bitcoin-cash',
'bitcoindark',
'bitcoin-gold',
'bitconnect',
'bitshares',
'blocknet',
'byteball',
'bytecoin-bcn',
'bytom',
'cardano',
'chainlink',
'civic',
'cryptonex',
'dash',
'decentraland',
'decred',
'digibyte',
'digixdao',
'dogecoin',
'dragonchain',
'edgeless',
'einsteinium',
'electroneum',
'eos',
'ethereum',
'ethereum-classic',
'ethos',
'factom',
'funfair',
'gamecredits',
'gas',
'gnosis',
'golem-network-tokens',
'gxshares',
'hshare',
'iconomi',
'iota',
'komodo',
'kyber-network',
'lisk',
'litecoin',
'maidsafecoin',
'metal',
'metaverse',
'minexcoin',
'monaco',
'monacoin',
'monero',
'nav-coin',
'nem',
'neo',
'nexus',
'nxt',
'omisego',
'paypie',
'peercoin',
'pivx',
'populous',
'power-ledger',
'pura',
'qash',
'qtum',
'raiblocks',
'raiden-network-token',
'rchain',
'request-network',
'revain',
'ripple',
'salt',
'santiment',
'siacoin',
'status',
'steem',
'stellar',
'storj',
'stratis',
'streamr-datacoin',
'substratum',
'syscoin',
'tenx',
'tether',
'tron',
'vechain',
'verge',
'veritaseum',
'vertcoin',
'walton',
'waves',
'zcash',
'zcoin']

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
    print 'DONE'
    time.sleep(3)
