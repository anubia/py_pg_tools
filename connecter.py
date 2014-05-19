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
        '''
        Target:
            - init a connection to PostgreSQL.
        Parameters:
            - server: a server which has PostgreSQL installed.
            - user: PostgreSQL user who makes the connection.
            - port: the target port of the connection.
            - logger: a logger to show and log some messages.
        '''
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
            self.logger.stop_exe('Error de conexión a PostgreSQL.')

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
            self.logger.stop_exe('Error al desconectarse de PostgreSQL.')

    def get_pid_str(self):
        '''
        Target:
            - get the name of the process id depending on the PostgreSQL
            version which is being used. Before the version 9.2 this variable
            was called "procpid", afterwards became "pid".
        Return:
            - a string which gives the name of the vaiable process id.
        '''
        pg_version = self.conn.server_version  # Get PostgreSQL version

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

        return(row['usesuper'])

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
