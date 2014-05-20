#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from casting.casting import Casting
from const.const import Messenger
from logger.logger import Logger


class Informer:

    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages
    dbnames = []  # List of databases to get some info about
    usernames = []  # List of users to get some info about

    def __init__(self, connecter=None, dbnames=[], usernames=[], logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if isinstance(dbnames, list) or dbnames is None:
            self.dbnames = dbnames
        else:
            self.dbnames = Casting.str_to_list(dbnames)

        if isinstance(dbnames, list) or dbnames is None:
            self.usernames = usernames
        else:
            self.usernames = Casting.str_to_list(usernames)

    def get_pg_db_data(self, dbname):
        '''
        Target:
            - show some info about a specified database.
        Parameters:
            - dbname: name of the database whose information is going to be
            shown.
        '''
        query_get_db_data = (
            'SELECT d.datname, d.datctype, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d '
            'WHERE d.datname = (%s);'
        )

        try:
            self.connecter.cursor.execute(query_get_db_data, (dbname, ))
        except Exception as e:
            self.logger.debug('Error en la función "get_pg_db_data": '
                              '{}.'.format(str(e)))
            self.connecter.cursor = None

    def show_pg_dbs_data(self):
        '''
        Target:
            - show some info about every PostgreSQL database.
        '''
        dbs_data = []
        for dbname in self.dbnames:
            self.get_pg_db_data(dbname)
            result = self.connecter.cursor.fetchone()
            if result:
                dbs_data.append(result)
        message = Messenger.SEARCHING_SELECTED_DBS_DATA
        self.logger.highlight('info', message, 'white')
        if dbs_data:
            for db in dbs_data:
                message = Messenger.DBNAME + db['datname']
                self.logger.highlight('info', message, 'cyan')
                message = Messenger.DBENCODING + db['datctype']
                self.logger.info(message)
                message = Messenger.DBOWNER + db['owner']
                self.logger.info(message)
        else:
            message = Messenger.NO_DB_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def get_pg_user_data(self, username):
        '''
        Target:
            - show some info about a specified user.
        Parameters:
            - username: name of the user whose information is going to be
            shown.
        '''
        query_get_user_data = (
            'SELECT usename, usesysid, usesuper '
            'FROM pg_user '
            'WHERE usename = (%s);'
        )

        try:
            self.connecter.cursor.execute(query_get_user_data, (username, ))
        except Exception as e:
            self.logger.debug('Error en la función "get_pg_user_data": '
                              '{}.'.format(str(e)))
            self.connecter.cursor = None

    def show_pg_users_data(self):
        '''
        Target:
            - show some info about every PostgreSQL user.
        '''
        users_data = []
        for username in self.usernames:
            self.get_pg_user_data(username)
            result = self.connecter.cursor.fetchone()
            if result:
                users_data.append(result)
        message = Messenger.SEARCHING_SELECTED_USERS_DATA
        self.logger.highlight('info', message, 'white')
        if users_data:
            for user in users_data:
                message = Messenger.USERNAME + user['usename']
                self.logger.highlight('info', message, 'cyan')
                message = Messenger.USERID + str(user['usesysid'])
                self.logger.info(message)
                message = Messenger.SUPERUSER
                if user['usesuper']:
                    message += 'Sí'
                else:
                    message += 'No'
                self.logger.info(message)
        else:
            message = Messenger.NO_USER_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')
