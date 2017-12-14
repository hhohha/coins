#!/usr/bin/python

import sys

def calc_avg(arr):
    total = 0.0
    for n in arr:
        total += n
    return total / len(arr)


if len(sys.argv) < 4:
    sys.exit()
else:
    currency = sys.argv[1]
    buythreshold = float(sys.argv[2])
    sellthreshold = float(sys.argv[3])

print '================'
print currency 
print '================\n\n'


earned, invested_crypto = 0, 0

fin = open('test_data/' + currency, 'r')

history = fin.read().split()

fin.close()

avg_arr = []

i = len(history) - 1
loops = 0
buying = True
selling = False 
buy_rate = 0

while i >= 0 and loops < 30:
    n = float(history[i])
    avg_arr.append(n)
    i -= 1; loops += 1

while i >= 0:

    n = float(history[i])

    avg = calc_avg(avg_arr)
    avg_arr[loops % 30] = n
    loops += 1

    if n < avg*buythreshold and buying:
        #BUY

        invested_crypto = 100.0 / n
        buying = False; selling = True
        buy_rate = n

        print 'buying ' + currency + ' for 100 dollars with rate of ' + str(n)
        print 'now have ' + str(invested_crypto) + ' of ' + currency
        print 'loop: ' + str(loops) + '\n\n'


    if not buying and selling and n > buy_rate * sellthreshold:
        #SELL
        selling = False; buying = True

        print 'selling ' + str(invested_crypto) + ' of ' + currency + ' for ' + str(n) + '$'
        print 'now I have ' + str(invested_crypto * n) + ' dollars'
        print 'loop: ' + str(loops) + '\n\n'
        earned += invested_crypto * n - 100

    i -= 1

if selling:
    print 'not sold yet'
    print 'i now have ' + str(invested_crypto * n) + ' still in ' + currency
    earned += invested_crypto * n - 100

print '\n\n'
print 'total earned: ' + str(earned)
print '\n\n\n\n\n\n'

