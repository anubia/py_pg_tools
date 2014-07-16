#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from const.const import Messenger as Msg
from const.const import Queries
from date_tools.date_tools import DateTools
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
            self.logger.stop_exe(Msg.NO_CONNECTION_PARAMS)

        # First check whether the name of the copy already exists in PostgreSQL
        self.connecter.cursor.execute(Queries.PG_DB_EXISTS, (new_dbname, ))
        # Do not replicate if the name already exists
        result = self.connecter.cursor.fetchone()
        if result:
            msg = Msg.DB_ALREADY_EXISTS.format(dbname=new_dbname)
            self.logger.stop_exe(msg)

        if new_dbname:
            self.new_dbname = new_dbname
        else:
            self.logger.stop_exe(Msg.NO_NEW_DBNAME)

        # First check whether the name of the source exists in PostgreSQL
        self.connecter.cursor.execute(Queries.PG_DB_EXISTS,
                                      (original_dbname, ))
        result = self.connecter.cursor.fetchone()
        if not result:
            msg = Msg.DB_DOES_NOT_EXIST.format(dbname=original_dbname)
            self.logger.stop_exe(msg)

        if original_dbname:
            self.original_dbname = original_dbname
        else:
            self.logger.stop_exe(Msg.NO_ORIGINAL_DBNAME)

        msg = Msg.REPLICATOR_VARS.format(server=self.connecter.server,
                                         user=self.connecter.user,
                                         port=self.connecter.port,
                                         original_dbname=self.original_dbname,
                                         new_dbname=self.new_dbname)
        self.logger.debug(Msg.REPLICATOR_VARS_INTRO)
        self.logger.debug(msg)

    def replicate_pg_db(self):
        '''
        Target:
            - clone a specified database in PostgreSQL.
        '''
        try:
            pg_pid = self.connecter.get_pid_str()
            formatted_sql = Queries.BACKEND_PG_DB_EXISTS.format(
                pg_pid=pg_pid, target_db=self.original_dbname)
            self.connecter.cursor.execute(formatted_sql)
            result = self.connecter.cursor.fetchone()

            if result:
                msg = Msg.ACTIVE_CONNS_ERROR.format(
                    dbname=self.original_dbname)
                self.logger.stop_exe(msg)

            formatted_query_clone_pg_db = Queries.CLONE_PG_DB.format(
                dbname=self.new_dbname, original_dbname=self.original_dbname,
                user=self.connecter.user)

            msg = Msg.BEGINNING_REPLICATOR.format(
                original_dbname=self.original_dbname)
            self.logger.highlight('info', msg, 'white')

            # Get the database's "datallowconn" value
            datallowconn = self.connecter.get_datallowconn(
                self.original_dbname)

            # If datallowconn is allowed, change it temporarily
            if datallowconn:
                # Disallow connections to the database during the
                # process
                result = self.connecter.disallow_db_conn(self.original_dbname)
                if not result:
                    msg = Msg.DISALLOW_CONN_TO_PG_DB_FAIL.format(
                        dbname=self.original_dbname)
                    self.logger.highlight('warning', msg, 'yellow')

            # self.connecter.cursor.execute('commit')
            start_time = DateTools.get_current_datetime()
            # Replicate the database
            self.connecter.cursor.execute(formatted_query_clone_pg_db)
            end_time = DateTools.get_current_datetime()
            # Get and show the process' duration
            diff = DateTools.get_diff_datetimes(start_time, end_time)

            # If datallowconn was allowed, leave it as it was
            if datallowconn:
                # Allow connections to the database at the end of
                # the process
                result = self.connecter.allow_db_conn(self.original_dbname)
                if not result:
                    msg = Msg.ALLOW_CONN_TO_PG_DB_FAIL.format(
                        dbname=self.original_dbname)
                    self.logger.highlight('warning', msg, 'yellow')

            msg = Msg.REPLICATE_DB_DONE.format(
                new_dbname=self.new_dbname,
                original_dbname=self.original_dbname, diff=diff)
            self.logger.highlight('info', msg, 'green')
            self.logger.highlight('info', Msg.REPLICATOR_DONE, 'green',
                                  effect='bold')

        except Exception as e:
            self.logger.debug('Error en la función "clone_pg_db": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Msg.REPLICATE_DB_FAIL)
