#email.py
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from flask import render_template

def send_mail(to, subject, template, **kwargs):
    from_email = app.config['MAIL_USERNAME']
    msg = MIMEText(render_template(template + '.txt', **kwargs))
    msg['From'] = from_email
    msg['To'] = to 
    msg['Subject'] = app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject
    email_server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_SERVER_PORT'])
    email_server.set_debuglevel(1)
    email_server.login(from_email, app.config['MAIL_PASSWORD'])
    email_server.sendmail(from_email, [to], msg.as_string())
    email_server.quit()

