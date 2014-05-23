#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from const.const import Messenger
from const.const import Queries
from logger.logger import Logger


class Replicator:

    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages
    new_dbname = ''  # Name of the copy
    original_dbname = ''  # Name of the original database

    def __init__(self, connecter=None, new_dbname='', original_dbname='',
                 logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        # First check whether the name of the copy already exists in PostgreSQL
        self.connecter.cursor.execute(Queries.PG_DB_EXISTS, (new_dbname, ))
        # Do not replicate if the name already exists
        result = self.connecter.cursor.fetchone()
        if result:
            message = Messenger.DB_ALREADY_EXISTS.format(dbname=new_dbname)
            self.logger.stop_exe(message)

        if new_dbname:
            self.new_dbname = new_dbname
        else:
            self.logger.stop_exe(Messenger.NO_NEW_DBNAME)
        if original_dbname:
            self.original_dbname = original_dbname
        else:
            self.logger.stop_exe(Messenger.NO_ORIGINAL_DBNAME)

    def replicate_pg_db(self):
        '''
        Target:
            - clone a specified database in PostgreSQL.
        '''
        formatted_query_clone_pg_db = Queries.CLONE_PG_DB.format(
            dbname=self.new_dbname, original_dbname=self.original_dbname,
            user=self.connecter.user)

        try:
            message = Messenger.BEGINNING_REPLICATOR.format(
                original_dbname=self.original_dbname)
            self.logger.highlight('info', message, 'white')

            self.connecter.cursor.execute('commit')
            self.connecter.cursor.execute(formatted_query_clone_pg_db)

            self.logger.highlight('info', Messenger.REPLICATE_DB_DONE.format(
                new_dbname=self.new_dbname,
                original_dbname=self.original_dbname), 'green')

        except Exception as e:
            self.logger.debug('Error en la función "clone_pg_db": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.REPLICATE_DB_FAIL)
