#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from connecter import Connecter

connecter = Connecter('localhost', 'anubia', 5433)

DROP_PG_DB = (
    'DROP DATABASE {dbname};'
)

TERMINATE_BACKEND_PG_DB = (
    "SELECT pg_terminate_backend({pg_pid}) "
    "FROM pg_stat_activity "
    "WHERE datname = '{target_db}' "
    "AND {pg_pid} <> pg_backend_pid();"
)

pid = connecter.get_pid_str()
print(pid)

try:
    connecter.cursor.execute(TERMINATE_BACKEND_PG_DB.format(pg_pid=pid, target_db='my_replicated_db'))
except Exception as e:
    print('TERMINATE ERROR: {}'.format(str(e)))

try:
    connecter.cursor.execute('commit')
    connecter.cursor.execute(DROP_PG_DB.format(dbname='my_replicated_db'))
except Exception as e:
    print('DROP ERROR: {}'.format(str(e)))
