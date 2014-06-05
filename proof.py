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

#from mailer.mailer import Mailer
#from orchestrator import Orchestrator

#config_type = 'mail'
## Get the variables from the config file
#parser = Orchestrator.get_cfg_vars(config_type,
                                   #'/mnt/store1/devel/code/ide-workspace/py_pg_tools/config/mailer/mailer.cfg')
#mailer = Mailer(parser.mail_vars['level'], parser.mail_vars['name'],
                #parser.mail_vars['address'], parser.mail_vars['password'],
                #parser.mail_vars['to'], parser.mail_vars['cc'],
                #parser.mail_vars['bcc'], parser.logger)

#mailer.send_mail()

dictionary = {
    'hola': 'holaword',
    'adios': 'adiosword',
}

if 'hola' in dictionary.keys():
    print('SI')
else:
    print('NO')
