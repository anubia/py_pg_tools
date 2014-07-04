#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import os  # To check the existance of some files
import re  # To work with regular expressions
import subprocess  # To execute commands in the shell

from const.const import Messenger
from const.const import Default
from date_tools.date_tools import DateTools
from logger.logger import Logger
from replicator import Replicator


class Restorer:

    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages
    db_backup = ''  # Absolute path of the backup file (of a database)
    new_dbname = ''  # New name for the database restored in PostgreSQL

    def __init__(self, connecter=None, db_backup='', new_dbname='',
                 logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if db_backup and os.path.isfile(db_backup):
            self.db_backup = db_backup
        else:
            self.logger.stop_exe(Messenger.NO_BKP_TO_RESTORE)

        if new_dbname:
            self.new_dbname = new_dbname
        else:
            self.logger.stop_exe(Messenger.NO_DBNAME_TO_RESTORE)

        message = Messenger.DB_RESTORER_VARS.format(
            server=self.connecter.server, user=self.connecter.user,
            port=self.connecter.port, db_backup=self.db_backup,
            new_dbname=self.new_dbname)
        self.logger.debug(Messenger.DB_RESTORER_VARS_INTRO)
        self.logger.debug(message)

    def restore_db_backup(self):
        '''
        Target:
            - restore a database's backup in PostgreSQL.
        '''
        replicator = Replicator(self.connecter, self.new_dbname,
                                Default.RESTORING_TEMPLATE, self.logger)
        result = self.connecter.allow_db_conn(Default.RESTORING_TEMPLATE)
        if result:
            replicator.replicate_pg_db()
            self.connecter.disallow_db_conn(Default.RESTORING_TEMPLATE)
        else:
            self.logger.stop_exe(Messenger.ALLOW_DB_CONN_FAIL.format(
                dbname=Default.RESTORING_TEMPLATE))

        # Regular expression which must match the backup's name
        regex = r'.*db_(.+)_(\d{8}_\d{6}_.+)\.(dump|bz2|gz|zip)$'
        regex = re.compile(regex)

        if re.match(regex, self.db_backup):
            # Store the parts of the backup's name (name, date, ext)
            parts = regex.search(self.db_backup).groups()
            # Store only the extension to know the type of file
            ext = parts[2]
        else:
            self.logger.stop_exe(Messenger.NO_BACKUP_FORMAT)

        message = Messenger.BEGINNING_DB_RESTORER.format(
            db_backup=self.db_backup, new_dbname=self.new_dbname)
        self.logger.highlight('info', message, 'white')
        self.logger.info(Messenger.WAIT_PLEASE)

        if ext == 'gz':
            command = 'gunzip -c {} -k | pg_restore -U {} -h {} -p {} ' \
                      '-d {}'.format(self.db_backup, self.connecter.user,
                                     self.connecter.server,
                                     self.connecter.port, self.new_dbname)
        elif ext == 'bz2':
            command = 'bunzip2 -c {} -k | pg_restore -U {} -h {} -p {} ' \
                      '-d {}'.format(self.db_backup, self.connecter.user,
                                     self.connecter.server,
                                     self.connecter.port, self.new_dbname)
        elif ext == 'zip':
            command = 'unzip -p {} | pg_restore -U {} -h {} -p {} ' \
                      '-d {}'.format(self.db_backup, self.connecter.user,
                                     self.connecter.server,
                                     self.connecter.port, self.new_dbname)
        else:
            command = 'pg_restore -U {} -h {} -p {} -d {} {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, self.new_dbname, self.db_backup)

        try:
            start_time = DateTools.get_current_datetime()
            # Make the restauration of the database
            result = subprocess.call(command, shell=True)
            end_time = DateTools.get_current_datetime()
            # Get and show the process' duration
            diff = DateTools.get_diff_datetimes(start_time, end_time)

            if result != 0:
                raise Exception()

            message = Messenger.RESTORE_DB_DONE.format(
                db_backup=self.db_backup, new_dbname=self.new_dbname,
                diff=diff)
            self.logger.highlight('info', message, 'green')

            self.logger.highlight('info', Messenger.RESTORER_DONE, 'green',
                                  effect='bold')

        except Exception as e:
            self.logger.debug('Error en la función "restore_db_backup": '
                              '{}.'.format(str(e)))
            message = Messenger.RESTORE_DB_FAIL.format(
                db_backup=self.db_backup, new_dbname=self.new_dbname)
            self.logger.stop_exe(message)


class RestorerCluster:

    # An object with connection parameters to connect to PostgreSQL
    connecter = None
    logger = None  # Logger to show and log some messages
    cluster_backup = ''  # Absolute path of the backup file (of a cluster)

    def __init__(self, connecter=None, cluster_backup='', logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if cluster_backup and os.path.isfile(cluster_backup):
            self.cluster_backup = cluster_backup
        else:
            self.logger.stop_exe(Messenger.NO_BKP_TO_RESTORE)

        message = Messenger.CL_RESTORER_VARS.format(
            server=self.connecter.server, user=self.connecter.user,
            port=self.connecter.port, cluster_backup=self.cluster_backup)
        self.logger.debug(Messenger.CL_RESTORER_VARS_INTRO)
        self.logger.debug(message)

    def restore_cluster_backup(self):
        '''
        Target:
            - restore a cluster's backup in PostgreSQL. The cluster must have
              been created before this process.
        '''
        # Regular expression which must match the backup's name
        regex = r'.*ht_(.+_cluster)_(\d{8}_\d{6}_.+)\.(dump|bz2|gz|zip)$'
        regex = re.compile(regex)

        if re.match(regex, self.cluster_backup):
            # Store the parts of the backup's name (servername, date, ext)
            parts = regex.search(self.cluster_backup).groups()
            # Store only the extension to know the type of file
            ext = parts[2]
        else:
            Messenger.NO_BACKUP_FORMAT

        message = Messenger.BEGINNING_CL_RESTORER.format(
            cluster_backup=self.cluster_backup)
        self.logger.highlight('info', message, 'white')
        self.logger.info(Messenger.WAIT_PLEASE)

        if ext == 'gz':
            command = 'gunzip -c {} -k | psql postgres -U {} -h {} ' \
                      '-p {}'.format(
                          self.cluster_backup, self.connecter.user,
                          self.connecter.server, self.connecter.port)
        elif ext == 'bz2':
            command = 'bunzip2 -c {} -k | psql postgres -U {} -h {} ' \
                      '-p {}'.format(
                          self.cluster_backup, self.connecter.user,
                          self.connecter.server, self.connecter.port)
        elif ext == 'zip':
            command = 'unzip -p {} | psql postgres -U {} -h {} -p {}'.format(
                self.cluster_backup, self.connecter.user,
                self.connecter.server, self.connecter.port)
        else:
            # TODO Hacer que desaparezcan todos los comandos SQL que se ven en
            # consola, crear automáticamente el clúster antes de restaurarlo
            command = 'psql postgres -U {} -h {} -p {} < {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, self.cluster_backup)

        try:
            start_time = DateTools.get_current_datetime()
            # Make the restauration of the cluster
            result = subprocess.call(command, shell=True)
            end_time = DateTools.get_current_datetime()
            # Get and show the process' duration
            diff = DateTools.get_diff_datetimes(start_time, end_time)

            if result != 0:
                raise Exception()

            message = Messenger.RESTORE_CL_DONE.format(
                cluster_backup=self.cluster_backup, diff=diff)
            self.logger.highlight('info', message, 'green')

            self.logger.highlight('info', Messenger.RESTORER_DONE, 'green',
                                  effect='bold')

        except Exception as e:
            self.logger.debug('Error en la función "restore_cluster_backup": '
                              '{}.'.format(str(e)))
            message = Messenger.RESTORE_CL_FAIL.format(
                cluster_backup=self.cluster_backup)
            self.logger.stop_exe(message)
