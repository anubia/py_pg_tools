#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#from connecter import Connecter

#connecter = Connecter('localhost', 'anubia', 5432)

#query_get_dbs1 = (
    #'SELECT * '
    #'FROM pg_database;'
#)

#try:
    #connecter.cursor.execute(query_get_dbs1)
#except:
    #print('ERROR')

#import time
#from datetime import datetime

#timestamp1 = time.time()
#timestamp2 = time.time()

#print(timestamp1)
#print(timestamp2)
#diff = timestamp2 - timestamp1
#print(diff)

#print(datetime.fromtimestamp(diff).strftime('%Y-%m-%d %H:%M:%S'))

from datetime import datetime

timestamp1 = datetime.now()
timestamp2 = datetime.now()

print(timestamp1)
print(timestamp2)
diff = timestamp2 - timestamp1
print(diff)
