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
            'WHERE d.datname = {dbname};'
        )
        try:
            result = self.connecter.cursor.execute(query_get_db_data)
        except Exception as e:
            self.logger.debug('Error en la función "get_pg_db_data": '
                              '{}.'.format(str(e)))
            result = None
        return result

    def get_pg_dbs_data(self):

        dbs_data = {}
        for dbname in self.dbnames:
            db_data = self.get_pg_db_data(dbname)
            dbs_data.append(db_data)
        #TODO Continue this function tomorrow
