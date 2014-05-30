#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from connecter import Connecter
import psycopg2  # To work with PostgreSQL
import psycopg2.extras  # To get real field names from PostgreSQL

connecter = Connecter('localhost', 'anubia', 5433)

REASSIGN = (
    "REASSIGN OWNED BY {old_role} TO {new_role};"
)
OWNER = (
    "ALTER DATABASE {dbname} OWNER TO {new_role};"
)

dbname = 'my_replicated_db'

try:
    connecter.cursor.execute(OWNER.format(dbname=dbname, new_role='openerp61'))
except Exception as e:
    print('OWNER ERROR: {}'.format(str(e)))

try:
    conn = psycopg2.connect(host='localhost', database='my_replicated_db',
                            user='anubia', port=5433)
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
except Exception as e:
    print('Error en la función "pg_connect": {}.'.format(str(e)))

try:
    cur.execute(REASSIGN.format(old_role='anubia', new_role='openerp61'))
except Exception as e:
    print('REASSIGN ERROR: {}'.format(str(e)))

cur.close()
conn.close()
connecter.pg_disconnect()
