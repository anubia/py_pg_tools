#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


#from casting.casting import Casting
from const.const import Messenger
from logger.logger import Logger


class Informer:

    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages
    connpids = []
    dbnames = []  # List of databases to get some info about
    usernames = []  # List of users to get some info about

    def __init__(self, connecter=None, connpids=[], dbnames=[], usernames=[],
                 logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        self.connpids = connpids
        self.dbnames = dbnames
        self.usernames = usernames

    def show_pg_dbnames(self):
        '''
        Target:
            - show the names of every PostgreSQL database.
        '''
        msg_len = len(Messenger.SHOWING_DBS_NAME)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_DBS_NAME
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        # Get all the names of PostgreSQL databases and show them
        dbnames = self.connecter.get_pg_dbnames()

        if dbnames:
            for dbname in dbnames:
                self.logger.info(dbname)
        else:
            message = Messenger.NO_DB_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def show_pg_usernames(self):
        '''
        Target:
            - show the names of every PostgreSQL user.
        '''
        msg_len = len(Messenger.SHOWING_USERS_NAME)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_USERS_NAME
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        # Get all the names of PostgreSQL users and show them
        usernames = self.connecter.get_pg_usernames()

        if usernames:
            for username in usernames:
                self.logger.info(username)
        else:
            message = Messenger.NO_USER_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def show_pg_connpids(self):
        '''
        Target:
            - show the PIDs of every PostgreSQL backend.
        '''
        msg_len = len(Messenger.SHOWING_CONNS_PID)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_CONNS_PID
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        # Get all the PIDs of PostgreSQL backends and show them
        connpids = self.connecter.get_pg_connpids()

        if connpids:
            for connpid in connpids:
                self.logger.info(str(connpid))
        else:
            message = Messenger.NO_CONN_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def show_pg_dbs_data(self):
        '''
        Target:
            - show some info about every PostgreSQL database.
        '''
        msg_len = len(Messenger.SHOWING_DBS_DATA)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_DBS_DATA
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        dbs_data = []
        # Get every PostgreSQL database if no list specified, otherwise, keep
        # the specified list (given by console arguments)
        if self.dbnames == []:
            self.dbnames = self.connecter.get_pg_dbnames()

        for dbname in self.dbnames:  # Get data of each selected database
            result = self.connecter.get_pg_db_data(dbname)
            if result:
                dbs_data.append(result)

        if dbs_data:
            for db in dbs_data:
                message = Messenger.DATNAME + str(db['datname'])
                self.logger.highlight('info', message, 'cyan')
                message = Messenger.OWNER + str(db['owner'])
                self.logger.info(message)
                message = Messenger.ENCODING + str(db['encoding'])
                self.logger.info(message)
                message = Messenger.DATSIZE + str(db['size'])
                self.logger.info(message)
                message = Messenger.DATCOLLATE + str(db['datcollate'])
                self.logger.info(message)
                message = Messenger.DATCTYPE + str(db['datctype'])
                self.logger.info(message)
                message = Messenger.DATISTEMPLATE + str(db['datistemplate'])
                self.logger.info(message)
                message = Messenger.DATALLOWCONN + str(db['datallowconn'])
                self.logger.info(message)
                message = Messenger.DATCONNLIMIT + str(db['datconnlimit'])
                self.logger.info(message)
                message = Messenger.DATLASTSYSOID + str(db['datlastsysoid'])
                self.logger.info(message)
                message = Messenger.DATFROZENXID + str(db['datfrozenxid'])
                self.logger.info(message)
                message = Messenger.DATTABLESPACE + str(db['dattablespace'])
                self.logger.info(message)
                message = Messenger.DATACL + str(db['datacl'])
                self.logger.info(message)
        else:
            message = Messenger.NO_DB_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def show_pg_users_data(self):
        '''
        Target:
            - show some info about every PostgreSQL user.
        '''
        msg_len = len(Messenger.SHOWING_USERS_DATA)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_USERS_DATA
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        users_data = []
        # Get every PostgreSQL user if no list specified, otherwise, keep
        # the specified list (given by console arguments)

        if self.usernames == []:
            self.usernames = self.connecter.get_pg_usernames()

        for username in self.usernames:  # Get data of each selected user
            result = self.connecter.get_pg_user_data(username)
            if result:
                users_data.append(result)

        pg_version = self.connecter.get_pg_version()  # Get PostgreSQL version

        if users_data:
            for user in users_data:
                message = Messenger.USENAME + str(user['usename'])
                self.logger.highlight('info', message, 'cyan')
                message = Messenger.USESYSID + str(user['usesysid'])
                self.logger.info(message)
                message = Messenger.USECREATEDB + str(user['usecreatedb'])
                self.logger.info(message)
                message = Messenger.USESUPER + str(user['usesuper'])
                self.logger.info(message)
                message = Messenger.USECATUPD + str(user['usecatupd'])
                self.logger.info(message)
                if pg_version >= self.connecter.PG_PID_VERSION_THRESHOLD:
                    message = Messenger.USEREPL + str(user['userepl'])
                    self.logger.info(message)
                message = Messenger.PASSWD + str(user['passwd'])
                self.logger.info(message)
                message = Messenger.VALUNTIL + str(user['valuntil'])
                self.logger.info(message)
                message = Messenger.USECONFIG + str(user['useconfig'])
                self.logger.info(message)
        else:
            message = Messenger.NO_USER_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def show_pg_conns_data(self):
        '''
        Target:
            - show some info about every PostgreSQL backend.
        '''
        msg_len = len(Messenger.SHOWING_CONNS_DATA)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_CONNS_DATA
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        conns_data = []
        # Get every PostgreSQL connection if no list specified, otherwise, keep
        # the specified list (given by console arguments)
        if self.connpids == []:
            self.connpids = self.connecter.get_pg_connpids()

        for connpid in self.connpids:  # Get data of each selected backend
            result = self.connecter.get_pg_conn_data(connpid)
            if result:
                conns_data.append(result)

        pg_version = self.connecter.get_pg_version()  # Get PostgreSQL version

        if conns_data:
            for conn in conns_data:
                if pg_version >= self.connecter.PG_PID_VERSION_THRESHOLD:
                    message = Messenger.PID + str(conn['pid'])
                else:
                    message = Messenger.PROCPID + str(conn['procpid'])
                self.logger.highlight('info', message, 'cyan')
                message = Messenger.DATID + str(conn['datid'])
                self.logger.info(message)
                message = Messenger.DATNAME + str(conn['datname'])
                self.logger.info(message)
                message = Messenger.USESYSID + str(conn['usesysid'])
                self.logger.info(message)
                message = Messenger.USENAME + str(conn['usename'])
                self.logger.info(message)
                message = Messenger.APPLICATION_NAME + str(
                    conn['application_name'])
                self.logger.info(message)
                message = Messenger.CLIENT_ADDR + str(conn['client_addr'])
                self.logger.info(message)
                message = Messenger.CLIENT_HOSTNAME + str(
                    conn['client_hostname'])
                self.logger.info(message)
                message = Messenger.CLIENT_PORT + str(conn['client_port'])
                self.logger.info(message)
                message = Messenger.BACKEND_START + str(conn['backend_start'])
                self.logger.info(message)
                message = Messenger.XACT_START + str(conn['xact_start'])
                self.logger.info(message)
                message = Messenger.QUERY_START + str(conn['query_start'])
                self.logger.info(message)
                if pg_version >= self.connecter.PG_PID_VERSION_THRESHOLD:
                    message = Messenger.STATE_CHANGE + str(
                        conn['state_change'])
                    self.logger.info(message)
                message = Messenger.WAITING + str(conn['waiting'])
                self.logger.info(message)
                if pg_version >= self.connecter.PG_PID_VERSION_THRESHOLD:
                    message = Messenger.STATE + str(conn['state'])
                    self.logger.info(message)
                    message = Messenger.QUERY + str(conn['query'])
                    self.logger.info(message)
        else:
            message = Messenger.NO_CONN_DATA_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def show_pg_version(self):
        '''
        Target:
            - show PostgreSQL version.
        '''
        msg_len = len(Messenger.SHOWING_PG_VERSION)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_PG_VERSION
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        pretty_pg_version = self.connecter.get_pretty_pg_version()
        if pretty_pg_version:
            self.logger.info(pretty_pg_version)
        else:
            message = Messenger.NO_PG_VERSION_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def show_pg_nversion(self):
        '''
        Target:
            - show PostgreSQL version in numeric format.
        '''
        pg_version = self.connecter.get_pg_version()
        print(pg_version)

    def show_pg_time_start(self):
        '''
        Target:
            - show when PostgreSQL was started.
        '''
        msg_len = len(Messenger.SHOWING_PG_TIME_START)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_PG_TIME_START
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        pg_time_start = self.connecter.get_pg_time_start()
        if pg_time_start:
            self.logger.info(str(pg_time_start))
        else:
            message = Messenger.NO_PG_TIME_START_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')

    def show_pg_time_up(self):
        '''
        Target:
            - show how long PostgreSQL has been working.
        '''
        msg_len = len(Messenger.SHOWING_PG_TIME_UP)
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')
        message = Messenger.SHOWING_PG_TIME_UP
        self.logger.highlight('info', message, 'white')
        message = '*' * msg_len
        self.logger.highlight('info', message, 'white')

        pg_time_up = self.connecter.get_pg_time_up()
        if pg_time_up:
            self.logger.info(str(pg_time_up))
        else:
            message = Messenger.NO_PG_TIME_UP_TO_SHOW
            self.logger.highlight('warning', message, 'yellow', effect='bold')
