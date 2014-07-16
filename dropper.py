#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from casting.casting import Casting
from const.const import Messenger as Msg
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
            self.logger.stop_exe(Msg.NO_CONNECTION_PARAMS)

        if isinstance(dbnames, list):
            self.dbnames = dbnames
        else:
            self.dbnames = Casting.str_to_list(dbnames)

        msg = Msg.DROPPER_VARS.format(server=self.connecter.server,
                                      user=self.connecter.user,
                                      port=self.connecter.port,
                                      dbnames=self.dbnames)
        self.logger.debug(Msg.DROPPER_VARS_INTRO)
        self.logger.debug(msg)

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
        delete = False

        try:
            self.connecter.cursor.execute(Queries.PG_DB_EXISTS, (dbname, ))
            result = self.connecter.cursor.fetchone()

            if result:

                pg_pid = self.connecter.get_pid_str()
                formatted_sql = Queries.BACKEND_PG_DB_EXISTS.format(
                    pg_pid=pg_pid, target_db=dbname)

                self.connecter.cursor.execute(formatted_sql)
                result = self.connecter.cursor.fetchone()

                # If there are not any connections to the target database...
                if not result:

                    # Users who are not superusers will only be able to drop
                    # the databases they own
                    if not pg_superuser:

                        self.connecter.cursor.execute(Queries.GET_PG_DB_OWNER,
                                                      (dbname, ))
                        db = self.connecter.cursor.fetchone()

                        if db['owner'] != self.connecter.user:

                            msg = Msg.DROP_DB_NOT_ALLOWED.format(
                                user=self.connecter.user, dbname=dbname)
                            self.logger.highlight('warning', msg, 'yellow')

                        else:
                            delete = True

                    else:
                        delete = True

                    if delete:

                        # Get the database's "datallowconn" value
                        datallowconn = self.connecter.get_datallowconn(dbname)

                        # If datallowconn is allowed, change it temporarily
                        if datallowconn:
                            # Disallow connections to the database during the
                            # process
                            result = self.connecter.disallow_db_conn(dbname)
                            if not result:
                                msg = Msg.DISALLOW_CONN_TO_PG_DB_FAIL.format(
                                    dbname=dbname)
                                self.logger.highlight('warning', msg, 'yellow')

                        fmt_query_drop_db = Queries.DROP_PG_DB.format(
                            dbname=dbname)

                        start_time = DateTools.get_current_datetime()
                        # Drop the database
                        self.connecter.cursor.execute(fmt_query_drop_db)
                        end_time = DateTools.get_current_datetime()
                        # Get and show the process' duration
                        diff = DateTools.get_diff_datetimes(start_time,
                                                            end_time)
                        msg = Msg.DROP_DB_DONE.format(dbname=dbname, diff=diff)
                        self.logger.highlight('info', msg, 'green')

                        # If datallowconn was allowed, leave it as it was
                        if datallowconn:
                            # Allow connections to the database at the end of
                            # the process
                            result = self.connecter.allow_db_conn(dbname)
                            if not result:
                                msg = Msg.ALLOW_CONN_TO_PG_DB_FAIL.format(
                                    dbname=dbname)
                                self.logger.highlight('warning', msg, 'yellow')

                else:
                    msg = Msg.ACTIVE_CONNS_ERROR.format(dbname=dbname)
                    self.logger.highlight('warning', msg, 'yellow')

            else:
                msg = Msg.DB_DOES_NOT_EXIST.format(dbname=dbname)
                self.logger.highlight('warning', msg, 'yellow')

        except Exception as e:
            self.logger.debug('Error en la función "drop_pg_db": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Msg.DROP_DB_FAIL.format(
                dbname=dbname), 'yellow')

    def drop_pg_dbs(self, dbnames):
        '''
        Target:
            - remove a list of databases in PostgreSQL.
        '''
        self.logger.highlight('info', Msg.BEGINNING_DROPPER, 'white')
        # Check if the role of user connected to PostgreSQL is superuser
        pg_superuser = self.connecter.is_pg_superuser()

        if dbnames:

            for dbname in self.dbnames:

                msg = Msg.PROCESSING_DB.format(dbname=dbname)
                self.logger.highlight('info', msg, 'cyan')

                self.drop_pg_db(dbname, pg_superuser)

        else:
            self.logger.highlight('warning', Msg.DROPPER_HAS_NOTHING_TO_DO,
                                  'yellow', effect='bold')

        self.logger.highlight('info', Msg.DROP_DBS_DONE, 'green',
                              effect='bold')
