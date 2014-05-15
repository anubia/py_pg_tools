#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y fatal_logger de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import Logger
# Importar la librería psycopg2 (para realizar consultas a PostgreSQL)
import psycopg2
import psycopg2.extras
from casting.casting import Casting
from checker.checker import Checker
from messenger.messenger import Messenger


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Connecter:

    conn = None
    cursor = None
    server = None
    user = None
    pwd = None
    port = None
    logger = None

    PG_PID_VERSION_THRESHOLD = 90200
    pg_pid_91 = 'procpid'  # Name for PostgreSQL PID variable till version 9.1
    pg_pid_92 = 'pid'  # Name for PostgreSQL PID variable since version 9.2

    def __init__(self, server, user, port, logger=None):
        '''
    Objetivo:
        - realizar una conexión a PostgreSQL con los parámetros especificados.
    Parámetros:
        - server: servidor donde está alojado PostgreSQL.
        - user: usuario de PostgreSQL con el que se realiza la conexión.
        - port: puerto por el que se realizala conexión a PostgreSQL.
    Devolución:
        - el resultado de la conexión.
    '''
        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        self.server = server

        self.user = user

        if isinstance(port, int):
            self.port = port
        elif Checker.str_is_int(port):
            self.port = Casting.str_to_int(port)
        else:
            self.logger.stop_exe(Messenger.INVALID_PORT)

        try:  # Probar si hay excepciones en...
            # Realizar la conexión a PostgreSQL con parámetros especificados
            self.conn = psycopg2.connect(host=self.server,
                                         database='postgres', user=self.user,
                                         port=self.port)  # password=self.pwd,
            # TODO: añadir argumento password a psycopg2.connect en caso de que
            # en futuro se quisiese añadir la opción de introducir contraseña
            # manualmente en vez de revisar .pgpass
            self.cursor = self.conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "pg_connect": {}.'.format(
                str(e)))
            self.logger.stop_exe('Error de conexión a PostgreSQL.')

    def pg_disconnect(self):
        '''
    Objetivo:
        - desconectarse de PostgreSQL.
    '''
        try:  # Probar si hay excepciones en...
            self.cursor.close()  # Cerrar cursor de la conexión
            self.conn.close()  # Cerrar comunicación con la base de datos
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "pg_disconnect": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe('Error al desconectarse de PostgreSQL.')

    def get_pid_str(self):
        '''
    Objetivo:
        - comprobar la versión de PostgreSQL a la que se realiza la conexión y
        devolver el nombre del de la variable que representa el id del proceso
        en PostgreSQL, según la versión de éste último. Antes de la versión 9.2
        se empleaba "procpid", posteriormente pasó a llamarse "pid".
    Devolución:
        - el nombre del atributo del id del proceso que se está empleando en la
        versión de PostgreSQL a la que se realiza la conexión.
    '''
        pg_version = self.conn.server_version  # Obtener versión de PostgreSQL
        # Asignar nombre del atributo según la versión de PostgreSQL
        if pg_version < self.PG_PID_VERSION_THRESHOLD:
            return self.pg_pid_91
        else:
            return self.pg_pid_92

    def is_pg_superuser(self):
        '''
    Objetivo:
        - comprobar si el usuario actualmente conectado a PostgreSQL es
        superusuario.
    Devolución:
        - un booleano, True si la conexión establecida es como superusuario,
        False de lo contrario.
    '''
        query_is_superuser = (
            'SELECT usesuper '
            'FROM pg_user '
            'WHERE usename = CURRENT_USER;'
        )
        self.cursor.execute(query_is_superuser)
        row = self.cursor.fetchone()
        return(row['usesuper'])  # return(row[0])

    def get_cursor_dbs(self, ex_templates=True, db_owner=''):
        '''
        Objetivo:
            - realizar una consulta a PostgreSQL para devolver un cursor que
            contiene la lista de bases de datos correspondiente a los
            parámetros del archivo de configuración.
        Parámetros:
            - ex_templates: indica si se deben ignorar las bases de datos que
            sean plantillas en PostgreSQL.
            - db_owner: indica el propietario que deben tener las bases de
            datos que se desean obtener. Si el propietario es nulo, se obtienen
            todas las bases de datos que hay en PostgreSQL.
        Devolución:
            - un booleano, True si la conexión establecida es como
            superusuario, False de lo contrario.
        '''
        query_get_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d;'
        )
        query_get_ex_template_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d '
            'WHERE not datistemplate;'
        )
        query_get_owner_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d '
            'WHERE pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
        )
        query_get_ex_template_owner_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) as owner '
            'FROM pg_catalog.pg_database d '
            'WHERE not datistemplate '
            'AND pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
        )

        # Obtener todas BDs (que no sean templates) de un propietario concreto
        if db_owner and ex_templates:
            self.cursor.execute(query_get_ex_template_owner_dbs, (db_owner, ))
        # Obtener todas BDs (templates incluidas) de un propietario concreto
        elif db_owner and ex_templates is False:
            self.cursor.execute(query_get_owner_dbs, (db_owner, ))
        # Obtener todas BDs (que no sean templates) de PostgreSQL
        elif not db_owner and ex_templates is False:
            self.cursor.execute(query_get_dbs)
        else:  # Obtener todas BDs (templates incluidas) de PostgreSQL
            self.cursor.execute(query_get_ex_template_dbs)

    def allow_db_conn(self, dbname):
        '''
    Objetivo:
        - habilitar las conexiones a una base de datos determinada.
    Parámetros:
        - dbname: el nombre de la base de datos a la que se modifica su
        atributo "datallowconn" para habilitar conexiones.
    '''
        query_db_allow_conn = (
            'UPDATE pg_database '
            'SET datallowconn = TRUE '
            'WHERE datname = (%s);'
        )
        # Habilitar conexiones para esta base de datos
        self.cursor.execute(query_db_allow_conn, (dbname, ))
        self.conn.commit()  # Hacer los cambios permanentes

    def disallow_db_conn(self, dbname):
        '''
    Objetivo:
        - deshabilitar las conexiones a una base de datos determinada.
    Parámetros:
        - dbname: el nombre de la base de datos a la que se modifica su
        atributo "datallowconn" para deshabilitar conexiones.
    '''
        query_db_disallow_conn = (
            'UPDATE pg_database '
            'SET datallowconn = FALSE '
            'WHERE datname = (%s);'
        )
        self.cursor.execute(query_db_disallow_conn, (dbname, ))
        # Deshabilitar conexiones para esta base de datos
        self.conn.commit()  # Hacer los cambios permanentes
