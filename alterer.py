#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from casting.casting import Casting
from connecter import Connecter
from const.const import Messenger
from const.const import Queries
from date_tools.date_tools import DateTools
from logger.logger import Logger


class Alterer:

    in_dbs = []  # List of databases to be included in the process
    old_role = ''  # Current owner of the database's tables
    new_role = ''  # New owner for the database and its tables
    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages

    def __init__(self, connecter=None, in_dbs=[], old_role='', new_role='',
                 logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if isinstance(in_dbs, list):
            self.in_dbs = in_dbs
        else:
            self.in_dbs = Casting.str_to_list(in_dbs)

        if old_role:
            self.old_role = old_role
        else:
            self.logger.stop_exe(Messenger.NO_OLD_ROLE)

        if not new_role:
            self.logger.stop_exe(Messenger.NO_NEW_ROLE)
        # First check whether the user exists in PostgreSQL or not
        self.connecter.cursor.execute(Queries.PG_USER_EXISTS, (new_role, ))
        # Do not alter database if the user does not exist
        result = self.connecter.cursor.fetchone()
        if result:
            self.new_role = new_role
        else:
            message = Messenger.USER_DOES_NOT_EXIST.format(user=new_role)
            self.logger.stop_exe(message)

        message = Messenger.ALTERER_VARS.format(
            server=self.connecter.server, user=self.connecter.user,
            port=self.connecter.port, in_dbs=self.in_dbs,
            old_role=self.old_role, new_role=self.new_role)
        self.logger.debug(Messenger.ALTERER_VARS_INTRO)
        self.logger.debug(message)

    def alter_db_owner(self, db):
        '''
        Target:
            - change the owner of a databases and its tables.
        Parameters:
            - db: database which is going to be altered.
        Return:
            - a boolean which indicates the success of the process.
        '''
        message = Messenger.ALTERER_FEEDBACK.format(old_role=self.old_role,
                                                    new_role=self.new_role)
        self.logger.info(message)

        success = True
        dbname = db['datname']

        if db['owner'] != 'postgres':  # Do not allow switch an owner postgres

            if db['datallowconn'] == 1:  # Check if the db allows connections

                try:
                    # Change the owner of the database
                    self.connecter.cursor.execute(
                        Queries.CHANGE_PG_DB_OWNER.format(
                            dbname=dbname, new_role=self.new_role))
                except Exception as e:
                    success = False
                    self.logger.debug('Error en la función "alter_db_owner": '
                                      '{}'.format(str(e)))
                    message = Messenger.CHANGE_PG_DB_OWNER_FAIL
                    self.logger.highlight('warning', message, 'yellow')

                # Start another connection to the target database to be able to
                # apply the next query
                own_connecter = Connecter(server=self.connecter.server,
                                          user=self.connecter.user,
                                          port=self.connecter.port,
                                          database=dbname, logger=self.logger)
                try:
                    # Change the owner of the database's tables
                    own_connecter.cursor.execute(
                        Queries.REASSIGN_PG_DB_TBLS_OWNER.format(
                            old_role=self.old_role, new_role=self.new_role))
                except Exception as e:
                    success = False
                    self.logger.debug('Error en la función "alter_db_owner": '
                                      '{}'.format(str(e)))
                    message = Messenger.REASSIGN_PG_DB_TBLS_OWNER_FAIL
                    self.logger.highlight('warning', message, 'yellow')

                # Close cursor and connection to the target database
                own_connecter.pg_disconnect()

            else:
                success = False
                message = Messenger.DB_DOES_NOT_ALLOW_CONN.format(
                    dbname=dbname)
                self.logger.highlight('warning', message, 'yellow')

        else:
            success = False
            message = Messenger.DB_OWNED_BY_POSTGRES_NOT_ALLOWED
            self.logger.highlight('warning', message, 'yellow')

        return success

    def alter_dbs_owner(self, alt_list):
        '''
        Target:
            - change the owner of a group of databases and their tables.
        Parameters:
            - alt_list: names of the databases which are going to be altered.
        '''
        self.logger.highlight('info', Messenger.PROCESSING_ALTERER, 'white')

        if alt_list:

            for db in alt_list:

                dbname = db['datname']

                message = Messenger.PROCESSING_DB.format(dbname=dbname)
                self.logger.highlight('info', message, 'cyan')

                start_time = DateTools.get_current_datetime()
                # Change the owner of the database
                success = self.alter_db_owner(db)
                end_time = DateTools.get_current_datetime()
                # Get and show the process' duration
                diff = DateTools.get_diff_datetimes(start_time, end_time)

                if success:
                    message = Messenger.DB_ALTERER_DONE.format(dbname=dbname,
                                                               diff=diff)
                    self.logger.highlight('info', message, 'green')
                else:
                    message = Messenger.DB_ALTERER_FAIL.format(dbname=dbname)
                    self.logger.highlight('warning', message, 'yellow',
                                          effect='bold')
        else:
            self.logger.highlight('warning',
                                  Messenger.ALTERER_HAS_NOTHING_TO_DO,
                                  'yellow', effect='bold')

        self.logger.highlight('info', Messenger.ALTERER_DONE, 'green',
                              effect='bold')
