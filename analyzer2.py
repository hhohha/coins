#!/usr/bin/python

import sys, datetime

class cHistory:
    def __init__(self, currency):
        self.cur_avg = 0.0
        self.avg_len = 0
        self.avg_sum = 0
        self.currency = currency 
        self.record = []
        self.buy_threshold = 0.0     
        self.sell_threshold = 0.0

    def reset(self):
        self.cur_avg = 0.0
        self.avg_len = 0
        self.avg_sum = 0

    def out(self):
        for r in self.record:
            print r
    
    def set_thresholds(self, buy, sell):
        self.buy_threshold = buy    
        self.sell_threshold = sell
            
    def analyze(self, upto_date = datetime.date.today()):
        buying, selling = True, False
        earned, invested_crypto, invested_fiat, loops, buy_rate, r = 0, 0, 0, 0, 0.0, 0.0
    
        i = len(self.record) - 1
        while i >=0 and self.record[i].date <= upto_date:            
            r = self.record[i].rate
            self.update_avg(i)
            i -= 1
            
            if self.avg_len < 30:
                continue
                   
            if r < self.cur_avg * self.buy_threshold and buying:
                invested_fiat += 100
                invested_crypto = 100.0 / r
                buying, selling = False, True
                buy_rate = r

                #print 'buying ' + currency + ' for 100 dollars with rate of ' + str(r)
                #print 'now have ' + str(invested_crypto) + ' of ' + currency + '\n\n'
                #print 'loop: ' + str(loops) + '\n\n'


            if selling and r > buy_rate * self.sell_threshold:
                
                selling, buying = False, True
                earned += invested_crypto * r - 100
                
                #print 'selling ' + str(invested_crypto) + ' of ' + currency + ' for ' + str(r) + '$'
                #print 'now I have ' + str(invested_crypto * r) + ' dollars\n\n'
                #print 'loop: ' + str(loops) + '\n\n'
            
        if selling:
            earned += invested_crypto * r - 100
            #print 'not sold yet'
            #print 'i now have ' + str(invested_crypto * r) + ' still in ' + currency + '\n\n'
     
        return earned, invested_fiat
                
    def update_avg(self, i):
        r = self.record[i].rate
        self.avg_sum += r
        
        if self.avg_len < 30:
            self.avg_len += 1
        else:
            try:
                self.avg_sum -= self.record[i+29].rate
            except IndexError:
                print 'CRAP EXCEPTION'
                
                sys.exit()
                
            
        self.cur_avg = float(self.avg_sum) / self.avg_len 
        
          
class cDayRate:
    def __init__(self, date, rate):
        self.date = date
        self.rate = rate 

    def __repr__(self):
        return str(self.date) + ' - ' + str(self.rate) 


if len(sys.argv) < 2:
    sys.exit()

  
currency = sys.argv[1]





fin = open('all_history/' + currency, 'r')

myHistory = cHistory(currency)

for line in fin:
    idx = line.index(':')
    dtm = datetime.datetime.strptime(line[:idx], '%b %d, %Y')
    date = datetime.date(dtm.year, dtm.month, dtm.day)
    rate = float(line[idx+1:])
    
    myHistory.record.append(cDayRate(date, rate))
    
     
fin.close()

print '\ninvestigating', currency.upper(), '\n'

sell_thresholds = [1.2, 1.4, 1.6, 1.8, 2.0, 2.5, 3.0, 4, 5]
buy_thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]

max_earned = [0, 0, 0]

for buy in buy_thresholds:
    for sell in sell_thresholds:
      myHistory.reset()  
      myHistory.set_thresholds(buy, sell)
      upto_date = datetime.date(2017, 1, 1)
      earned, invested = myHistory.analyze(upto_date)
      
      if earned > max_earned[0]:
          max_earned = [earned, buy, sell] 
      
      print 'buy threshold:', buy, '      sell threshold:', sell, '         invested: ', invested, '        earned:', earned
      
print '\n\nmaximum earned:', max_earned[0], '  buying coeff:', max_earned[1],'  selling coeff:', max_earned[2], '\n\n'   


