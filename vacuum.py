#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger de la librería personalizada
# logger.logger (para utilizar un logger que muestre información al usuario)
from logger.logger import create_logger, logger_colored
# Importar la funciones pg_connect y pg_disconnect de la librería
# personalizada pg_connection.pg_connection (para conectarse y desconectarse a
# PostgreSQL y poder ejecutar consultas)
from pg_connection.pg_connection import pg_connect, pg_disconnect
from pg_tools.pg_tools import is_pg_superuser, get_cursor_dbs, allow_db_conn, \
    disallow_db_conn
# Importar la función default_cfg_path de la librería personalizada
# dir_tools.dir_tools (para obtener la ruta del archivo de configuración por
# defecto)
from dir_tools.dir_tools import default_cfg_path
# Importar la función load_vacuum de la librería personalizada
# config.config_tools (para obtener datos del archivo config)
from config.config_tools import load_vacuum
# Importar la función get_dbs_to_bkp de la librería personalizada
# db_selector.db_selector (para filtrar listados de bases de datos)
from db_selector.db_selector import get_dbs_to_bkp
# Importar la librería subprocess (para realizar consultas a las bases de datos
# de PostgreSQL)
import subprocess
# Importar la librería argparse (para trabajar con el vector argv fácilmente)
import argparse


# ************************* DEFINICIÓN DE FUNCIONES *************************

def vacuum_db(logger, dbname, user, server='localhost', port=5432):
    '''
Objetivo:
    - crear una copia de seguridad de la base de datos especificada.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - dbname: nombre de la base de datos de la que se quiere realizar una
    copia de seguridad.
    - user: usuario de PostgreSQL.
    - server: servidor donde se se encuentra alojada la bases de datos que se
    quiere copiar.
    - port: puerto por el que se realiza la conexión.
'''
    success = True
    # Almacenar la instrucción a realizar en consola
    command = 'vacuumdb {} -U {} -h {} -p {}'.format(dbname, user, server,
                                                     port)
    try:  # Probar que la copia se realiza correctamente
        # Ejecutar la instrucción de la copia de seguridad en consola
        result = subprocess.call(command, shell=True)
        if result != 0:  # Si el comando no de resultados en consola...
            raise Exception()  # Lanzar excepción
    except Exception as e:
        logger.debug('Error en la función "vacuum_db": {}.'.format(str(e)))
        success = False
    return success


def make_vacuum(logger, conn, cursor, dbs_all, bkp_vars):
    '''
Objetivo:
    - crear copias de seguridad de las bases de datos especificadas, las que
    están incluidas en la variable "dbs_all".
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - conn: conexión realizada desde el script a PostgreSQL
    - cursor: cursor de la conexión para permitir realizar operaciones y
    consultas a las bases de datos de PostgreSQL
    - dbs_all: una lista con todos los nombres de las bases de datos de
    PostgreSQL de las que se desea hacer una copia de seguridad (vienen dadas
    por el archivo de configuración).
    - bkp_vars: diccionario con los parámetros especificados en el archivo .cfg
'''
    message = 'Procesando bases de datos a limpiar...'
    logger_colored(logger, 'info', message, 'white')
    for db in dbs_all:  # Para cada base de datos de la que se quiere backup...
        dbname = db['name']  # Almacenar nombre de la BD por claridad
        mod_allow_conn = False  # En principio no se modifica datallowconn
        # Si se exigen copias de bases de datos sin permisos de conexión...
        if not db['allow_connection'] and bkp_vars['in_forbidden']:
            allow_db_conn(conn, cursor, dbname)  # Permitir conexiones
            mod_allow_conn = True  # Marcar que se modifica datallowconn
            logger.info('Habilitando conexiones a la base de datos...')
        logger.info('Iniciando limpieza de la base de datos '
                    '"{}"...'.format(dbname))
        # Realizar copia de seguridad de la base de datos
        success = vacuum_db(logger, dbname, bkp_vars['user'],
                            bkp_vars['server'], bkp_vars['port'])
        if mod_allow_conn:  # Si se modificó datallowconn...
            # Deshabilitar nuevamente las conexiones y dejarlo como estaba
            disallow_db_conn(conn, cursor, dbname)
            logger.info('Deshabilitando conexiones a la base de datos...')
        if success:
            message = 'Limpieza de la base de datos "{}" completada.'.format(
                dbname)
            logger_colored(logger, 'info', message, 'green')
        else:
            message = 'La limpieza de la base de datos "{}" no se pudo ' \
                      'completar.'.format(dbname)
            logger_colored(logger, 'warning', message, 'yellow', effect='bold')
    message = 'Limpieza de bases de datos finalizada.'
    logger_colored(logger, 'info', message, 'green')


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

     # Crear un logger para los mensajes de información
    logger = create_logger()

    # Asignar ruta por defecto al archivo de configuración
    cfg_path = default_cfg_path('vacuum/vacuum.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    parser.add_argument('-c', '--config',
                        help='load a configuration file (.cfg)',
                        default=cfg_path)
    args = parser.parse_args()  # Guardar los parámetros creados

    # Cargar variables del archivo .cfg
    bkp_vars = load_vacuum(logger, args.config)

    # Iniciar conexión a la base de datos "template1" con el usuario
    # especificado
    conn = pg_connect(logger, bkp_vars['server'], bkp_vars['user'],
                      bkp_vars['pwd'], bkp_vars['port'])
    # Inicializar un cursor para realizar operaciones en la base de datos
    cursor = conn.cursor()

    # Comprobar si el usuario actualmente conectado es superusuario de
    # PostgreSQL
    pg_superuser = is_pg_superuser(cursor)
    if not pg_superuser:  # Si no es superusuario de PostgreSQL...
        # Sólo puede manipular las BDs de las que es propietario
        bkp_vars['db_owner'] = bkp_vars['user']
        logger.warning('El usuario especificado para la conexión a PostgreSQL '
                       'no tiene rol de superusuario: sólo podrá actuar sobre '
                       'las bases de datos de las cuales es propietario.')

    # Ejecutar consulta de PostgreSQL y obtener nombres de todas las bases de
    # datos almacenadas, sus permisos de conexión y sus propietarios
    cursor = get_cursor_dbs(cursor, bkp_vars['ex_templates'],
                            bkp_vars['db_owner'])

    dbs_all = []  # Inicializar lista de nombres de las bases de datos
    for record in cursor:  # Para cada registro de la consulta...
        dictionary = {  # Crear diccionario con...
            'name': record[0],  # Nombre de la base de datos
            'allow_connection': record[1],  # Permiso de conexión
            'owner': record[2],  # Propietario de la base de datos
        }
        dbs_all.append(dictionary)  # Añadir diccionario a la lista de BDs

    message = 'Analizando datos en PostgreSQL... Detectadas las siguientes ' \
              'bases de datos: '
    for db in dbs_all:  # Para cada BD en PostgreSQL...
        if db is dbs_all[-1]:
            message += '"{}".'.format(db['name'])
            break
        message += '"{}", '.format(db['name'])
    logger_colored(logger, 'info', message, 'white')

    # Almacenar las bases de datos de las que se realizará una copia de
    # seguridad
    vacuum_list = get_dbs_to_bkp(logger, dbs_all, bkp_vars)

    # Realizar las nuevas copias de seguridad (dump)
    make_vacuum(logger, conn, cursor, vacuum_list, bkp_vars)

    # Cerrar comunicación con la base de datos
    pg_disconnect(logger, conn, cursor)
