#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from connecter import Connecter
from const.const import Messenger
from const.const import Queries
import psycopg2  # To work with PostgreSQL
import psycopg2.extras  # To get real field names from PostgreSQL

connecter = Connecter('localhost', 'anubia', 5433)

ex_templates = False
db_owner = ''

try:
    # Get all databases (no templates) of a specific owner
    if db_owner and ex_templates:
        connecter.cursor.execute(Queries.GET_PG_NO_TEMPLATE_DBS_BY_OWNER,
                                 (db_owner, ))
    # Get all databases (templates too) of a specific owner
    elif db_owner and ex_templates is False:
        connecter.cursor.execute(Queries.GET_PG_DBS_BY_OWNER, (db_owner, ))
    # Get all databases (no templates)
    elif not db_owner and ex_templates is False:
        connecter.cursor.execute(Queries.GET_PG_DBS)
    else:  # Get all databases (templates too)
        connecter.cursor.execute(Queries.GET_PG_NO_TEMPLATE_DBS)

    dbs = connecter.cursor.fetchall()

except Exception as e:
    # Rollback to avoid errors in next queries because of waiting
    # this transaction to finish
    connecter.conn.rollback()
    connecter.logger.debug('Error en la función "get_pg_dbs_data": '
                           '{}.'.format(str(e)))
    message = Messenger.GET_PG_DBS_DATA
    connecter.logger.highlight('warning', message, 'yellow')
    dbs = None

print(dbs)
