#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from logger.logger import Logger
from const.const import Messenger
from casting.casting import Casting
from checker.checker import Checker


class Terminator:

    target_all = None  # Flag which determinates if terminate any connection
    target_user = None  # Terminate any connection of an specific user
    target_dbs = []  # Terminate any connection to a list of databases
    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages

    # Terminate process by an target user
    query_terminate_backend_user = (
        "SELECT pg_terminate_backend({pg_pid}) "
        "FROM pg_stat_activity "
        "WHERE usename = '{target_user}';"
    )
    # This will kill existing connections except for yours to target database
    query_terminate_backend_db = (
        "SELECT pg_terminate_backend({pg_pid}) "
        "FROM pg_stat_activity "
        "WHERE datname = '{target_db}' "
        "AND {pg_pid} <> pg_backend_pid();"
    )
    # This will kill existing connections except for yours to any database
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

        if target_all is None:
            self.target_all = target_all
        elif isinstance(target_all, bool):
            self.target_all = target_all
        elif Checker.str_is_bool(target_all):
            self.target_all = Casting.str_to_bool(target_all)
        else:
            self.logger.stop_exe(Messenger.INVALID_TARGET_ALL)

        self.target_user = target_user

        if isinstance(target_dbs, list):
            self.target_dbs = target_dbs
        else:
            self.target_dbs = Casting.str_to_list(target_dbs)

    def terminate_backend_user(self):
        '''
        Target:
            - terminate every connection of a specific user to PostgreSQL (as
            long as the target user is the one who is running the program).
        '''
        message = Messenger.BEGINNING_TERMINATE_USER_CONN.format(
            target_user=self.target_user)
        self.logger.highlight('info', message, 'white')
        sql = self.query_terminate_backend_user

        try:
            pg_pid = self.connecter.get_pid_str()  # Get PID variable's name
            sql = sql.format(pg_pid=pg_pid, target_user=self.target_user)
            self.connecter.cursor.execute(sql)

            message = Messenger.TERMINATE_USER_CONN_DONE.format(
                target_user=self.target_user)
            self.logger.highlight('info', message, 'green')

        except Exception as e:
            self.logger.debug('Error en la función "terminate_backend_user": '
                              '{}.'.format(str(e)))
            message = Messenger.TERMINATE_USER_CONN_FAIL.format(
                target_user=self.target_user)
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def terminate_backend_db(self, target_db):
        '''
        Target:
            - terminate every connection to a PostgreSQL database (except the
            current one, if it is connected to the target database).
        '''
        sql = self.query_terminate_backend_db

        try:
            pg_pid = self.connecter.get_pid_str()  # Get PID variable's name
            if isinstance(target_db, dict):
                sql = sql.format(pg_pid=pg_pid, target_db=target_db['name'])
            else:
                sql = sql.format(pg_pid=pg_pid, target_db=target_db)
            self.connecter.cursor.execute(sql)

            if isinstance(target_db, dict):
                message = Messenger.TERMINATE_DB_CONN_DONE.format(
                    target_dbname=target_db['name'])
            else:
                message = Messenger.TERMINATE_DB_CONN_DONE.format(
                    target_dbname=target_db)
            self.logger.info(message)

        except Exception as e:
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
        Target:
            - terminate every connection to some PostgreSQL databases (except
            the current one, if it is connected to one of the target
            databases).
        '''
        message = Messenger.BEGINNING_TERMINATE_DBS_CONN
        self.logger.highlight('info', message, 'white')

        for target_db in self.target_dbs:
            self.terminate_backend_db(target_db)

        self.logger.highlight('info', Messenger.TERMINATE_DBS_CONN_DONE,
                              'green')

    def terminate_backend_all(self):
        '''
        Target:
            - remove every connection to PostgreSQL (except the current one).
        '''
        sql = self.query_terminate_backend_all

        try:
            message = Messenger.BEGINNING_TERMINATE_ALL_CONN
            self.logger.highlight('info', message, 'white')

            pg_pid = self.connecter.get_pid_str()  # Get PID variable's name
            sql = sql.format(pg_pid=pg_pid)
            self.connecter.cursor.execute(sql)

            self.logger.highlight('info', Messenger.TERMINATE_ALL_CONN_DONE,
                                  'green')

        except Exception as e:
            self.logger.debug('Error en la función "terminate_backend_all": '
                              '{}.'.format(str(e)))
            message = Messenger.TERMINATE_ALL_CONN_FAIL
            self.logger.highlight('warning', message, 'yellow', effect='bold')
