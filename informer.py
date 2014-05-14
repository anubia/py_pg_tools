#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y fatal_logger de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import Logger
from messenger.messenger import Messenger


# ************************* DEFINICIÓN DE FUNCIONES *************************
class Informer:

    connecter = None
    logger = None
    dbnames = []
    usernames = []

    def __init__(self, connecter=None, dbnames=[], usernames=[], logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        self.dbnames = dbnames
        self.usernames = usernames

    def get_pg_db_data(self, dbname):

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
