#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
.. module:: py_pg_tools
   :platform: Unix, Windows
   :synopsis: A group of scripts made to dump and vacuum PostgreSQL databases,
              dump PostgreSQL clusters, and clean PostgreSQL databases/clusters
              backups.

.. moduleauthor:: Juan Formoso Vasco <jfv@anubia.es>

'''
import argparse  # To work with console parameters
import sys  # To get the console subparser

from argparse import RawTextHelpFormatter  # To insert newlines in console help

from const.const import Messenger
from orchestrator import Orchestrator

setup = {
    'author': 'Juan Formoso Vasco <jfv@anubia.es>',
    'copyright': 'Copyright 2014, Anubía, soluciones en la nube, SL',
    'credits': ['Alejandro Santana <alejandrosantana@anubia.es>'],
    'licens': 'AGPL-3',
    'version': '0.1.1',
    'maintainer': 'Juan Formoso Vasco',
    'email': 'jfv@anubia.es',
    'status': 'Testing',
}

# ******************************** MAIN PROGRAM *******************************

if __name__ == '__main__':

    # ***************************** MAIN PARSER *******************************

    arg_parser = argparse.ArgumentParser(
        description=Messenger.PROGRAM_DESCRIPTION,
        formatter_class=RawTextHelpFormatter)

    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--info', action='store_true',
                       help=Messenger.PROGRAM_INFO_HELP)
    group.add_argument('-v', '--version', action='store_true',
                       help=Messenger.PROGRAM_VERSION_HELP)

    sub_parsers = arg_parser.add_subparsers()

    # ******************************** ALTERER ********************************

    alterer = sub_parsers.add_parser('a', help=Messenger.ALTERER_HELP)

    alterer.add_argument('-cC', '--config-connection',
                         help=Messenger.CONFIG_CONNECTION_HELP)

    alterer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    alterer.add_argument('-cp', '--pg-port', type=int,
                         help=Messenger.PORT_HELP)

    alterer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    alterer.add_argument('-C', '--config', help=Messenger.A_CONFIG_HELP)

    alterer.add_argument('-d', '--db-name', nargs='+',
                         help=Messenger.A_DB_NAME_HELP)

    alterer.add_argument('-o', '--old-role', help=Messenger.A_OLD_ROLE_HELP)

    alterer.add_argument('-n', '--new-role', help=Messenger.A_NEW_ROLE_HELP)

    alterer.add_argument('-t', '--terminate', action='store_true',
                         help=Messenger.A_TERMINATE_HELP)

    alterer.add_argument('-Lc', '--config-logger',
                         help=Messenger.CONFIG_LOGGER_HELP)

    alterer.add_argument('-Lf', '--logger-logfile',
                         help=Messenger.LOGGER_LOGFILE_HELP)

    alterer.add_argument('-Ll', '--logger-level',
                         help=Messenger.LOGGER_LEVEL_HELP,
                         choices=['debug', 'info', 'warning', 'error',
                                  'critical'])

    alterer.add_argument('-Lm', '--logger-mute', action='store_true',
                         help=Messenger.LOGGER_MUTE_HELP)

    # ******************************** BACKER *********************************

    backer = sub_parsers.add_parser('B', help=Messenger.BACKER_HELP)

    backer.add_argument('-cC', '--config-connection',
                        help=Messenger.CONFIG_CONNECTION_HELP)

    backer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    backer.add_argument('-cp', '--pg-port', type=int, help=Messenger.PORT_HELP)

    backer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    backer.add_argument('-C', '--config', help=Messenger.B_CONFIG_HELP)

    groupA = backer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-name', nargs='+',
                        help=Messenger.B_DB_NAME_HELP)
    groupA.add_argument('-c', '--cluster', action='store_true',
                        help=Messenger.B_CLUSTER_HELP)

    backer.add_argument('-p', '--bkp-path', help=Messenger.B_BKP_PATH_HELP)

    backer.add_argument('-f', '--backup-format',
                        help=Messenger.B_BACKUP_FORMAT_HELP,
                        choices=['dump', 'bz2', 'gz', 'zip'])

    backer.add_argument('-g', '--group', help=Messenger.B_GROUP_HELP)

    groupB = backer.add_mutually_exclusive_group()
    groupB.add_argument('-m', '--ex-templates', action='store_true',
                        help=Messenger.B_EX_TEMPLATES_HELP)
    groupB.add_argument('-M', '--no-ex-templates', action='store_true',
                        help=Messenger.B_NO_EX_TEMPLATES_HELP)

    groupC = backer.add_mutually_exclusive_group()
    groupC.add_argument('-v', '--vacuum', action='store_true',
                        help=Messenger.B_VACUUM_HELP)
    groupC.add_argument('-V', '--no-vacuum', action='store_true',
                        help=Messenger.B_NO_VACUUM_HELP)

    backer.add_argument('-o', '--db-owner', help=Messenger.B_DB_OWNER_HELP)

    backer.add_argument('-t', '--terminate', action='store_true',
                        help=Messenger.B_TERMINATE_HELP)

    backer.add_argument('-Lc', '--config-logger',
                        help=Messenger.CONFIG_LOGGER_HELP)

    backer.add_argument('-Lf', '--logger-logfile',
                        help=Messenger.LOGGER_LOGFILE_HELP)

    backer.add_argument('-Ll', '--logger-level',
                        help=Messenger.LOGGER_LEVEL_HELP,
                        choices=['debug', 'info', 'warning', 'error',
                                 'critical'])

    backer.add_argument('-Lm', '--logger-mute', action='store_true',
                        help=Messenger.LOGGER_MUTE_HELP)

    # ******************************** DROPPER ********************************

    dropper = sub_parsers.add_parser('d', help=Messenger.DROPPER_HELP)

    dropper.add_argument('-cC', '--config-connection',
                         help=Messenger.CONFIG_CONNECTION_HELP)

    dropper.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    dropper.add_argument('-cp', '--pg-port', type=int,
                         help=Messenger.PORT_HELP)

    dropper.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    dropper.add_argument('-C', '--config', help=Messenger.D_CONFIG_HELP)

    dropper.add_argument('-d', '--db-name', nargs='+',
                         help=Messenger.D_DB_NAME_HELP)

    dropper.add_argument('-t', '--terminate', action='store_true',
                         help=Messenger.D_TERMINATE_HELP)

    dropper.add_argument('-Lc', '--config-logger',
                         help=Messenger.CONFIG_LOGGER_HELP)

    dropper.add_argument('-Lf', '--logger-logfile',
                         help=Messenger.LOGGER_LOGFILE_HELP)

    dropper.add_argument('-Ll', '--logger-level',
                         help=Messenger.LOGGER_LEVEL_HELP,
                         choices=['debug', 'info', 'warning', 'error',
                                  'critical'])

    dropper.add_argument('-Lm', '--logger-mute', action='store_true',
                         help=Messenger.LOGGER_MUTE_HELP)

    # ******************************** INFORMER *******************************

    informer = sub_parsers.add_parser('i', help=Messenger.INFORMER_HELP)

    informer.add_argument('-cC', '--config-connection',
                          help=Messenger.CONFIG_CONNECTION_HELP)

    informer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    informer.add_argument('-cp', '--pg-port', type=int,
                          help=Messenger.PORT_HELP)

    informer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    informer.add_argument('-dc', '--details-conns', nargs='*', type=int,
                          help=Messenger.I_DETAILS_CONNS_HELP)

    informer.add_argument('-dd', '--details-dbs', nargs='*',
                          help=Messenger.I_DETAILS_DBS_HELP)

    informer.add_argument('-du', '--details-users', nargs='*',
                          help=Messenger.I_DETAILS_USERS_HELP)

    informer.add_argument('-lc', '--list-conns', action='store_true',
                          help=Messenger.I_LIST_CONNS_HELP)

    informer.add_argument('-ld', '--list-dbs', action='store_true',
                          help=Messenger.I_LIST_DBS_HELP)

    informer.add_argument('-lu', '--list-users', action='store_true',
                          help=Messenger.I_LIST_USERS_HELP)

    informer.add_argument('-vpg', '--version-pg', action='store_true',
                          help=Messenger.I_VERSION_PG_HELP)

    informer.add_argument('-vnpg', '--version-num-pg', action='store_true',
                          help=Messenger.I_VERSION_NUM_PG_HELP)

    informer.add_argument('-ts', '--time-start', action='store_true',
                          help=Messenger.I_TIME_START_HELP)

    informer.add_argument('-tu', '--time-up', action='store_true',
                          help=Messenger.I_TIME_UP_HELP)

    informer.add_argument('-Lc', '--config-logger',
                          help=Messenger.CONFIG_LOGGER_HELP)

    informer.add_argument('-Lf', '--logger-logfile',
                          help=Messenger.LOGGER_LOGFILE_HELP)

    informer.add_argument('-Ll', '--logger-level',
                          help=Messenger.LOGGER_LEVEL_HELP,
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    informer.add_argument('-Lm', '--logger-mute', action='store_true',
                          help=Messenger.LOGGER_MUTE_HELP)

    # ****************************** REPLICATOR *******************************

    replicator = sub_parsers.add_parser('r', help=Messenger.REPLICATOR_HELP)

    replicator.add_argument('-cC', '--config-connection',
                            help=Messenger.CONFIG_CONNECTION_HELP)

    replicator.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    replicator.add_argument('-cp', '--pg-port', type=int,
                            help=Messenger.PORT_HELP)

    replicator.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    replicator.add_argument('-C', '--config', help=Messenger.R_CONFIG_HELP)

    replicator.add_argument('-d', '--db-name', nargs=2,
                            help=Messenger.R_DB_NAME_HELP)

    replicator.add_argument('-t', '--terminate', action='store_true',
                            help=Messenger.R_TERMINATE_HELP)

    replicator.add_argument('-Lc', '--config-logger',
                            help=Messenger.CONFIG_LOGGER_HELP)

    replicator.add_argument('-Lf', '--logger-logfile',
                            help=Messenger.LOGGER_LOGFILE_HELP)

    replicator.add_argument('-Ll', '--logger-level',
                            help=Messenger.LOGGER_LEVEL_HELP,
                            choices=['debug', 'info', 'warning', 'error',
                                     'critical'])

    replicator.add_argument('-Lm', '--logger-mute', action='store_true',
                            help=Messenger.LOGGER_MUTE_HELP)

    # ******************************* RESTORER ********************************

    restorer = sub_parsers.add_parser('R', help=Messenger.RESTORER_HELP)

    restorer.add_argument('-cC', '--config-connection',
                          help=Messenger.CONFIG_CONNECTION_HELP)

    restorer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    restorer.add_argument('-cp', '--pg-port', type=int,
                          help=Messenger.PORT_HELP)

    restorer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    restorer.add_argument('-C', '--config', help=Messenger.RS_CONFIG_HELP)

    groupA = restorer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-backup', nargs=2,
                        help=Messenger.RS_DB_BACKUP_HELP)
    groupA.add_argument('-p', '--cluster-backup',
                        help=Messenger.RS_CLUSTER_BACKUP_HELP)

    restorer.add_argument('-c', '--cluster', action='store_true',
                          help=Messenger.RS_CLUSTER_HELP)

    restorer.add_argument('-Lc', '--config-logger',
                          help=Messenger.CONFIG_LOGGER_HELP)

    restorer.add_argument('-Lf', '--logger-logfile',
                          help=Messenger.LOGGER_LOGFILE_HELP)

    restorer.add_argument('-Ll', '--logger-level',
                          help=Messenger.LOGGER_LEVEL_HELP,
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    restorer.add_argument('-Lm', '--logger-mute', action='store_true',
                          help=Messenger.LOGGER_MUTE_HELP)

    # ****************************** TERMINATOR *******************************

    terminator = sub_parsers.add_parser('t', help=Messenger.TERMINATOR_HELP)

    terminator.add_argument('-cC', '--config-connection',
                            help=Messenger.CONFIG_CONNECTION_HELP)

    terminator.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    terminator.add_argument('-cp', '--pg-port', type=int,
                            help=Messenger.PORT_HELP)

    terminator.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    terminator.add_argument('-C', '--config', help=Messenger.T_CONFIG_HELP)

    groupA = terminator.add_mutually_exclusive_group()
    groupA.add_argument('-a', '--all', action='store_true',
                        help=Messenger.T_ALL_HELP)
    groupA.add_argument('-d', '--db-name', nargs='+',
                        help=Messenger.T_DB_NAME_HELP)
    groupA.add_argument('-u', '--user', help=Messenger.T_USER_HELP)

    terminator.add_argument('-Lc', '--config-logger',
                            help=Messenger.CONFIG_LOGGER_HELP)

    terminator.add_argument('-Lf', '--logger-logfile',
                            help=Messenger.LOGGER_LOGFILE_HELP)

    terminator.add_argument('-Ll', '--logger-level',
                            help=Messenger.LOGGER_LEVEL_HELP,
                            choices=['debug', 'info', 'warning', 'error',
                                     'critical'])

    terminator.add_argument('-Lm', '--logger-mute', action='store_true',
                            help=Messenger.LOGGER_MUTE_HELP)

    # ******************************** TRIMMER ********************************

    trimmer = sub_parsers.add_parser('T', help=Messenger.TRIMMER_HELP)

    trimmer.add_argument('-cC', '--config-connection',
                         help=Messenger.CONFIG_CONNECTION_HELP)

    trimmer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    trimmer.add_argument('-cp', '--pg-port', type=int,
                         help=Messenger.PORT_HELP)

    trimmer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    trimmer.add_argument('-C', '--config', help=Messenger.TR_CONFIG_HELP)

    groupA = trimmer.add_mutually_exclusive_group()
    groupA.add_argument('-d', '--db-name', nargs='+',
                        help=Messenger.TR_DB_NAME_HELP)
    groupA.add_argument('-c', '--cluster', action='store_true',
                        help=Messenger.TR_CLUSTER_HELP)

    trimmer.add_argument('-f', '--bkp-folder',
                         help=Messenger.TR_BKP_FOLDER_HELP)

    trimmer.add_argument('-p', '--prefix', help=Messenger.TR_PREFIX_HELP)

    trimmer.add_argument('-n', '--n-backups', type=int,
                         help=Messenger.TR_N_BACKUPS_HELP)

    trimmer.add_argument('-e', '--expiry-days', type=int,
                         help=Messenger.TR_EXPIRY_DAYS_HELP)

    trimmer.add_argument('-s', '--max-size', help=Messenger.TR_MAX_SIZE_HELP)

    trimmer.add_argument('-Lc', '--config-logger',
                         help=Messenger.CONFIG_LOGGER_HELP)

    trimmer.add_argument('-Lf', '--logger-logfile',
                         help=Messenger.LOGGER_LOGFILE_HELP)

    trimmer.add_argument('-Ll', '--logger-level',
                         help=Messenger.LOGGER_LEVEL_HELP,
                         choices=['debug', 'info', 'warning', 'error',
                                  'critical'])

    trimmer.add_argument('-Lm', '--logger-mute', action='store_true',
                         help=Messenger.LOGGER_MUTE_HELP)

    # ******************************* VACUUMER ********************************

    vacuumer = sub_parsers.add_parser('v', help=Messenger.VACUUMER_HELP)

    vacuumer.add_argument('-cC', '--config-connection',
                          help=Messenger.CONFIG_CONNECTION_HELP)

    vacuumer.add_argument('-ch', '--pg-host', help=Messenger.HOST_HELP)

    vacuumer.add_argument('-cp', '--pg-port', type=int,
                          help=Messenger.PORT_HELP)

    vacuumer.add_argument('-cu', '--pg-user', help=Messenger.USER_HELP)

    vacuumer.add_argument('-C', '--config', help=Messenger.V_CONFIG_HELP)

    vacuumer.add_argument('-d', '--db-name', nargs='+',
                          help=Messenger.V_DB_NAME_HELP)

    vacuumer.add_argument('-o', '--db-owner', help=Messenger.V_DB_OWNER_HELP)

    vacuumer.add_argument('-t', '--terminate',  action='store_true',
                          help=Messenger.V_TERMINATE_HELP)

    vacuumer.add_argument('-Lc', '--config-logger',
                          help=Messenger.CONFIG_LOGGER_HELP)

    vacuumer.add_argument('-Lf', '--logger-logfile',
                          help=Messenger.LOGGER_LOGFILE_HELP)

    vacuumer.add_argument('-Ll', '--logger-level',
                          help=Messenger.LOGGER_LEVEL_HELP,
                          choices=['debug', 'info', 'warning', 'error',
                                   'critical'])

    vacuumer.add_argument('-Lm', '--logger-mute', action='store_true',
                          help=Messenger.LOGGER_MUTE_HELP)

    # *************************** PARSING SYS.ARGV ****************************

    args = arg_parser.parse_args()

    action = sys.argv[1]

    # ********************* INFO & VERSION REQUIREMENTS ***********************

    if ('-i' in sys.argv or '--info' in sys.argv) and len(sys.argv) > 2:
        arg_parser.error(Messenger.PROGRAM_INFO_ARGS_ERROR)

    elif ('-v' in sys.argv or '--version' in sys.argv) and len(sys.argv) > 2:
        arg_parser.error(Messenger.PROGRAM_VERSION_ARGS_ERROR)

    # ************************** ALTERER REQUIREMENTS *************************

    if action == 'a':
        if not (args.config or
                (args.db_name and args.old_role and args.new_role)):
            alterer.error(Messenger.ALTERER_ARGS_ERROR)
        if not (args.config_connection or
                (args.pg_host and isinstance(args.pg_port, int)
                 and args.pg_user)):
            alterer.error(Messenger.CONNECTION_ARGS_ERROR)

    # ************************** BACKER REQUIREMENTS **************************

    elif action == 'B':
        if not (args.config or args.db_name or args.cluster):
            backer.error(Messenger.BACKER_ARGS_ERROR)
        if not (args.config_connection or
                (args.pg_host and isinstance(args.pg_port, int)
                 and args.pg_user)):
            backer.error(Messenger.CONNECTION_ARGS_ERROR)

    # ************************** DROPPER REQUIREMENTS *************************

    elif action == 'd':
        if not (args.config or args.db_name):
            dropper.error(Messenger.DROPPER_ARGS_ERROR)
        if not (args.config_connection or
                (args.pg_host and isinstance(args.pg_port, int)
                 and args.pg_user)):
            dropper.dropper(Messenger.CONNECTION_ARGS_ERROR)

    # ************************* INFORMER REQUIREMENTS *************************

    elif action == 'i':
        if (args.details_conns is None and args.details_dbs is None
            and args.details_users is None) \
                and not (args.details_conns or args.details_dbs
                         or args.details_users or args.list_conns
                         or args.list_dbs or args.list_users
                         or args.version_pg or args.version_num_pg
                         or args.time_start or args.time_up):
            informer.error(Messenger.INFORMER_ARGS_ERROR)
        if not (args.config_connection or
                (args.pg_host and isinstance(args.pg_port, int)
                 and args.pg_user)):
            informer.error(Messenger.CONNECTION_ARGS_ERROR)

    # ****************************** REPLICATOR *******************************

    elif action == 'r':
        if not (args.config or args.db_name):
            replicator.error(Messenger.REPLICATOR_ARGS_ERROR)
        if not (args.config_connection or
                (args.pg_host and isinstance(args.pg_port, int)
                 and args.pg_user)):
            replicator.error(Messenger.CONNECTION_ARGS_ERROR)

    # ******************************* RESTORER ********************************

    elif action == 'R':
        if not (args.config or args.db_backup or
                (args.cluster and args.cluster_backup)):
            restorer.error(Messenger.RESTORER_ARGS_ERROR)
        if not (args.config_connection or
                (args.pg_host and isinstance(args.pg_port, int)
                 and args.pg_user)):
            restorer.error(Messenger.CONNECTION_ARGS_ERROR)

    # ************************ TERMINATOR REQUIREMENTS ************************

    elif action == 't':
        if not (args.config or args.all or args.db_name or args.user):
            terminator.error(Messenger.TERMINATOR_ARGS_ERROR)
        if not (args.config_connection or
                (args.pg_host and isinstance(args.pg_port, int)
                 and args.pg_user)):
            terminator.error(Messenger.CONNECTION_ARGS_ERROR)

    # ************************** TRIMMER REQUIREMENTS *************************

    elif action == 'T':
        if not (args.config or
                ((args.db_name or args.cluster) and args.bkp_folder)):
            trimmer.error(Messenger.TRIMMER_ARGS_ERROR_1)
        if not (args.config or
                (isinstance(args.n_backups, int) and
                 isinstance(args.expiry_days, int))):
            trimmer.error(Messenger.TRIMMER_ARGS_ERROR_2)
        if not args.cluster and not \
            (args.config_connection or
             (args.pg_host and isinstance(args.pg_port, int)
              and args.pg_user)):
            trimmer.error(Messenger.CONNECTION_ARGS_ERROR)
        if args.cluster and (args.config_connection or args.pg_host
                             or args.pg_port or args.pg_user):
            trimmer.error(Messenger.TRIMMER_CONNECTION_ARGS_ERROR)

    # ************************* VACUUMER REQUIREMENTS *************************

    elif action == 'v':
        if not (args.config or args.db_name):
            vacuumer.error(Messenger.VACUUMER_ARGS_ERROR)
        if not (args.config_connection or
                (args.pg_host and isinstance(args.pg_port, int)
                 and args.pg_user)):
            vacuumer.error(Messenger.CONNECTION_ARGS_ERROR)

    else:
        pass

    if args.version:
        print(Messenger.PROGRAM_VERSION)

    elif args.info:
        print(Messenger.PROGRAM_INFO)

    else:
        # Load a specific module depending on the gotten console parameters
        orchestrator = Orchestrator(action, args)
        orchestrator.detect_module()
