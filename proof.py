#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#from connecter import Connecter

#connecter = Connecter('localhost', 'anubia', 5432)

#query_get_dbs1 = (
    #'SELECT * '
    #'FROM pg_database;'
#)
#query_get_dbs2 = (
    #'SELECT * '
    #'FOM pg_database;'
#)

#try:
    #connecter.cursor.execute(query_get_dbs2)
#except:
    #print('ERROR')

#try:
    #connecter.cursor.execute(query_get_dbs1)
#except:
    #print('ERROR')

#for record in connecter.cursor:
    #print(record)

import psycopg2  # To work with PostgreSQL
import psycopg2.extras  # To get real field names from PostgreSQL

conn = psycopg2.connect(host='localhost',
                        database='postgres',
                        user='anubia',
                        port=5432)

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

query_get_dbs1 = (
    'SELECT * '
    'FRO pg_database;'
)
query_get_dbs2 = (
    'SELECT * '
    'FROM pg_database;'
)

try:
    cursor.execute(query_get_dbs1)
except Exception as e:
    conn.rollback()
    print('ERROR')
    print(str(e))

try:
    cursor.execute(query_get_dbs2)
except Exception as e:
    print('ERROR')
    print(str(e))

cursor.close()
conn.close()
