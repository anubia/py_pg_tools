#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from casting.casting import Casting
from const.const import Messenger
from logger.logger import Logger


class Dropper:

    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages
    dbnames = []  # List of databases to be removed

    def __init__(self, connecter=None, dbnames=[], logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if isinstance(dbnames, list):
            self.dbnames = dbnames
        else:
            self.dbnames = Casting.str_to_list(dbnames)

    def drop_pg_db(self, dbname):
        '''
        Target:
            - remove a database in PostgreSQL.
        Parameters:
            - dbname: the PostgreSQL database's name which is going to be
              removed.
        '''
        query_drop_db = (
            'DROP DATABASE %s;'
        )
        format_query_drop_db = query_drop_db % (dbname)

        try:
            self.connecter.cursor.execute('commit')
            self.connecter.cursor.execute(format_query_drop_db)
            self.logger.info(Messenger.DROP_DB_DONE.format(dbname=dbname))
        except Exception as e:
            self.logger.debug('Error en la función "drop_pg_db": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Messenger.DROP_DB_FAIL.format(
                dbname=dbname), 'yellow')

    def drop_pg_dbs(self):
        '''
        Target:
            - remove a list of databases in PostgreSQL.
        '''
        self.logger.highlight('info', Messenger.BEGINNING_DROPPER, 'white')
        for dbname in self.dbnames:
            self.drop_pg_db(dbname)
        self.logger.highlight('info', Messenger.DROP_DBS_DONE, 'green')
