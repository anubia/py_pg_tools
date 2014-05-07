#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from logger.logger import Logger
from messenger.messenger import Messenger


class Terminator:

    target_all = None
    target_user = None
    target_dbs = []
    connecter = None
    logger = None

    #-- terminate process by an target user
    query_terminate_backend_user = (
        "SELECT pg_terminate_backend({pg_pid}) "
        "FROM pg_stat_activity "
        "WHERE usename = '{target_user}';"
    )
    #This will kill existing connections except for yours to target db:
    query_terminate_backend_db = (
        "SELECT pg_terminate_backend({pg_pid}) "
        "FROM pg_stat_activity "
        "WHERE datname = '{target_db}' "
        "AND {pg_pid} <> pg_backend_pid();"
    )
    #This will kill existing connections except for yours to any db:
    query_terminate_backend_all = (
        "SELECT pg_terminate_backend({pg_pid}) "
        "FROM pg_stat_activity "
        "WHERE {pg_pid} <> pg_backend_pid();"
    )

    def __init__(self, connecter, target_all=False, target_user='',
                 target_dbs=[], logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        self.target_all = target_all
        self.target_user = target_user
        self.target_dbs = target_dbs

    def terminate_backend_user(self):
        '''
    Objetivo:
        - eliminar todas las conexiones a PostgreSQL de un usuario (siempre
        que el usuario no sea el que ejecuta esta sentencia).
    '''
        message = Messenger.BEGINNING_TERMINATE_USER_CONN.format(
            target_user=self.target_user)
        self.logger.highlight('info', message, 'white')
        sql = self.query_terminate_backend_user
        try:  # Probar si hay excepciones en...
            # Obtener el nombre de la variable que indica el pg_pid según la
            # versión de PostgreSQL
            pg_pid = self.connecter.get_pid_str()
            sql = sql.format(pg_pid=pg_pid, target_user=self.target_user)
            self.connecter.cursor.execute(sql)  # Ejecutar consulta
            message = Messenger.TERMINATE_USER_CONN_DONE.format(
                target_user=self.target_user)
            self.logger.highlight('info', message, 'green')
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "terminate_backend_user": '
                              '{}.'.format(str(e)))
            message = Messenger.TERMINATE_USER_CONN_FAIL.format(
                target_user=self.target_user)
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def terminate_backend_db(self, target_db):
        '''
    Objetivo:
        - eliminar todas las conexiones a una base de datos de PostgreSQL
        (excepto la actual, en caso de ser a dicha base de datos).
    '''
        sql = self.query_terminate_backend_db
        try:  # Probar si hay excepciones en...
            # Obtener el nombre de la variable que indica el pg_pid según la
            # versión de PostgreSQL
            pg_pid = self.connecter.get_pid_str()
            if isinstance(target_db, dict):
                sql = sql.format(pg_pid=pg_pid, target_db=target_db['name'])
            else:
                sql = sql.format(pg_pid=pg_pid, target_db=target_db)
            self.connecter.cursor.execute(sql)  # Ejecutar consulta
            if isinstance(target_db, dict):
                message = Messenger.TERMINATE_DB_CONN_DONE.format(
                    target_dbname=target_db['name'])
            else:
                message = Messenger.TERMINATE_DB_CONN_DONE.format(
                    target_dbname=target_db)
            self.logger.info(message)
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "terminate_backend_db": '
                              '{}.'.format(str(e)))
            if isinstance(target_db, dict):
                message = Messenger.TERMINATE_DB_CONN_FAIL.format(
                    target_dbname=target_db['name'])
            else:
                message = Messenger.TERMINATE_DB_CONN_FAIL.format(
                    target_dbname=target_db)
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def terminate_backend_dbs(self):
        '''
    Objetivo:
        - eliminar todas las conexiones a varias bases de datos de PostgreSQL
        (excepto la actual, en caso de ser a dicha base de datos).
    '''
        message = Messenger.BEGINNING_TERMINATE_DBS_CONN
        self.logger.highlight('info', message, 'white')
        for target_db in self.target_dbs:
            self.terminate_backend_db(target_db)
        self.logger.highlight('info', Messenger.TERMINATE_DBS_CONN_DONE,
                              'green')

    def terminate_backend_all(self):
        '''
    Objetivo:
        - eliminar todas las conexiones a PostgreSQL excepto la actual.
    '''
        sql = self.query_terminate_backend_all
        try:  # Probar si hay excepciones en...
            message = Messenger.BEGINNING_TERMINATE_ALL_CONN
            self.logger.highlight('info', message, 'white')
            # Obtener el nombre de la variable que indica el pg_pid según la
            # versión de PostgreSQL
            pg_pid = self.connecter.get_pid_str()
            sql = sql.format(pg_pid=pg_pid)
            self.connecter.cursor.execute(sql)  # Ejecutar consulta
            self.logger.highlight('info', Messenger.TERMINATE_ALL_CONN_DONE,
                                  'green')
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "terminate_backend_all": '
                              '{}.'.format(str(e)))
            message = Messenger.TERMINATE_ALL_CONN_FAIL
            self.logger.highlight('warning', message, 'yellow', effect='bold')
