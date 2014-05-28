#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


class Messenger:

    PROGRAM_DESCRIPTION = 'This program allows the user the possibility to ' \
                          ' manage PostgreSQL data in an easy way. ' \
                          'Available options:\n' \
                          '- Make a backup of a specified database\n' \
                          '- Make a backup of a specified cluster\n' \
                          '- Delete a specified database\n' \
                          '- Get information about databases or users\n' \
                          '- Replicate a specified database\n' \
                          '- Terminate a specified connection to ' \
                          'PostgreSQL\n' \
                          '- Delete a specified backup\n' \
                          '- Vacuum a specified database\n' \
                          'See more information below and in the help of ' \
                          'each command'
    PROGRAM_VERSION = 'Version: v.0.1'
    PROGRAM_INFO = PROGRAM_VERSION + '\n' \
                                     'Repository: https://gitlab.com/' \
                                     'anubia/py_pg_tools.git\n' \
                                     'Author: Juan Formoso Vasco ' \
                                     '<jfv@anubia.es>\n' \
                                     'Year: 2014'
    PROGRAM_VERSION_HELP = 'Gives the program\'s version'
    PROGRAM_INFO_HELP = 'Gives some information about the program, (the ' \
                        'version, the repository where you can download ' \
                        'it, the author and the year when it was created)'

    BACKER_HELP = 'BACKER: makes a backup of a PostgreSQL cluster or a ' \
                  'specified group of databases'
    B_CONFIG_HELP = 'load a configuration file (.cfg) to get the backer ' \
                    'conditions'
    B_DB_NAME_HELP = 'specify the name/s of the PostgreSQL database/s ' \
                     'to be dumped'
    B_CLUSTER_HELP = 'select dumping the PostgreSQL cluster'
    B_BKP_PATH_HELP = 'specify the path where the backups are going to be ' \
                      'stored'
    B_BACKUP_FORMAT_HELP = 'select the backup\'s file format (dump, bz2, ' \
                           'gz, zip)'
    B_GROUP_HELP = 'select a name to put in the each backup\'s name to ' \
                   'agrupate them'
    B_EX_TEMPLATES_HELP = 'specify whether the databases which are ' \
                          'templates have to be dumped'
    B_NO_EX_TEMPLATES_HELP = 'specify whether the databases which are ' \
                             'templates do not have to be dumped'
    B_VACUUM_HELP = 'vacuum those databases which are going to be dumped ' \
                    'dumped before the process'
    B_NO_VACUUM_HELP = 'do not vacuum those databases which are going to be ' \
                       'dumped before the process'
    B_DB_OWNER_HELP = 'only if the user who is running the program is a ' \
                      'PostgreSQL superuser, this option allows him to ' \
                      'play other PostgreSQL role writting its username'
    B_TERMINATE_HELP = 'terminate every connection (except yours) to each ' \
                       'database which is going to be dumped'

    DROPPER_HELP = 'DROPPER: deletes the specified PostgreSQL databases'
    D_CONFIG_HELP = 'load a configuration file (.cfg) to get the dropper ' \
                    'conditions'
    D_DB_NAME_HELP = 'specify the PostgreSQL databases to be deleted'
    D_TERMINATE_HELP = 'terminate every connection (except yours) to each ' \
                       'database which is going to be dropped'

    INFORMER_HELP = 'INFORMER: gives some information about PostgreSQL'
    I_CONFIG_HELP = 'load a configuration file (.cfg) to get the dropper ' \
                    'conditions'
    I_DETAILS_CONNS_HELP = 'specify a list of PIDs and it will give you ' \
                           'some details about the PostgreSQL connections ' \
                           'which have those PIDs. If no one is specified, ' \
                           'it will show some details about every ' \
                           'connection to PostgreSQL'
    I_DETAILS_DBS_HELP = 'specify a list of PostgreSQL databases and it ' \
                         'will give you some details about them. If no one ' \
                         'is specified, it will show some details about ' \
                         'every PostgreSQL database'
    I_DETAILS_USERS_HELP = 'specify a list of PostgreSQL users and it will ' \
                           'give you some details about them. If no one is ' \
                           'specified, it will show some details about ' \
                           'every PostgreSQL user'
    I_LIST_CONNS_HELP = 'gives a list of the current PostgreSQL connection ' \
                        'PIDs'
    I_LIST_DBS_HELP = 'gives a list of the PostgreSQL databases'
    I_LIST_USERS_HELP = 'gives a list of the PostgreSQL users'
    I_VERSION_PG_HELP = 'gives the PostgreSQL version installed in the host'
    I_VERSION_NUM_PG_HELP = 'gives the PostgreSQL version installed in the ' \
                            'host (numeric format)'
    I_TIME_START_HELP = 'gives the moment when PostgreSQL was started'
    I_TIME_UP_HELP = 'gives how long PostgreSQL has been working'

    REPLICATOR_HELP = 'REPLICATOR: clones the specified PostgreSQL database'
    R_CONFIG_HELP = 'load a configuration file (.cfg) to get the replicator ' \
                    'conditions'
    R_DB_NAME_HELP = 'specifies the new name of the database generated and ' \
                     'the name of the database which is being cloned, ' \
                     'respectively'
    R_TERMINATE_HELP = 'terminate every connection (except yours) to the ' \
                       'database which is going to be replicated'

    RESTORER_HELP = 'RESTORER: restores a database\'s backup file in ' \
                    'PostgreSQL'
    RS_CONFIG_HELP = 'load a configuration file (.cfg) to get the restorer ' \
                     'conditions'
    RS_DB_BACKUP_HELP = 'specifies the path of the backup\'s file ' \
                        '(database) which is going to be loaded and the ' \
                        'name of the PostgreSQL database which is going to ' \
                        'be generated, respectively'
    RS_CLUSTER_BACKUP_HELP = 'specifies the path of the backup\'s file ' \
                             '(cluster) which is going to be loaded'
    RS_CLUSTER_HELP = 'specifies whether the specified path is a ' \
                      'database\'s backup or a cluster\'s backup'

    TERMINATOR_HELP = 'TERMINATOR: terminates the specified connections to ' \
                      'PostgreSQL'
    T_CONFIG_HELP = 'load a configuration file (.cfg) to get the terminator ' \
                    'conditions'
    T_ALL_HELP = 'terminates every connection (except yours) to the host ' \
                 'which you are connected to'
    T_DB_NAME_HELP = 'terminates every connection (except yours) to the ' \
                     'specified PostgreSQL database'
    T_USER_HELP = 'terminates every connection of the specified user ' \
                  '(except if you are the specified user)'

    TRIMMER_HELP = 'TRIMMER: deletes (if necessary) a group of PostgreSQL ' \
                   'backups (cluster or databases) according to some ' \
                   'specified conditions'
    TR_CONFIG_HELP = 'load a configuration file (.cfg) to get the trimmer ' \
                     'conditions'
    TR_DB_NAME_HELP = 'trim the backups of a specified group of PostgreSQL ' \
                      'databases'
    TR_CLUSTER_HELP = 'trim the backups of the PostgreSQL cluster'
    TR_BKP_FOLDER_HELP = 'select the path of the folder to be trimmed. The ' \
                         'folder\'s name must be the group\'s name'
    TR_PREFIX_HELP = 'specify the prefix of the backups which are going to ' \
                     'be trimmed'
    TR_N_BACKUPS_HELP = 'specify the minimum number of backups of each ' \
                        'database to keep stored, regardless of the rest of ' \
                        'conditions'
    TR_EXPIRY_DAYS_HELP = 'specify the number of days which have to be ' \
                          'elapsed to consider a backup expired'
    TR_MAX_SIZE_HELP = 'when the size of a group of a database\'s backups ' \
                       'exceeds this maximum size, a message will be shown ' \
                       'to let the user know it'

    VACUUMER_HELP = 'VACUUMER: makes a vacuum of a specified group of ' \
                    'PostgreSQL databases'
    V_CONFIG_HELP = 'load a configuration file (.cfg) to get the vacuum ' \
                    'conditions'
    V_DB_NAME_HELP = 'specify the name/s of the PostgreSQL database/s to be ' \
                     'vacuumed'
    V_DB_OWNER_HELP = 'only if the user who is running the program is a ' \
                      'PostgreSQL superuser, this option allows him to play ' \
                      'other PostgreSQL role writting its username'
    V_TERMINATE_HELP = 'terminate every connection (except yours) to each ' \
                       'database which is going to be vacuumed'

    CONFIG_CONNECTION_HELP = 'load a configuration file (.cfg) to get the ' \
                             'PostgreSQL connection parameters'

    HOST_HELP = 'indicates the host you are going to connect to'

    PORT_HELP = 'indicates the port you are going to connect to'

    USER_HELP = 'indicates the PostgreSQL username with whom you are going ' \
                'to connect'

    CONFIG_LOGGER_HELP = 'load a configuration file (.cfg) to get the ' \
                         'logger parameters'

    LOGGER_LOGFILE_HELP = 'indicates the path of the file in which the ' \
                          'logger is going to store the log info'

    LOGGER_LEVEL_HELP = 'indicates the logger\'s verbosity level (debug, ' \
                        'info, warning, error, critical)'

    LOGGER_MUTE_HELP = 'indicates not to store anything'

    PROGRAM_INFO_ARGS_ERROR = 'cannot specify more parameters when using ' \
                              '[-i/--info]'
    PROGRAM_VERSION_ARGS_ERROR = 'cannot specify more parameters when using ' \
                                 '[-v/--version]'
    BACKER_ARGS_ERROR = 'insufficient parameters to work - [-C/--config | ' \
                        '-d/--db-name | -c/--cluster] must be specified'
    DROPPER_ARGS_ERROR = 'insufficient parameters to work - [-C/--config | ' \
                         '-d/--db-name] must be specified'
    INFORMER_ARGS_ERROR = 'insufficient parameters to work - ' \
                          '[-dc/--details-conns | -dd/--details-dbs | ' \
                          '-du/--details-users | -lc/--list-conns | ' \
                          '-ld/--list-dbs | -lu/--list-users | ' \
                          '-vpg/--version-pg | -vnpg/--version-num-pg | ' \
                          '-ts/--time-start | -tu/--time-up] must be ' \
                          'specified'
    REPLICATOR_ARGS_ERROR = 'insufficient parameters to work - ' \
                            '[-C/--config | -d/--db-name] must be specified'
    RESTORER_ARGS_ERROR = 'insufficient parameters to work - [-C/--config | ' \
                          '-d/--db-backup | (-c/--cluster & ' \
                          '-p/--cluster-backup)] must be specified'
    TERMINATOR_ARGS_ERROR = 'insufficient parameters to work - [-C/--config ' \
                            '| -a/--all | -d/--db-name | -u/--user] must be ' \
                            'specified'
    TRIMMER_ARGS_ERROR = 'insufficient parameters to work - [-C/--config | ' \
                         '(-f/--bkp-folder & (-d/--db-name | ' \
                         '-c/--cluster))] must be specified'
    TRIMMER_CONNECTION_ARGS_ERROR = 'connection parameters no needed to ' \
                                    'work with clusters\' trimmer'
    VACUUMER_ARGS_ERROR = 'insufficient parameters to work - [-C/--config ' \
                          '| -d/--db-name] must be specified'
    CONNECTION_ARGS_ERROR = 'insufficient connection parameters to work - ' \
                            '[-cC/--config-connection | (-ch/--host & ' \
                            '-cp/--port & -cu/--user)] must be specified'

    BEGINNING_EXE_DB_BACKER = 'INICIANDO EJECUCIÓN DE BACKER (BASES DE DATOS)'
    BEGINNING_EXE_CL_BACKER = 'INICIANDO EJECUCIÓN DE BACKER (CLÚSTER)'
    BEGINNING_EXE_DROPPER = 'INICIANDO EJECUCIÓN DE DROPPER'
    BEGINNING_EXE_INFORMER = 'INICIANDO EJECUCIÓN DE INFORMER'
    BEGINNING_EXE_REPLICATOR = 'INICIANDO EJECUCIÓN DE REPLICATOR'
    BEGINNING_EXE_DB_RESTORER = 'INICIANDO EJECUCIÓN DE RESTORER (BASES DE ' \
                                'DATOS)'
    BEGINNING_EXE_CL_RESTORER = 'INICIANDO EJECUCIÓN DE RESTORER (CLÚSTER)'
    BEGINNING_EXE_TERMINATOR = 'INICIANDO EJECUCIÓN DE TERMINATOR'
    BEGINNING_EXE_DB_TRIMMER = 'INICIANDO EJECUCIÓN DE TRIMMER (BASES DE ' \
                               'DATOS)'
    BEGINNING_EXE_CL_TRIMMER = 'INICIANDO EJECUCIÓN DE TRIMMER (CLÚSTER)'
    BEGINNING_EXE_VACUUMER = 'INICIANDO EJECUCIÓN DE VACUUMER'

    ACTIVE_CONNS_ERROR = 'No se pudo completar la operación, ya que hay ' \
                         'procesos en curso usando la base de datos ' \
                         '"{dbname}". Puede volver a intentarlo indicando ' \
                         'el argumento -t o terminando directamente los ' \
                         'procesos mencionados.'

    DB_BACKER_VARS_INTRO = 'VARIABLES DE BACKER (BASE DE DATOS):'
    DB_BACKER_VARS = 'SERVER: {server}, USER: {user}, PORT: {port}, ' \
                     'BKP_PATH: {bkp_path}, GROUP: {group}, BKP_TYPE: ' \
                     '{bkp_type}, PREFIX: {prefix}, IN_DBS: {in_dbs}, ' \
                     'IN_REGEX: {in_regex}, IN_PRIORITY: {in_priority}, ' \
                     'EX_DBS: {ex_dbs}, EX_REGEX: {ex_regex}, EX_TEMPLATES: ' \
                     '{ex_templates}, VACUUM: {vacuum}, DB_OWNER: {db_owner}.'
    CL_BACKER_VARS_INTRO = 'VARIABLES DE BACKER (CLÚSTER):'
    CL_BACKER_VARS = 'SERVER: {server}, USER: {user}, PORT: {port}, ' \
                     'BKP_PATH: {bkp_path}, GROUP: {group}, BKP_TYPE: ' \
                     '{bkp_type}, PREFIX: {prefix}, VACUUM: {vacuum}.'
    DROPPER_VARS_INTRO = 'VARIABLES DE DROPPER:'
    DROPPER_VARS = 'SERVER: {server}, USER: {user}, PORT: {port}, ' \
                   'DBNAMES: {dbnames}.'
    REPLICATOR_VARS_INTRO = 'VARIABLES DE REPLICATOR:'
    REPLICATOR_VARS = 'SERVER: {server}, USER: {user}, PORT: {port}, ' \
                      'ORIGINAL_DBNAME: {original_dbname}, NEW_DBNAME: ' \
                      '{new_dbname}.'
    DB_RESTORER_VARS_INTRO = 'VARIABLES DE RESTORER (BASE DE DATOS):'
    DB_RESTORER_VARS = 'SERVER: {server}, USER: {user}, PORT: {port}, ' \
                       'DB_BACKUP: {db_backup}, NEW_DBNAME: {new_dbname}.'
    CL_RESTORER_VARS_INTRO = 'VARIABLES DE RESTORER (CLÚSTER):'
    CL_RESTORER_VARS = 'SERVER: {server}, USER: {user}, PORT: {port}, ' \
                       'DB_BACKUP: {db_backup}, NEW_DBNAME: {new_dbname}.'
    TERMINATOR_VARS_INTRO = 'VARIABLES DE TERMINATOR:'
    TERMINATOR_VARS = 'SERVER: {server}, USER: {user}, PORT: {port}, ' \
                      'TARGET_ALL: {target_all}, TARGET_USER: ' \
                      '{target_user}, TARGET_DBS: {target_dbs}.'
    DB_TRIMMER_VARS_INTRO = 'VARIABLES DE TRIMMER (BASE DE DATOS):'
    DB_TRIMMER_VARS = 'BKP_PATH: {bkp_path}, PREFIX: {prefix}, IN_DBS: ' \
                      '{in_dbs}, IN_REGEX: {in_regex}, IN_PRIORITY: ' \
                      '{in_priority}, EX_DBS: {ex_dbs}, EX_REGEX: ' \
                      '{ex_regex},  MIN_N_BKPS: {min_n_bkps}, EXP_DAYS: ' \
                      '{exp_days}, MAX_SIZE: {max_size}, PG_WARNINGS: ' \
                      '{pg_warnings}.'
    CL_TRIMMER_VARS_INTRO = 'VARIABLES DE TRIMMER (CLÚSTER):'
    CL_TRIMMER_VARS = 'BKP_PATH: {bkp_path}, PREFIX: {prefix}, MIN_N_BKPS: ' \
                      '{min_n_bkps}, EXP_DAYS: {exp_days}, MAX_SIZE: ' \
                      '{max_size}, PG_WARNINGS: {pg_warnings}.'
    VACUUMER_VARS_INTRO = 'VARIABLES DE VACUUMER:'
    VACUUMER_VARS = 'SERVER: {server}, USER: {user}, PORT: {port}, ' \
                    'IN_DBS: {in_dbs}, IN_REGEX: {in_regex}, IN_PRIORITY: ' \
                    '{in_priority}, EX_DBS: {ex_dbs}, EX_REGEX: {ex_regex}, ' \
                    'EX_TEMPLATES: {ex_templates}, DB_OWNER: {db_owner}.'

    ACTION_DB_NO_SUPERUSER = 'El usuario especificado para la conexión a ' \
                             'PostgreSQL no tiene rol de superusuario: sólo ' \
                             'podrá actuar sobre las bases de datos de las ' \
                             'cuales es propietario.'
    ACTION_CL_NO_SUPERUSER = 'El usuario especificado para la conexión a ' \
                             'PostgreSQL no tiene rol de superusuario: no ' \
                             'puede actuar sobre el clúster de bases de datos.'
    DIR_DOES_NOT_EXIST = 'El directorio especificado en el archivo de ' \
                         'configuración no existe.'
    NO_FILE_IN_DIR = 'El directorio especificado en el archivo de ' \
                     'configuración está vacío.'
    NO_BACKUP_IN_DIR = 'El directorio especificado en el archivo de ' \
                       'configuración no contiene copias de seguridad ' \
                       'cuyos nombres sigan el patrón del programa.'
    BEGINNING_DB_TRIMMER = 'Iniciando limpieza de copias de seguridad de la ' \
                           'base de datos "{dbname}"...'
    DELETING_OBSOLETE_BACKUP = 'Copia de seguridad obsoleta: eliminando el ' \
                               'archivo "%s"...'
    NO_DB_BACKUP_DELETED = 'No se ha eliminado ninguna copia de la base de ' \
                           'datos "{dbname}".'
    DB_BKPS_SIZE_EXCEEDED = 'El tamaño del total de copias de seguridad en ' \
                            'disco de la base de datos {dbname} es de ' \
                            '{tsize_unit} {unit}, que es mayor que el ' \
                            'máximo especificado ({size} {unit}).'
    DB_TRIMMER_DONE = 'Limpieza de copias de seguridad de la base de ' \
                      'datos "{dbname}" completada (Duración del proceso: ' \
                      '{diff}).'
    BEGINNING_CL_TRIMMER = 'Iniciando limpieza de copias de seguridad del ' \
                           'clúster de PostgreSQL del servidor...'
    NO_CL_BACKUP_DELETED = 'No se ha eliminado ninguna copia del clúster ' \
                           'del servidor.'
    CL_BKPS_SIZE_EXCEEDED = 'El tamaño del total de copias de seguridad en ' \
                            'disco del clúster es de {tsize_unit} {unit}, ' \
                            'que es mayor que el máximo especificado ' \
                            '({size} {unit}).'
    CL_TRIMMER_DONE = 'Limpieza de copias de seguridad del clúster del ' \
                      'servidor completada (Duración del proceso: {diff}).'
    NO_CONNECTION_PARAMS = 'No se han especificado todos los parámetros ' \
                           'necesarios para la conexión a PostgreSQL.'
    CHECKING_BACKUP_DIR = 'Comprobando directorio de destino de las copias... '
    DESTINY_DIR = 'Directorio de destino: "{path}".'
    PROCESSING_DUMPER = 'Procesando copias de seguridad a realizar...'
    ALLOWING_DB_CONN = 'Habilitando conexiones a la base de datos...'
    DISALLOWING_DB_CONN = 'Deshabilitando conexiones a la base de datos...'
    PROCESSING_DB = 'Base de datos: "{dbname}".'
    PRE_VACUUMING_DB = 'Iniciando limpieza previa de la base de datos ' \
                       '"{dbname}"...'
    PRE_VACUUMING_DB_DONE = 'Limpieza previa de la base de datos "{dbname}" ' \
                            'completada.'
    PRE_VACUUMING_DB_FAIL = 'La limpieza previa de la base de datos ' \
                            '"{dbname}" no se pudo completar.'
    BEGINNING_DB_BACKER = 'Iniciando copia de seguridad de la base de datos ' \
                          '"{dbname}"...'
    DB_BACKER_DONE = 'Copia de seguridad de la base de datos "{dbname}" ' \
                     'completada (Duración del proceso: {diff}).'
    DB_BACKER_FAIL = 'La copia de seguridad de la base de datos "{dbname}" ' \
                     'no se pudo completar.'
    DBS_BACKER_DONE = 'Copias de seguridad finalizadas.'
    BEGINNING_CL_BACKER = 'Iniciando copia de seguridad de del clúster de ' \
                          'bases de datos...'
    CL_BACKER_DONE = 'Copia de seguridad del clúster de bases de datos ' \
                     'completada (Duración del proceso: {diff}).'
    CL_BACKER_FAIL = 'La copia de seguridad del clúster de bases de datos ' \
                     'no se pudo completar.'
    BEGINNING_VACUUMER = 'Iniciando limpieza de bases de datos...'
    VACUUMER_DONE = 'Limpieza de bases de datos completada.'
    VACUUMER_FAIL = 'La limpieza de bases de datos no se pudo completar.'
    DB_VACUUMER_DONE = 'Limpieza de la base de datos "{dbname}" completada ' \
                       '(Duración del proceso: {diff}).'
    DB_VACUUMER_FAIL = 'La limpieza de la base de datos "{dbname}" no se ' \
                       'pudo completar.'
    TERMINATE_USER_CONN_DONE = 'Conexiones del usuario "{target_user}" a ' \
                               'PostgreSQL terminadas.'
    TERMINATE_DB_CONN_DONE = 'Conexiones a la bases de datos ' \
                             '"{target_dbname}" terminadas.'
    TERMINATE_DBS_CONN_DONE = 'Conexiones a las bases de datos de ' \
                              'PostgreSQL especificadas terminadas.'
    TERMINATE_ALL_CONN_DONE = 'Conexiones a PostgreSQL terminadas con éxito.'
    TERMINATE_USER_CONN_FAIL = 'No fue posible terminar las conexiones del ' \
                               'usuario "{target_user}" a PostgreSQL.'
    TERMINATE_DB_CONN_FAIL = 'No fue posible terminar las conexiones a la ' \
                             'base de datos "{target_dbname}" de PostgreSQL.'
    TERMINATE_ALL_CONN_FAIL = 'No fue posible terminar las conexiones a ' \
                              'PostgreSQL.'
    NO_TERMINATE_PARAMS = 'No se han especificado todos los parámetros ' \
                          'necesarios para la terminación de conexiones a ' \
                          'PostgreSQL.'
    EMPTY_DB_LIST = 'Ninguna base de datos cumple los parámetros de ' \
                    'configuración especificados: no se realizará ninguna ' \
                    'operación.'
    SELECTED_DB = 'Base de datos seleccionada: "{dbname}".'
    SEARCHING_SELECTED_DBS = 'Analizando criterios de búsqueda...'
    EMPTY_DBNAME_LIST = 'Ninguna base de datos cumple los parámetros de ' \
                        'configuración especificados: no se realizará ' \
                        'ninguna limpieza de copias de seguridad.'
    BEGINNING_TERMINATE_USER_CONN = 'Terminando todas las conexiones del ' \
                                    'usuario "{target_user}" a PostgreSQL...'
    BEGINNING_TERMINATE_DBS_CONN = 'Terminando todas las conexiones a las ' \
                                   'bases de datos de PostgreSQL ' \
                                   'especificadas...'
    BEGINNING_TERMINATE_ALL_CONN = 'Terminando todas las conexiones a ' \
                                   'PostgreSQL...'

    NO_CONNS = 'Actualmente no hay ninguna conexión a PostgreSQL (a ' \
               'excepción de la suya).'
    NO_DB_CONNS = 'Actualmente no hay ninguna conexión a la base de datos ' \
                  '"{target_db}".'
    NO_USER_CONNS = 'Actualmente no hay ninguna conexión a PostgreSQL del ' \
                    'usuario "{target_user}".'
    TARGET_USER_IS_CURRENT_USER = 'Actualmente está conectado a PostgreSQL ' \
                                  'a través del usuario "{target_user}". No ' \
                                  'es posible terminar su propia conexión.'

    SHOWING_DBS_DATA = 'Información de las bases de datos de PostgreSQL'
    SHOWING_DBS_NAME = 'Bases de datos de PostgreSQL'
    NO_DB_DATA_TO_SHOW = 'No hay información disponible para las bases de ' \
                         'datos especificadas.'

    DATNAME = 'Datname:\t\t'
    OWNER = 'Owner:\t\t'
    ENCODING = 'Encoding:\t\t'
    DATSIZE = 'Size:\t\t'
    DATCOLLATE = 'Datcollate:\t'
    DATCTYPE = 'Datctype:\t\t'
    DATISTEMPLATE = 'Datistemplate:\t'
    DATALLOWCONN = 'Datallowconn:\t'
    DATCONNLIMIT = 'Datconnlimit:\t'
    DATLASTSYSOID = 'Datlastsysoid:\t'
    DATFROZENXID = 'Datfrozenxid:\t'
    DATTABLESPACE = 'Dattablespace:\t'
    DATACL = 'Datacl:\t\t'

    SHOWING_USERS_DATA = 'Información de los usuarios de PostgreSQL'
    SHOWING_USERS_NAME = 'Usuarios de PostgreSQL'
    NO_USER_DATA_TO_SHOW = 'No hay información disponible para los usuarios ' \
                           'especificados.'

    USENAME = 'Usename:\t\t'
    USESYSID = 'Usesysid:\t\t'
    USECREATEDB = 'Usecreatedb:\t'
    USESUPER = 'Usesuper:\t\t'
    USECATUPD = 'Usecatupd:\t'
    USEREPL = 'Userepl:\t\t'
    PASSWD = 'Passwd:\t\t'
    VALUNTIL = 'Valuntil:\t\t'
    USECONFIG = 'Useconfig:\t'

    SHOWING_CONNS_DATA = 'Información de las conexiones a PostgreSQL'
    SHOWING_CONNS_PID = 'PIDs de conexiones a PostgreSQL'
    NO_CONN_DATA_TO_SHOW = 'No hay información disponible para las ' \
                           'conexiones con el PID especificado.'

    PID = 'Pid:\t\t'
    PROCPID = 'Procpid:\t\t'
    DATID = 'Datid:\t\t'
    APPLICATION_NAME = 'Application_name:\t'
    CLIENT_ADDR = 'Client_addr:\t'
    CLIENT_HOSTNAME = 'Client_hostname:\t'
    CLIENT_PORT = 'Client_port:\t'
    BACKEND_START = 'Backend_start:\t'
    XACT_START = 'Xact_start:\t'
    QUERY_START = 'Query_start:\t'
    STATE_CHANGE = 'State_change:\t'
    WAITING = 'Waiting:\t\t'
    STATE = 'State:\t\t'
    QUERY = 'Query:\t\t'

    SHOWING_PG_VERSION = 'Versión de PostgreSQL'
    NO_PG_VERSION_TO_SHOW = 'No hay información acerca de la versión de ' \
                            'PostgreSQL.'

    SHOWING_PG_TIME_START = 'Fecha de inicio de ejecución de PostgreSQL'
    NO_PG_TIME_START_TO_SHOW = 'No hay información acerca de la fecha de ' \
                               'inicio de ejecución de PostgreSQL.'
    SHOWING_PG_TIME_UP = 'Tiempo que lleva PostgreSQL en marcha'
    NO_PG_TIME_UP_TO_SHOW = 'No hay información acerca del tiempo que ' \
                            'lleva PostgreSQL en marcha.'

    CONNECT_FAIL = 'Se produjo un error al realizar la conexión a ' \
                   'PostgreSQL. Por favor, revise que el servidor, puerto y ' \
                   'usuario especificados sean correctos.'
    DISCONNECT_FAIL = 'Se produjo un error al realizar la desconexión de ' \
                      'PostgreSQL.'
    GET_PG_VERSION_FAIL = 'Ha ocurrido un problema al recuperar la versión ' \
                          'de PostgreSQL.'
    GET_PG_TIME_START_FAIL = 'Ha ocurrido un problema al recuperar la ' \
                             'fecha de inicio de ejecución de PostgreSQL.'
    GET_PG_TIME_UP_FAIL = 'Ha ocurrido un problema al recuperar el tiempo ' \
                          'que lleva PostgreSQL ejecutándose.'
    GET_PG_DB_DATA = 'Ha ocurrido un problema al recuperar información de ' \
                     'la base de datos "{dbname}" de PostgreSQL.'
    GET_PG_USER_DATA = 'Ha ocurrido un problema al recuperar información ' \
                       'del usuario "{username}" de PostgreSQL.'
    GET_PG_CONN_DATA = 'Ha ocurrido un problema al recuperar información ' \
                       'del proceso {connpid} conectado a PostgreSQL.'
    GET_PG_DBNAMES_DATA = 'Ha ocurrido un problema al recuperar los nombres ' \
                          'de las bases de datos de PostgreSQL.'
    GET_PG_USERNAMES_DATA = 'Ha ocurrido un problema al recuperar los ' \
                            'nombres de los usuarios de PostgreSQL.'
    GET_PG_CONNPIDS_DATA = 'Ha ocurrido un problema al recuperar los ' \
                           'identificadores de procesos conectados a ' \
                           'PostgreSQL.'

    NO_NEW_DBNAME = 'No se ha especificado un nombre para la nueva base de ' \
                    'datos.'
    NO_ORIGINAL_DBNAME = 'No se ha especificado el nombre de la base de ' \
                         'datos que se desea clonar.'
    BEGINNING_REPLICATOR = 'Copiando la base de datos "{original_dbname}"...'
    REPLICATE_DB_DONE = 'Generada con éxito una copia "{new_dbname}" en ' \
                        'PostgreSQL de la base de datos "{original_dbname}" ' \
                        '(Duración del proceso: {diff}).'
    REPLICATE_DB_FAIL = 'No fue posible copiar la base de datos ' \
                        'especificada de PostgreSQL.'
    NO_DBS_TO_DROP = 'No se ha especificado ninguna base de datos para ' \
                     'eliminar en PostgreSQL.'
    BEGINNING_DROPPER = 'Eliminando bases de datos especificadas en ' \
                        'PostgreSQL...'
    DROP_DB_DONE = 'Eliminada base de datos "{dbname}" (Duración del ' \
                   'proceso: {diff}).'
    DROP_DB_FAIL = 'La base de datos "{dbname}" no se pudo eliminar.'
    DROP_DBS_DONE = 'Bases de datos especificadas eliminadas en PostgreSQL.'
    NO_BKP_TO_RESTORE = 'El archivo especificado que contiene la copia a ' \
                        'restaurar no existe.'
    NO_DBNAME_TO_RESTORE = 'No se ha especificado un nombre para la nueva ' \
                           'base de datos que se generará en PostgreSQL a ' \
                           'partir de la copia.'
    BEGINNING_DB_RESTORER = 'Restaurando la copia "{db_backup}" con el ' \
                            'nombre "{new_dbname}"...'
    WAIT_PLEASE = 'Esta operación puede llevar unos minutos, espere por ' \
                  'favor...'
    RESTORE_DB_DONE = 'Restaurada con éxito la copia "{db_backup}" en ' \
                      'PostgreSQL con el nombre "{new_dbname}" (Duración ' \
                      'del proceso: {diff}).'
    RESTORE_DB_FAIL = 'No fue posible restaurar la copia "{db_backup}" ' \
                      'especificada de PostgreSQL con el nombre ' \
                      '"{new_dbname}".'
    BEGINNING_CL_RESTORER = 'Restaurando la copia "{cluster_backup}"...'
    RESTORE_CL_DONE = 'Restaurada con éxito la copia "{cluster_backup}" en ' \
                      'PostgreSQL (Duración del proceso: {diff}).'
    RESTORE_CL_FAIL = 'No fue posible restaurar la copia "{cluster_backup}" ' \
                      'en PostgreSQL.'
    INVALID_IN_REGEX = 'La expresión regular para la inclusión de bases de ' \
                       'datos en la operación es incorrecta.'
    INVALID_EX_REGEX = 'La expresión regular para la exclusión de bases de ' \
                       'datos en la operación es incorrecta.'
    INVALID_IN_REGEX = 'La expresión regular para la inclusión de bases de ' \
                       'datos en la operación es incorrecta.'
    INVALID_EX_REGEX = 'La expresión regular para la exclusión de bases de ' \
                       'datos en la operación es incorrecta.'
    FORBIDDEN_DB_CONNECTION = 'Conexión no permitida a la base de datos ' \
                              '"{dbname}".'
    INVALID_IN_PRIORITY = 'El valor de la variable para determinar si las ' \
                          'condiciones de inclusión predominan sobre las de ' \
                          'exclusión en la operación es incorrecto.'
    INVALID_EX_TEMPLATES = 'El valor de la variable para determinar la ' \
                           'exclusión de plantillas en la operación es ' \
                           'incorrecto.'
    INVALID_VACUUM = 'El valor de la variable para determinar si se realiza ' \
                     'una limpieza de bases de datos previa a la operación ' \
                     'es incorrecto.'
    INVALID_BKP_TYPE = 'El formato de copia de seguridad establecido es ' \
                       'incorrecto.'
    INVALID_MIN_BKPS = 'El número mínimo establecido de copias de seguridad ' \
                       'a conservar es incorrecto.'
    INVALID_OBS_DAYS = 'El número de días transcurridos establecido para ' \
                       'considerar una copia de seguridad obsoleta es ' \
                       'incorrecto.'
    INVALID_MAX_TSIZE = 'El tamaño máximo total establecido del conjunto de ' \
                        'copias de seguridad de un determinado elemento es ' \
                        'incorrecto.'
    INVALID_PG_WARNINGS = 'El valor de la variable para activar mensajes ' \
                          'de aviso de PostgreSQL es incorrecto.'
    INVALID_TARGET_ALL = 'El valor de la variable para terminar todas las ' \
                         'conexiones a PostgreSQL es incorrecto.'
    INVALID_CFG_PATH = 'La ruta de alguno de los archivos de configuración ' \
                       'es incorrecta.'
    CONNECTER_CFG_DAMAGED = 'El archivo de configuración con los parámetros ' \
                            'de la conexión a PostgreSQL está dañado. Por ' \
                            'favor, revise que los nombres por defecto de ' \
                            'secciones y atributos son correctos.'
    DB_BACKER_CFG_DAMAGED = 'El archivo de configuración con las ' \
                            'condiciones para las copias de seguridad de ' \
                            'bases de datos en PostgreSQL está dañado. Por ' \
                            'favor, revise que los nombres por defecto de ' \
                            'secciones y atributos son correctos.'
    CL_BACKER_CFG_DAMAGED = 'El archivo de configuración con las ' \
                            'condiciones para las copias de seguridad del ' \
                            'clúster de PostgreSQL está dañado. Por favor, ' \
                            'revise que los nombres por defecto de ' \
                            'secciones y atributos son correctos.'
    DROPPER_CFG_DAMAGED = 'El archivo de configuración con las condiciones ' \
                          'para la eliminación de bases de datos en ' \
                          'PostgreSQL está dañado. Por favor, revise que ' \
                          'los nombres por defecto de secciones y atributos ' \
                          'son correctos.'
    REPLICATOR_CFG_DAMAGED = 'El archivo de configuración con las ' \
                             'condiciones para clonar una base de datos de ' \
                             'PostgreSQL está dañado. Por favor, revise que ' \
                             'los nombres por defecto de secciones y ' \
                             'atributos son correctos.'
    DB_RESTORER_CFG_DAMAGED = 'El archivo de configuración con las ' \
                              'condiciones para restaurar la copia de ' \
                              'seguridad de una base de datos en ' \
                              'PostgreSQL está dañado. Por favor, revise ' \
                              'que los nombres por defecto de secciones y ' \
                              'atributos son correctos.'
    CL_RESTORER_CFG_DAMAGED = 'El archivo de configuración con las ' \
                              'condiciones para restaurar la copia de ' \
                              'seguridad de un clúster de bases de datos ' \
                              'en PostgreSQL está dañado. Por favor, ' \
                              'revise que los nombres por defecto de ' \
                              'secciones y atributos son correctos.'
    TERMINATOR_CFG_DAMAGED = 'El archivo de configuración con las ' \
                             'condiciones para la finalización de ' \
                             'conexiones a PostgreSQL está dañado. Por ' \
                             'favor, revise que los nombres por defecto de ' \
                             'secciones y atributos son correctos.'
    DB_TRIMMER_CFG_DAMAGED = 'El archivo de configuración con las ' \
                             'condiciones para la limpieza de copias de ' \
                             'seguridad de bases de datos de PostgreSQL ' \
                             'está dañado. Por favor, revise que los ' \
                             'nombres por defecto de secciones y atributos ' \
                             'son correctos.'
    CL_TRIMMER_CFG_DAMAGED = 'El archivo de configuración con las ' \
                             'condiciones para la limpieza de copias de ' \
                             'seguridad de clústers de PostgreSQL está ' \
                             'dañado. Por favor, revise que los nombres por ' \
                             'defecto de secciones y atributos son correctos.'
    VACUUMER_CFG_DAMAGED = 'El archivo de configuración con las ' \
                           'condiciones para la limpieza de bases de datos ' \
                           'en PostgreSQL está dañado. Por favor, revise ' \
                           'que los nombres por defecto de secciones y ' \
                           'atributos son correctos.'
    LOGGER_CFG_DAMAGED = 'El archivo de configuración con los parámetros de ' \
                         'verbosidad de mensajes está dañado. Por favor, ' \
                         'revise que los nombres por defecto de secciones y ' \
                         'atributos son correctos.'
    NO_BACKUP_FOR_POSTGRESQL_DB = 'La base de datos "{dbname}" almacenada ' \
                                  'en PostgreSQL no tiene copias de ' \
                                  'seguridad en el directorio especificado ' \
                                  'en el archivo de configuración.'
    NO_POSTGRESQL_DB_FOR_BACKUP = 'La base de datos "{dbname}" tiene copias ' \
                                  'de seguridad en el directorio ' \
                                  'especificado en el archivo de ' \
                                  'configuración, pero no está almacenada ' \
                                  'en PostgreSQL .'
    ROOT_NOT_ALLOWED = 'Por seguridad, no se permite la ejecución del ' \
                       'programa como usuario "root".'
    USER_NOT_ALLOWED_TO_CHDIR = 'El programa no pudo generar directorios o ' \
                                'archivos necesarios para su ' \
                                'funcionamiento: revise los permisos de las ' \
                                'carpetas que emplea.'
    DB_ALREADY_EXISTS = 'La base de datos "{dbname}" ya existe en PostgreSQL.'
    NO_BACKUP_FORMAT = 'La copia de seguridad que se pretende restaurar no ' \
                       'sigue el formato estándar de nombres del programa.'
    ANALIZING_PG_DATA = 'Analizando datos en PostgreSQL...'
    DETECTED_DB = 'Detectada base de datos: "{dbname}".'
    DB_DOES_NOT_EXIST = 'La base de datos: "{dbname}" no existe en PostgreSQL.'

    def __init__(self):
        pass


class Default:

    BKP_PATH = '/opt/backups/pg_backups/'
    BKP_TYPE = 'dump'
    BKP_TYPES = ['dump', 'gz', 'bz2', 'zip']
    DB_BKPS_DIR = '/db_backups/'
    DB_OWNER = ''
    CL_BKPS_DIR = '/cl_backups/'
    EX_DBS = []
    EX_REGEX = ''
    EX_TEMPLATES = True
    EXP_DAYS = 365
    GROUP = 'default_group'
    IN_DBS = []
    IN_REGEX = ''
    IN_FORBIDDEN = False
    IN_PRIORITY = False
    LOG_LEVEL = 'debug'
    LOG_LEVELS = ['debug', 'info', 'warning', 'error', 'critical']
    MAX_SIZE = '10000MB'
    MIN_N_BKPS = 1
    MUTE = False
    PREFIX = ''
    RESTORING_TEMPLATE = 'template0'  # TODO: cambiar template0 por otra
    VACUUM = True
    VALID_BOOLS = ['True', 'true', 'False', 'false']
    VALID_EXP_DAYS = [-1, int]

    def __init__(self):
        pass


class Queries:

    ALLOW_CONN_TO_PG_DB = (
        'UPDATE pg_database '
        'SET datallowconn = TRUE '
        'WHERE datname = (%s);'
    )
    BACKEND_PG_ALL_EXISTS = (
        "SELECT 1 "
        "FROM pg_stat_activity "
        "WHERE {pg_pid} <> pg_backend_pid();"
    )
    BACKEND_PG_DB_EXISTS = (
        "SELECT 1 "
        "FROM pg_stat_activity "
        "WHERE datname = '{target_db}' "
        "AND {pg_pid} <> pg_backend_pid();"
    )
    BACKEND_PG_USER_EXISTS = (
        "SELECT 1 "
        "FROM pg_stat_activity "
        "WHERE usename = '{target_user}' "
        "AND usename <> CURRENT_USER;"
    )
    CLONE_PG_DB = (
        'CREATE DATABASE {dbname} '
        'WITH TEMPLATE {original_dbname} OWNER {user};'
    )
    DISALLOW_CONN_TO_PG_DB = (
        'UPDATE pg_database '
        'SET datallowconn = FALSE '
        'WHERE datname = (%s);'
    )
    DROP_PG_DB = (
        'DROP DATABASE {dbname};'
    )
    GET_CURRENT_PG_USER = (
        "SELECT CURRENT_USER;"
    )
    GET_PG_CONNPIDS = (
        'SELECT {pid} as pid '
        'FROM pg_stat_activity;'
    )
    GET_PG_DBNAMES = (
        'SELECT datname '
        'FROM pg_database;'
    )
    GET_PG_DBS = (
        'SELECT d.datname, d.datallowconn, '
        'pg_catalog.pg_get_userbyid(d.datdba) as owner '
        'FROM pg_catalog.pg_database d;'
    )
    GET_PG_DBS_BY_OWNER = (
        'SELECT d.datname, d.datallowconn, '
        'pg_catalog.pg_get_userbyid(d.datdba) as owner '
        'FROM pg_catalog.pg_database d '
        'WHERE pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
    )
    GET_PG_NO_TEMPLATE_DBNAMES = (
        'SELECT datname '
        'FROM pg_database '
        'WHERE not datistemplate;'
    )
    GET_PG_NO_TEMPLATE_DBS = (
        'SELECT d.datname, d.datallowconn, '
        'pg_catalog.pg_get_userbyid(d.datdba) as owner '
        'FROM pg_catalog.pg_database d '
        'WHERE not datistemplate;'
    )
    GET_PG_NO_TEMPLATE_DBS_BY_OWNER = (
        'SELECT d.datname, d.datallowconn, '
        'pg_catalog.pg_get_userbyid(d.datdba) as owner '
        'FROM pg_catalog.pg_database d '
        'WHERE not datistemplate '
        'AND pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
    )
    GET_PG_DB_DATA = (
        'SELECT datname, pg_get_userbyid(datdba) as owner, '
        'pg_encoding_to_char(encoding) as encoding, datcollate, datctype, '
        'datistemplate, datallowconn, datconnlimit, datlastsysoid, '
        'datfrozenxid, dattablespace, datacl, '
        'pg_size_pretty(pg_database_size(datname)) as size '
        'FROM pg_database '
        'WHERE datname = (%s);'
    )
    GET_PG_PRETTY_VERSION = (
        'select version();'
    )
    GET_PG_TIME_START = (
        'SELECT pg_postmaster_start_time();'
    )
    GET_PG_TIME_UP = (
        'SELECT now() - pg_postmaster_start_time();'
    )
    GET_PG_USERNAMES = (
        'SELECT usename '
        'FROM pg_user;'
    )
    GET_PG91_CONN_DATA = (
        'SELECT datid, datname, procpid, usesysid, usename, '
        'application_name, client_addr, client_hostname, client_port, '
        'backend_start, xact_start, query_start, waiting '
        'FROM pg_stat_activity '
        'WHERE procpid = (%s);'
    )
    GET_PG92_CONN_DATA = (
        'SELECT datid, datname, pid, usesysid, usename, application_name, '
        'client_addr, client_hostname, client_port, backend_start, '
        'xact_start, query_start, state_change, waiting, state, query '
        'FROM pg_stat_activity '
        'WHERE pid = (%s);'
    )
    GET_PG91_USER_DATA = (
        'SELECT usename, usesysid, usecreatedb, usesuper, usecatupd, '
        'passwd, valuntil, useconfig '
        'FROM pg_user '
        'WHERE usename = (%s);'
    )
    GET_PG92_USER_DATA = (
        'SELECT usename, usesysid, usecreatedb, usesuper, usecatupd, '
        'userepl, passwd, valuntil, useconfig '
        'FROM pg_user '
        'WHERE usename = (%s);'
    )
    IS_PG_SUPERUSER = (
        'SELECT usesuper '
        'FROM pg_user '
        'WHERE usename = CURRENT_USER;'
    )
    PG_DB_EXISTS = (
        'SELECT 1 '
        'FROM pg_database '
        'WHERE datname=(%s);'
    )
    TERMINATE_BACKEND_PG_ALL = (
        "SELECT pg_terminate_backend({pg_pid}) "
        "FROM pg_stat_activity "
        "WHERE {pg_pid} <> pg_backend_pid();"
    )
    TERMINATE_BACKEND_PG_DB = (
        "SELECT pg_terminate_backend({pg_pid}) "
        "FROM pg_stat_activity "
        "WHERE datname = '{target_db}' "
        "AND {pg_pid} <> pg_backend_pid();"
    )
    TERMINATE_BACKEND_PG_USER = (
        "SELECT pg_terminate_backend({pg_pid}) "
        "FROM pg_stat_activity "
        "WHERE usename = '{target_user}' "
        "AND usename <> CURRENT_USER;"
    )

    def __init__(self):
        pass
