#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from config.config_tools import CfgParser
from config.config_tools import LogCfgParser
#from logger.logger import Logger


class Configurator:

    cfg_type = None
    path = None
    parser = None
    logger = None

    def __init__(self):
        pass

    def load_cfg(self, cfg_type, path, logger=None):

        self.cfg_type = cfg_type
        self.path = path

        if self.cfg_type == 'log':
            self.parser = LogCfgParser()
        else:
            self.parser = CfgParser(logger)

        if self.cfg_type == 'connect':
            self.parser.load_cfg(self.path)
            self.parser.parse_connecter()

        elif self.cfg_type == 'backup':
            self.parser.load_cfg(self.path)
            self.parser.parse_backer()

        elif self.cfg_type == 'backup_all':
            self.parser.load_cfg(self.path)
            self.parser.parse_backer_cluster()

        elif self.cfg_type == 'log':
            self.parser.load_cfg(self.path)
            self.parser.parse_logger()

        elif self.cfg_type == 'vacuum':
            self.parser.load_cfg(self.path)
            self.parser.parse_vacuumer()

        elif self.cfg_type == 'trim':
            self.parser.load_cfg(self.path)
            self.parser.parse_trimmer()

        elif self.cfg_type == 'trim_all':
            self.parser.load_cfg(self.path)
            self.parser.parse_trimmer_cluster()

        elif self.cfg_type == 'terminate':
            self.parser.load_cfg(self.path)
            self.parser.parse_terminator()
        else:
            pass
