#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import logging  # to create logger objects
import logging.handlers  # to create console and file handlers
import os.path  # to check the existance of some paths
import re  # to work with regular expressions
import sys  # to work with the argv array

from casting.casting import Casting
from checker.checker import Checker
from const.const import Default
from date_tools.date_tools import DateTools


class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):

    # Regular expression to escape colors in file handler
    ansi_escape = re.compile(r'\x1b[^m]*m')

    def emit(self, record):
        '''
        Target:
            - escape ANSI codes in file handlers, this way they will not be
            seen in log files.
        Parameters:
            - record: a line to be written in the log file.
        '''
        record.msg = self.ansi_escape.sub('', record.msg)
        logging.handlers.RotatingFileHandler.emit(self, record)


class Logger:

    logger = None  # A logger to show and log some messages
    log_dir = None  # The directory where the log files will be stored
    level = None  # The verbosity level of the file handler
    # A flag to determinate if use a file handler and create log files
    mute = False

    def __init__(self, log_dir=None, level=None, mute=False):
        '''
        Target:
            - create a logger to store the activity of the program.
        '''
        if log_dir:
            self.log_dir = log_dir
        else:
            # Get script's directory
            script_dir = os.path.dirname(os.path.realpath(__file__))
            # Get program's main directory
            script_pardir = os.path.abspath(os.path.join(script_dir,
                                                         os.pardir))
            # Get directory to store log files
            self.log_dir = os.path.join(script_pardir, 'log/')

        if level in Default.LOG_LEVELS:
            self.level = level
        else:
            self.level = Default.LOG_LEVEL

        if isinstance(mute, bool):
            self.mute = mute
        elif Checker.str_is_bool(mute):
            self.mute = Casting.str_to_bool(mute)
        else:
            self.mute = Default.MUTE

        # Get current date and time of the zone
        init_ts = DateTools.get_date()
        # Get file's name
        script_filename = os.path.basename(sys.argv[0])
        # Get main program's name
        script_name = os.path.splitext(script_filename)[0]
        # Set format for the log files' names
        log_name = script_name + '_' + init_ts + '.log'
        # Set absolute path for log files
        log_file = os.path.join(self.log_dir, log_name)
        # Create logger with the main program's name
        self.logger = logging.getLogger(script_name)
        # Set DEBUG as maximum verbosity level
        self.logger.setLevel(logging.DEBUG)
        # Create a handler for console
        ch = logging.StreamHandler()
        # Set the verbosity of console handler to "INFO"
        ch.setLevel(logging.INFO)
        # Create a format for console and file logs
        formatter = logging.Formatter('%(asctime)s - PID %(process)d - '
                                      '%(levelname)-4s - %(message)s',
                                      datefmt='%Y.%m.%d_%H:%M:%S_%Z')
        if self.mute is False:  # If log files are required...
            # Create directory for log files if it does not exist yet
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            # Set size for each log file
            max_bytes = 4 * 1024 * 1024  # 4MiB
            # Create a file handler
            fh = CustomRotatingFileHandler(log_file, 'a', max_bytes, 10)
            # Set the verbosity of console handler to the selected level
            if self.level == 'debug':
                fh.setLevel(logging.DEBUG)
            if self.level == 'info':
                fh.setLevel(logging.INFO)
            if self.level == 'warning':
                fh.setLevel(logging.WARNING)
            if self.level == 'error':
                fh.setLevel(logging.ERROR)
            if self.level == 'critical':
                fh.setLevel(logging.CRITICAL)

            fh.setFormatter(formatter)  # Set format for file handler

        ch.setFormatter(formatter)  # Set format for console handler
        self.logger.addHandler(ch)  # Add console handler

        if self.mute is False:  # If log files are required...
            self.logger.addHandler(fh)  # Add file handler

    def debug(self, message):
        '''
        Target:
            - show and log a message with debug level.
        Parameters:
            - message: the message to show and log.
        '''
        self.logger.debug(message)

    def info(self, message):
        '''
        Target:
            - show and log a message with info level.
        Parameters:
            - message: the message to show and log.
        '''
        self.logger.info(message)

    def warning(self, message):
        '''
        Target:
            - show and log a message with warning level.
        Parameters:
            - message: the message to show and log.
        '''
        self.logger.warning(message)

    def error(self, message):
        '''
        Target:
            - show and log a message with error level.
        Parameters:
            - message: the message to show and log.
        '''
        self.logger.error(message)

    def critical(self, message):
        '''
        Target:
            - show and log a message with critical level.
        Parameters:
            - message: the message to show and log.
        '''
        self.logger.critical(message)

    def highlight(self, level, message, txtcolor='default', bgcolor='black',
                  effect='default'):
        '''
        Target:
            - show a message with colors and effects in console and log it.
        Parameters:
            - message: the message to show and log.
        '''
        eff = Logger.__get_effect_code(effect)
        bg = Logger.__get_bgcolor_code(bgcolor)
        txt = Logger.__get_txtcolor_code(txtcolor)

        if level == 'info':
            self.info('\033[{};{};{}m'.format(eff, bg, txt) + message +
                      '\033[0m')
        elif level == 'warning':
            self.warning('\033[{};{};{}m'.format(eff, bg, txt) + message +
                         '\033[0m')
        elif level == 'error':
            self.error('\033[{};{};{}m'.format(eff, bg, txt) + message +
                       '\033[0m')
        elif level == 'critical':
            self.critical('\033[{};{};{}m'.format(eff, bg, txt) + message +
                          '\033[0m')
        else:
            self.debug('\033[{};{};{}m'.format(eff, bg, txt) + message +
                       '\033[0m')

    def stop_exe(self, message):
        '''
        Target:
            - show and log an error message with colors and effcets, and stop
            the execution of the program.
        Parameters:
            - message: the message to show and log.
        '''
        self.highlight('error', message, 'white', 'red', 'bold')
        sys.exit(1)

    @staticmethod
    def __get_txtcolor_code(txtcolor):
        '''
        Target:
            - turn a string with the name of a text color into its ANSI code.
        Parameters:
            - txtcolor: the common name of a color.
        Return:
            - an integer which gives an ANSI code.
        '''
        txtcolors = {
            'black': 90,
            'darkred': 31,
            'red': 91,
            'darkgreen': 32,
            'green': 92,
            'orange': 33,
            'yellow': 93,
            'darkblue': 34,
            'blue': 94,
            'darkpurple': 35,
            'purple': 95,
            'darkcyan': 36,
            'cyan': 96,
            'white': 97,
            'default': 37,
        }

        return txtcolors[txtcolor]

    @staticmethod
    def __get_bgcolor_code(bgcolor):
        '''
        Target:
            - turn a string with the name of a background color into its ANSI
            code.
        Parameters:
            - bgcolor: the common name of a color.
        Return:
            - an integer which gives an ANSI code.
        '''
        bgcolors = {
            'black': 40,
            'red': 41,
            'green': 42,
            'orange': 43,
            'blue': 44,
            'purple': 45,
            'cyan': 46,
            'white': 47,
        }

        return bgcolors[bgcolor]

    @staticmethod
    def __get_effect_code(effect):
        '''
        Target:
            - turn a string with the name of an effect into its ANSI code.
        Parameters:
            - effect: the common name of an effect.
        Return:
            - an integer which gives an ANSI code.
        '''
        effects = {
            'default': 0,
            'bold': 1,
            'underline': 4,
            'blink': 5,
            'inverse': 7,
            'hidden': 8,
        }

        return effects[effect]
