#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import argparse  # To work with console parameters
import sys  # To get the console subparser

from argparse import RawTextHelpFormatter  # To insert newlines in console help

from const.const import Messenger
from orchestrator import Orchestrator


# ******************************** MAIN PROGRAM *******************************

if __name__ == "__main__":

    # ***************************** MAIN PARSER *******************************

    arg_parser = argparse.ArgumentParser(
        description=Messenger.PROGRAM_DESCRIPTION,
        formatter_class=RawTextHelpFormatter)
    sub_parsers = arg_parser.add_subparsers()

    # ******************************** BACKER *********************************

    backer = sub_parsers.add_parser('B', help=Messenger.BACKER_HELP)

    backer.add_argument('-cC', '--config-connection',
                        help=Messenger.CONFIG_CONNECTION_HELP)

    backer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    backer.add_argument('-cp', '--pg-port', help=Messenger.PORT_HELP, type=int)

    backer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

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
                        help=Messenger.CONFIG_LOGGER_HELP)

    backer.add_argument('-Lf', '--logger-logfile',
                        help=Messenger.LOGGER_LOGFILE_HELP)

    backer.add_argument('-Ll', '--logger-level',
                        help=Messenger.LOGGER_LEVEL_HELP,
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'])

    backer.add_argument('-Lm', '--logger-mute',
                        help=Messenger.LOGGER_MUTE_HELP, action='store_true')

    # ******************************** DROPPER ********************************

    dropper = sub_parsers.add_parser('d', help=Messenger.DROPPER_HELP)

    dropper.add_argument('-cC', '--config-connection',
                         help=Messenger.CONFIG_CONNECTION_HELP)

    dropper.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    dropper.add_argument('-cp', '--pg-port', help=Messenger.PORT_HELP,
                         type=int)

    dropper.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    dropper.add_argument('-C', '--config',
                         help='load a configuration file (.cfg) to get the '
                         'dropper conditions')

    dropper.add_argument('-d', '--db-name', nargs='+',
                         help='specify the PostgreSQL databases to be deleted')

    dropper.add_argument('-t', '--terminate',
                         help='terminate every connection (except yours) '
                         'to each database which is going to be dropped',
                         action='store_true')

    dropper.add_argument('-Lc', '--config-logger',
                         help=Messenger.CONFIG_LOGGER_HELP)

    dropper.add_argument('-Lf', '--logger-logfile',
                         help=Messenger.LOGGER_LOGFILE_HELP)

    dropper.add_argument('-Ll', '--logger-level',
                         help=Messenger.LOGGER_LEVEL_HELP,
                         choices=['debug', 'info', 'warning', 'error',
                                  'critical'])

    dropper.add_argument('-Lm', '--logger-mute',
                         help=Messenger.LOGGER_MUTE_HELP, action='store_true')

    # ******************************** INFORMER *******************************

    informer = sub_parsers.add_parser('i', help=Messenger.INFORMER_HELP)

    informer.add_argument('-cC', '--config-connection',
                          help=Messenger.CONFIG_CONNECTION_HELP)

    informer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    informer.add_argument('-cp', '--pg-port', help=Messenger.PORT_HELP,
                          type=int)

    informer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    informer.add_argument('-C', '--config',
                          help='load a configuration file (.cfg) to get the '
                          'informer conditions')

    groupA = informer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-name', nargs='+',
                        help='gives the owner and the codification of the '
                        'specified databases')

    groupA.add_argument('-u', '--users', nargs='+',
                        help='gives the role of the specified users')

    informer.add_argument('-Lc', '--config-logger',
                          help=Messenger.CONFIG_LOGGER_HELP)

    informer.add_argument('-Lf', '--logger-logfile',
                          help=Messenger.LOGGER_LOGFILE_HELP)

    informer.add_argument('-Ll', '--logger-level',
                          help=Messenger.LOGGER_LEVEL_HELP,
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    informer.add_argument('-Lm', '--logger-mute',
                          help=Messenger.LOGGER_MUTE_HELP, action='store_true')

    # ****************************** REPLICATOR *******************************

    replicator = sub_parsers.add_parser('r', help=Messenger.REPLICATOR_HELP)

    replicator.add_argument('-cC', '--config-connection',
                            help=Messenger.CONFIG_CONNECTION_HELP)

    replicator.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    replicator.add_argument('-cp', '--pg-port', help=Messenger.PORT_HELP,
                            type=int)

    replicator.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    replicator.add_argument('-C', '--config',
                            help='load a configuration file (.cfg) to get the '
                            'replicator conditions')

    replicator.add_argument('-d', '--db-name', nargs=2,
                            help='specifies the new name of the database '
                            'generated and the name of the database which is '
                            'being cloned, respectively')

    replicator.add_argument('-t', '--terminate',
                            help='terminate every connection (except yours) '
                            'to the database which is going to be replicated',
                            action='store_true')

    replicator.add_argument('-Lc', '--config-logger',
                            help=Messenger.CONFIG_LOGGER_HELP)

    replicator.add_argument('-Lf', '--logger-logfile',
                            help=Messenger.LOGGER_LOGFILE_HELP)

    replicator.add_argument('-Ll', '--logger-level',
                            help=Messenger.LOGGER_LEVEL_HELP,
                            choices=['debug', 'info', 'warning', 'error',
                                     'critical'])

    replicator.add_argument('-Lm', '--logger-mute',
                            help=Messenger.LOGGER_MUTE_HELP,
                            action='store_true')

    # ******************************* RESTORER ********************************

    restorer = sub_parsers.add_parser('R', help=Messenger.RESTORER_HELP)

    restorer.add_argument('-cC', '--config-connection',
                          help=Messenger.CONFIG_CONNECTION_HELP)

    restorer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    restorer.add_argument('-cp', '--pg-port', help=Messenger.PORT_HELP,
                          type=int)

    restorer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    restorer.add_argument('-C', '--config',
                          help='load a configuration file (.cfg) to get the '
                          'restorer conditions')

    groupA = restorer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-backup', nargs=2,
                        help='specifies the path of the backup\'s file '
                        '(database) which is going to be loaded and the name '
                        'of the PostgreSQL database which is going to be '
                        'generated, respectively')
    groupA.add_argument('-p', '--cluster-backup',
                        help='specifies the path of the backup\'s file '
                        '(cluster) which is going to be loaded')

    restorer.add_argument('-c', '--cluster',
                          help='specifies whether the specified path is a '
                          'database\'s backup or a cluster\'s backup',
                          action='store_true')

    restorer.add_argument('-Lc', '--config-logger',
                          help=Messenger.CONFIG_LOGGER_HELP)

    restorer.add_argument('-Lf', '--logger-logfile',
                          help=Messenger.LOGGER_LOGFILE_HELP)

    restorer.add_argument('-Ll', '--logger-level',
                          help=Messenger.LOGGER_LEVEL_HELP,
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    restorer.add_argument('-Lm', '--logger-mute',
                          help=Messenger.LOGGER_MUTE_HELP, action='store_true')

    # ****************************** TERMINATOR *******************************

    terminator = sub_parsers.add_parser('t', help=Messenger.TERMINATOR_HELP)

    terminator.add_argument('-cC', '--config-connection',
                            help=Messenger.CONFIG_CONNECTION_HELP)

    terminator.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    terminator.add_argument('-cp', '--pg-port', help=Messenger.PORT_HELP,
                            type=int)

    terminator.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

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
                            help=Messenger.CONFIG_LOGGER_HELP)

    terminator.add_argument('-Lf', '--logger-logfile',
                            help=Messenger.LOGGER_LOGFILE_HELP)

    terminator.add_argument('-Ll', '--logger-level',
                            help=Messenger.LOGGER_LEVEL_HELP,
                            choices=['debug', 'info', 'warning', 'error',
                                     'critical'])

    terminator.add_argument('-Lm', '--logger-mute',
                            help=Messenger.LOGGER_MUTE_HELP,
                            action='store_true')

    # ******************************** TRIMMER ********************************

    trimmer = sub_parsers.add_parser('T', help=Messenger.TRIMMER_HELP)

    trimmer.add_argument('-cC', '--config-connection',
                         help=Messenger.CONFIG_CONNECTION_HELP)

    trimmer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    trimmer.add_argument('-cp', '--pg-port', help=Messenger.PORT_HELP,
                         type=int)

    trimmer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

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
                         help=Messenger.CONFIG_LOGGER_HELP)

    trimmer.add_argument('-Lf', '--logger-logfile',
                         help=Messenger.LOGGER_LOGFILE_HELP)

    trimmer.add_argument('-Ll', '--logger-level',
                         help=Messenger.LOGGER_LEVEL_HELP,
                         choices=['debug', 'info', 'warning', 'error',
                                  'critical'])

    trimmer.add_argument('-Lm', '--logger-mute',
                         help=Messenger.LOGGER_MUTE_HELP, action='store_true')

    # ******************************* VACUUMER ********************************

    vacuumer = sub_parsers.add_parser('v', help=Messenger.VACUUMER_HELP)

    vacuumer.add_argument('-cC', '--config-connection',
                          help=Messenger.CONFIG_CONNECTION_HELP)

    vacuumer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    vacuumer.add_argument('-cp', '--pg-port', help=Messenger.PORT_HELP,
                          type=int)

    vacuumer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

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
                          help=Messenger.CONFIG_LOGGER_HELP)

    vacuumer.add_argument('-Lf', '--logger-logfile',
                          help=Messenger.LOGGER_LOGFILE_HELP)

    vacuumer.add_argument('-Ll', '--logger-level',
                          help=Messenger.LOGGER_LEVEL_HELP,
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    vacuumer.add_argument('-Lm', '--logger-mute',
                          help=Messenger.LOGGER_MUTE_HELP, action='store_true')

    # *************************** PARSING SYS.ARGV ****************************

    args = arg_parser.parse_args()

    action = sys.argv[1]

    # ************************** BACKER REQUIREMENTS **************************

    if action == 'B':
        if not (args.config or args.db_name or args.cluster):
            backer.error('insufficient parameters to work - [-C/--config | '
                         '-d/--db-name | -c/--cluster] must be specified')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            backer.error('insufficient connection parameters to work - '
                         '[-cC/--config-connection | (-ch/--host & '
                         '-cp/--port & -cu/--user)] must be specified')

    # ************************** DROPPER REQUIREMENTS *************************

    elif action == 'd':
        if not (args.config or args.db_name):
            dropper.error('insufficient parameters to work - [-C/--config | '
                          '-d/--db-name] must be specified')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            dropper.dropper('insufficient connection parameters to work - '
                            '[-cC/--config-connection | (-ch/--host & '
                            '-cp/--port & -cu/--user)] must be specified')

    # ************************* INFORMER REQUIREMENTS *************************

    elif action == 'i':
        if not (args.config or args.db_name or args.users):
            informer.error('insufficient parameters to work - [-C/--config | '
                           '-d/--db-name | -u/--users] must be specified')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            informer.error('insufficient connection parameters to work - '
                           '[-cC/--config-connection | (-ch/--host & '
                           '-cp/--port & -cu/--user)] must be specified')

    # ****************************** REPLICATOR *******************************

    elif action == 'r':
        if not (args.config or args.db_name):
            replicator.error('insufficient parameters to work - '
                             '[-C/--config | -d/--db-name] must be specified')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            replicator.error('insufficient connection parameters to work - '
                             '[-cC/--config-connection | (-ch/--host & '
                             '-cp/--port & -cu/--user)] must be specified')

    # ******************************* RESTORER ********************************

    elif action == 'R':
        if not (args.config or args.db_backup or
                (args.cluster and args.cluster_backup)):
            restorer.error('insufficient parameters to work - [-C/--config | '
                           '-d/--db-backup | (-c/--cluster & '
                           '-p/--cluster-backup)] must be specified')

        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            restorer.error('insufficient connection parameters to work - '
                           '[-cC/--config-connection | (-ch/--host & '
                           '-cp/--port & -cu/--user)] must be specified')

    # ************************ TERMINATOR REQUIREMENTS ************************

    elif action == 't':
        if not (args.config or args.all or args.db_name or args.user):
            terminator.error('insufficient parameters to work - [-C/--config '
                             '| -a/--all | -d/--db-name | -u/--user] must be '
                             'specified')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            terminator.error('insufficient connection parameters to work - '
                             '[-cC/--config-connection | (-ch/--host & '
                             '-cp/--port & -cu/--user)] must be specified')

    # ************************** TRIMMER REQUIREMENTS *************************

    elif action == 'T':
        if not (args.config or
                ((args.db_name or args.cluster) and args.bkp_folder)):
            trimmer.error('insufficient parameters to work - [-C/--config | '
                          '(-f/--bkp-folder & (-d/--db-name | -c/--cluster))] '
                          'must be specified')
        if not args.cluster and not \
            (args.config_connection or
             (args.pg_host and args.pg_port and args.pg_user)):
            trimmer.error('insufficient connection parameters to work - '
                          '[-cC/--config-connection | (-ch/--host & '
                          '-cp/--port & -cu/--user)] must be specified')
        if args.cluster and (args.config_connection or args.pg_host
                             or args.pg_port or args.pg_user):
            trimmer.error('connection parameters no needed to work with '
                          'clusters\' trimmer')

    # ************************* VACUUMER REQUIREMENTS *************************

    elif action == 'v':
        if not (args.config or args.db_name):
            vacuumer.error('insufficient parameters to work - [-C/--config '
                           '| -d/--db-name] must be specified')
        if not (args.config_connection or
                (args.pg_host and args.pg_port and args.pg_user)):
            vacuumer.error('insufficient connection parameters to work - '
                           '[-cC/--config-connection | (-ch/--host & '
                           '-cp/--port & -cu/--user)] must be specified')

    else:
        pass

    # Load a specific module depending on the gotten console parameters
    orchestrator = Orchestrator(action, args)
    orchestrator.detect_module()
