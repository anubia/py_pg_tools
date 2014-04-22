#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y fatal_logger de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import Logger
# Importar la librería psycopg2 (para realizar consultas a PostgreSQL)
import psycopg2


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Connection:

    conn = None
    cursor = None
    server = None
    user = None
    pwd = None
    port = None
    logger = None

    def __init__(self, server, user, pwd, port, logger=None):
        '''
    Objetivo:
        - realizar una conexión a PostgreSQL con los parámetros especificados.
    Parámetros:
        - server: servidor donde está alojado PostgreSQL.
        - user: usuario de PostgreSQL con el que se realiza la conexión.
        - pwd: contraseña del usuario de PostgreSQL con el que se realiza la
        conexión.
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
        self.pwd = pwd
        self.port = port

        try:  # Probar si hay excepciones en...
            # Realizar la conexión a PostgreSQL con parámetros especificados
            self.conn = psycopg2.connect(host=self.server,
                                         database='template1', user=self.user,
                                         password=self.pwd, port=self.port)
            self.cursor = self.conn.cursor()
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "pg_connect": {}.'.format(
                str(e)))
            self.logger.stop_exe('Error de conexión a PostgreSQL.')

    def __get_pid_str(self):
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
        pg_pid = 'procpid' if pg_version < 90200 else 'pid'
        # Devolver el nombre del atributo que se emplea realmente
        return pg_pid

    def __kill_connections(self):
        '''
    Objetivo:
        - eliminar todas las conexiones a PostgreSQL del usuario.
    '''
        sql = ('SELECT pg_terminate_backend({pg_pid}) '
               'FROM pg_stat_activity '
               'WHERE {pg_pid} <> pg_backend_pid();')
        try:  # Probar si hay excepciones en...
            # Obtener el nombre de la variable que indica el pg_pid según la
            # versión de PostgreSQL
            pg_pid = self.__get_pid_str()
            sql = sql.format(pg_pid=pg_pid)
            self.cursor.execute(sql)  # Ejecutar consulta
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "kill_connections": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe('Error al eliminar conexiones a PostgreSQL.')

    def pg_disconnect(self):
        '''
    Objetivo:
        - desconectarse de PostgreSQL.
    '''
        try:  # Probar si hay excepciones en...
            #self.__kill_connections()  # Eliminar todas las conexiones
            self.cursor.close()  # Cerrar cursor de la conexión
            self.conn.close()  # Cerrar comunicación con la base de datos
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "pg_disconnect": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe('Error al desconectarse de PostgreSQL.')

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
        return(row[0])

    def get_cursor_dbs(self, ex_templates=True, db_owner=''):
        '''
    Objetivo:
        - realizar una consulta a PostgreSQL para devolver un cursor que
        contiene la lista de bases de datos correspondiente a los parámetros
        del archivo de configuración.
    Parámetros:
        - ex_templates: indica si se deben ignorar las bases de datos que sean
        plantillas en PostgreSQL.
        - db_owner: indica el propietario que deben tener las bases de datos
        que se desean obtener. Si el propietario es nulo, se obtienen todas las
        bases de datos que hay en PostgreSQL.
    Devolución:
        - un booleano, True si la conexión establecida es como superusuario,
        False de lo contrario.
    '''
        query_get_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) '
            'FROM pg_catalog.pg_database d;'
        )
        query_get_ex_template_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) '
            'FROM pg_catalog.pg_database d '
            'WHERE not datistemplate;'
        )
        query_get_owner_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) '
            'FROM pg_catalog.pg_database d '
            'WHERE pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
        )
        query_get_ex_template_owner_dbs = (
            'SELECT d.datname, d.datallowconn, '
            'pg_catalog.pg_get_userbyid(d.datdba) '
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
