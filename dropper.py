#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y fatal_logger de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import Logger
from messenger.messenger import Messenger


# ************************* DEFINICIÓN DE FUNCIONES *************************
class Dropper:

    connecter = None
    logger = None
    dbnames = []

    def __init__(self, connecter=None, dbnames=[], logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if dbnames:
            self.dbnames = dbnames
        else:
            self.logger.stop_exe(Messenger.NO_DBS_TO_DROP)

    def drop_pg_db(self, dbname):

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
        self.logger.highlight('info', Messenger.BEGINNING_DROPPER, 'white')
        for dbname in self.dbnames:
            self.drop_pg_db(dbname)
        self.logger.highlight('info', Messenger.DROP_DBS_DONE, 'green')
