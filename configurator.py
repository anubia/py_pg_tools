#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from config.config_tools import CfgParser
from config.config_tools import LogCfgParser


class Configurator:

    cfg_type = None  # Type of config file to load
    path = None  # Path of the config file to load
    parser = None  # Parser which stores the variables of the config file
    logger = None  # Logger to show and log some messages

    def __init__(self):
        pass

    def load_cfg(self, cfg_type, path, logger=None):
        '''
        Target:
            - store a config parser with the obtained variables.
        Parameters:
            - cfg_type: the type of config file which is going to be loaded.
            - path: the path of the config file to be loaded.
            - logger: the logger which will be show and log the messages. It
              will be None if the config file to load is for the logger
              configuration.
        '''
        self.cfg_type = cfg_type
        self.path = path

        if self.cfg_type == 'log':
            # Log needs other type of parser to avoid redundancy errors
            self.parser = LogCfgParser()
        else:
            # The other actions will load with the standard parser
            self.parser = CfgParser(logger)

        if self.cfg_type == 'connect':
            self.parser.load_cfg(self.path)
            self.parser.parse_connecter()

        elif self.cfg_type == 'alter':
            self.parser.load_cfg(self.path)
            self.parser.parse_alterer()

        elif self.cfg_type == 'backup':
            self.parser.load_cfg(self.path)
            self.parser.parse_backer()

        elif self.cfg_type == 'backup_all':
            self.parser.load_cfg(self.path)
            self.parser.parse_backer_cluster()

        elif self.cfg_type == 'drop':
            self.parser.load_cfg(self.path)
            self.parser.parse_dropper()

        elif self.cfg_type == 'log':
            self.parser.load_cfg(self.path)
            self.parser.parse_logger()

        elif self.cfg_type == 'mail':
            self.parser.load_cfg(self.path)
            self.parser.parse_mailer()

        elif self.cfg_type == 'replicate':
            self.parser.load_cfg(self.path)
            self.parser.parse_replicator()

        elif self.cfg_type == 'restore':
            self.parser.load_cfg(self.path)
            self.parser.parse_restorer()

        elif self.cfg_type == 'restore_all':
            self.parser.load_cfg(self.path)
            self.parser.parse_restorer_cluster()

        elif self.cfg_type == 'schedule':
            self.parser.load_cfg(self.path)
            self.parser.parse_scheduler()

        elif self.cfg_type == 'trim':
            self.parser.load_cfg(self.path)
            self.parser.parse_trimmer()

        elif self.cfg_type == 'trim_all':
            self.parser.load_cfg(self.path)
            self.parser.parse_trimmer_cluster()

        elif self.cfg_type == 'terminate':
            self.parser.load_cfg(self.path)
            self.parser.parse_terminator()

        elif self.cfg_type == 'vacuum':
            self.parser.load_cfg(self.path)
            self.parser.parse_vacuumer()

        else:
            pass
