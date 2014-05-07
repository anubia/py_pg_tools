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
                            '{tsize_mb} MB, que es mayor que el máximo ' \
                            'especificado ({max_tsize_mb} MB).'
    DB_TRIMMER_DONE = 'Limpieza de copias de seguridad de la base de ' \
                      'datos "{dbname}" completada.'
    BEGINNING_CL_TRIMMER = 'Iniciando limpieza de copias de seguridad del ' \
                           'clúster de PostgreSQL del servidor...'
    NO_CL_BACKUP_DELETED = 'No se ha eliminado ninguna copia del clúster ' \
                           'del servidor.'
    CL_BKPS_SIZE_EXCEEDED = 'El tamaño del total de copias de seguridad en ' \
                            'disco del clúster es de {tsize_mb} MB, que es ' \
                            'mayor que el máximo especificado ' \
                            '({max_tsize_mb} MB).'
    CL_TRIMMER_DONE = 'Limpieza de copias de seguridad del clúster del ' \
                      'servidor completada.'
    NO_CONNECTION_PARAMS = 'No se han especificado todos los parámetros ' \
                           'necesarios para la conexión a PostgreSQL.'
    CHECKING_BACKUP_DIR = 'Comprobando directorio de destino de las copias... '
    DIR_EXISTS = 'Directorio de destino existente.'
    PROCESSING_DUMPER = 'Procesando copias de seguridad a realizar...'
    ALLOWING_DB_CONN = 'Habilitando conexiones a la base de datos...'
    DISALLOWING_DB_CONN = 'Deshabilitando conexiones a la base de datos...'
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
                    'configuración especificados : no se realizará ' \
                    'ninguna copia de seguridad.'
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

    def __init__(self):
        pass


class Default:

    BKP_PATH = '/opt/backups/pg_backups/'
    SERVER_ALIAS = 'my_server'
    BKP_TYPE = '.dump'
    PREFIX = ''
    IN_DBS = []
    IN_REGEX = ''
    IN_FORBIDDEN = False
    IN_PRIORITY = False
    EX_DBS = []
    EX_REGEX = ''
    EX_TEMPLATES = True
    VACUUM = True
    DB_OWNER = ''

    def __init__(self):
        pass
