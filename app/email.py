#email.py
# -*- coding: utf-8 -*-
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from flask import render_template, current_app
from . import logger

def get_maintype(suffix):
    return 'text'
def get_subtype(suffix):
    d_subtypes = {
        'txt': 'plain',
        'pdf': 'pdf',
        'mobi': 'mobi',
    }
    subtype = d_subtypes.get(suffix)
    if subtype:
        logger.info('suffix %s subtype %s ' % (suffix, subtype) )
        return subtype
    logger.info('suffix %s' % suffix)
    return 'plain'


def send_mail(to, subject, template, attachments = [], **kwargs):
    from_email = current_app.config['MAIL_USERNAME']
    msg = EmailMessage()
    #msg.set_content(render_template(template + '.txt', **kwargs))
    msg.add_alternative(render_template(template + '.html', **kwargs), subtype='html')
    msg['From'] = from_email
    msg['To'] = to 
    msg['Subject'] = current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject
    for fl in attachments:
        suffix = fl.split('.')[1]
        subtype = get_subtype(suffix)
        with open(fl, 'rb') as fp:
            atm = fp.read()
        msg.add_attachment(atm, maintype='text', subtype=subtype, filename=fl)
    email_server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_SERVER_PORT'])
    email_server.set_debuglevel(1)
    email_server.login(from_email, current_app.config['MAIL_PASSWORD'])
    email_server.send_message(msg)
    email_server.quit()

