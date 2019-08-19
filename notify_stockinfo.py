#!/bin/python3
# -*- coding: UTF-8 -*-
#python html.parser


import os
import time
from urllib.request import urlopen
import smtplib
from email.mime.text import MIMEText
import threading
import logging


HTML_STR = 'http://hq.sinajs.cn/?func=getData._hq_cron();&list='
SEL_LIST    = ['sh000001', 'sh601398', 'sh510880']  
NAME_LIST    = ['上证综指', '工商银行', '红利etf']  
HIGH_LIST    = [3000, 5.9, 2.9]  
LOW_LIST    = [2700, 5.4, 2.6]  
ALERT_LIST    = [False, False, False]  
RCV_EMAIL = 'liu198456@126.com'

def onlyNum(s,oth=','):
    s2 = s.lower();
    my_filter = '0123456789.'
    for c in s2:
        if c != oth and c not in my_filter:
            s = s.replace(c, '')
    return s;

def send_mail(to, subject, str_content):
    from_email = os.environ.get('MAIL_USERNAME')
    mail_password = os.environ.get('MAIL_PASSWORD')
    mail_server = os.environ.get('MAIL_SERVER')
    mail_srvport = os.environ.get('MAIL_SERVER_PORT')
    msg = MIMEText(str_content)
    msg['From'] = from_email
    msg['To'] = to 
    msg['Subject'] = subject
    email_server = smtplib.SMTP(mail_server, 25)
    email_server.set_debuglevel(1)
    email_server.login(from_email, mail_password)
    email_server.sendmail(from_email, [to], msg.as_string())
    email_server.quit()

def thread_notify_stock(delay):
    global ALERT_LIST
    global HIGH_LIST
    global LOW_LIST
    global NAME_LIST
    global RCV_EMAIL
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
    print('thread notify stock has entered')
    while True:
        curr_datetime = time.localtime()
        if curr_datetime.tm_hour == 8:
            for alert in ALERT_LIST:
                alert = False
            for alert in ALERT_LIST:
                print (alert)
        if curr_datetime.tm_hour >= 9 and curr_datetime.tm_hour <= 15:
            strdate = time.strftime("%Y.%m.%d", curr_datetime)
            str_message = strdate + ':\n';

            response = urlopen(HTML_STR)
            response_encoding = response.headers.get_content_charset()
            print(response_encoding)
            str_content = response.read().decode(response_encoding)
            print(str_content)
            #logging.info(str_content)
            lines = str_content.split('\n')
            index = 0;
            b_notify = False
            for line in lines:
                s1 = onlyNum(line)
                print(s1)
                if s1.count(',') > 3:
                    str_val = s1.split(',')[3];
                    f_val = float(str_val)
                    if not ALERT_LIST[index] and f_val <= LOW_LIST[index]:
                        str_message = str_message + NAME_LIST[index] + ' ' + str_val + ', '
                        ALERT_LIST[index] = True
                        b_notify = True
                    if not ALERT_LIST[index] and f_val >= HIGH_LIST[index]:
                        str_message = str_message + NAME_LIST[index] + ' ' + str_val + ', '
                        ALERT_LIST[index] = True
                        b_notify = True
                index = index + 1
            if b_notify:
                #logging.info (str_message)         
                send_mail(RCV_EMAIL,  'stock chance', str_message) 
        print('thread notify stock is running')
        time.sleep(delay)


def main():
    logging.basicConfig(filename='log_notify_stock.txt', level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s', datefmt='%Y/%m/%d %I:%M:%S')
try:
    thread_notify = threading.Thread( target = thread_notify_stock, args = (600, ) )
    thread_notify.start()
except:
    print('Error: unable to start thread')



if __name__ == '__main__':
    main()


