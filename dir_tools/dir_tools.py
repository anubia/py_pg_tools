#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import os  # to work with directories and files
import re  # to work with regular expressions

from getpass import getuser

from const.const import Messenger
from const.const import Default
from logger.logger import Logger


class Dir:

    def __init__(self):
        pass

    @staticmethod
    def forbid_root(logger=None):
        '''
        Target:
        - stop the execution of the program if this is being run by "root".
        '''
        if not logger:
            logger = Logger()
        try:
            if getuser() == 'root':  # Get system username
                raise Exception()
        except Exception as e:
            logger.debug('Error en la función "forbid_root": {}.'.format(
                str(e)))
            logger.stop_exe(Messenger.ROOT_NOT_ALLOWED)

    @staticmethod
    def create_dir(path, logger=None):
        '''
        Target:
        - stop the execution of the program if this is being run by "root".
        Parameters:
        - path: directory to create.
        - logger: a logger to show and log some messages.
        '''
        if not logger:
            logger = Logger()

        try:
            if not os.path.exists(path):  # If path does not exist...
                os.makedirs(path)  # Create it
        except Exception as e:
            logger.debug('Error en la función "create_dir": {}.'.format(
                str(e)))
            logger.stop_exe(Messenger.USER_NOT_ALLOWED_TO_CHDIR)

    @staticmethod
    def default_bkps_path():
        '''
        Target:
        - get the default directory where the backups must be stored.
        Return:
        - A string which gives the absolute path where the backups will be
        stored.
        '''
        ## Get the script's directory
        #script_dir = os.path.dirname(os.path.realpath(__file__))
        ## Get the program's main directory
        #parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        ## Get the final path of the backups
        #bkps_folder = 'pg_backups/'
        #bkps_file = os.path.join(parent_dir, bkps_folder)

        return Default.BKP_PATH

    @staticmethod
    def default_cfg_path(subpath):
        '''
        Target:
        - get the default directory where the configuration files should be.
        Parameters:
        - subpath: the last part of the default path which depends on the type
        of configuration file.
        Return:
        - a string which gives the absolute path where a specific configuration
        file should be.
        '''
        # Get the script's directory
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Get the program's main directory
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        # Get the final path of the configuration file
        cfg_folder = 'config/' + subpath
        cfg_file = os.path.join(parent_dir, cfg_folder)

        return cfg_file

    @staticmethod
    def sorted_flist(path):
        '''
        Target:
        - generate a list which contains every file in the specified directory
        (and its subdirectories) sorted by modification date.
        Parameters:
        - path: the directory where the files are.
        Return:
        - a sorted list with all the files in the directory.
        '''
        files_list = []

        for dirname, dirnames, filenames in os.walk(path):
            for file in filenames:
                filepath = os.path.realpath(os.path.join(dirname, file))
                files_list.append(filepath)

        sorted_list = sorted(files_list, key=lambda f: os.stat(f).st_mtime)

        return sorted_list

    @staticmethod
    def get_dbs_bkped(bkps_list=[]):
        '''
        Target:
        - extract the databases' names from the files' names of the list
        received and store them in a list.
        Parameters:
        - bkps_list: a list with backup's files.
        Return:
        - a list with those databases' names extracted from the backup's list.
        '''
        bkped_dbs = []

        # Regular expression which each backup's name must match
        regex = r'(.*)?db_(.+)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
        regex = re.compile(regex)

        for f in bkps_list:

            # Get the file name from the absolute path
            filename = os.path.basename(f)

            # If the file is a backup (matches the established pattern)...
            if re.match(regex, filename):

                # Extract name's parts ([prefix], dbname, date)
                parts = regex.search(filename).groups()

                # If the database's name is not in the list yet, add it
                # (this condition is to avoid repeated names)
                dbname = parts[1]
                if dbname not in bkped_dbs:
                    bkped_dbs.append(dbname)

            else:
                continue

        return bkped_dbs

    @staticmethod
    def show_pg_warnings(pg_dbs=[], bkped_dbs=[], logger=None):
        '''
        Target:
        - compare two lists with databases. This function will be used to show
        which PostgreSQL databases do not have a backup in a specified
        directory and which databases have a backup but are not stored in
        PostgreSQL.
        Parameters:
        - pg_dbs: list of PostgreSQL databases.
        - bkped_dbs: list of databases which have a backup.
        - logger: a logger to show and log some messages.
        '''
        if not logger:
            logger = Logger()

        for dbname in pg_dbs:
            if dbname not in bkped_dbs:  # PostgreSQL without backup
                message = Messenger.NO_BACKUP_FOR_POSTGRESQL_DB.format(
                    dbname=dbname)
                logger.highlight('warning', message, 'purple', effect='bold')

        for dbname in bkped_dbs:
            # Backup of an nonexistent PostgreSQL database
            if dbname not in pg_dbs:
                message = Messenger.NO_POSTGRESQL_DB_FOR_BACKUP.format(
                    dbname=dbname)
                logger.highlight('warning', message, 'purple', effect='bold')

    @staticmethod
    def get_files_tsize(files_list=[]):
        '''
        Target:
        - give the total size in Bytes of a files' list.
        Parameters:
        - files_list: a list with some files' absolute paths.
        Return:
        - an integer which gives the total size in bytes
        '''
        tsize = 0

        for f in files_list:
            file_info = os.stat(f)  # Get file's data
            tsize += file_info.st_size  # Add file's size to the total

        return tsize

    @staticmethod
    def remove_empty_dir(path):
        '''
        Target:
        - remove a directory if empty.
        Parameters:
        - path: the absolute path of the directory.
        '''
        try:
            os.rmdir(path)  # Remove dir (will give an exception if not empty)
        except OSError:
            pass

    @staticmethod
    def remove_empty_dirs(path):
        '''
        Target:
        - remove every subdirectory if empty (even the whole directory in case
        it turns empty).
        Parameters:
        - path: the absolute path of the directory.
        '''
        for root, dirnames, filenames in os.walk(path, topdown=False):
            for dirname in dirnames:
                Dir.remove_empty_dir(os.path.realpath(os.path.join(root,
                                                                   dirname)))
