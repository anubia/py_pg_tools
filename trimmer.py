#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from math import ceil  # To round up some values
import os  # To work with directories and files
import re  # To work with regular expressions
import time  # To calculate time intervals

from casting.casting import Casting
from checker.checker import Checker
from const.const import Default
from const.const import Messenger
from dir_tools.dir_tools import Dir
from logger.logger import Logger


class Trimmer:

    bkp_path = ''  # The path where the backups are stored
    prefix = ''  # The prefix of the backups' names
    in_dbs = []  # List of databases to be included in the process
    in_regex = ''  # Regular expression which must match the included databases
    # Flag which determinates whether inclusion conditions predominate over the
    # exclusion ones
    in_priority = False
    ex_dbs = []  # List of databases to be excluded in the process
    ex_regex = ''  # Regular expression which must match the excluded databases
    min_n_bkps = None  # Minimum number of a database's backups to keep
    exp_days = None  # Number of days which make a backup obsolete
    max_size = None  # Maximum size of a group of database's backups
    # Flag which determinates whether show alerts about PostgreSQL
    pg_warnings = True
    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages

    def __init__(self, bkp_path='', prefix='', in_dbs=[], in_regex='',
                 in_priority=False, ex_dbs=[], ex_regex='', min_n_bkps=1,
                 exp_days=365, max_size='10000MB', pg_warnings=True,
                 connecter=None, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if bkp_path and os.path.isdir(bkp_path):
            self.bkp_path = bkp_path
        else:
            self.logger.stop_exe(Messenger.DIR_DOES_NOT_EXIST)

        if prefix is None:
            self.prefix = Default.PREFIX
        else:
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

        if min_n_bkps is None:
            self.min_n_bkps = Default.MIN_N_BKPS
        elif isinstance(min_n_bkps, int):
            self.min_n_bkps = min_n_bkps
        elif Checker.str_is_int(min_n_bkps):
            self.min_n_bkps = Casting.str_to_int(min_n_bkps)
        else:
            self.logger.stop_exe(Messenger.INVALID_MIN_BKPS)

        if exp_days is None:
            self.exp_days = Default.EXP_DAYS
        elif isinstance(exp_days, int) and exp_days >= -1:
            self.exp_days = exp_days
        elif Checker.str_is_valid_exp_days(exp_days):
            self.exp_days = Casting.str_to_int(exp_days)
        else:
            self.logger.stop_exe(Messenger.INVALID_OBS_DAYS)
        if max_size is None:
            self.max_size = Default.MAX_SIZE
        elif Checker.str_is_valid_max_size(max_size):
            self.max_size = max_size
        else:
            self.logger.stop_exe(Messenger.INVALID_MAX_TSIZE)

        if isinstance(pg_warnings, bool):
            self.pg_warnings = pg_warnings
        elif Checker.str_is_bool(pg_warnings):
            self.pg_warnings = Casting.str_to_bool(pg_warnings)
        else:
            self.logger.stop_exe(Messenger.INVALID_PG_WARNINGS)

        if self.pg_warnings:
            if connecter:
                self.connecter = connecter
            else:
                self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        message = Messenger.DB_TRIMMER_VARS.format(
            bkp_path=self.bkp_path, prefix=self.prefix, in_dbs=self.in_dbs,
            in_regex=self.in_regex, in_priority=self.in_priority,
            ex_dbs=self.ex_dbs, ex_regex=self.ex_regex,
            min_n_bkps=self.min_n_bkps, exp_days=self.exp_days,
            max_size=self.max_size, pg_warnings=self.pg_warnings)
        self.logger.debug(Messenger.DB_TRIMMER_VARS_INTRO)
        self.logger.debug(message)

    def trim_db(self, dbname, db_bkps_list):
        '''
        Target:
            - remove (if necessary) some database's backups, taking into
              account some parameters in the following order: minimum number of
              backups to keep > obsolete backups.
        Parameters:
            - dbname: name of the database whose backups are going to be
              trimmed.
            - db_bkps_list: list of backups of a database to analyse and trim.
        '''
        if self.exp_days == -1:  # No expiration date
            x_days_ago = None
        else:
            x_days_ago = time.time() - (60 * 60 * 24 * self.exp_days)

        # Split a string with size and unit of measure into a dictionary
        max_size = Casting.str_to_max_size(self.max_size)

        if max_size['unit'] == 'MB':
            equivalence = 10 ** 6
        elif max_size['unit'] == 'GB':
            equivalence = 10 ** 9
        elif max_size['unit'] == 'TB':
            equivalence = 10 ** 12
        elif max_size['unit'] == 'PB':
            equivalence = 10 ** 15

        self.max_size = max_size['size'] * equivalence

        # Store the total number of backups of the database
        num_bkps = len(db_bkps_list)
        # Clone the list to avoid conflict errors when removing
        db_bkps_lt = db_bkps_list[:]

        unlinked = False

        message = Messenger.BEGINNING_DB_TRIMMER.format(dbname=dbname)
        self.logger.highlight('info', message, 'white')

        for f in db_bkps_list:

            # Break if number of backups do not exceed the minimum
            if num_bkps <= self.min_n_bkps:
                break

            file_info = os.stat(f)

            # Obsolete backup
            if x_days_ago and file_info.st_ctime < x_days_ago:

                self.logger.info(Messenger.DELETING_OBSOLETE_BACKUP % f)
                os.unlink(f)  # Remove backup's file
                unlinked = True
                # Update the number of backups of the database
                num_bkps -= 1
                db_bkps_lt.remove(f)  # Update the list of database's backups

        # Get total size of the backups in Bytes
        tsize = Dir.get_files_tsize(db_bkps_lt)
        # Get total size of the backups in the selected unit of measure
        tsize_unit = ceil(tsize / equivalence)

        ## UNCOMMENT NEXT SECTION TO PROCEDURE WITH THE BACKUP'S DELETION IF
        ## THEIR TOTAL SIZE EXCEEDS THE SPECIFIED MAXIMUM SIZE

        #db_bkps_list = db_bkps_lt[:]

        #for f in db_bkps_list:
            ## If there are less backups than the minimum required...
            #if num_bkps <= self.min_n_bkps:
                #break
            #if tsize <= self.max_size:
                #break
            #else:
                #file_info = os.stat(f)
                #self.logger.info('Tamaño de copias de seguridad en disco '
                                 #'mayor que {} {}: eliminando el archivo '
                                 #'{}...' %
                                 #(max_size['size'], max_size['unit'], f))
                #os.unlink(f)  # Remove backup's file
                #unlinked = True
                ## Update the number of backups of the database
                #num_bkps -= 1
                ## Update the list of database's backups
                ## db_bkps_lt.remove(f)
                #tsize -= file_info.st_size  # Update total size after deletion

        if not unlinked:

            message = Messenger.NO_DB_BACKUP_DELETED.format(dbname=dbname)
            self.logger.highlight('warning', message, 'yellow')

        if tsize > self.max_size:  # Total size exceeds the maximum

            message = Messenger.DB_BKPS_SIZE_EXCEEDED.format(
                dbname=dbname, tsize_unit=tsize_unit, size=max_size['size'],
                unit=max_size['unit'])
            self.logger.highlight('warning', message, 'yellow', effect='bold')

        self.logger.highlight('info', Messenger.DB_TRIMMER_DONE.format(
            dbname=dbname), 'green')

    def trim_dbs(self, bkps_list, dbs_to_clean):
        '''
        Target:
            - remove (if necessary) some backups of a group of databases,
              taking into account some parameters in the following order:
              minimum number of backups to keep > obsolete backups.
        Parameters:
            - bkps_list: list of backups found in the specified directory.
            - dbs_to_clean: name of the database whose backups are going to be
              trimmed.
        '''
        # If not prefix specified, trim all the backups (not only the ones
        # without prefix)
        if self.prefix:
            regex = r'(' + self.prefix + ')db_(.+)_(\d{8}_\d{6}_.+)\.' \
                    '(?:dump|bz2|gz|zip)$'
        else:
            regex = r'(.*)?db_(.+)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
        regex = re.compile(regex)

        for dbname in dbs_to_clean:

            db_bkps_list = []

            for file in bkps_list:

                # Extract file's name from the absolute path
                filename = os.path.basename(file)

                # If file matches regex (it means that file is a backup)
                if re.match(regex, filename):

                    # Extract parts of the name ([prefix], dbname, date)
                    parts = regex.search(filename).groups()
                    # Store the database's name whose this backup belongs to
                    fdbname = parts[1]

                    # If that backup belongs to a database which is has to be
                    # trimmed
                    if dbname == fdbname:
                        # Append backup to the group of database's backups
                        db_bkps_list.append(file)
                    else:
                        continue
                else:
                    continue

            # Remove (if necessary) some backups of the specified database
            self.trim_db(dbname, db_bkps_list)

        # Remove directories which could be empty after the trim
        Dir.remove_empty_dirs(self.bkp_path)


class TrimmerCluster:

    bkp_path = ''  # The path where the backups are stored
    prefix = ''  # The prefix of the backups' names
    min_n_bkps = None  # Minimum number of a database's backups to keep
    exp_days = None  # Number of days which make a backup obsolete
    max_size = None  # Maximum size of a group of database's backups

    def __init__(self, bkp_path='', prefix='', min_n_bkps=1, exp_days=365,
                 max_size=5000, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if bkp_path and os.path.isdir(bkp_path):
            self.bkp_path = bkp_path
        else:
            self.logger.stop_exe(Messenger.DIR_DOES_NOT_EXIST)

        if prefix is None:
            self.prefix = Default.PREFIX
        else:
            self.prefix = prefix

        if min_n_bkps is None:
            self.min_n_bkps = Default.MIN_N_BKPS
        elif isinstance(min_n_bkps, int):
            self.min_n_bkps = min_n_bkps
        elif Checker.str_is_int(min_n_bkps):
            self.min_n_bkps = Casting.str_to_int(min_n_bkps)
        else:
            self.logger.stop_exe(Messenger.INVALID_MIN_BKPS)

        if exp_days is None:
            self.exp_days = Default.EXP_DAYS
        elif isinstance(exp_days, int) and exp_days >= -1:
            self.exp_days = exp_days
        elif Checker.str_is_valid_exp_days(exp_days):
            self.exp_days = Casting.str_to_int(exp_days)
        else:
            self.logger.stop_exe(Messenger.INVALID_OBS_DAYS)

        if max_size is None:
            self.max_size = Default.MAX_SIZE
        elif Checker.str_is_valid_max_size(max_size):
            self.max_size = max_size
        else:
            self.logger.stop_exe(Messenger.INVALID_MAX_TSIZE)

        message = Messenger.CL_TRIMMER_VARS.format(
            bkp_path=self.bkp_path, prefix=self.prefix,
            min_n_bkps=self.min_n_bkps, exp_days=self.exp_days,
            max_size=self.max_size)
        self.logger.debug(Messenger.CL_TRIMMER_VARS_INTRO)
        self.logger.debug(message)

    def trim_cluster(self, ht_bkps_list):
        '''
        Target:
            - remove (if necessary) some cluster's backups, taking into
              account some parameters in the following order: minimum number of
              backups to keep > obsolete backups.
        Parameters:
            - ht_bkps_list: list of backups of a cluster to analyse and trim.
        '''
        if self.exp_days == -1:  # No expiration date
            x_days_ago = None
        else:
            x_days_ago = time.time() - (60 * 60 * 24 * self.exp_days)

        max_size = Casting.str_to_max_size(self.max_size)

        if max_size['unit'] == 'MB':
            equivalence = 10 ** 6
        elif max_size['unit'] == 'GB':
            equivalence = 10 ** 9
        elif max_size['unit'] == 'TB':
            equivalence = 10 ** 12
        elif max_size['unit'] == 'PB':
            equivalence = 10 ** 15

        self.max_size = max_size['size'] * equivalence

        # Store the total number of backups of the cluster
        num_bkps = len(ht_bkps_list)
        # Clone the list to avoid conflict errors when removing
        ht_bkps_lt = ht_bkps_list[:]

        unlinked = False

        self.logger.highlight('info', Messenger.BEGINNING_CL_TRIMMER, 'white')

        for f in ht_bkps_list:

            # Break if number of backups do not exceed the minimum
            if num_bkps <= self.min_n_bkps:
                break

            file_info = os.stat(f)

            # Obsolete backup
            if x_days_ago and file_info.st_ctime < x_days_ago:

                self.logger.info(Messenger.DELETING_OBSOLETE_BACKUP % f)
                os.unlink(f)  # Remove backup's file
                unlinked = True
                # Update the number of backups of the database
                num_bkps -= 1
                ht_bkps_lt.remove(f)  # Update the list of cluster's backups

        # Get total size of the backups in Bytes
        tsize = Dir.get_files_tsize(ht_bkps_lt)
        # Get total size of the backups in the selected unit of measure
        tsize_unit = ceil(tsize / equivalence)

        ## UNCOMMENT NEXT SECTION TO PROCEDURE WITH THE BACKUP'S DELETION IF
        ## THEIR TOTAL SIZE EXCEEDS THE SPECIFIED MAXIMUM SIZE

        #ht_bkps_list = ht_bkps_lt[:]

        #for f in ht_bkps_list:
            ## If there are less backups than the minimum required...
            #if num_bkps <= self.min_n_bkps:
                #break
            #if tsize <= self.max_size:
                #break
            #else:
                #file_info = os.stat(f)
                #self.logger.info('Tamaño de copias de seguridad en disco '
                                 #'mayor que {} {}: eliminando el archivo '
                                 #'{}...' %
                                 #(max_size['size'], max_size['unit'], f))
                #os.unlink(f)  # Remove backup's file
                #unlinked = True
                ## Update the number of backups of the cluster
                #num_bkps -= 1
                ## ht_bkps_lt.remove(f)  # Update the list of cluster's backups
                #tsize -= file_info.st_size  # Update total size after deletion

        if not unlinked:

            message = Messenger.NO_CL_BACKUP_DELETED
            self.logger.highlight('warning', message, 'yellow')

        if tsize > self.max_size:  # Total size exceeds the maximum

            message = Messenger.CL_BKPS_SIZE_EXCEEDED.format(
                tsize_unit=tsize_unit, size=max_size['size'],
                unit=max_size['unit'])
            self.logger.highlight('warning', message, 'yellow', effect='bold')

        self.logger.highlight('info', Messenger.CL_TRIMMER_DONE, 'green')

    def trim_clusters(self, bkps_list):
        '''
        Target:
            - remove (if necessary) some backups of a cluster, taking into
              account some parameters in the following order: minimum number of
              backups to keep > obsolete backups.
        Parameters:
            - bkps_list: list of backups found in the specified directory.
        '''
        # If not prefix specified, trim all the backups (not only the ones
        # without prefix)
        if self.prefix:
            regex = r'(' + self.prefix + ')ht_(.+_cluster)_' \
                    '(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
        else:
            regex = r'(.*)?ht_(.+_cluster)_(\d{8}_\d{6}_.+)\.' \
                    '(?:dump|bz2|gz|zip)$'
        regex = re.compile(regex)

        ht_bkps_list = []

        for file in bkps_list:

            # Extract file's name from the absolute path
            filename = os.path.basename(file)

            # If file matches regex (it means that file is a backup)
            if re.match(regex, filename):

                # Append backup to the group of cluster's backups
                ht_bkps_list.append(file)

            else:
                continue

        if ht_bkps_list:

            # Remove (if necessary) some backups of the cluster
            self.trim_cluster(ht_bkps_list)
            # Remove directories which could be empty after the trim
            Dir.remove_empty_dirs(self.bkp_path)

        else:
            self.logger.highlight('warning', Messenger.NO_BACKUP_IN_DIR,
                                  'yellow', effect='bold')
