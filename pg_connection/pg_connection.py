#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y logger_fatal de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import logger_fatal
# Importar la librería psycopg2 (para realizar consultas a PostgreSQL)
import psycopg2


# ************************* DEFINICIÓN DE FUNCIONES *************************

def pg_connect(logger, server, user, pwd, port):
    '''
Objetivo:
    - realizar una conexión a PostgreSQL con los parámetros especificados.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - server: servidor donde está alojado PostgreSQL.
    - user: usuario de PostgreSQL con el que se realiza la conexión.
    - pwd: contraseña del usuario de PostgreSQL con el que se realiza la
    conexión.
    - port: puerto por el que se realizala conexión a PostgreSQL.
Devolución:
    - el resultado de la conexión.
'''
    try:  # Probar si hay excepciones en...
        # Realizar la conexión a PostgreSQL con los parámetros especificados
        conn = psycopg2.connect(host=server, database='template1', user=user,
                                password=pwd, port=port)
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "pg_connect": {}.'.format(str(e)))
        logger_fatal(logger, 'Error de conexión a PostgreSQL.')
    return conn  # Devolver el resultado de la conexión


def get_pid_str(conn):
    '''
Objetivo:
    - comprobar la versión de PostgreSQL a la que se realiza la conexión y
    devolver el nombre del de la variable que representa el id del proceso en
    PostgreSQL, según la versión de éste último. Antes de la versión 9.2 se
    empleaba "procpid", posteriormente pasó a llamarse "pid".
Parámetros:
    - conn: variable que representa la conexión a PostgreSQL.
Devolución:
    - el nombre del atributo del id del proceso que se está empleando en la
    versión de PostgreSQL a la que se realiza la conexión.
'''
    pg_version = conn.server_version  # Obtener versión de PostgreSQL
    # Asignar nombre del atributo según la versión de PostgreSQL
    pg_pid = 'procpid' if pg_version < 90200 else 'pid'
    return pg_pid  # Devolver el nombre del atributo que se emplea realmente


def kill_connections(logger, conn, cursor):
    '''
Objetivo:
    - eliminar todas las conexiones a PostgreSQL del usuario.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - conn: variable que representa la conexión a PostgreSQL.
    - cursor: cursor para las consultas de la conexión a PostgreSQL.
'''
    sql = ('SELECT pg_terminate_backend({pg_pid}) '
           'FROM pg_stat_activity '
           'WHERE {pg_pid} <> pg_backend_pid();')
    try:  # Probar si hay excepciones en...
        # Obtener el nombre de la variable que indica el pg_pid según la
        # versión de PostgreSQL
        pg_pid = get_pid_str(conn=conn)
        sql = sql.format(pg_pid=pg_pid)
        cursor.execute(sql)  # Ejecutar consulta
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "kill_connections": {}.'.format(
            str(e)))
        logger_fatal(logger, 'Error al eliminar conexiones a PostgreSQL.')


def pg_disconnect(logger, conn, cursor):
    '''
Objetivo:
    - desconectarse de PostgreSQL.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - conn: variable que representa la conexión a PostgreSQL.
    - cursor: cursor para las consultas de la conexión a PostgreSQL.
'''
    try:  # Probar si hay excepciones en...
        kill_connections(logger, conn, cursor)  # Eliminar todas las conexiones
        cursor.close()  # Cerrar cursor de la conexión
        conn.close()  # Cerrar comunicación con la base de datos
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "pg_disconnect": {}.'.format(str(e)))
        logger_fatal(logger, 'Error al desconectarse de PostgreSQL.')
