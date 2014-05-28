#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import subprocess  # To execute some commands in the shell

from casting.casting import Casting
from checker.checker import Checker
from const.const import Default
from const.const import Messenger
from date_tools.date_tools import DateTools
from logger.logger import Logger


class Vacuumer:

    in_dbs = []  # List of databases to be included in the process
    in_regex = ''  # Regular expression which must match the included databases
    # Flag which determinates whether inclusion conditions predominate over the
    # exclusion ones
    in_priority = False
    ex_dbs = []  # List of databases to be excluded in the process
    ex_regex = ''  # Regular expression which must match the excluded databases
    # Flag which determinates whether the templates must be included
    ex_templates = True
    # Use other PostgreSQL user during the backup process (only for superusers)
    db_owner = ''
    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages

    def __init__(self, connecter=None, in_dbs=[], in_regex='',
                 in_priority=False, ex_dbs=['postgres'], ex_regex='',
                 ex_templates=True, db_owner='', logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if isinstance(in_dbs, list):
            self.in_dbs = in_dbs
        else:
            self.in_dbs = Casting.str_to_list(in_dbs)

        if Checker.check_regex(in_regex):
            self.in_regex = in_regex
        else:
            self.logger.stop_exe(Messenger.INVALID_IN_REGEX)

        if isinstance(in_priority, bool):
            self.in_priority = in_priority
        elif Checker.str_is_bool(in_priority):
            self.in_priority = Casting.str_to_bool(in_priority)
        else:
            self.logger.stop_exe(Messenger.INVALID_IN_PRIORITY)

        if isinstance(ex_dbs, list):
            self.ex_dbs = ex_dbs
        else:
            self.ex_dbs = Casting.str_to_list(ex_dbs)

        if Checker.check_regex(ex_regex):
            self.ex_regex = ex_regex
        else:
            self.logger.stop_exe(Messenger.INVALID_EX_REGEX)

        if isinstance(ex_templates, bool):
            self.ex_templates = ex_templates
        elif Checker.str_is_bool(ex_templates):
            self.ex_templates = Casting.str_to_bool(ex_templates)
        else:
            self.logger.stop_exe(Messenger.INVALID_EX_TEMPLATES)

        if db_owner is None:
            self.db_owner = Default.DB_OWNER
        else:
            self.db_owner = db_owner

        message = Messenger.VACUUMER_VARS.format(
            server=self.connecter.server, user=self.connecter.user,
            port=self.connecter.port, in_dbs=self.in_dbs,
            in_regex=self.in_regex, in_priority=self.in_priority,
            ex_dbs=self.ex_dbs, ex_regex=self.ex_regex,
            ex_templates=self.ex_templates, db_owner=self.db_owner)
        self.logger.debug(Messenger.VACUUMER_VARS_INTRO)
        self.logger.debug(message)

    def vacuum_db(self, dbname):
        '''
        Target:
            - vacuum a PostgreSQL database.
        Parameters:
            - dbname: name of the database which is going to be vacuumed.
        Return:
            - a boolean which indicates the success of the process.
        '''
        success = True

        # Store the command to do
        command = 'vacuumdb {} -U {} -h {} -p {}'.format(
            dbname, self.connecter.user, self.connecter.server,
            self.connecter.port)

        try:
            # Execute the command in console
            result = subprocess.call(command, shell=True)
            if result != 0:
                raise Exception()
        except Exception as e:
            self.logger.debug('Error en la función "vacuum_db": {}.'.format(
                str(e)))
            success = False
        return success

    def vacuum_dbs(self, vacuum_list):
        '''
        Target:
            - vacuum a group of PostgreSQL databases.
        Parameters:
            - vacuum_list: names of the databases which are going to be
              vacuumed.
        '''
        if vacuum_list:
            self.logger.highlight('info', Messenger.BEGINNING_VACUUMER,
                                  'white')

        for db in vacuum_list:

            dbname = db['name']

            message = Messenger.PROCESSING_DB.format(dbname=dbname)
            self.logger.highlight('info', message, 'cyan')

            # Let the user know whether the database connection is allowed
            if not db['allow_connection']:
                message = Messenger.FORBIDDEN_DB_CONNECTION.format(
                    dbname=dbname)
                self.logger.highlight('warning', message, 'yellow',
                                      effect='bold')
                success = False
            else:
                start_time = DateTools.get_current_datetime()
                # Vacuum the database
                success = self.vacuum_db(dbname)
                end_time = DateTools.get_current_datetime()
                # Get and show the process' duration
                diff = DateTools.get_diff_datetimes(start_time, end_time)

            if success:
                message = Messenger.DB_VACUUMER_DONE.format(dbname=dbname,
                                                            diff=diff)
                self.logger.highlight('info', message, 'green')

            else:
                message = Messenger.DB_VACUUMER_FAIL.format(dbname=dbname)
                self.logger.highlight('warning', message, 'yellow',
                                      effect='bold')

        self.logger.highlight('info', Messenger.VACUUMER_DONE, 'green',
                              effect='bold')
