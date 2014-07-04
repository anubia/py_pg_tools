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

#import hashlib
#from hashlib import md5

#string = "hola"

#m = hashlib.md5()
#m.update(string.encode('utf-8'))
#print(m.hexdigest())
#import smtplib

#msg_header = 'From: sender@server\n' \
             #'To: receiver@server\n' \
             #'Cc: receiver2@server\n' \
             #'MIME-Version: 1.0\n' \
             #'Content-type: text/html\n' \
             #'Subject: Any subject\n'
#title = 'My title'
#msg_content = '<h2>{title} > <font color="green">OK</font></h2>\n'.format(
    #title=title)
#msg_full = (''.join([msg_header, msg_content])).encode()

#server = smtplib.SMTP('smtp.gmail.com:587')
#server.starttls()
#server.login('sender@server.com', 'receiver@server.com', 'receiver2@server.com')
#server.sendmail('Sender Name <sender@server.com>',
                #['Receiver Name <receiver@server.com>',
                 #'Receiver2 Name <receiver@server.com>'], msg_full)
#server.quit()

#from crontab import CronTab

#cron = CronTab(user=True)

#job = cron.new(command='python3 /mnt/store1/devel/code/ide-workspace/py_pg_tools/py_pg_tools.py v -ch localhost -cu anubia -cp 5432 -d devel__v61__test_01 -zc config/mailer/mailer.cfg')

#job.minute.on(2)
#job.hour.on(12)
#cron.write()
#print(cron.render())

from crontab import CronTab

cron = CronTab(user=True)

for job in cron:
    print(job)
