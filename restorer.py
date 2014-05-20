#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import os  # To check the existance of some files
import re  # To work with regular expressions
import subprocess  # To execute commands in the shell

from const.const import Messenger
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

    def restore_db_backup(self):
        '''
        Target:
            - restore a database's backup in PostgreSQL.
        '''
        # TODO cambiar template0 por otra
        replicator = Replicator(self.connecter, self.new_dbname, 'template0',
                                self.logger)
        self.connecter.allow_db_conn('template0')
        replicator.replicate_pg_db()
        self.connecter.disallow_db_conn('template0')

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
            result = subprocess.call(command, shell=True)
            if result != 0:
                raise Exception()

            message = Messenger.RESTORE_DB_DONE.format(
                db_backup=self.db_backup, new_dbname=self.new_dbname)
            self.logger.highlight('info', message, 'green')

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
            result = subprocess.call(command, shell=True)
            if result != 0:
                raise Exception()

            message = Messenger.RESTORE_CL_DONE.format(
                cluster_backup=self.cluster_backup)
            self.logger.highlight('info', message, 'green')

        except Exception as e:
            self.logger.debug('Error en la función "restore_cluster_backup": '
                              '{}.'.format(str(e)))
            message = Messenger.RESTORE_CL_FAIL.format(
                cluster_backup=self.cluster_backup)
            self.logger.stop_exe(message)
