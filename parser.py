#!/usr/bin/python

from html.parser import HTMLParser


path = 'tst'
path = '/cygdrive/c/Users/jhammer/Desktop/testpage2.htm'
fin = open(path, 'r')


r = fin.read()
fin.close()



class CryptoHistoryParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

        self.PS_NO = 0
        self.PS_IN_TBODY = 1
        self.PS_IN_TR = 2
        self.PS_IN_TD1 = 3
        self.PS_IN_TD2 = 4

        self.parse_status = self.PS_NO

        self.output = []
        self.last_date = ''


    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.parse_status = self.PS_IN_TBODY
        elif  self.parse_status == self.PS_IN_TBODY and tag == 'tr':
            self.parse_status = self.PS_IN_TR
        elif self.parse_status == self.PS_IN_TR and tag == 'td':
            self.parse_status = self.PS_IN_TD1
        elif self.parse_status == self.PS_IN_TD1 and tag == 'td':
            self.parse_status = self.PS_IN_TD2
        elif self.parse_status == self.PS_IN_TD2:
            self.parse_status = self.PS_IN_TBODY




    def handle_endtag(self, tag):
        if tag == 'tbody':
            self.parse_status = self.PS_NO

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self.parse_status == self.PS_IN_TD1:
            # print 'DATE: ' + data
            self.last_date = data
        elif self.parse_status == self.PS_IN_TD2:
            # print 'VALUE: ' + data + '\n\n'
            if self.last_date:
                self.output.append((self.last_date, data))

    def feed(self, input_string):
        HTMLParser.feed(self, input_string)
        return self.output


myparser = CryptoHistoryParser()

output = myparser.feed(r)

for x in output:
    print x[0] + ':' + x[1]


