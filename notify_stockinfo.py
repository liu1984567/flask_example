#!/bin/python3
# -*- coding: UTF-8 -*-
#python html.parser


import os
import time
from urllib.request import urlopen
import smtplib
from email.mime.text import MIMEText


HTML_STR = 'http://hq.sinajs.cn/?func=getData._hq_cron();&list='
SEL_LIST    = ['sh000300', 'sh000016', 'sh000905', 'sh000947', 'sh000991', 'sh000912']  
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

def main():
    global SEL_LIST;
    global HTML_STR;
    count = len(SEL_LIST);
    strtmp = '';
    str_message = '';
    str_content = '';
    for i in range(0,count):
        strtmp = strtmp + SEL_LIST[i];
        if i < count - 1:
            strtmp = strtmp + ','
    HTML_STR = HTML_STR + strtmp;
    print(HTML_STR);
    

    strdate = time.strftime("%Y.%m.%d", time.localtime())
    str_message = strdate + ':\n';

    response = urlopen(HTML_STR)
    response_encoding = response.headers.get_content_charset()
    print(response_encoding)
    content = response.read()
    #print(content)
    str_content = content.decode(response_encoding)
    print(str_content)
    lines = str_content.split('\n')
    for line in lines:
        print(line)
        s1 = onlyNum(line)
        print(s1)
        if s1.count(',') > 3:
            str_val = s1.split(',')[3];
            print (str_val)
            str_message = str_message + str_val + ', ';
    print (str_message)         
    send_mail(RCV_EMAIL,  'stock chance', str_message) 


if __name__ == '__main__':
    main()


