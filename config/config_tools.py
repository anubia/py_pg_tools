#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import configparser  # To parse config files
import os  # To work with directories and files

from const.const import Messenger
from logger.logger import Logger


class LogCfgParser:

    logger = None  # Logger to show and log some messages
    cfg = None  # Parser which stores the variables of the config file
    log_vars = {}  # Dictionary to store the loaded logger variables

    def __init__(self):
        pass

    def load_cfg(self, cfg_file):
        '''
        Target:
            - create a parser and read a config file.
        Parameters:
            - cfg_file: the config file to be readed.
        '''
        try:
            self.cfg = configparser.ConfigParser()
            # If config file exists, read it
            if os.path.exists(cfg_file):
                self.cfg.read(cfg_file)
            else:
                raise Exception()
        except Exception as e:
            # Create logger in the exception to avoid redundancy errors
            if not self.logger:
                self.logger = Logger()
            self.logger.debug('Error en la función "load_cfg": {}.'.format(
                str(e)))
            self.logger.stop_exe(Messenger.INVALID_CFG_PATH)

    def parse_logger(self):
        '''
        Target:
            - get the logger variables from a configuration file and store them
              in a dictionary.
        '''
        try:
            self.log_vars = {
                'log_dir': self.cfg.get('settings', 'log_dir').strip(),
                'level': self.cfg.get('settings', 'level').strip(),
                'mute': self.cfg.get('settings', 'mute').strip(),
            }
        except Exception as e:
            # Create logger in the exception to avoid redundancy errors
            if not self.logger:
                self.logger = Logger()
            self.logger.debug('Error en la función "parse_logger": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.LOGGER_CFG_DAMAGED)


class CfgParser:

    logger = None  # Logger to show and log some messages
    cfg = None  # Parser which stores the variables of the config file
    conn_vars = {}  # Dictionary to store the loaded connection variables
    bkp_vars = {}  # Dictionary to store the loaded backup variables
    kill_vars = {}  # Dictionary to store the loaded terminator variables
    mail_vars = {}  # Dictionary to store the loaded logger variables

    def __init__(self, logger):
        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

    def load_cfg(self, cfg_file):
        '''
        Target:
            - create a parser and read a config file.
        Parameters:
            - cfg_file: the config file to be readed.
        '''
        try:  # Probar si hay excepciones en...
            self.cfg = configparser.ConfigParser()  # Crear un Parser
            if os.path.exists(cfg_file):
                self.cfg.read(cfg_file)  # Parsear el archivo .cfg
            else:
                raise Exception()
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "load_cfg": {}.'.format(
                str(e)))
            self.logger.stop_exe(Messenger.INVALID_CFG_PATH)

    def parse_connecter(self):
        '''
        Target:
            - get the connecter variables from a configuration file and store
              them in a dictionary.
        '''
        try:
            self.conn_vars = {
                'server': self.cfg.get('postgres', 'server').strip(),
                'user': self.cfg.get('postgres', 'username').strip(),
                'port': self.cfg.get('postgres', 'port'),
            }
        except Exception as e:
            self.logger.debug('Error en la función "parse_connecter": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.CONNECTER_CFG_DAMAGED)

    def parse_mailer(self):
        '''
        Target:
            - get the mailer variables from a configuration file and store
              them in a dictionary.
        '''
        try:
            self.mail_vars = {
                'name': self.cfg.get('from', 'name').strip(),
                'address': self.cfg.get('from', 'address').strip(),
                'password': self.cfg.get('from', 'password').strip(),
                'to': self.cfg.get('to', 'to').strip(),
                'cc': self.cfg.get('to', 'cc').strip(),
                'bcc': self.cfg.get('to', 'bcc').strip(),
                'level': self.cfg.get('settings', 'level').strip(),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_mailer": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.MAILER_CFG_DAMAGED)

    def parse_alterer(self):
        '''
        Target:
            - get the alterer variables from a configuration file and store
              them in a dictionary.
        '''
        try:
            self.bkp_vars = {
                'in_dbs': self.cfg.get('settings', 'in_dbs'),
                'old_role': self.cfg.get('settings', 'old_role'),
                'new_role': self.cfg.get('settings', 'new_role'),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_alterer": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.ALTERER_CFG_DAMAGED)

    def parse_backer(self):
        '''
        Target:
            - get the backer variables from a configuration file and store them
              in a dictionary (database case).
        '''
        try:
            self.bkp_vars = {
                'bkp_path': self.cfg.get('dir', 'bkp_path').strip(),
                'group': self.cfg.get('dir', 'group').strip(),
                'bkp_type': self.cfg.get('file', 'bkp_type').strip(),
                'prefix': self.cfg.get('file', 'prefix').strip(),
                'in_dbs': self.cfg.get('includes', 'in_dbs'),
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                'ex_dbs': self.cfg.get('excludes', 'ex_dbs'),
                'ex_regex': self.cfg.get('excludes', 'ex_regex').strip(),
                'ex_templates': self.cfg.get(
                    'excludes', 'ex_templates').strip(),
                'vacuum': self.cfg.get('other', 'vacuum').strip(),
                'db_owner': self.cfg.get('other', 'db_owner').strip(),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_backer": {}.'.format(
                str(e)))
            self.logger.stop_exe(Messenger.DB_BACKER_CFG_DAMAGED)

    def parse_backer_cluster(self):
        '''
        Target:
            - get the backer variables from a configuration file and store them
              in a dictionary (cluster case).
        '''
        try:
            self.bkp_vars = {
                'bkp_path': self.cfg.get('dir', 'bkp_path').strip(),
                'group': self.cfg.get('dir', 'group').strip(),
                'bkp_type': self.cfg.get('file', 'bkp_type').strip(),
                'prefix': self.cfg.get('file', 'prefix').strip(),
                'vacuum': self.cfg.get('other', 'vacuum').strip(),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_backer_cluster": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.CL_BACKER_CFG_DAMAGED)

    def parse_dropper(self):
        '''
        Target:
            - get the dropper variables from a configuration file and store
              them in a dictionary.
        '''
        try:
            self.bkp_vars = {
                'in_dbs': self.cfg.get('includes', 'in_dbs'),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_dropper": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.DROPPER_CFG_DAMAGED)

    def parse_replicator(self):
        '''
        Target:
            - get the replicator variables from a configuration file and store
              them in a dictionary.
        '''
        try:
            self.bkp_vars = {
                'new_dbname': self.cfg.get('settings', 'new_dbname'),
                'original_dbname': self.cfg.get('settings', 'original_dbname'),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_replicator": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.REPLICATOR_CFG_DAMAGED)

    def parse_restorer(self):
        '''
        Target:
            - get the restorer variables from a configuration file and store
              them in a dictionary (database case).
        '''
        try:
            self.bkp_vars = {
                'bkp_path': self.cfg.get('settings', 'bkp_path'),
                'new_dbname': self.cfg.get('settings', 'new_dbname'),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_restorer": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.DB_RESTORER_CFG_DAMAGED)

    def parse_restorer_cluster(self):
        '''
        Target:
            - get the restorer variables from a configuration file and store
              them in a dictionary (cluster case).
        '''
        try:
            self.bkp_vars = {
                'bkp_path': self.cfg.get('settings', 'bkp_path'),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_restorer_cluster": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.CL_RESTORER_CFG_DAMAGED)

    def parse_scheduler(self):
        '''
        Target:
            - get the scheduler variables from a configuration file and store
              them in a dictionary.
        '''
        try:
            self.bkp_vars = {
                'a_line': self.cfg.get('add', 'line').strip(),
                'a_m': self.cfg.get('add', 'm').strip(),
                'a_h': self.cfg.get('add', 'h').strip(),
                'a_dom': self.cfg.get('add', 'dom').strip(),
                'a_mon': self.cfg.get('add', 'mon').strip(),
                'a_dow': self.cfg.get('add', 'dow').strip(),
                'a_user': self.cfg.get('add', 'user').strip(),
                'a_command': self.cfg.get('add', 'command').strip(),
                'r_line': self.cfg.get('remove', 'line').strip(),
                'r_m': self.cfg.get('remove', 'm').strip(),
                'r_h': self.cfg.get('remove', 'h').strip(),
                'r_dom': self.cfg.get('remove', 'dom').strip(),
                'r_mon': self.cfg.get('remove', 'mon').strip(),
                'r_dow': self.cfg.get('remove', 'dow').strip(),
                'r_user': self.cfg.get('remove', 'user').strip(),
                'r_command': self.cfg.get('remove', 'command').strip(),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_scheduler": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.SCHEDULER_CFG_DAMAGED)

    def parse_terminator(self):
        '''
        Target:
            - get the terminator variables from a configuration file and store
              them in a dictionary.
        '''
        try:
            self.kill_vars = {
                'kill_all': self.cfg.get('settings', 'kill_all').strip(),
                'kill_user': self.cfg.get('settings', 'kill_user').strip(),
                'kill_dbs': self.cfg.get('settings', 'kill_dbs').strip(),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_terminator": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.TERMINATOR_CFG_DAMAGED)

    def parse_trimmer(self):
        '''
        Target:
            - get the trimmer variables from a configuration file and store
              them in a dictionary (database case).
        '''
        try:
            self.bkp_vars = {
                'bkp_path': self.cfg.get('dir', 'bkp_path').strip(),
                'prefix': self.cfg.get('file', 'prefix').strip(),
                'in_dbs': self.cfg.get('includes', 'in_dbs'),
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                'ex_dbs': self.cfg.get('excludes', 'ex_dbs'),
                'ex_regex': self.cfg.get('excludes', 'ex_regex').strip(),
                'min_n_bkps': self.cfg.get('conditions', 'min_n_bkps').strip(),
                'exp_days': self.cfg.get('conditions', 'exp_days').strip(),
                'max_size': self.cfg.get('conditions', 'max_size').strip(),
                'pg_warnings': self.cfg.get('other', 'pg_warnings').strip(),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_trimmer": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.DB_TRIMMER_CFG_DAMAGED)

    def parse_trimmer_cluster(self):
        '''
        Target:
            - get the trimmer variables from a configuration file and store
              them in a dictionary (cluster case).
        '''
        try:
            self.bkp_vars = {
                'bkp_path': self.cfg.get('dir', 'bkp_path').strip(),
                'prefix': self.cfg.get('file', 'prefix').strip(),
                'min_n_bkps': self.cfg.get('conditions', 'min_n_bkps').strip(),
                'exp_days': self.cfg.get('conditions', 'exp_days').strip(),
                'max_size': self.cfg.get('conditions', 'max_size').strip(),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_trimmer_cluster": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.CL_TRIMMER_CFG_DAMAGED)

    def parse_vacuumer(self):
        '''
        Target:
            - get the vacuumer variables from a configuration file and store
              them in a dictionary.
        '''
        try:
            self.bkp_vars = {
                'in_dbs': self.cfg.get('includes', 'in_dbs'),
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                'ex_dbs': self.cfg.get('excludes', 'ex_dbs'),
                'ex_regex': self.cfg.get('excludes', 'ex_regex').strip(),
                'ex_templates': self.cfg.get(
                    'excludes', 'ex_templates').strip(),
                'db_owner': self.cfg.get('other', 'db_owner').strip(),
            }

        except Exception as e:
            self.logger.debug('Error en la función "parse_vacuumer": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.VACUUMER_CFG_DAMAGED)
