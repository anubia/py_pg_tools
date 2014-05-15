#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import argparse
import sys
from orchestrator import Orchestrator


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

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

    backer.add_argument('-ch', '--pg-host',
                        help='indicates the host you are going to connect to')

    backer.add_argument('-cp', '--pg-port',
                        help='indicates the port you are going to connect to',
                        type=int)

    backer.add_argument('-cu', '--pg-user',
                        help='indicates the PostgreSQL username with whom you '
                        'are going to connect')

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

    backer.add_argument('-p', '--bkp-path',
                        help='specify the path where the backups are going '
                        'to be stored')

    backer.add_argument('-f', '--backup-format',
                        help='select the backup\'s file format (dump, bz2, '
                        'gz, zip)', choices=['dump', 'bz2', 'gz', 'zip'])

    backer.add_argument('-g', '--group',
                        help='select a name to put in the each backup\'s name '
                        'to agrupate them')

    groupB = backer.add_mutually_exclusive_group()
    groupB.add_argument('-m', '--ex-templates',
                        help='specify whether the databases which are '
                        'templates have to be dumped', action='store_true')
    groupB.add_argument('-M', '--no-ex-templates',
                        help='specify whether the databases which are '
                        'templates have not to be dumped', action='store_true')

    groupC = backer.add_mutually_exclusive_group()
    groupC.add_argument('-v', '--vacuum',
                        help='vacuum those databases which are going to be '
                        'dumped before the process', action='store_true')
    groupC.add_argument('-V', '--no-vacuum',
                        help='not to vacuum those databases which are going '
                        'to be dumped before the process', action='store_true')

    backer.add_argument('-o', '--db-owner',
                        help='only if the user who is running the program is '
                        'a PostgreSQL superuser, this option allows him to '
                        'play other PostgreSQL role writting its username')

    backer.add_argument('-t', '--terminate',
                        help='terminate every connection (except yours) '
                        'to each database which is going to be dumped',
                        action='store_true')

    backer.add_argument('-Lc', '--config-logger',
                        help='load a configuration file (.cfg) to get the '
                        'logger parameters')

    backer.add_argument('-Lf', '--logger-logfile',
                        help='indicates the path of the file in which the '
                        'logger is going to store the log info')

    backer.add_argument('-Ll', '--logger-level',
                        help='indicates the logger\'s verbosity level (debug, '
                        'info, warning, error, critical)',
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'])

    backer.add_argument('-Lm', '--logger-mute',
                        help='indicates not to store anything',
                        action='store_true')

    # ******************************** DROPPER ********************************

    dropper = sub_parsers.add_parser('d', help='DROPPER: deletes the '
                                     'specified PostgreSQL databases')

    dropper.add_argument('-cC', '--config-connection',
                         help='load a configuration file (.cfg) to get the '
                         'PostgreSQL connection parameters')

    dropper.add_argument('-ch', '--pg-host',
                         help='indicates the host you are going to connect to')

    dropper.add_argument('-cp', '--pg-port',
                         help='indicates the port you are going to connect to',
                         type=int)

    dropper.add_argument('-cu', '--pg-user',
                         help='indicates the PostgreSQL username with whom '
                         'you are going to connect')

    dropper.add_argument('-d', '--db-name', nargs='+',
                         help='specify the PostgreSQL databases to be deleted')

    dropper.add_argument('-t', '--terminate',
                         help='terminate every connection (except yours) '
                         'to each database which is going to be dropped',
                         action='store_true')

    dropper.add_argument('-Lc', '--config-logger',
                         help='load a configuration file (.cfg) to get the '
                         'logger parameters')

    dropper.add_argument('-Lf', '--logger-logfile',
                         help='indicates the path of the file in which the '
                         'logger is going to store the log info')

    dropper.add_argument('-Ll', '--logger-level',
                         help='indicates the logger\'s verbosity level '
                         '(debug, info, warning, error, critical)',
                         choices=['debug', 'info', 'warning', 'error',
                                  'critical'])

    dropper.add_argument('-Lm', '--logger-mute',
                         help='indicates not to store anything',
                         action='store_true')

    # ******************************** INFORMER *******************************

    informer = sub_parsers.add_parser('i', help='INFORMER: gives some '
                                      'information about PostgreSQL')

    informer.add_argument('-cC', '--config-connection',
                          help='load a configuration file (.cfg) to get the '
                          'PostgreSQL connection parameters')

    informer.add_argument('-ch', '--pg-host',
                          help='indicates the host you are going to connect '
                          'to')

    informer.add_argument('-cp', '--pg-port',
                          help='indicates the port you are going to connect '
                          'to', type=int)

    informer.add_argument('-cu', '--pg-user',
                          help='indicates the PostgreSQL username with whom '
                          'you are going to connect')

    groupA = informer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-name', nargs='+',
                        help='gives the owner and the codification of the '
                        'specified databases')

    groupA.add_argument('-u', '--users', nargs='+',
                        help='gives the role of the specified users')

    informer.add_argument('-Lc', '--config-logger',
                          help='load a configuration file (.cfg) to get the '
                          'logger parameters')

    informer.add_argument('-Lf', '--logger-logfile',
                          help='indicates the path of the file in which the '
                          'logger is going to store the log info')

    informer.add_argument('-Ll', '--logger-level',
                          help='indicates the logger\'s verbosity level '
                          '(debug, info, warning, error, critical)',
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    informer.add_argument('-Lm', '--logger-mute',
                          help='indicates not to store anything',
                          action='store_true')

    # ****************************** REPLICATOR *******************************

    replicator = sub_parsers.add_parser('r', help='REPLICATOR: clone the '
                                        'specified PostgreSQL database')

    replicator.add_argument('-cC', '--config-connection',
                            help='load a configuration file (.cfg) to get the '
                            'PostgreSQL connection parameters')

    replicator.add_argument('-ch', '--pg-host',
                            help='indicates the host you are going to connect '
                            'to')

    replicator.add_argument('-cp', '--pg-port',
                            help='indicates the port you are going to connect '
                            'to', type=int)

    replicator.add_argument('-cu', '--pg-user',
                            help='indicates the PostgreSQL username with whom '
                            'you are going to connect')

    replicator.add_argument('-d', '--db-name', nargs=2,
                            help='specifies the new name of the database '
                            'generated and the name of the database which is '
                            'being cloned, respectively')

    replicator.add_argument('-t', '--terminate',
                            help='terminate every connection (except yours) '
                            'to the database which is going to be replicated',
                            action='store_true')

    replicator.add_argument('-Lc', '--config-logger',
                            help='load a configuration file (.cfg) to get the '
                            'logger parameters')

    replicator.add_argument('-Lf', '--logger-logfile',
                            help='indicates the path of the file in which the '
                            'logger is going to store the log info')

    replicator.add_argument('-Ll', '--logger-level',
                            help='indicates the logger\'s verbosity level '
                            '(debug, info, warning, error, critical)',
                            choices=['debug', 'info', 'warning', 'error',
                                     'critical'])

    replicator.add_argument('-Lm', '--logger-mute',
                            help='indicates not to store anything',
                            action='store_true')

    # ******************************* RESTORER ********************************

    restorer = sub_parsers.add_parser('R', help='RESTORER: restores a '
                                      'database\'s backup file in PostgreSQL')

    restorer.add_argument('-cC', '--config-connection',
                          help='load a configuration file (.cfg) to get the '
                          'PostgreSQL connection parameters')

    restorer.add_argument('-ch', '--pg-host',
                          help='indicates the host you are going to connect '
                          'to')

    restorer.add_argument('-cp', '--pg-port',
                          help='indicates the port you are going to connect '
                          'to', type=int)

    restorer.add_argument('-cu', '--pg-user',
                          help='indicates the PostgreSQL username with whom '
                          'you are going to connect')

    groupA = restorer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-backup', nargs=2,
                        help='specifies the path of the backup\'s file which '
                        'is going to be loaded and the name of the PostgreSQL '
                        'database which is going to be generated, '
                        'respectively')

    groupA.add_argument('-c', '--cluster-backup',
                        help='specifies the new name of the database '
                        'generated and the name of the database which is '
                        'being cloned, respectively')

    restorer.add_argument('-Lc', '--config-logger',
                          help='load a configuration file (.cfg) to get the '
                          'logger parameters')

    restorer.add_argument('-Lf', '--logger-logfile',
                          help='indicates the path of the file in which the '
                          'logger is going to store the log info')

    restorer.add_argument('-Ll', '--logger-level',
                          help='indicates the logger\'s verbosity level '
                          '(debug, info, warning, error, critical)',
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    restorer.add_argument('-Lm', '--logger-mute',
                          help='indicates not to store anything',
                          action='store_true')

    # ****************************** TERMINATOR *******************************

    terminator = sub_parsers.add_parser('t', help='TERMINATOR: terminates '
                                        'the specified connections to '
                                        'PostgreSQL')

    terminator.add_argument('-cC', '--config-connection',
                            help='load a configuration file (.cfg) to get the '
                            'PostgreSQL connection parameters')

    terminator.add_argument('-ch', '--pg-host',
                            help='indicates the host you are going to connect '
                            'to')

    terminator.add_argument('-cp', '--pg-port',
                            help='indicates the port you are going to connect '
                            'to', type=int)

    terminator.add_argument('-cu', '--pg-user',
                            help='indicates the PostgreSQL username with whom '
                            'you are going to connect')

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

    terminator.add_argument('-Lc', '--config-logger',
                            help='load a configuration file (.cfg) to get the '
                            'logger parameters')

    terminator.add_argument('-Lf', '--logger-logfile',
                            help='indicates the path of the file in which the '
                            'logger is going to store the log info')

    terminator.add_argument('-Ll', '--logger-level',
                            help='indicates the logger\'s verbosity level '
                            '(debug, info, warning, error, critical)',
                            choices=['debug', 'info', 'warning', 'error',
                                     'critical'])

    terminator.add_argument('-Lm', '--logger-mute',
                            help='indicates not to store anything',
                            action='store_true')

    # ******************************** TRIMMER ********************************

    trimmer = sub_parsers.add_parser('T', help='TRIMMER: deletes (if '
                                     'necessary) a group of PostgreSQL '
                                     'backups (cluster or databases) '
                                     'according to some specified conditions')

    trimmer.add_argument('-cC', '--config-connection',
                         help='load a configuration file (.cfg) to get the '
                         'PostgreSQL connection parameters')

    trimmer.add_argument('-ch', '--pg-host',
                         help='indicates the host you are going to connect to')

    trimmer.add_argument('-cp', '--pg-port',
                         help='indicates the port you are going to connect to',
                         type=int)

    trimmer.add_argument('-cu', '--pg-user',
                         help='indicates the PostgreSQL username with whom '
                         'you are going to connect')

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

    trimmer.add_argument('-f', '--bkp-folder',
                         help='select the path of the folder to be trimmed. '
                         'The folder\'s name must be the group\'s name')

    trimmer.add_argument('-p', '--prefix',
                         help='specify the prefix of the backups which are '
                         'going to be trimmed')

    trimmer.add_argument('-n', '--n-backups',
                         help='specify the minimum number of backups of each '
                         'database to keep stored, regardless of the rest of '
                         'conditions', type=int)

    trimmer.add_argument('-e', '--expiry-days',
                         help='specify the number of days which have to be '
                         'elapsed to consider a backup expired', type=int)

    trimmer.add_argument('-s', '--max-size',
                         help='when the size of a group of a database\'s '
                         'backups exceeds this maximum size, a message will'
                         'be shown to let the user know it')

    trimmer.add_argument('-Lc', '--config-logger',
                         help='load a configuration file (.cfg) to get the '
                         'logger parameters')

    trimmer.add_argument('-Lf', '--logger-logfile',
                         help='indicates the path of the file in which the '
                         'logger is going to store the log info')

    trimmer.add_argument('-Ll', '--logger-level',
                         help='indicates the logger\'s verbosity level '
                         '(debug, info, warning, error, critical)',
                         choices=['debug', 'info', 'warning', 'error',
                                  'critical'])

    trimmer.add_argument('-Lm', '--logger-mute',
                         help='indicates not to store anything',
                         action='store_true')

    # ******************************* VACUUMER ********************************

    vacuumer = sub_parsers.add_parser('v', help='VACUUMER: makes a vacuum '
                                      'of a specified group of PostgreSQL '
                                      'databases')

    vacuumer.add_argument('-cC', '--config-connection',
                          help='load a configuration file (.cfg) to get the '
                               'PostgreSQL connection parameters')

    vacuumer.add_argument('-ch', '--pg-host',
                          help='indicates the host you are going to connect '
                          'to')

    vacuumer.add_argument('-cp', '--pg-port',
                          help='indicates the port you are going to connect '
                          'to', type=int)

    vacuumer.add_argument('-cu', '--pg-user',
                          help='indicates the PostgreSQL username with whom '
                          'you are going to connect')

    vacuumer.add_argument('-C', '--config',
                          help='load a configuration file (.cfg) to get the '
                               'vacuum conditions')

    vacuumer.add_argument('-d', '--db-name', nargs='+',
                          help='specify the name/s of the PostgreSQL '
                          'database/s to be vacuumed')

    vacuumer.add_argument('-o', '--db-owner',
                          help='only if the user who is running the program '
                          'is a PostgreSQL superuser, this option allows him '
                          'to play other PostgreSQL role writting its '
                          'username')

    vacuumer.add_argument('-t', '--terminate',
                          help='terminate every connection (except yours) '
                               'to each database which is going to be '
                               'vacuumed', action='store_true')

    vacuumer.add_argument('-Lc', '--config-logger',
                          help='load a configuration file (.cfg) to get the '
                               'logger parameters')

    vacuumer.add_argument('-Lf', '--logger-logfile',
                          help='indicates the path of the file in which the '
                          'logger is going to store the log info')

    vacuumer.add_argument('-Ll', '--logger-level',
                          help='indicates the logger\'s verbosity level '
                          '(debug, info, warning, error, critical)',
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    vacuumer.add_argument('-Lm', '--logger-mute',
                          help='indicates not to store anything',
                          action='store_true')

    # *************************** PARSING SYS.ARGV ****************************

    args = arg_parser.parse_args()

    action = sys.argv[1]

    # ************************** BACKER REQUIREMENTS **************************

    if action == 'B':
        if not (args.config or args.db_name or args.cluster):
            backer.error('insufficient parameters to work')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            backer.error('insufficient connection parameters to work')

    # ************************** DROPPER REQUIREMENTS *************************

    elif action == 'd':
        if not args.db_name:
            dropper.error('insufficient parameters to work')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            dropper.error('insufficient connection parameters to work')

    # ************************* INFORMER REQUIREMENTS *************************

    elif action == 'i':
        if not (args.db_name or args.users):
            informer.error('insufficient parameters to work')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            informer.error('insufficient connection parameters to work')

    # ****************************** REPLICATOR *******************************

    elif action == 'r':
        if not (args.db_name):
            replicator.error('insufficient parameters to work')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            replicator.error('insufficient connection parameters to work')

    # ******************************* RESTORER ********************************

    elif action == 'R':
        if not (args.db_backup or args.cluster_backup):
            restorer.error('insufficient parameters to work')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            restorer.error('insufficient connection parameters to work')

    # ************************ TERMINATOR REQUIREMENTS ************************

    elif action == 't':
        if not (args.config or args.all or args.db_name or args.user):
            terminator.error('insufficient parameters to work')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            terminator.error('insufficient connection parameters to work')

    # ************************** TRIMMER REQUIREMENTS *************************

    elif action == 'T':
        if not (args.config or
                ((args.db_name or args.cluster) and args.bkp_folder)):
            trimmer.error('insufficient parameters to work')
        if not args.cluster and not \
            (args.config_connection or
             (args.pg_host and args.pg_port and args.pg_user)):
            trimmer.error('insufficient connection parameters to work')
        if args.cluster and (args.config_connection or args.pg_host
                             or args.pg_port or args.pg_user):
            trimmer.error('connection parameters no needed to work with '
                          'clusters\' trimmer')

    # ************************* VACUUMER REQUIREMENTS *************************

    elif action == 'v':
        if not (args.config or args.db_name):
            vacuumer.error('insufficient parameters to work')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            vacuumer.error('insufficient connection parameters to work')

    else:
        pass

    orchestrator = Orchestrator(action, args)

    orchestrator.detect_module()
