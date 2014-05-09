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
    users = False

    def __init__(self, connecter=None, dbnames=[], users=False, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        self.dbnames = dbnames
        self.users = users

    def get_pg_db_data(self, dbname):

        query_get_db_data = (
            'SELECT d.datname, d.datctype, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d '
            'WHERE d.datname = (%s);'
        )
        try:
            #self.connecter.allow_db_conn(dbname)
            self.connecter.cursor.execute('commit')
            result = self.connecter.cursor.execute(
                query_get_db_data, (dbname, ))
            print('*' * 80)
            print(result)
            print('*' * 80)
            #self.connecter.disallow_db_conn(dbname)
        except Exception as e:
            self.logger.debug('Error en la función "get_pg_db_data": '
                              '{}.'.format(str(e)))
            result = None
        return result

    def show_pg_dbs_data(self):

        dbs_data = []
        for dbname in self.dbnames:
            db_data = self.get_pg_db_data(dbname)
            if db_data:
                dbs_data.append(db_data)
        message = Messenger.SEARCHING_SELECTED_DBS_DATA
        self.logger.highlight('info', message, 'white')
        if dbs_data:
            for db in dbs_data:
                message = Messenger.DBNAME + db['datname']
                self.logger.info(message)
                message = Messenger.DBENCODING + db['datctype']
                self.logger.info(message)
                message = Messenger.DBOWNER + db['owner']
                self.logger.info(message)
        else:
            message = Messenger.NO_DB_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')
