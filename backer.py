#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import subprocess  # To execute some commands in the shell

from casting.casting import Casting
from checker.checker import Checker
from const.const import Default
from const.const import Messenger
from date_tools.date_tools import DateTools
from db_selector.db_selector import DbSelector
from dir_tools.dir_tools import Dir
from logger.logger import Logger
from vacuumer import Vacuumer


class Backer:

    bkp_path = ''  # The path where the backups are stored
    group = ''  # The name of the subdirectory where the backups are stored
    bkp_type = ''  # The type of the backups' files
    prefix = ''  # The prefix of the backups' names
    in_dbs = []  # List of databases to be included in the process
    in_regex = ''  # Regular expression which must match the included databases
    # Flag which determinates whether inclusion conditions predominate over the
    # exclusion ones
    in_priority = False
    ex_dbs = []  # List of databases to be excluded in the process
    ex_regex = ''  # Regular expression which must match the excluded databases
    # Flag which determinates whether the templates must be included
    ex_templates = True
    # Flag which determinates whether the included databases must be vacuumed
    # before the backup process
    vacuum = True
    # Use other PostgreSQL user during the backup process (only for superusers)
    db_owner = ''
    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages

    def __init__(self, connecter=None, bkp_path='', group='',
                 bkp_type='dump', prefix='', in_dbs=[], in_regex='',
                 in_priority=False, ex_dbs=['postgres'], ex_regex='',
                 ex_templates=True, vacuum=True, db_owner='', logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        # If backup directory is not specified, create a default one to store
        # the backups
        if bkp_path:
            self.bkp_path = bkp_path
        else:
            self.bkp_path = Default.BKP_PATH
            Dir.create_dir(self.bkp_path, self.logger)

        if group:
            self.group = group
        else:
            self.group = Default.GROUP

        if bkp_type is None:
            self.bkp_type = Default.BKP_TYPE
        elif Checker.check_compress_type(bkp_type):
            self.bkp_type = bkp_type
        else:
            self.logger.stop_exe(Messenger.INVALID_BKP_TYPE)

        self.prefix = prefix

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

        if isinstance(vacuum, bool):
            self.vacuum = vacuum
        elif Checker.str_is_bool(vacuum):
            self.vacuum = Casting.str_to_bool(vacuum)
        else:
            self.logger.stop_exe(Messenger.INVALID_VACUUM)

        if db_owner is None:
            self.db_owner = db_owner
        else:
            self.db_owner = Default.DB_OWNER

    def backup_db(self, dbname, bkps_dir):
        '''
        Target:
            - make a backup of a specified database.
        Parameters:
            - dbname: name of the database which is going to be backuped.
            - bkps_dir: directory where the backup is going to be stored.
        Return:
            - a boolean which indicates the success of the process.
        '''
        success = True
        # Get date and time of the zone
        init_ts = DateTools.get_date()
        # Get current year
        year = str(DateTools.get_year(init_ts))
        # Get current month
        month = str(DateTools.get_month(init_ts))
        # Create new directories with the year and the month of the backup
        bkp_dir = bkps_dir + year + '/' + month + '/'
        Dir.create_dir(bkp_dir, self.logger)
        # Set backup's name
        file_name = self.prefix + 'db_' + dbname + '_' + init_ts + '.' + \
            self.bkp_type
        # Store the command to do depending on the backup type
        if self.bkp_type == 'gz':  # Zip with gzip
            command = 'pg_dump {} -Fc -U {} -h {} -p {} | gzip > {}'.format(
                dbname, self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        elif self.bkp_type == 'bz2':  # Zip with bzip2
            command = 'pg_dump {} -Fc -U {} -h {} -p {} | bzip2 > {}'.format(
                dbname, self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        elif self.bkp_type == 'zip':  # Zip with zip
            command = 'pg_dump {} -Fc -U {} -h {} -p {} | zip > {}'.format(
                dbname, self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        else:  # Do not zip
            command = 'pg_dump {} -Fc -U {} -h {} -p {} > {}'.format(
                dbname, self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        try:
            # Execute the command in console
            result = subprocess.call(command, shell=True)
            if result != 0:
                raise Exception()
        except Exception as e:
            self.logger.debug('Error en la función "backup_db": {}.'.format(
                str(e)))
            success = False

        return success

    def backup_dbs(self, dbs_all):
        '''
        Target:
            - make a backup of some specified databases.
        Parameters:
            - dbs_all: names of the databases which are going to be backuped.
        '''
        self.logger.highlight('info', Messenger.CHECKING_BACKUP_DIR, 'white')

        # Create a new directory with the name of the group
        bkps_dir = self.bkp_path + self.group + Default.DB_BKPS_DIR
        Dir.create_dir(bkps_dir, self.logger)

        self.logger.info(Messenger.DESTINY_DIR.format(path=bkps_dir))

        self.logger.highlight('info', Messenger.PROCESSING_DUMPER, 'white')

        for db in dbs_all:

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
                # Vaccum the database before the backup process if necessary
                if self.vacuum:
                    self.logger.info(Messenger.PRE_VACUUMING_DB.format(
                        dbname=dbname))
                    vacuumer = Vacuumer(self.connecter, self.in_dbs,
                                        self.in_regex, self.in_priority,
                                        self.ex_dbs, self.ex_regex,
                                        self.ex_templates, self.db_owner,
                                        self.logger)

                    # Vacuum the database
                    success = vacuumer.vacuum_db(dbname)
                    if success:
                        message = Messenger.PRE_VACUUMING_DB_DONE.format(
                            dbname=dbname)
                        self.logger.info(message)
                    else:
                        message = Messenger.PRE_VACUUMING_DB_FAIL.format(
                            dbname=dbname)
                        self.logger.highlight('warning', message, 'yellow')
                self.logger.info(Messenger.BEGINNING_DB_BACKER.format(
                    dbname=dbname))

                # Make the backup of the database
                success = self.backup_db(dbname, bkps_dir)
            if success:
                message = Messenger.DB_BACKER_DONE.format(dbname=dbname)
                self.logger.highlight('info', message, 'green')
            else:
                message = Messenger.DB_BACKER_FAIL.format(dbname=dbname)
                self.logger.highlight('warning', message, 'yellow',
                                      effect='bold')
        self.logger.highlight('info', Messenger.DBS_BACKER_DONE, 'green',
                              effect='bold')


class BackerCluster:

    bkp_path = ''  # The path where the backups are stored
    group = ''  # The name of the subdirectory where the backups are stored
    bkp_type = ''  # The type of the backups' files
    prefix = ''  # The prefix of the backups' names
    # Flag which determinates whether the databases must be vacuumed before the
    # backup process
    vacuum = True
    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages

    def __init__(self, connecter=None, bkp_path='', group='',
                 bkp_type='dump', prefix='', vacuum=True, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        # If backup directory is not specified, create a default one to store
        # the backups
        if bkp_path:
            self.bkp_path = bkp_path
        else:
            self.bkp_path = Default.BKP_PATH
            Dir.create_dir(self.bkp_path, self.logger)

        if group:
            self.group = group
        else:
            self.group = Default.GROUP

        if bkp_type is None:
            self.bkp_type = Default.BKP_TYPE
        elif Checker.check_compress_type(bkp_type):
            self.bkp_type = bkp_type
        else:
            self.logger.stop_exe(Messenger.INVALID_BKP_TYPE)

        self.prefix = prefix

        if isinstance(vacuum, bool):
            self.vacuum = vacuum
        elif Checker.str_is_bool(vacuum):
            self.vacuum = Casting.str_to_bool(vacuum)
        else:
            self.logger.stop_exe(Messenger.INVALID_VACUUM)

    def backup_all(self, bkps_dir):
        '''
        Target:
            - make a backup of a cluster.
        Parameters:
            - bkps_dir: directory where the backup is going to be stored.
        Return:
            - a boolean which indicates the success of the process.
        '''
        success = True
        # Get date and time of the zone
        init_ts = DateTools.get_date()
        # Get current year
        year = str(DateTools.get_year(init_ts))
        # Get current month
        month = str(DateTools.get_month(init_ts))
        # Create new directories with the year and the month of the backup
        bkp_dir = bkps_dir + year + '/' + month + '/'
        Dir.create_dir(bkp_dir, self.logger)

        # Set backup's name
        file_name = self.prefix + 'ht_' + self.connecter.server + \
            str(self.connecter.port) + '_cluster_' + init_ts + '.' + \
            self.bkp_type

        # Store the command to do depending on the backup type
        if self.bkp_type == 'gz':  # Zip with gzip
            command = 'pg_dumpall -U {} -h {} -p {} | gzip > {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        elif self.bkp_type == 'bz2':  # Zip with bzip2
            command = 'pg_dumpall -U {} -h {} -p {} | bzip2 > {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        elif self.bkp_type == 'zip':  # Zip with zip
            command = 'pg_dumpall -U {} -h {} -p {} | zip > {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        else:  # Do not zip
            command = 'pg_dumpall -U {} -h {} -p {} > {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        try:
            # Execute the command in console
            result = subprocess.call(command, shell=True)
            if result != 0:
                raise Exception()
        except Exception as e:
            self.logger.debug('Error en la función "backup_all": {}.'.format(
                str(e)))
            success = False

        return success

    def backup_cl(self):
        '''
        Target:
            - vacuum if necessary and make a backup of a cluster.
        '''
        self.logger.highlight('info', Messenger.CHECKING_BACKUP_DIR, 'white')

        # Create a new directory with the name of the group
        bkps_dir = self.bkp_path + self.group + Default.CL_BKPS_DIR
        Dir.create_dir(bkps_dir, self.logger)

        self.logger.info(Messenger.DESTINY_DIR.format(path=bkps_dir))

        # Vaccum the databases before the backup process if necessary
        if self.vacuum:
            vacuumer = Vacuumer(connecter=self.connecter, logger=self.logger)
            vacuumer.connecter.get_cursor_dbs(vacuumer.ex_templates,
                                              vacuumer.db_owner)
            dbs_all = DbSelector.list_pg_dbs(self.connecter.cursor)
            vacuumer.vacuum_dbs(dbs_all)

        self.logger.highlight('info', Messenger.BEGINNING_CL_BACKER, 'white')

        # Make the backup of the cluster
        success = self.backup_all(bkps_dir)
        if success:
            self.logger.highlight('info', Messenger.CL_BACKER_DONE, 'green',
                                  effect='bold')
        else:
            self.logger.highlight('warning', Messenger.CL_BACKER_FAIL,
                                  'yellow', effect='bold')
