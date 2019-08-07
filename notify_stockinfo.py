#!/bin/python3
# -*- coding: UTF-8 -*-
#python html.parser


import os
import time
from urllib.request import urlopen

HTML_STR = 'http://hq.sinajs.cn/?func=getData._hq_cron();&list='
SEL_LIST    = ['sh000300', 'sh000016', 'sh000905', 'sh000947', 'sh000991', 'sh000912']  
DATA_FILE = 'sina_finance_data_0.csv'

def onlyNum(s,oth=','):
    s2 = s.lower();
    my_filter = '0123456789.'
    for c in s2:
        if c != oth and c not in my_filter:
            s = s.replace(c, '')
    return s;

def main():
    global SEL_LIST;
    global HTML_STR;
    count = len(SEL_LIST);
    strtmp = '';
    for i in range(0,count):
        strtmp = strtmp + SEL_LIST[i];
        if i < count - 1:
            strtmp = strtmp + ','
    HTML_STR = HTML_STR + strtmp;
    print(HTML_STR);
    
    global DATA_FILE
    if not os.path.exists(DATA_FILE):
        fo = open(DATA_FILE, "w+");
        fo.write("date, " + strtmp + "\n");
        fo.close();

    fo = open(DATA_FILE, "a+");
    strdate = time.strftime("%Y.%m.%d", time.localtime())
    fo.write(strdate+", ");

    response = urlopen(HTML_STR)
    content = response.read()
    str_content = content.decode()# error decode
    print(str_ontent)
    lines = str_content.split('\n')
    for line in lines:
        print(line)
    count = content.count('\n');
    for strtmp in content.splitlines(count):
        #print strtmp
        s1 = onlyNum(strtmp)
        print(s1)
        if s1.count(',') > 3:
            print (s1.split(',')[3] )
            fo.write(s1.split(',')[3] + ", ");
    
    fo.write('\n');
    fo.close()


if __name__ == '__main__':
    main()


