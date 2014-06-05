#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os  # To check the existance of some files

from const.const import Messenger
from const.const import Default
from logger.logger import Logger


class Scheduler:

    cron_path = ''
    cron_file = None
    logger = None  # Logger to show and log some messages

    def __init__(self, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if os.path.isfile(Default.CRON_PATH):
            self.cron_path = Default.CRON_PATH
        else:
            #cron_file = open(Default.CRON_PATH, 'w')
            #cron_file.close()
            self.logger.stop_exe(Messenger.CRON_FILE_DOES_NOT_EXIST.format(
                Default.CRON_PATH))

        #message = Messenger.SCHEDULER_VARS.format()
        #self.logger.debug(Messenger.SCHEDULER_VARS_INTRO)
        #self.logger.debug(message)

    def show_lines(self):
        '''
        Target:
            - show the lines of the program's CRON file.
        '''
        self.cron_file = open(Default.CRON_PATH, 'r')

        for line in self.cron_file:
            line = line.rstrip()
            if line:
                self.logger.info('{}'.format(line))

        self.cron_file.close()
