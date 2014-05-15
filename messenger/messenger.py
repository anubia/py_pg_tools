#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


class Messenger:

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
                      'datos "{dbname}" completada.'
    BEGINNING_CL_TRIMMER = 'Iniciando limpieza de copias de seguridad del ' \
                           'clúster de PostgreSQL del servidor...'
    NO_CL_BACKUP_DELETED = 'No se ha eliminado ninguna copia del clúster ' \
                           'del servidor.'
    CL_BKPS_SIZE_EXCEEDED = 'El tamaño del total de copias de seguridad en ' \
                            'disco del clúster es de {tsize_unit} {unit}, ' \
                            'que es mayor que el máximo especificado ' \
                            '({size} {unit}).'
    CL_TRIMMER_DONE = 'Limpieza de copias de seguridad del clúster del ' \
                      'servidor completada.'
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
                     'completada.'
    DB_BACKER_FAIL = 'La copia de seguridad de la base de datos "{dbname}" ' \
                     'no se pudo completar.'
    DBS_BACKER_DONE = 'Copias de seguridad finalizadas.'
    BEGINNING_CL_BACKER = 'Iniciando copia de seguridad de del clúster de ' \
                          'bases de datos...'
    CL_BACKER_DONE = 'Copia de seguridad del clúster de bases de datos ' \
                     'completada.'
    CL_BACKER_FAIL = 'La copia de seguridad del clúster de bases de datos ' \
                     'no se pudo completar.'
    BEGINNING_VACUUMER = 'Iniciando limpieza de bases de datos...'
    VACUUMER_DONE = 'Limpieza de bases de datos completada.'
    VACUUMER_FAIL = 'La limpieza de bases de datos no se pudo completar.'
    DB_VACUUMER_DONE = 'Limpieza de la base de datos "{dbname}" completada.'
    DB_VACUUMER_FAIL = 'La limpieza de la base de datos "{dbname}" no se ' \
                       'pudo completar.'
    TERMINATE_USER_CONN_DONE = 'Conexiones del usuario "{target_user}" a ' \
                               'PostgreSQL terminadas con éxito.'
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
    SEARCHING_SELECTED_DBS_DATA = 'Analizando información de las bases de ' \
                                  'datos de PostgreSQL...'
    NO_DB_DATA_TO_SHOW = 'No hay información disponible para las bases de ' \
                         'datos especificadas.'
    DBNAME = 'Nombre: '
    DBENCODING = 'Codificación: '
    DBOWNER = 'Propietario: '
    SEARCHING_SELECTED_USERS_DATA = 'Analizando información de los usuarios ' \
                                    'de PostgreSQL...'
    NO_USER_DATA_TO_SHOW = 'No hay información disponible para los usuarios ' \
                           'especificados.'
    USERNAME = 'Nombre: '
    USERID = 'System ID: '
    SUPERUSER = 'Superusuario: '
    NO_NEW_DBNAME = 'No se ha especificado un nombre para la nueva base de ' \
                    'datos.'
    NO_ORIGINAL_DBNAME = 'No se ha especificado el nombre de la base de ' \
                         'datos que se desea clonar.'
    BEGINNING_REPLICATOR = 'Copiando la base de datos "{original_dbname}"...'
    REPLICATE_DB_DONE = 'Generada con éxito una copia "{new_dbname}" en ' \
                        'PostgreSQL de la base de datos "{original_dbname}".'
    REPLICATE_DB_FAIL = 'No fue posible copiar la base de datos ' \
                        'especificada de PostgreSQL.'
    NO_DBS_TO_DROP = 'No se ha especificado ninguna base de datos para ' \
                     'eliminar en PostgreSQL.'
    BEGINNING_DROPPER = 'Eliminando bases de datos especificadas en ' \
                        'PostgreSQL...'
    DROP_DB_DONE = 'Eliminada base de datos "{dbname}".'
    DROP_DB_FAIL = 'La base de datos "{dbname}" no se pudo eliminar.'
    DROP_DBS_DONE = 'Bases de datos especificadas eliminadas en PostgreSQL.'
    NO_BKP_TO_RESTORE = 'No se ha especificado la ruta del archivo que ' \
                        'contiene la copia a restaurar.'
    NO_DBNAME_TO_RESTORE = 'No se ha especificado un nombre para la nueva ' \
                           'base de datos que se generará en PostgreSQL a ' \
                           'partir de la copia.'
    BEGINNING_DB_RESTORER = 'Restaurando la copia "{db_backup}" con el ' \
                            'nombre "{new_dbname}"...'
    WAIT_PLEASE = 'Esta operación puede llevar unos minutos, espere por ' \
                  'favor...'
    RESTORE_DB_DONE = 'Restaurada con éxito la copia "{db_backup}" en ' \
                      'PostgreSQL con el nombre "{new_dbname}".'
    RESTORE_DB_FAIL = 'No fue posible restaurar la copia "{db_backup}" ' \
                      'especificada de PostgreSQL con el nombre ' \
                      '"{new_dbname}".'
    BEGINNING_CL_RESTORER = 'Restaurando la copia "{cluster_backup}"...'
    RESTORE_CL_DONE = 'Restaurada con éxito la copia "{cluster_backup}" en ' \
                      'PostgreSQL.'
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
    VACUUMER_CFG_DAMAGED = 'El archivo de configuración con las ' \
                           'condiciones para la limpieza de bases de datos ' \
                           'en PostgreSQL está dañado. Por favor, revise ' \
                           'que los nombres por defecto de secciones y ' \
                           'atributos son correctos.'
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
    TERMINATOR_CFG_DAMAGED = 'El archivo de configuración con las ' \
                             'condiciones para la finalización de ' \
                             'conexiones a PostgreSQL está dañado. Por ' \
                             'favor, revise que los nombres por defecto de ' \
                             'secciones y atributos son correctos.'
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
    VACUUM = True
    VALID_BOOLS = ['True', 'true', 'False', 'false']
    VALID_EXP_DAYS = [-1, int]

    def __init__(self):
        pass
