#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from logger.logger import Logger
from const.const import Messenger
from const.const import Queries
from casting.casting import Casting
from checker.checker import Checker


class Terminator:

    target_all = None  # Flag which determinates if terminate any connection
    target_user = None  # Terminate any connection of an specific user
    target_dbs = []  # Terminate any connection to a list of databases
    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages

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

        if target_dbs is None:
            self.target_dbs = []
        elif isinstance(target_dbs, list):
            self.target_dbs = target_dbs
        else:
            self.target_dbs = Casting.str_to_list(target_dbs)

        message = Messenger.TERMINATOR_VARS.format(
            server=self.connecter.server, user=self.connecter.user,
            port=self.connecter.port, target_all=self.target_all,
            target_user=target_user, target_dbs=self.target_dbs)
        self.logger.debug(Messenger.TERMINATOR_VARS_INTRO)
        self.logger.debug(message)

    def terminate_backend_user(self):
        '''
        Target:
            - terminate every connection of a specific user to PostgreSQL (as
              long as the target user is the one who is running the program).
        '''
        message = Messenger.BEGINNING_TERMINATE_USER_CONN.format(
            target_user=self.target_user)
        self.logger.highlight('info', message, 'white')

        try:
            pg_pid = self.connecter.get_pid_str()  # Get PID variable's name

            sql = Queries.GET_CURRENT_PG_USER
            self.connecter.cursor.execute(sql)
            current_pg_user = self.connecter.cursor.fetchone()[0]

            if self.target_user == current_pg_user:
                message = Messenger.TARGET_USER_IS_CURRENT_USER.format(
                    target_user=self.target_user)
                self.logger.highlight('warning', message, 'yellow')

            else:
                formatted_sql = Queries.BACKEND_PG_USER_EXISTS.format(
                    pg_pid=pg_pid, target_user=self.target_user)
                self.connecter.cursor.execute(formatted_sql)
                result = self.connecter.cursor.fetchone()

                if result:
                    formatted_sql = Queries.TERMINATE_BACKEND_PG_USER.format(
                        pg_pid=pg_pid, target_user=self.target_user)
                    self.connecter.cursor.execute(formatted_sql)
                else:
                    message = Messenger.NO_USER_CONNS.format(
                        target_user=self.target_user)
                    self.logger.info(message)

            message = Messenger.TERMINATE_USER_CONN_DONE.format(
                target_user=self.target_user)
            self.logger.highlight('info', message, 'green')

        except Exception as e:
            self.logger.debug('Error en la función "terminate_backend_user": '
                              '{}.'.format(str(e)))
            message = Messenger.TERMINATE_USER_CONN_FAIL.format(
                target_user=self.target_user)
            self.logger.highlight('warning', message, 'yellow', effect='bold')

        self.logger.highlight('info', Messenger.TERMINATOR_DONE, 'green')

    def terminate_backend_db(self, target_db):
        '''
        Target:
            - terminate every connection to a PostgreSQL database (except the
              current one, if it is connected to the target database).
        '''
        try:
            # This function is sometimes called by other functions which send
            # it a dictionary as the target_db (the majority send a string as
            # the target_db)
            if isinstance(target_db, dict):
                target_db = target_db['name']

            pg_pid = self.connecter.get_pid_str()  # Get PID variable's name

            formatted_sql = Queries.BACKEND_PG_DB_EXISTS.format(
                pg_pid=pg_pid, target_db=target_db)

            self.connecter.cursor.execute(formatted_sql)
            result = self.connecter.cursor.fetchone()

            if result:

                formatted_sql = Queries.TERMINATE_BACKEND_PG_DB.format(
                    pg_pid=pg_pid, target_db=target_db)

                self.connecter.cursor.execute(formatted_sql)

                message = Messenger.TERMINATE_DB_CONN_DONE.format(
                    target_dbname=target_db)
                self.logger.info(message)

            else:
                message = Messenger.NO_DB_CONNS.format(target_db=target_db)
                self.logger.info(message)

        except Exception as e:
            self.logger.debug('Error en la función "terminate_backend_db": '
                              '{}.'.format(str(e)))
            message = Messenger.TERMINATE_DB_CONN_FAIL.format(
                target_dbname=target_db)
            self.logger.highlight('warning', message, 'yellow')

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

        self.logger.highlight('info', Messenger.TERMINATOR_DONE, 'green')

    def terminate_backend_all(self):
        '''
        Target:
            - remove every connection to PostgreSQL (except the current one).
        '''
        try:
            message = Messenger.BEGINNING_TERMINATE_ALL_CONN
            self.logger.highlight('info', message, 'white')

            pg_pid = self.connecter.get_pid_str()  # Get PID variable's name

            formatted_sql = Queries.BACKEND_PG_ALL_EXISTS.format(pg_pid=pg_pid)

            self.connecter.cursor.execute(formatted_sql)
            result = self.connecter.cursor.fetchone()

            if result:
                formatted_sql = Queries.TERMINATE_BACKEND_PG_ALL.format(
                    pg_pid=pg_pid)
                self.connecter.cursor.execute(formatted_sql)
            else:
                self.logger.info(Messenger.NO_CONNS)

            self.logger.highlight('info', Messenger.TERMINATE_ALL_CONN_DONE,
                                  'green')

        except Exception as e:
            self.logger.debug('Error en la función "terminate_backend_all": '
                              '{}.'.format(str(e)))
            message = Messenger.TERMINATE_ALL_CONN_FAIL
            self.logger.highlight('warning', message, 'yellow', effect='bold')

        self.logger.highlight('info', Messenger.TERMINATOR_DONE, 'green')
