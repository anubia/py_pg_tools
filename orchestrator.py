#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


from backer import Backer
from backer import BackerCluster
from configurator import Configurator
from connecter import Connecter
from db_selector.db_selector import DbSelector
from dir_tools.dir_tools import Dir
from dropper import Dropper
from informer import Informer
from logger.logger import Logger
from const.const import Messenger
from replicator import Replicator
from restorer import Restorer
from restorer import RestorerCluster
from terminator import Terminator
from trimmer import Trimmer
from trimmer import TrimmerCluster
from vacuumer import Vacuumer


class Orchestrator:

    action = None  # The action to do
    args = []  # The list of parameters received in console
    logger = None  # A logger to show and log some messages

    def __init__(self, action, args):

        self.action = action
        self.args = args
        self.logger = self.get_logger()

        # Stop execution if the user running the program is root
        Dir.forbid_root(self.logger)

    @staticmethod
    def show_dbs(dbs_list, logger):
        '''
        Target:
            - show in console and log a list of databases.
        Parameters:
            - dbs_list: the list of databases to be shown.
            - logger: a logger to show and log some messages.
        '''

        logger.highlight('info', Messenger.ANALIZING_PG_DATA, 'white')

        for db in dbs_list:  # Para cada BD en PostgreSQL...
            message = Messenger.DETECTED_DB.format(dbname=db['name'])
            logger.info(message)

    @staticmethod
    def get_cfg_vars(config_type, config_path, logger=None):
        '''
        Target:
            - get all the variables stored in a config file with cfg extension.
        Parameters:
            - config_type: the type of config file which is going to be loaded,
            to differ it from the other types which will have different
            sections and variables.
            - logger: a logger to show and log some messages.
        Return:
            - the parser which will contain all the config file variables.
        '''
        configurator = Configurator()

        # In the case of logger being None, this is because a logger config
        # file is being loaded to specify some settings
        if logger:
            configurator.load_cfg(config_type, config_path, logger)
        else:
            configurator.load_cfg(config_type, config_path)

        return configurator.parser

    def get_logger(self):
        '''
        Target:
            - get a logger object with its variables.
        Return:
            - a logger to show and log some messages.
        '''
        # If the user specified a logger config file through console...
        if self.args.config_logger:

            config_type = 'log'
            # Get the variables from the config file, without sending any
            # logger!! It would give a redundancy error
            parser = Orchestrator.get_cfg_vars(config_type,
                                               self.args.config_logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.logger_logfile:
                parser.log_vars['log_dir'] = self.args.logger_logfile
            if self.args.logger_level:
                parser.log_vars['level'] = self.args.logger_level
            if self.args.logger_mute:
                parser.log_vars['mute'] = self.args.logger_mute

            # Create the logger with the specified variables
            logger = Logger(parser.log_vars['log_dir'],
                            parser.log_vars['level'], parser.log_vars['mute'])

        # If the user did not specify a logger config file through console...
        else:

            # Create the logger with the console variables
            logger = Logger(self.args.logger_logfile, self.args.logger_level,
                            self.args.logger_mute)

        return logger

    def get_connecter(self):
        '''
        Target:
            - get a connecter object with its variables.
        Return:
            - a connecter which will allow queries to PostgreSQL.
        '''
        # If the user specified a connecter config file through console...
        if self.args.config_connection:

            config_type = 'connect'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type,
                                               self.args.config_connection,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.pg_host:
                parser.conn_vars['server'] = self.args.pg_host
            if self.args.pg_user:
                parser.conn_vars['user'] = self.args.pg_user
            if self.args.pg_port:
                parser.conn_vars['port'] = self.args.pg_port

            # Create the connecter with the specified variables
            connecter = Connecter(parser.conn_vars['server'],
                                  parser.conn_vars['user'],
                                  parser.conn_vars['port'], self.logger)

        # If the user did not specify a connecter config file through console..
        else:

            # Create the connecter with the console variables
            connecter = Connecter(self.args.pg_host, self.args.pg_user,
                                  self.args.pg_port, self.logger)

        return connecter

    def get_db_backer(self, connecter):
        '''
        Target:
            - get a backer object with variables to backup databases.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a backer which will backup databases.
        '''
        # If the user specified a backer config file through console...
        if self.args.config:

            config_type = 'backup'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.bkp_path:
                parser.bkp_vars['bkp_path'] = self.args.bkp_path
            if self.args.group:
                parser.bkp_vars['group'] = self.args.group
            if self.args.backup_format:
                parser.bkp_vars['bkp_type'] = self.args.backup_format
            if self.args.db_name:
                parser.bkp_vars['in_dbs'] = self.args.db_name
                parser.bkp_vars['ex_dbs'] = []
                parser.bkp_vars['in_regex'] = ''
                parser.bkp_vars['ex_regex'] = ''
            if self.args.ex_templates:
                parser.bkp_vars['ex_templates'] = True
            elif self.args.no_ex_templates:
                parser.bkp_vars['ex_templates'] = False
            if self.args.vacuum:
                parser.bkp_vars['vacuum'] = True
            elif self.args.no_vacuum:
                parser.bkp_vars['vacuum'] = False
            if self.args.db_owner:
                parser.bkp_vars['db_owner'] = self.args.db_owner

            # Create the backer with the specified variables
            backer = Backer(connecter, parser.bkp_vars['bkp_path'],
                            parser.bkp_vars['group'],
                            parser.bkp_vars['bkp_type'],
                            parser.bkp_vars['prefix'],
                            parser.bkp_vars['in_dbs'],
                            parser.bkp_vars['in_regex'],
                            parser.bkp_vars['in_priority'],
                            parser.bkp_vars['ex_dbs'],
                            parser.bkp_vars['ex_regex'],
                            parser.bkp_vars['ex_templates'],
                            parser.bkp_vars['vacuum'],
                            parser.bkp_vars['db_owner'], self.logger)

        # If the user did not specify a backer config file through console...
        else:

            if self.args.ex_templates:
                ex_templates = True
            elif self.args.no_ex_templates:
                ex_templates = False
            else:
                ex_templates = True
            if self.args.vacuum:
                vacuum = True
            elif self.args.no_vacuum:
                vacuum = False
            else:
                vacuum = True

            # Create the backer with the console variables
            backer = Backer(connecter, bkp_path=self.args.bkp_path,
                            group=self.args.group,
                            bkp_type=self.args.backup_format,
                            in_dbs=self.args.db_name,
                            ex_templates=ex_templates, vacuum=vacuum,
                            db_owner=self.args.db_owner,
                            logger=self.logger)

        return backer

    def get_cl_backer(self, connecter):
        '''
        Target:
            - get a backer object with variables to backup databases' clusters.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a backer which will backup databases' clusters.
        '''
        # If the user specified a backer config file through console...
        if self.args.config:
            config_type = 'backup_all'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.bkp_path:
                parser.bkp_vars['bkp_path'] = self.args.bkp_path
            if self.args.group:
                parser.bkp_vars['group'] = self.args.group
            if self.args.backup_format:
                parser.bkp_vars['bkp_type'] = self.args.backup_format
            if self.args.vacuum:
                parser.bkp_vars['vacuum'] = True
            elif self.args.no_vacuum:
                parser.bkp_vars['vacuum'] = False

            # Create the backer with the specified variables
            backer = BackerCluster(connecter, parser.bkp_vars['bkp_path'],
                                   parser.bkp_vars['group'],
                                   parser.bkp_vars['bkp_type'],
                                   parser.bkp_vars['prefix'],
                                   parser.bkp_vars['vacuum'], self.logger)

        # If the user did not specify a backer config file through console...
        else:
            if self.args.vacuum:
                vacuum = True
            elif self.args.no_vacuum:
                vacuum = False
            else:
                vacuum = True

            # Create the backer with the console variables
            backer = BackerCluster(connecter, bkp_path=self.args.bkp_path,
                                   group=self.args.group,
                                   bkp_type=self.args.backup_format,
                                   vacuum=vacuum, logger=self.logger)

        return backer

    def get_dropper(self, connecter):
        '''
        Target:
            - get a dropper object with variables to drop some PostgreSQL
            databases.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a dropper which will delete some PostgreSQL databases.
        '''
        # If the user specified a dropper config file through console...
        if self.args.config:
            config_type = 'drop'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.db_name:
                parser.bkp_vars['in_dbs'] = self.args.db_name

            # Create the dropper with the specified variables
            dropper = Dropper(connecter, parser.bkp_vars['in_dbs'],
                              self.logger)

        # If the user did not specify a dropper config file through console...
        else:
            # Create the dropper with the console variables
            dropper = Dropper(connecter, self.args.db_name, self.logger)

        return dropper

    def get_informer(self, connecter):
        '''
        Target:
            - get an informer object with variables to show some PostgreSQL
            information.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a informer which will get and show some PostgreSQL information.
        '''
        # If the user specified a informer config file through console...
        if self.args.config:
            config_type = 'inform'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.db_name:
                parser.bkp_vars['in_dbs'] = self.args.db_name
                parser.bkp_vars['in_users'] = []
            elif self.args.users:
                parser.bkp_vars['in_dbs'] = []
                parser.bkp_vars['in_users'] = self.args.users

            # Create the informer with the specified variables
            informer = Informer(connecter, parser.bkp_vars['in_dbs'],
                                parser.bkp_vars['in_users'], self.logger)

        # If the user did not specify a informer config file through console...
        else:
            # Create the informer with the console variables
            informer = Informer(connecter, self.args.db_name, self.args.users,
                                self.logger)

        return informer

    def get_replicator(self, connecter):
        '''
        Target:
            - get a replicator object with variables to clone a PostgreSQL
            database.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a replicator which will clone a PostgreSQL database.
        '''
        # If the user specified a replicator config file through console...
        if self.args.config:
            config_type = 'replicate'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.db_name:
                parser.bkp_vars['new_dbname'] = self.args.db_name[0]
                parser.bkp_vars['original_dbname'] = self.args.db_name[1]

            # Create the replicator with the specified variables
            replicator = Replicator(connecter, parser.bkp_vars['new_dbname'],
                                    parser.bkp_vars['original_dbname'],
                                    self.logger)

        # If the user did not specify a replicator config file through
        # console...
        else:
            # Create the replicator with the console variables
            replicator = Replicator(connecter, self.args.db_name[0],
                                    self.args.db_name[1], self.logger)

        return replicator

    def get_db_restorer(self, connecter):
        '''
        Target:
            - get a restorer object with variables to restore a database backup
            in PostgreSQL.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a restorer which will restore a PostgreSQL database.
        '''
        # If the user specified a restorer config file through console...
        if self.args.config:
            config_type = 'restore'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.db_backup:
                parser.bkp_vars['bkp_path'] = self.args.db_backup[0]
                parser.bkp_vars['new_dbname'] = self.args.db_backup[1]

            # Create the restorer with the specified variables
            restorer = Restorer(connecter, parser.bkp_vars['bkp_path'],
                                parser.bkp_vars['new_dbname'], self.logger)

        # If the user did not specify a restorer config file through console...
        else:
            # Create the restorer with the console variables
            restorer = Restorer(connecter, self.args.db_backup[0],
                                self.args.db_backup[1], self.logger)

        return restorer

    def get_cl_restorer(self, connecter):
        '''
        Target:
            - get a restorer object with variables to restore a cluster backup
            in PostgreSQL.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a restorer which will restore a PostgreSQL cluster.
        '''
        # If the user specified a restorer config file through console...
        if self.args.config:
            config_type = 'restore_all'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.cluster_backup:
                parser.bkp_vars['bkp_path'] = self.args.cluster_backup

            # Create the restorer with the specified variables
            restorer = RestorerCluster(connecter, parser.bkp_vars['bkp_path'],
                                       self.logger)

        # If the user did not specify a restorer config file through console...
        else:
            # Create the restorer with the console variables
            restorer = Restorer(connecter, self.args.cluster_backup,
                                self.logger)

        return restorer

    def get_terminator(self, connecter):
        '''
        Target:
            - get a terminator object with variables to terminate connections
            to PostgreSQL.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a terminator which will terminate connections to
            PostgreSQL.
        '''
        # If the user specified a terminator config file through console...
        if self.args.config:
            config_type = 'terminate'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.all:
                parser.kill_vars['kill_all'] = True
            elif self.args.db_name:
                parser.kill_vars['kill_user'] = self.args.db_name
            elif self.args.user:
                parser.kill_vars['kill_dbs'] = self.args.user
            else:
                pass

            # Create the terminator with the specified variables
            terminator = Terminator(connecter,
                                    parser.kill_vars['kill_all'],
                                    parser.kill_vars['kill_user'],
                                    parser.kill_vars['kill_dbs'],
                                    self.logger)

        # If the user did not specify a terminator config file through
        # console...
        else:
            # Create the terminator with the console variables
            terminator = Terminator(connecter, self.args.all,
                                    self.args.db_name, self.args.user,
                                    self.logger)

        return terminator

    def get_db_trimmer(self):
        '''
        Target:
            - get a trimmer object with its variables to delete some databases'
            backups in a selected directory.
        Return:
            - a trimmer which will delete databases' backups.
        '''
        # If the user specified a trimmer config file through console...
        if self.args.config:
            config_type = 'trim'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.db_name:
                parser.bkp_vars['in_dbs'] = self.args.db_name
                parser.bkp_vars['ex_dbs'] = []
                parser.bkp_vars['in_regex'] = ''
                parser.bkp_vars['ex_regex'] = ''
            if self.args.bkp_folder:
                parser.bkp_vars['bkp_path'] = self.args.bkp_folder
            if self.args.prefix:
                parser.bkp_vars['prefix'] = self.args.prefix
            if self.args.n_backups:
                parser.bkp_vars['min_n_bkps'] = self.args.n_backups
            if self.args.expiry_days:
                parser.bkp_vars['exp_days'] = self.args.expiry_days
            if self.args.max_size:
                parser.bkp_vars['max_size'] = self.args.max_size
            if parser.bkp_vars['pg_warnings']:
                connecter = self.get_connecter()
            else:
                connecter = None

            # Create the trimmer with the specified variables
            trimmer = Trimmer(connecter, parser.bkp_vars['bkp_path'],
                              parser.bkp_vars['prefix'],
                              parser.bkp_vars['in_dbs'],
                              parser.bkp_vars['in_regex'],
                              parser.bkp_vars['in_priority'],
                              parser.bkp_vars['ex_dbs'],
                              parser.bkp_vars['ex_regex'],
                              parser.bkp_vars['min_n_bkps'],
                              parser.bkp_vars['exp_days'],
                              parser.bkp_vars['max_size'],
                              parser.bkp_vars['pg_warnings'], self.logger)

        # If the user did not specify a trimmer config file through console...
        else:
            # There is no option "pg_warnings" in console so it is obligatory
            # to connect to PostgreSQL here
            connecter = self.get_connecter()

            # Create the trimmer with the console variables
            trimmer = Trimmer(connecter=connecter,
                              bkp_path=self.args.bkp_folder,
                              prefix=self.args.prefix,
                              in_dbs=self.args.db_name,
                              min_n_bkps=self.args.n_backups,
                              exp_days=self.args.expiry_days,
                              max_size=self.args.max_size, logger=self.logger)

        return trimmer

    def get_cl_trimmer(self):
        '''
        Target:
            - get a trimmer object with its variables to delete some clusters'
            backups in a selected directory.
        Return:
            - a trimmer which will delete clusters' backups.
        '''
        # If the user specified a trimmer config file through console...
        if self.args.config:
            config_type = 'trim_all'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.bkp_folder:
                parser.bkp_vars['bkp_path'] = self.args.bkp_folder
            if self.args.prefix:
                parser.bkp_vars['prefix'] = self.args.prefix
            if self.args.n_backups:
                parser.bkp_vars['min_n_bkps'] = self.args.n_backups
            if self.args.expiry_days:
                parser.bkp_vars['exp_days'] = self.args.expiry_days
            if self.args.max_size:
                parser.bkp_vars['max_size'] = self.args.max_size

            # Create the trimmer with the specified variables
            trimmer = TrimmerCluster(parser.bkp_vars['bkp_path'],
                                     parser.bkp_vars['prefix'],
                                     parser.bkp_vars['min_n_bkps'],
                                     parser.bkp_vars['exp_days'],
                                     parser.bkp_vars['max_size'], self.logger)
        else:
            # Create the trimmer with the console variables
            trimmer = TrimmerCluster(self.args.bkp_folder, self.args.prefix,
                                     self.args.n_backups,
                                     self.args.expiry_days, self.args.max_size,
                                     self.logger)

        return trimmer

    def get_vacuumer(self, connecter):
        '''
        Target:
            - get a vacuumer object with variables to vacuum databases in
            PostgreSQL.
        Parameters:
            - connecter: an object with connection parameters to connect to
            PostgreSQL.
        Return:
            - a vacuumer which will vacuum PostgreSQL databases.
        '''
        # If the user specified a vacuumer config file through console...
        if self.args.config:

            config_type = 'vacuum'
            # Get the variables from the config file
            parser = Orchestrator.get_cfg_vars(config_type, self.args.config,
                                               self.logger)

            # Overwrite the config variables with the console ones if necessary
            if self.args.db_name:
                parser.bkp_vars['in_dbs'] = self.args.db_name
                parser.bkp_vars['ex_dbs'] = []
                parser.bkp_vars['in_regex'] = ''
                parser.bkp_vars['ex_regex'] = ''
            if self.args.db_owner:
                parser.bkp_vars['db_owner'] = self.args.db_owner

            # Create the vacuumer with the specified variables
            vacuumer = Vacuumer(connecter,
                                parser.bkp_vars['in_dbs'],
                                parser.bkp_vars['in_regex'],
                                parser.bkp_vars['in_priority'],
                                parser.bkp_vars['ex_dbs'],
                                parser.bkp_vars['ex_regex'],
                                parser.bkp_vars['ex_templates'],
                                parser.bkp_vars['db_owner'],
                                self.logger)

        # If the user did not specify a vacuumer config file through console...
        else:

            # Create the vacuumer with the console variables
            vacuumer = Vacuumer(connecter, in_dbs=self.args.db_name,
                                db_owner=self.args.db_owner,
                                logger=self.logger)

        return vacuumer

    def setup_backer(self):
        '''
        Target:
            - executes the backer depending on the type of backup to make, the
            role of the user who is connected to PostgreSQL and the rest of the
            conditions. It calls a terminator if necessary.
        '''
        connecter = self.get_connecter()

        # Get databases or clusters' backer depending on the option selected
        # by the user in console
        if self.args.cluster:
            backer = self.get_cl_backer(connecter)
        else:
            backer = self.get_db_backer(connecter)

        # Check if the role of user connected to PostgreSQL is superuser
        pg_superuser = connecter.is_pg_superuser()
        if not pg_superuser:
            if self.args.cluster is False:
                # Users who are not superusers will only be able to backup the
                # databases they own
                backer.db_owner = connecter.user
                self.logger.highlight(
                    'warning', Messenger.ACTION_DB_NO_SUPERUSER,
                    'yellow', effect='bold')
            else:  # Backup the cluster can only be made by superuser
                self.logger.stop_exe(Messenger.ACTION_CL_NO_SUPERUSER)

        # Make the backups
        if self.args.cluster is False:  # Backup databases

            # Get PostgreSQL databases' names, connection permissions and
            # owners
            connecter.get_cursor_dbs(backer.ex_templates, backer.db_owner)
            # Get these data in a list
            dbs_all = DbSelector.list_pg_dbs(connecter.cursor)
            # Show and log their names
            Orchestrator.show_dbs(dbs_all, self.logger)

            # Get the target databases in a list
            bkp_list = DbSelector.get_filtered_dbs(
                dbs_all, backer.in_dbs, backer.ex_dbs, backer.in_regex,
                backer.ex_regex, backer.in_priority, self.logger)

            # Terminate every connection to these target databases if necessary
            if self.args.terminate:
                terminator = Terminator(connecter, target_dbs=bkp_list,
                                        logger=self.logger)
                terminator.terminate_backend_dbs()

            backer.backup_dbs(bkp_list)  # Make databases' backup

        else:  # Backup a cluster
            # Terminate every connection to any database of the cluster if
            # necessary
            if self.args.terminate:
                terminator = Terminator(connecter, target_all=True,
                                        logger=self.logger)
                terminator.terminate_backend_all()

            backer.backup_cl()  # Make cluster's backup

        # Close connection to PostgreSQL
        connecter.pg_disconnect()

    def setup_dropper(self):
        '''
        Target:
            - delete specified databases in PostgreSQL.
        '''
        connecter = self.get_connecter()
        dropper = self.get_dropper(connecter)

        # Terminate every connection to the target databases if necessary
        if self.args.terminate:
            terminator = Terminator(connecter, target_dbs=dropper.dbnames,
                                    logger=self.logger)
            terminator.terminate_backend_dbs()

        # Delete the databases
        dropper.drop_pg_dbs()

        # Close connection to PostgreSQL
        connecter.pg_disconnect()

    def setup_informer(self):
        '''
        Target:
            - give information about PostgreSQL to the user.
        '''
        connecter = self.get_connecter()
        informer = self.get_informer(connecter)

        if informer.dbnames:  # Give information about databases
            informer.show_pg_dbs_data()
        elif informer.usernames:  # Give information about users
            informer.show_pg_users_data()
        else:
            pass

        # Close connection to PostgreSQL
        connecter.pg_disconnect()

    def setup_replicator(self):
        '''
        Target:
            - clone a database in PostgreSQL.
        '''
        connecter = self.get_connecter()
        replicator = self.get_replicator(connecter)

        # Terminate every connection to the database which is going to be
        # replicated, if necessary
        if self.args.terminate:
            terminator = Terminator(connecter,
                                    target_dbs=replicator.original_dbname,
                                    logger=self.logger)
            terminator.terminate_backend_dbs()

        # Clone the database
        replicator.replicate_pg_db()

        # Close connection to PostgreSQL
        connecter.pg_disconnect()

    def setup_restorer(self):
        '''
        Target:
            - restore a specified backup file as a new database or cluster in
            PostgreSQL.
        '''
        connecter = self.get_connecter()

        if self.args.cluster:  # Restore a cluster (must be created first)
            restorer = self.get_cl_restorer(connecter)
            restorer.restore_cluster_backup()
        else:  # Restore a database
            restorer = self.get_db_restorer(connecter)
            restorer.restore_db_backup()

        # Close connection to PostgreSQL
        connecter.pg_disconnect()

    def setup_terminator(self):
        '''
        Target:
            - executes the terminator taking into account the value of its
            variables.
        '''
        connecter = self.get_connecter()
        terminator = self.get_terminator(connecter)

        if terminator.target_all:  # Terminate all connections
            terminator.terminate_backend_all()
        elif terminator.target_dbs:  # Terminate connections to some databases
            terminator.terminate_backend_dbs()
        elif terminator.target_user:  # Terminate connections of a user
            terminator.terminate_backend_user()
        else:
            pass

        # Close connection to PostgreSQL
        connecter.pg_disconnect()

    def setup_trimmer(self):
        '''
        Target:
            - executes the trimmer in a specified directory and delete its
            selected backups.
        '''
        # Get databases or clusters' trimmer depending on the option selected
        # by the user in console
        if self.args.cluster:
            trimmer = self.get_cl_trimmer()
        else:
            trimmer = self.get_db_trimmer()

        # Get a list with all the files stored in the specified directory and
        # its subdirectories, sorted by modification date
        bkps_list = Dir.sorted_flist(trimmer.bkp_path)

        if bkps_list:  # If there are any files in the specified directory...

            if self.args.cluster is False:  # Trim databases' backups

                # Extract a list of databases' names from the files' names
                bkped_dbs = Dir.get_dbs_bkped(bkps_list)

                if bkped_dbs:  # If there are any backups...

                    # Store those databases whose backups are going to be
                    # trimmed
                    dbs_to_clean = DbSelector.get_filtered_dbnames(
                        bkped_dbs, trimmer.in_dbs, trimmer.ex_dbs,
                        trimmer.in_regex, trimmer.ex_regex,
                        trimmer.in_priority, self.logger)

                    # Delete the selected backups
                    trimmer.trim_dbs(bkps_list, dbs_to_clean)

                else:  # If there are not any backups...
                    self.logger.highlight('warning',
                                          Messenger.NO_BACKUP_IN_DIR,
                                          'yellow', effect='bold')

            else:  # Trim clusters' backups
                trimmer.trim_clusters(bkps_list)

        else:  # If there are not any files in the specified directory...
            self.logger.highlight('warning', Messenger.NO_FILE_IN_DIR,
                                  'yellow', effect='bold')

        # If the user wants some feedback of PostgreSQL databases and backups'
        # status...
        if self.args.cluster is False and trimmer.pg_warnings:

            # Get PostgreSQL databases' names, connection permissions and
            # owners
            trimmer.connecter.get_cursor_dbs(False)

            # On the one hand, store their names in a list
            pg_dbs = []
            for record in trimmer.connecter.cursor:
                pg_dbs.append(record['datname'])

            # On the other hand, store the databases' names which have a backup
            # in the specified directory
            bkped_dbs = Dir.get_dbs_bkped(bkps_list)

            # Compare both lists and show the resultant messages
            Dir.show_pg_warnings(pg_dbs, bkped_dbs, self.logger)

            # Close connection to PostgreSQL
            trimmer.connecter.pg_disconnect()

    def setup_vacuumer(self):
        '''
        Target:
            - executes the vacuumer taking into account the value of its
            variables.
        '''
        connecter = self.get_connecter()

        vacuumer = self.get_vacuumer(connecter)

        # Check if the role of user connected to PostgreSQL is superuser
        pg_superuser = connecter.is_pg_superuser()
        if not pg_superuser:
            # Users who are not superusers will only be able to vacuum the
            # databases they own
            vacuumer.db_owner = connecter.user
            self.logger.warning(Messenger.ACTION_DB_NO_SUPERUSER)

        # Get PostgreSQL databases' names, connection permissions and owners
        connecter.get_cursor_dbs(vacuumer.ex_templates, vacuumer.db_owner)
        # Get their names in a list
        dbs_all = DbSelector.list_pg_dbs(connecter.cursor)
        # Show and log their names
        Orchestrator.show_dbs(dbs_all, self.logger)

        # Get the target databases in a list
        vacuum_list = DbSelector.get_filtered_dbs(
            dbs_all, vacuumer.in_dbs, vacuumer.ex_dbs, vacuumer.in_regex,
            vacuumer.ex_regex, vacuumer.in_priority, self.logger)

        # Terminate every connection to these target databases if necessary
        if self.args.terminate:
            terminator = Terminator(connecter, target_dbs=vacuum_list,
                                    logger=self.logger)
            terminator.terminate_backend_dbs()

        # Vacuum the target databases
        vacuumer.vacuum_dbs(vacuum_list)

        # Close connection to PostgreSQL
        connecter.pg_disconnect()

    def detect_module(self):
        '''
        Target:
            - call the corresponding function to the action stored.
        '''
        if self.action == 'B':  # Call backer
            self.setup_backer()

        elif self.action == 'd':  # Call dropper
            self.setup_dropper()

        elif self.action == 'i':  # Call informer
            self.setup_informer()

        elif self.action == 'r':  # Call replicator
            self.setup_replicator()

        elif self.action == 'R':  # Call restorer
            self.setup_restorer()

        elif self.action == 't':  # Call terminator
            self.setup_terminator()

        elif self.action == 'T':  # Call trimmer
            self.setup_trimmer()

        elif self.action == 'v':  # Call vacuumer
            self.setup_vacuumer()

        else:  # Do nothing
            pass
