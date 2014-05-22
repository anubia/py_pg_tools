#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import psycopg2  # To work with PostgreSQL
import psycopg2.extras  # To get real field names from PostgreSQL

from casting.casting import Casting
from checker.checker import Checker
from const.const import Messenger
from logger.logger import Logger


class Connecter:

    conn = None  # The PostgreSQL connection object
    cursor = None  # The cursor of the PostgreSQL connection
    server = None  # The target host of the connection
    user = None  # The PostgreSQL user who makes the connection
    port = None  # The target port of the connection
    logger = None  # A logger to show and log some messages

    # PostgreSQL version (from this one on some variables change their names)
    PG_PID_VERSION_THRESHOLD = 90200
    pg_pid_91 = 'procpid'  # Name for PostgreSQL PID variable till version 9.1
    pg_pid_92 = 'pid'  # Name for PostgreSQL PID variable since version 9.2

    def __init__(self, server, user, port, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        self.server = server

        self.user = user

        if isinstance(port, int):
            self.port = port
        elif Checker.str_is_int(port):
            self.port = Casting.str_to_int(port)
        else:
            self.logger.stop_exe(Messenger.INVALID_PORT)

        try:
            self.conn = psycopg2.connect(host=self.server,
                                         database='postgres', user=self.user,
                                         port=self.port)
            # TODO: añadir argumento password a psycopg2.connect en caso de que
            # en futuro se quisiese añadir la opción de introducir contraseña
            # manualmente en vez de revisar .pgpass
            self.cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:
            self.logger.debug('Error en la función "pg_connect": {}.'.format(
                str(e)))
            self.logger.stop_exe(Messenger.CONNECT_FAIL)

    def pg_disconnect(self):
        '''
        Target:
            - disconnect from PostgreSQL.
        '''
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            self.logger.debug('Error en la función "pg_disconnect": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.DISCONNECT_FAIL)

    def get_pg_version(self):
        '''
        Target:
            - get the PostgreSQL version.
        Return:
            - a integer which gives the PostgreSQL version.
        '''
        return self.conn.server_version

    def get_pretty_pg_version(self):
        '''
        Target:
            - get the pretty PostgreSQL version.
        Return:
            - a string which gives the PostgreSQL version and more details.
        '''
        query_get_pretty_pg_version = 'select version();'
        try:
            self.cursor.execute(query_get_pretty_pg_version)
            pretty_pg_version = self.cursor.fetchone()

            return pretty_pg_version[0]

        except Exception as e:
            self.logger.debug('Error en la función "get_pretty_pg_version": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Messenger.GET_PG_VERSION_FAIL,
                                  'yellow')
            return None

    def get_pid_str(self):
        '''
        Target:
            - get the name of the process id depending on the PostgreSQL
            version which is being used. Before the version 9.2 this variable
            was called "procpid", afterwards became "pid".
        Return:
            - a string which gives the name of the vaiable process id.
        '''
        pg_version = self.get_pg_version()  # Get PostgreSQL version

        if pg_version < self.PG_PID_VERSION_THRESHOLD:
            return self.pg_pid_91
        else:
            return self.pg_pid_92

    def is_pg_superuser(self):
        '''
        Target:
            - check if a user connected to PostgreSQL has a superuser role.
        Return:
            - a boolean which indicates whether a user is a PostgreSQL
            superuser or not.
        '''
        query_is_superuser = (
            'SELECT usesuper '
            'FROM pg_user '
            'WHERE usename = CURRENT_USER;'
        )
        self.cursor.execute(query_is_superuser)
        row = self.cursor.fetchone()

        return row['usesuper']

    def get_pg_time_start(self):
        '''
        Target:
            - get the time when PostgreSQL was started.
        Return:
            - a date which indicates the time when PostgreSQL was started.
        '''
        query_get_pg_time_start = 'SELECT pg_postmaster_start_time();'

        try:
            self.cursor.execute(query_get_pg_time_start)
            row = self.cursor.fetchone()

            return row[0]

        except Exception as e:
            self.logger.debug('Error en la función "get_pg_time_start": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Messenger.GET_PG_TIME_START_FAIL,
                                  'yellow')
            return None

    def get_pg_time_up(self):
        '''
        Target:
            - get how long PostgreSQL has been working.
        Return:
            - a date which indicates how long PostgreSQL has been working.
        '''
        query_get_pg_time_up = 'SELECT now() - pg_postmaster_start_time();'

        try:
            self.cursor.execute(query_get_pg_time_up)
            row = self.cursor.fetchone()

            return row[0]

        except Exception as e:
            self.logger.debug('Error en la función "get_pg_time_up": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Messenger.GET_PG_TIME_UP_FAIL,
                                  'yellow')
            return None

    def get_cursor_dbs(self, ex_templates=True, db_owner=''):
        '''
        Target:
            - do different queries to PostgreSQL depending on the parameters
            received, and store the results in the connection cursor.
        Parameters:
            - ex_templates: flag which determinates whether or not get those
            databases which are templates.
            - db_owner: the name of the user whose databases are going to be
            obtained.
        '''
        query_get_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d;'
        )
        query_get_ex_template_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d '
            'WHERE not datistemplate;'
        )
        query_get_owner_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d '
            'WHERE pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
        )
        query_get_ex_template_owner_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d '
            'WHERE not datistemplate '
            'AND pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
        )

        # Get all databases (no templates) of a specific owner
        if db_owner and ex_templates:
            self.cursor.execute(query_get_ex_template_owner_dbs, (db_owner, ))
        # Get all databases (templates too) of a specific owner
        elif db_owner and ex_templates is False:
            self.cursor.execute(query_get_owner_dbs, (db_owner, ))
        # Get all databases (no templates)
        elif not db_owner and ex_templates is False:
            self.cursor.execute(query_get_dbs)
        else:  # Get all databases (templates too)
            self.cursor.execute(query_get_ex_template_dbs)

    def get_pg_db_data(self, dbname):
        '''
        Target:
            - show some info about a specified database.
        Parameters:
            - dbname: name of the database whose information is going to be
            shown.
        '''
        query_get_db_data = (
            'SELECT datname, pg_get_userbyid(datdba) as owner, '
            'pg_encoding_to_char(encoding) as encoding, datcollate, datctype, '
            'datistemplate, datallowconn, datconnlimit, datlastsysoid, '
            'datfrozenxid, dattablespace, datacl, '
            'pg_size_pretty(pg_database_size(datname)) as size '
            'FROM pg_database '
            'WHERE datname = (%s);'
        )

        try:
            self.cursor.execute(query_get_db_data, (dbname, ))
            db = self.cursor.fetchone()

        except Exception as e:
            self.logger.debug('Error en la función "get_pg_db_data": '
                              '{}.'.format(str(e)))
            message = Messenger.GET_PG_DB_DATA.format(dbname=dbname)
            self.logger.highlight('warning', message, 'yellow')
            db = None

        return db

    def get_pg_user_data(self, username):
        '''
        Target:
            - show some info about a specified user.
        Parameters:
            - username: name of the user whose information is going to be
            shown.
        '''
        query_get_user_data_91 = (
            'SELECT usename, usesysid, usecreatedb, usesuper, usecatupd, '
            'passwd, valuntil, useconfig '
            'FROM pg_user '
            'WHERE usename = (%s);'
        )

        query_get_user_data_92 = (
            'SELECT usename, usesysid, usecreatedb, usesuper, usecatupd, '
            'userepl, passwd, valuntil, useconfig '
            'FROM pg_user '
            'WHERE usename = (%s);'
        )

        try:
            pg_version = self.get_pg_version()  # Get PostgreSQL version

            if pg_version < self.PG_PID_VERSION_THRESHOLD:
                self.cursor.execute(query_get_user_data_91, (username, ))
            else:
                self.cursor.execute(query_get_user_data_92, (username, ))
            user = self.cursor.fetchone()

        except Exception as e:
            self.logger.debug('Error en la función "get_pg_user_data": '
                              '{}.'.format(str(e)))
            message = Messenger.GET_PG_USER_DATA.format(username=username)
            self.logger.highlight('warning', message, 'yellow')
            user = None

        return user

    def get_pg_conn_data(self, connpid):
        '''
        Target:
            - show some info about backends.
        Parameters:
            - connpid: PID of the backend whose information is going to be
            shown.
        '''
        query_get_conn_data_91 = (
            'SELECT datid, datname, procpid, usesysid, usename, '
            'application_name, client_addr, client_hostname, client_port, '
            'backend_start, xact_start, query_start, waiting '
            'FROM pg_stat_activity '
            'WHERE procpid = (%s);'
        )
        query_get_conn_data_92 = (
            'SELECT datid, datname, pid, usesysid, usename, application_name, '
            'client_addr, client_hostname, client_port, backend_start, '
            'xact_start, query_start, state_change, waiting, state, query '
            'FROM pg_stat_activity '
            'WHERE pid = (%s);'
        )

        try:
            pg_version = self.get_pg_version()  # Get PostgreSQL version

            if pg_version < self.PG_PID_VERSION_THRESHOLD:
                self.cursor.execute(query_get_conn_data_91, (connpid, ))
            else:
                self.cursor.execute(query_get_conn_data_92, (connpid, ))
            conn = self.cursor.fetchone()

        except Exception as e:
            self.logger.debug('Error en la función "get_pg_conn_data": '
                              '{}.'.format(str(e)))
            message = Messenger.GET_PG_CONN_DATA.format(connpid=connpid)
            self.logger.highlight('warning', message, 'yellow')
            conn = None

        return conn

    def get_pg_dbnames(self, ex_templates=False):
        '''
        Target:
            - get PostgreSQL databases' names depending on the parameters
            received, and store the results in the connection cursor.
        Parameters:
            - ex_templates: flag which determinates whether or not get those
            databases which are templates.
        '''
        query_get_dbnames = (
            'SELECT datname '
            'FROM pg_database;'
        )
        query_get_ex_template_dbnames = (
            'SELECT datname '
            'FROM pg_database '
            'WHERE not datistemplate;'
        )

        try:
            if ex_templates:
                self.cursor.execute(query_get_ex_template_dbnames)
            else:
                self.cursor.execute(query_get_dbnames)
            result = self.cursor.fetchall()

            dbnames = []
            for record in result:
                dbnames.append(record['datname'])

        except Exception as e:
            self.logger.debug('Error en la función "get_pg_dbnames": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Messenger.GET_PG_DBNAMES_DATA,
                                  'yellow')
            dbnames = None

        return dbnames

    def get_pg_usernames(self):
        '''
        Target:
            - get PostgreSQL users' names.
        '''
        query_get_usernames = (
            'SELECT usename '
            'FROM pg_user;'
        )

        try:
            # TODO: ver por qué si peta get_pg_db_data, peta esto, y lo mismo
            # con varias funciones de este informer
            self.cursor.execute(query_get_usernames)
            result = self.cursor.fetchall()

            usernames = []
            for record in result:
                usernames.append(record['usename'])

        except Exception as e:
            self.logger.debug('Error en la función "get_pg_usernames": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Messenger.GET_PG_USERNAMES_DATA,
                                  'yellow')
            usernames = None

        return usernames

    def get_pg_connpids(self):
        '''
        Target:
            - get PostgreSQL backends' PIDs.
        '''
        pid = self.get_pid_str()  # Get PID variable's name
        query_get_pids = (
            'SELECT {pid} as pid '
            'FROM pg_stat_activity;'.format(pid=pid)
        )

        try:
            self.cursor.execute(query_get_pids)
            result = self.cursor.fetchall()

            pids = []
            for record in result:
                pids.append(record['pid'])

        except Exception as e:
            self.logger.debug('Error en la función "get_pg_connpids": '
                              '{}.'.format(str(e)))
            self.logger.highlight('warning', Messenger.GET_PG_CONNPIDS_DATA,
                                  'yellow')
            pids = None

        return pids

    def allow_db_conn(self, dbname):
        '''
        Target:
            - enable connections to a specified PostgreSQL database.
        Parameters:
            - dbname: name of the database whose property "datallowconn" is
            going to be changed to allow connections to itself.
        '''
        query_db_allow_conn = (
            'UPDATE pg_database '
            'SET datallowconn = TRUE '
            'WHERE datname = (%s);'
        )

        self.cursor.execute(query_db_allow_conn, (dbname, ))
        self.conn.commit()  # Make changes permanent

    def disallow_db_conn(self, dbname):
        '''
        Target:
            - disable connections to a specified PostgreSQL database.
        Parameters:
            - dbname: name of the database whose property "datallowconn" is
            going to be changed to disallow connections to itself.
        '''
        query_db_disallow_conn = (
            'UPDATE pg_database '
            'SET datallowconn = FALSE '
            'WHERE datname = (%s);'
        )

        self.cursor.execute(query_db_disallow_conn, (dbname, ))
        self.conn.commit()  # Make changes permanent
