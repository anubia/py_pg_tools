#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#from connecter import Connecter
#from const.const import Messenger
#from const.const import Queries
#import psycopg2  # To work with PostgreSQL
#import psycopg2.extras  # To get real field names from PostgreSQL

#connecter = Connecter('localhost', 'anubia', 5433)
#query1 = "REVOKE ALL ON DATABASE my_replicated_db3 FROM openerp61;"
#query2 = "GRANT CONNECT ON DATABASE my_replicated_db3 TO openerp61;"

#try:
    #connecter.cursor.execute(query1)
    ##connecter.cursor.execute(query2)

#except Exception as e:
    ## Rollback to avoid errors in next queries because of waiting
    ## this transaction to finish
    #connecter.conn.rollback()
    #print(str(e))

#from crontab import CronTab

#cron = CronTab(user=True)

#job = cron.new(command='python3 /mnt/store1/devel/code/ide-workspace/py_pg_tools/py_pg_tools.py v -ch localhost -cu anubia -cp 5432 -d devel__v61__test_01 -zc config/mailer/mailer.cfg')

#job.minute.on(2)
#job.hour.on(12)
#cron.write()
#print(cron.render())

#import socket
#print(socket.gethostname())

#import smtplib
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart

#title = 'My title'
#html = '<h2>{title}: <span style="color:green">OK</span></h2>\n'.format(title=title)
#text = 'Tu servidor de correo es una basura sin HTML.'

#message = MIMEMultipart('alternative')
#message['From'] = 'Sender Name <sender@server>'
#message['To'] = 'Receiver Name <receiver@server>'
#message['Cc'] = 'Receiver2 Name <receiver2@server>'
#message['Subject'] = 'Any subject'

## Record the MIME types of both parts - text/plain and text/html.
#part1 = MIMEText(text, 'plain')
#part2 = MIMEText(html, 'html')

## Attach parts into message container.
## According to RFC 2046, the last part of a multipart message, in this case
## the HTML message, is best and preferred.
#message.attach(part1)
#message.attach(part2)

#msg_full = message.as_string()

#server = smtplib.SMTP('smtp.gmail.com:587')
#server.starttls()
#server.login('jfv@anubia.es', '1337!vomisacaasi')
#server.sendmail('jfv@anubia.es', ['jfv@anubia.es'], msg_full)
#server.quit()

#import netifaces

#netifaces_ips = []
#for netiface in netifaces.interfaces():
    #addrs = netifaces.ifaddresses(netiface)
    #for item in addrs[netifaces.AF_INET]:
        #if 'addr' in item.keys():
            #netifaces_ips.append({netiface: item['addr'], })
            #break
#print(netifaces_ips)

import smtplib
# Sending the mail
try:
    #server = smtplib.SMTP('smtp.gmail.com:587')
    server = smtplib.SMTP('localhost:25')
    server.ehlo()
    server.starttls()
    server.ehlo()
    #server.login(self.from_info['email'], self.from_info['pwd'])
    #server.login(None, None)
    server.sendmail('Juan <jfv@anubia.es>', ['jfv@anubia.es'], 'Hi')
    server.quit()

except smtplib.SMTPException as e:
    print('Error en la función "send_mail": {}'.format(str(e)))
