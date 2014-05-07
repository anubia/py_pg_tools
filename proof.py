#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from connecter import Connecter

connecter = Connecter('localhost', 'anubia', '', 5432)

query_get_dbs = (
    'SELECT d.datname, d.datallowconn, '
    'pg_catalog.pg_get_userbyid(d.datdba) as owner '
    'FROM pg_catalog.pg_database d;'
)

connecter.cursor.execute(query_get_dbs)

for record in connecter.cursor:
    print(record['encoding'])
