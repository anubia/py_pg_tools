#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from casting.casting import Casting
from const.const import Messenger
from const.const import Queries
from date_tools.date_tools import DateTools
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

        message = Messenger.DROPPER_VARS.format(
            server=self.connecter.server, user=self.connecter.user,
            port=self.connecter.port, dbnames=self.dbnames)
        self.logger.debug(Messenger.DROPPER_VARS_INTRO)
        self.logger.debug(message)

    def drop_pg_db(self, dbname, pg_superuser):
        '''
        Target:
            - remove a database in PostgreSQL.
        Parameters:
            - dbname: the PostgreSQL database's name which is going to be
              removed.
            - pg_superuser: a flag which indicates whether the current user is
              PostgreSQL superuser or not.
        '''
        try:
            self.connecter.cursor.execute(Queries.PG_DB_EXISTS, (dbname, ))
            result = self.connecter.cursor.fetchone()

            if result:
                pg_pid = self.connecter.get_pid_str()
                formatted_sql = Queries.BACKEND_PG_DB_EXISTS.format(
                    pg_pid=pg_pid, target_db=dbname)

                self.connecter.cursor.execute(formatted_sql)
                result = self.connecter.cursor.fetchone()

                if not result:

                    # Users who are not superusers will only be able to drop
                    # the databases they own
                    if not pg_superuser:

                        self.connecter.cursor.execute(Queries.GET_PG_DB_OWNER,
                                                      (dbname, ))
                        db = self.connecter.cursor.fetchone()

                        if db['owner'] != self.connecter.user:

                            message = Messenger.DROP_DB_NOT_ALLOWED.format(
                                user=self.connecter.user, dbname=dbname)
                            self.logger.highlight('warning', message, 'yellow')

                        else:
                            fmt_query_drop_db = Queries.DROP_PG_DB.format(
                                dbname=dbname)

                            start_time = DateTools.get_current_datetime()
                            # Drop the database
                            self.connecter.cursor.execute(fmt_query_drop_db)
                            end_time = DateTools.get_current_datetime()
                            # Get and show the process' duration
                            diff = DateTools.get_diff_datetimes(start_time,
                                                                end_time)
                            message = Messenger.DROP_DB_DONE.format(
                                dbname=dbname, diff=diff)
                            self.logger.highlight('info', message, 'green')

                else:
                    message = Messenger.ACTIVE_CONNS_ERROR.format(
                        dbname=dbname)
                    self.logger.highlight('warning', message, 'yellow')

            else:
                message = Messenger.DB_DOES_NOT_EXIST.format(dbname=dbname)
                self.logger.highlight('warning', message, 'yellow')
        except Exception as e:
            self.logger.debug('Error en la función "drop_pg_db": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Messenger.DROP_DB_FAIL.format(
                dbname=dbname), 'yellow')

    def drop_pg_dbs(self, dbnames):
        '''
        Target:
            - remove a list of databases in PostgreSQL.
        '''
        self.logger.highlight('info', Messenger.BEGINNING_DROPPER, 'white')
        # Check if the role of user connected to PostgreSQL is superuser
        pg_superuser = self.connecter.is_pg_superuser()

        if dbnames:

            for dbname in self.dbnames:

                message = Messenger.PROCESSING_DB.format(dbname=dbname)
                self.logger.highlight('info', message, 'cyan')

                self.drop_pg_db(dbname, pg_superuser)

        else:
            self.logger.highlight('warning',
                                  Messenger.DROPPER_HAS_NOTHING_TO_DO,
                                  'yellow', effect='bold')

        self.logger.highlight('info', Messenger.DROP_DBS_DONE, 'green',
                              effect='bold')
