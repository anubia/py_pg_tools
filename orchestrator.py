#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from vacuumer import Vacuumer
from backer import Backer
from backer import BackerCluster
from trimmer import Trimmer
from trimmer import TrimmerCluster
from terminator import Terminator
from connecter import Connecter
from configurator import Configurator
from informer import Informer
from replicator import Replicator
from dropper import Dropper
from restorer import Restorer
from restorer import RestorerCluster

from logger.logger import Logger
from messenger.messenger import Messenger
from db_selector.db_selector import DbSelector
from dir_tools.dir_tools import Dir


class Orchestrator:

    action = None
    args = []
    logger = None

    def __init__(self, action, args, logger=None):
        self.action = action
        self.args = args
        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

    @staticmethod
    def show_dbs(dbs_list, logger):
        message = 'Analizando datos en PostgreSQL...'
        logger.highlight('info', message, 'white')

        for db in dbs_list:  # Para cada BD en PostgreSQL...
            message = 'Detectada base de datos: "{}".'.format(db['name'])
            logger.info(message)

    @staticmethod
    def get_cfg_vars(config_type, config_path, logger):
        configurator = Configurator(logger)
        configurator.load_cfg(config_type, config_path)
        return configurator.parser

    def get_connecter(self):
        # Parse connection vars file and connect to PostgreSQL
        config_type = 'connect'
        parser = Orchestrator.get_cfg_vars(config_type,
                                           self.args.config_connection,
                                           self.logger)
        connecter = Connecter(parser.conn_vars['server'],
                              parser.conn_vars['user'],
                              parser.conn_vars['pwd'],
                              parser.conn_vars['port'], self.logger)
        return connecter

    def get_db_backer(self, connecter):
        config_type = 'backup'
        if self.args.config:  # If config exists, load its params
            parser = Orchestrator.get_cfg_vars(config_type,
                                               self.args.config,
                                               self.logger)
            backer = Backer(connecter, parser.bkp_vars['bkp_path'],
                            parser.bkp_vars['server_alias'],
                            parser.bkp_vars['bkp_type'],
                            parser.bkp_vars['prefix'],
                            parser.bkp_vars['in_dbs'],
                            parser.bkp_vars['in_regex'],
                            parser.bkp_vars['in_forbidden'],
                            parser.bkp_vars['in_priority'],
                            parser.bkp_vars['ex_dbs'],
                            parser.bkp_vars['ex_regex'],
                            parser.bkp_vars['ex_templates'],
                            parser.bkp_vars['vacuum'],
                            parser.bkp_vars['db_owner'], self.logger)
            # Overwrite the config vars with the console ones
            if self.args.group:
                backer.server_alias = self.args.group
            if self.args.backup_format:
                backer.bkp_type = '.' + self.args.backup_format
            if self.args.db_name:
                backer.in_dbs = self.args.db_name
                backer.ex_dbs = []
                backer.in_regex = ''
                backer.ex_regex = ''
                backer.ex_templates = False
        else:  # If config does not exist, load default params
            if self.args.backup_format:
                bkp_type = '.' + self.args.backup_format
            else:
                bkp_type = None
            backer = Backer(connecter, server_alias=self.args.group,
                            bkp_type=bkp_type, in_dbs=self.args.db_name,
                            logger=self.logger)
        return backer

    def get_cl_backer(self, connecter):
        config_type = 'backup_all'
        if self.args.config:  # If config exists, load its params
            parser = Orchestrator.get_cfg_vars(config_type,
                                               self.args.config,
                                               self.logger)
            backer = BackerCluster(connecter, parser.bkp_vars['bkp_path'],
                                   parser.bkp_vars['server_alias'],
                                   parser.bkp_vars['bkp_type'],
                                   parser.bkp_vars['prefix'],
                                   parser.bkp_vars['vacuum'], self.logger)
            # Overwrite the config vars with the console ones
            if self.args.group:
                backer.server_alias = self.args.group
            if self.args.backup_format:
                backer.bkp_type = '.' + self.args.backup_format
        else:  # If config does not exist, load default params
            if self.args.backup_format:
                bkp_type = '.' + self.args.backup_format
            else:
                bkp_type = None
            backer = BackerCluster(connecter, server_alias=self.args.group,
                                   bkp_type=bkp_type, logger=self.logger)
        return backer

    def setup_backer(self):

        connecter = self.get_connecter()

        # Parse bkp_vars depending on the action to do
        if self.args.cluster:
            backer = self.get_cl_backer(connecter)
        else:
            backer = self.get_db_backer(connecter)

        # Comprobar si el usuario actualmente conectado es superusuario de
        # PostgreSQL
        pg_superuser = connecter.is_pg_superuser()
        if not pg_superuser:  # Si no es superusuario de PostgreSQL...
            if self.args.cluster is False:
                # Sólo puede manipular las BDs de las que es propietario
                backer.db_owner = connecter.user
                self.logger.highlight(
                    'warning', Messenger.ACTION_DB_NO_SUPERUSER,
                    'yellow', effect='bold')
            else:
                self.logger.stop_exe(Messenger.ACTION_CL_NO_SUPERUSER)

        # Do the backups
        if self.args.cluster is False:
            # Ejecutar consulta de PostgreSQL y obtener nombres de todas
            # las bases de datos almacenadas, sus permisos de conexión y
            # sus propietarios
            connecter.get_cursor_dbs(backer.ex_templates, backer.db_owner)

            dbs_all = DbSelector.list_pg_dbs(connecter.cursor)

            Orchestrator.show_dbs(dbs_all, self.logger)

            # Almacenar las bases de datos de las que se realizará una
            # copia de seguridad
            bkp_list = DbSelector.get_filtered_dbs(
                dbs_all, backer.in_dbs, backer.ex_dbs, backer.in_regex,
                backer.ex_regex, backer.in_priority, self.logger)

            if self.args.terminate:  # Terminate dbs connections if necessary
                terminator = Terminator(connecter, target_dbs=bkp_list,
                                        logger=self.logger)
                terminator.terminate_backend_dbs()

            # Realizar las nuevas copias de seguridad (dump)
            backer.backup_dbs(bkp_list)
        else:
            if self.args.terminate:  # Terminate all connections if necessary
                terminator = Terminator(connecter, target_all=True,
                                        logger=self.logger)
                terminator.terminate_backend_all()
            # Realizar copias de seguridad del cluster (dumpall)
            backer.backup_cl()

        # Cerrar comunicación con la base de datos
        connecter.pg_disconnect()

    def get_terminator(self, connecter):

        if self.args.config:
            config_type = 'terminate'
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)
            terminator = Terminator(connecter,
                                    parser.kill_vars['kill_all'],
                                    parser.kill_vars['kill_user'],
                                    parser.kill_vars['kill_dbs'],
                                    self.logger)
        else:
            terminator = Terminator(connecter, logger=self.logger)

        if self.args.all:
            terminator.target_all = True
        elif self.args.db_name:
            terminator.target_dbs = self.args.db_name
        elif self.args.user:
            terminator.target_user = self.args.user
        else:
            pass

        return terminator

    def setup_terminator(self):

        connecter = self.get_connecter()
        terminator = self.get_terminator(connecter)

        if terminator.target_all:
            terminator.terminate_backend_all()
        elif terminator.target_dbs:
            terminator.terminate_backend_dbs()
        elif terminator.target_user:
            terminator.terminate_backend_user()
        else:
            pass  # Info here: doing nothing

    def get_trimmer(self):

        # Parse bkp_vars depending on the action to do
        if self.args.cluster:
            config_type = 'trim_all'
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            trimmer = TrimmerCluster(parser.bkp_vars['bkp_path'],
                                     parser.bkp_vars['prefix'],
                                     parser.bkp_vars['min_bkps'],
                                     parser.bkp_vars['obs_days'],
                                     parser.bkp_vars['max_tsize'],
                                     self.logger)
        else:
            config_type = 'trim'
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            trimmer = Trimmer(parser.bkp_vars['bkp_path'],
                              parser.bkp_vars['prefix'],
                              parser.bkp_vars['in_dbs'],
                              parser.bkp_vars['in_regex'],
                              parser.bkp_vars['in_priority'],
                              parser.bkp_vars['ex_dbs'],
                              parser.bkp_vars['ex_regex'],
                              parser.bkp_vars['min_bkps'],
                              parser.bkp_vars['obs_days'],
                              parser.bkp_vars['max_tsize'],
                              parser.bkp_vars['pg_warnings'],
                              self.logger)

            if self.args.db_name:
                trimmer.in_dbs = self.args.db_name
                trimmer.ex_dbs = []
                trimmer.in_regex = ''
                trimmer.ex_regex = ''

        return trimmer

    def setup_trimmer(self):

        trimmer = self.get_trimmer()

        bkps_list = Dir.sorted_flist(trimmer.bkp_path)

        if bkps_list:

            if self.args.cluster is False:
                bkped_dbs = Dir.get_dbs_bkped(bkps_list)

                if bkped_dbs:

                    # Almacenar las bases de datos de las que se realizará
                    # una copia de seguridad
                    dbs_to_clean = DbSelector.get_filtered_dbnames(
                        bkped_dbs, trimmer.in_dbs, trimmer.ex_dbs,
                        trimmer.in_regex, trimmer.ex_regex,
                        trimmer.in_priority, self.logger)

                    # Realizar la limpieza (clean)
                    trimmer.trim_dbs(bkps_list, dbs_to_clean)

                else:
                    self.logger.highlight('warning',
                                          Messenger.NO_BACKUP_IN_DIR,
                                          'yellow', effect='bold')

            else:
                trimmer.trim_clusters(bkps_list)

        else:
            self.logger.highlight('warning', Messenger.NO_FILE_IN_DIR,
                                  'yellow', effect='bold')

        if self.args.cluster is False and trimmer.pg_warnings:

            # Parse connection vars file and connect to PostgreSQL
            connecter = self.get_connecter()

            # Ejecutar consulta de PostgreSQL y obtener nombres de todas
            # las bases de datos almacenadas, sus permisos de conexión y
            # sus propietarios
            connecter.get_cursor_dbs(False)

            pg_dbs = []
            # Para cada registro de la consulta...
            for record in connecter.cursor:
                pg_dbs.append(record['datname'])

            bkped_dbs = Dir.get_dbs_bkped(bkps_list)

            Dir.show_pg_warnings(pg_dbs, bkped_dbs, self.logger)

            # Cerrar comunicación con la base de datos
            connecter.pg_disconnect()

    def get_vacuumer(self, connecter):

        config_type = 'vacuum'
        parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                           self.logger)

        vacuumer = Vacuumer(connecter,
                            parser.bkp_vars['in_dbs'],
                            parser.bkp_vars['in_regex'],
                            parser.bkp_vars['in_forbidden'],
                            parser.bkp_vars['in_priority'],
                            parser.bkp_vars['ex_dbs'],
                            parser.bkp_vars['ex_regex'],
                            parser.bkp_vars['ex_templates'],
                            parser.bkp_vars['db_owner'],
                            self.logger)
        return vacuumer

    def setup_vacuumer(self):

        connecter = self.get_connecter()

        vacuumer = self.get_vacuumer(connecter)

        pg_superuser = connecter.is_pg_superuser()
        if not pg_superuser:
            vacuumer.db_owner = connecter.user
            self.logger.warning(Messenger.ACTION_DB_NO_SUPERUSER)

        connecter.get_cursor_dbs(vacuumer.ex_templates, vacuumer.db_owner)

        dbs_all = DbSelector.list_pg_dbs(connecter.cursor)

        Orchestrator.show_dbs(dbs_all, self.logger)

        # Almacenar las bases de datos de las que se realizará una copia de
        # seguridad
        vacuum_list = DbSelector.get_filtered_dbs(
            dbs_all, vacuumer.in_dbs, vacuumer.ex_dbs, vacuumer.in_regex,
            vacuumer.ex_regex, vacuumer.in_priority, self.logger)

        # Realizar las nuevas copias de seguridad (dump)
        vacuumer.vacuum_dbs(vacuum_list)

        if self.args.terminate:  # Terminate dbs connections if necessary
            terminator = Terminator(connecter, target_dbs=vacuum_list,
                                    logger=self.logger)
            terminator.terminate_backend_dbs()

        # Cerrar comunicación con la base de datos
        connecter.pg_disconnect()

    def setup_informer(self):

        connecter = self.get_connecter()
        informer = Informer(connecter, self.args.db_name, self.args.users,
                            self.logger)
        if self.args.db_name:
            informer.show_pg_dbs_data()
        else:
            # TODO Poner aquí lo que ocurre si se manda una lista de usuarios
            # de PostgreSQL al informer
            pass

    def setup_replicator(self):

        connecter = self.get_connecter()
        replicator = Replicator(connecter, self.args.db_name[0],
                                self.args.db_name[1], self.logger)
        replicator.replicate_pg_db()

    def setup_dropper(self):

        connecter = self.get_connecter()
        dropper = Dropper(connecter, self.args.db_name, self.logger)
        dropper.drop_pg_dbs()

    def setup_restorer(self):

        connecter = self.get_connecter()
        if self.args.db_backup:
            restorer = Restorer(connecter, self.args.db_backup[0],
                                self.args.db_backup[1], self.logger)
            restorer.restore_db_backup()
        else:
            restorer = RestorerCluster(connecter, self.args.cluster_backup,
                                       self.logger)
            restorer.restore_cluster_backup()

    def detect_module(self):

        # ****************************** BACKER *******************************
        if self.action == 'B':
            self.setup_backer()

        # ***************************** INFORMER ******************************
        elif self.action == 'd':
            self.setup_dropper()

        # ***************************** INFORMER ******************************
        elif self.action == 'i':
            self.setup_informer()

        # **************************** REPLICATOR *****************************
        elif self.action == 'r':
            self.setup_replicator()

        # ***************************** RESTORER ******************************
        elif self.action == 'R':
            self.setup_restorer()

        # **************************** TERMINATOR *****************************
        elif self.action == 't':
            self.setup_terminator()

        # ***************************** TRIMMER *******************************
        elif self.action == 'T':
            self.setup_trimmer()

        # ***************************** VACUUMER ******************************
        elif self.action == 'v':
            self.setup_vacuumer()

        else:
            pass
