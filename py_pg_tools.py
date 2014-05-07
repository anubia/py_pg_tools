#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import argparse
import sys
from orchestrator import Orchestrator
from logger.logger import Logger
from dir_tools.dir_tools import Dir


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

    # NOTA: CON dest = xxx EN CADA ARGUMENT, CAMBIAMOS EL NOMBRE DE LA VARIABLE
    # A NUESTRO GUSTO

    # def my_funcion(args): bla bla bla
    # backer.set_defaults(func=my_funcion) y así llama auto a la función

    arg_parser = argparse.ArgumentParser(
        description='This program allows you to manage the backups of your '
                    'PostgreSQL cluster or databases')
    sub_parsers = arg_parser.add_subparsers()

    # ******************************** BACKER *********************************

    backer = sub_parsers.add_parser('B', help='BACKER: makes a backup of a '
                                    'PostgreSQL cluster or a specified group '
                                    'of databases')

    backer.add_argument('-cC', '--config-connection',
                        help='load a configuration file (.cfg) to get the '
                             'PostgreSQL connection parameters')

    backer.add_argument('-C', '--config',
                        help='load a configuration file (.cfg) to get the '
                             'backer conditions')

    groupA = backer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-name', nargs='+',
                        help='specify the name/s of the PostgreSQL database/s '
                             'to be dumped')
    groupA.add_argument('-c', '--cluster',
                        help='select dumping the PostgreSQL cluster',
                        action='store_true')

    backer.add_argument('-f', '--backup-format',
                        help='select the backup\'s file format (dump, '
                             'bz2, gzip, zip)',
                        choices=['dump', 'bz2', 'gzip', 'zip'])

    backer.add_argument('-g', '--group',
                        help='select a name to put in the each backup\'s name '
                             'to agrupate them')

    backer.add_argument('-t', '--terminate',
                        help='terminate every connection (except yours) '
                             'to each database which is going to be '
                             'dumped', action='store_true')

    # ******************************* CONNECTER *******************************

    connecter = sub_parsers.add_parser('c', help='CONNECTER: makes a '
                                       'connection to PostgreSQL with the '
                                       'specified parameters')

    connecter.add_argument('-cC', '--config-connection',
                           help='load a configuration file (.cfg) to get the '
                                'PostgreSQL connection parameters')

    connecter.add_argument('-ch', '--pg-host',
                           help='indicates the host you are going to connect '
                                'to')

    connecter.add_argument('-cp', '--pg-port',
                           help='indicates the port you are going to connect '
                                'to', type=int)

    connecter.add_argument('-cu', '--pg-user',
                           help='indicates the PostgreSQL username with whom '
                                'you are going to connect')

    connecter.add_argument('-cP', '--pg-password',
                           help='indicates the password of the PostgreSQL '
                           'account you are going to use')

    # ******************************** LOGGER *********************************

    logger = sub_parsers.add_parser('L', help='LOGGER: specifies the '
                                    'propierties of the info messages and the '
                                    'log file ones')

    logger.add_argument('-Lc', '--config-logger',
                        help='load a configuration file (.cfg) to get the '
                             'logger parameters')

    logger.add_argument('-Lf', '--logger-logfile',
                        help='indicates the path of the file in which the '
                        'logger is going to store the log info')

    logger.add_argument('-Ll', '--logger-level',
                        help='indicates the logger\'s verbosity level (debug, '
                        'info, warning, error, critical)',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'])

    logger.add_argument('-Lm', '--logger-mute',
                        help='indicates not to store anything',
                        action='store_true')

    # ****************************** TERMINATOR *******************************

    terminator = sub_parsers.add_parser('t', help='TERMINATOR: terminates '
                                        'the specified connections to '
                                        'PostgreSQL')

    terminator.add_argument('-cC', '--config-connection',
                            help='load a configuration file (.cfg) to get the '
                                 'PostgreSQL connection parameters')

    terminator.add_argument('-C', '--config',
                            help='load a configuration file (.cfg) to get the '
                                 'terminator conditions')

    groupA = terminator.add_mutually_exclusive_group()
    groupA.add_argument('-a', '--all',
                        help='terminates every connection (except yours) '
                             'to the host which you are connected to',
                             action='store_true')
    groupA.add_argument('-d', '--db-name', nargs='+',
                        help='terminates every connection (except yours) '
                             'to the specified PostgreSQL database')
    groupA.add_argument('-u', '--user',
                        help='terminates every connection of the specified '
                             'user (except if you are the specified user)')

    # ******************************** TRIMMER ********************************

    trimmer = sub_parsers.add_parser('T', help='TRIMMER: deletes (if '
                                     'necessary) a group of PostgreSQL '
                                     'backups (cluster or databases) '
                                     'according to some specified conditions')

    trimmer.add_argument('-cC', '--config-connection',
                         help='load a configuration file (.cfg) to get the '
                              'PostgreSQL connection parameters')

    trimmer.add_argument('-C', '--config',
                         help='load a configuration file (.cfg) to get the '
                              'trimmer conditions')

    groupA = trimmer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-name', nargs='+',
                        help='trim the backups of a specified group of '
                        'PostgreSQL databases')
    groupA.add_argument('-c', '--cluster',
                        help='trim the backups of the PostgreSQL cluster',
                        action='store_true')

    # ******************************* VACUUMER ********************************

    vacuumer = sub_parsers.add_parser('v', help='VACUUMER: makes a vacuum '
                                      'of a specified group of PostgreSQL '
                                      'databases')

    vacuumer.add_argument('-cC', '--config-connection',
                          help='load a configuration file (.cfg) to get the '
                               'PostgreSQL connection parameters')

    vacuumer.add_argument('-C', '--config',
                          help='load a configuration file (.cfg) to get the '
                               'vacuum conditions')

    vacuumer.add_argument('-t', '--terminate',
                          help='terminate every connection (except yours) '
                               'to each database which is going to be '
                               'vacuumed', action='store_true')

    # *************************** PARSING SYS.ARGV ****************************

    args = arg_parser.parse_args()

    action = sys.argv[1]

    # ************************** BACKER REQUIREMENTS **************************

    if action == 'B':
        if not (args.config or args.db_name or args.cluster):
            backer.error('insufficient parameters to work')

    # ************************ TERMINATOR REQUIREMENTS ************************

    elif action == 't':
        if not (args.config or args.all or args.db_name or args.user):
            terminator.error('insufficient parameters to work')

    # ************************** TRIMMER REQUIREMENTS *************************

    elif action == 'T':
        if not (args.config or args.db_name or args.cluster):
            trimmer.error('insufficient parameters to work')

    else:
        pass

    logger = Logger()

    Dir.forbid_root(logger)

    orchestrator = Orchestrator(action, args, logger)

    orchestrator.detect_module()
