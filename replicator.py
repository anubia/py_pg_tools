#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y fatal_logger de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import Logger
from messenger.messenger import Messenger


# ************************* DEFINICIÓN DE FUNCIONES *************************
class Replicator:

    connecter = None
    logger = None
    new_dbname = ''
    original_dbname = ''

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

        if new_dbname:
            self.new_dbname = new_dbname
        else:
            self.logger.stop_exe(Messenger.NO_NEW_DBNAME)
        if original_dbname:
            self.original_dbname = original_dbname
        else:
            self.logger.stop_exe(Messenger.NO_ORIGINAL_DBNAME)

    def replicate_pg_db(self):

        query_clone_db = (
            'CREATE DATABASE %s WITH TEMPLATE %s OWNER %s;'
        )

        format_query_clone_db = query_clone_db % (
            self.new_dbname, self.original_dbname, self.connecter.user)

        try:
            message = Messenger.BEGINNING_REPLICATOR.format(
                original_dbname=self.original_dbname)
            self.logger.highlight('info', message, 'white')
            self.connecter.cursor.execute('commit')
            self.connecter.cursor.execute(format_query_clone_db)
            self.logger.highlight('info', Messenger.REPLICATE_DB_DONE.format(
                new_dbname=self.new_dbname,
                original_dbname=self.original_dbname), 'green')
        # TODO capturar excepción ¿ProgrammingError?: ocurre cuando se intenta
        # crear en PostgreSQL una base de datos con un nombre que ya existe
        except Exception as e:
            self.logger.debug('Error en la función "clone_pg_db": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.REPLICATE_DB_FAIL)
