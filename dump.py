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
# Importar las funciones create_dir, default_bkps_path, default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para crear directorios de forma
# automática y localizar archivos creados por defecto)
from dir_tools.dir_tools import create_dir, default_bkps_path, default_cfg_path
# Importar la función get_date de la librería personalizada
# date_tools.date_tools (para obtener la fecha y hora actuales de la zona en
# el formato deseado)
from date_tools.date_tools import get_date, get_year
# Importar la función load_dump de la librería personalizada
# config.config_tools (para obtener datos del archivo config)
from config.config_tools import load_dump
# Importar la función get_dbs_to_bkp de la librería personalizada
# db_selector.db_selector (para filtrar listados de bases de datos)
from db_selector.db_selector import get_dbs_to_bkp
# Importar la función vacuum_db de la librería vacuum (para realizar limpiezas
# de bases de datos previas a sus copias)
from vacuum import vacuum_db
# Importar la librería subprocess (para realizar consultas a las bases de datos
# de PostgreSQL)
import subprocess
# Importar la librería argparse (para trabajar con el vector argv fácilmente)
import argparse


# ************************* DEFINICIÓN DE FUNCIONES *************************

def dump_db(logger, bkps_dir, ext, dbname, user, prefix='', server='localhost',
            port=5432):
    '''
Objetivo:
    - crear una copia de seguridad de la base de datos especificada.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - bkps_dir: directorio donde se guardan las copias de seguridad.
    - ext: tipo de extensión que tendrá el archivo que contiene la copia.
    - dbname: nombre de la base de datos de la que se quiere realizar una
    copia de seguridad.
    - user: usuario de PostgreSQL.
    - prefix: prefijo a incluir en el nombre de las copias de seguridad.
    - server: servidor donde se se encuentra alojada la bases de datos que se
    quiere copiar.
    - port: puerto por el que se realiza la conexión.
'''
    success = True
    init_ts = get_date()  # Obtener fecha y hora actuales de la zona
    year = str(get_year(init_ts))  # Obtener el año de la fecha almacenada
    bkp_dir = bkps_dir + year + '/'
    create_dir(logger, bkp_dir)
    # Establecer nombre del archivo que contiene la copia de seguridad
    file_name = prefix + 'db_' + dbname + '_' + init_ts + ext
    # Almacenar la instrucción a realizar en consola
    if ext == '.gz':  # Comprimir con gzip
        command = 'pg_dump {} -Fp -U {} -h {} -p {} | gzip > {}'.format(
            dbname, user, server, port, bkp_dir + file_name)
    elif ext == '.bz2':  # Comprimir con bzip2
        command = 'pg_dump {} -Fp -U {} -h {} -p {} | bzip2 > {}'.format(
            dbname, user, server, port, bkp_dir + file_name)
    elif ext == '.zip':  # Comprimir con zip
        command = 'pg_dump {} -Fp -U {} -h {} -p {} | zip > {}'.format(
            dbname, user, server, port, bkp_dir + file_name)
    else:  # No comprimir la copia
        command = 'pg_dump {} -Fp -U {} -h {} -p {} > {}'.format(
            dbname, user, server, port, bkp_dir + file_name)
    try:  # Probar que la copia se realiza correctamente
        # Ejecutar la instrucción de la copia de seguridad en consola
        result = subprocess.call(command, shell=True)
        if result != 0:  # Si el comando no de resultados en consola...
            raise Exception()  # Lanzar excepción
    except Exception as e:
        logger.debug('Error en la función "dump_db": {}.'.format(str(e)))
        success = False
    return success


def make_bkps(logger, conn, cursor, dbs_all, bkp_dir, bkp_vars):
    '''
Objetivo:
    - crear copias de seguridad de las bases de datos especificadas, las que
    están incluidas en la variable "dbs_all".
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - conn: conexión realizada desde el script a PostgreSQL.
    - cursor: cursor de la conexión para permitir realizar operaciones y
    consultas a las bases de datos de PostgreSQL.
    - dbs_all: una lista con todos los nombres de las bases de datos de
    PostgreSQL de las que se desea hacer una copia de seguridad (vienen dadas
    por el archivo de configuración).
    - bkp_dir: directorio donde se guardan las copias de seguridad.
    - bkp_vars: diccionario con los parámetros especificados en el archivo .cfg
'''
    message = 'Comprobando directorio de destino de las copias... '
    bkps_dir = bkp_dir + bkp_vars['server_alias'] + '/dump/'
    create_dir(logger, bkps_dir)
    message += 'Directorio de destino existente.'
    logger_colored(logger, 'info', message, 'white')
    message = 'Procesando copias de seguridad a realizar...'
    logger_colored(logger, 'info', message, 'white')
    for db in dbs_all:  # Para cada base de datos de la que se quiere backup...
        dbname = db['name']  # Almacenar nombre de la BD por claridad
        mod_allow_conn = False  # En principio no se modifica datallowconn
        # Si se exigen copias de bases de datos sin permisos de conexión...
        if not db['allow_connection'] and bkp_vars['in_forbidden']:
            allow_db_conn(conn, cursor, dbname)  # Permitir conexiones
            mod_allow_conn = True  # Marcar que se modifica datallowconn
            logger.info('Habilitando conexiones a la base de datos...')
        if bkp_vars['vacuum']:
            logger.info('Iniciando limpieza previa de la base de datos '
                        '"{}"...'.format(dbname))
            success = vacuum_db(logger, dbname, bkp_vars['user'],
                                bkp_vars['server'], bkp_vars['port'])
            if success:
                logger.info('Limpieza previa de la base de datos "{}" '
                            'completada.'.format(dbname))
            else:
                logger.warning('La limpieza previa de la base de datos "{}" '
                               'no se pudo completar.'.format(dbname))
        logger.info('Iniciando copia de seguridad de la base de datos '
                    '"{}"...'.format(dbname))
        # Realizar copia de seguridad de la base de datos
        success = dump_db(logger, bkps_dir, bkp_vars['bkp_type'], dbname,
                          bkp_vars['user'], bkp_vars['prefix'],
                          bkp_vars['server'], bkp_vars['port'])
        if mod_allow_conn:  # Si se modificó datallowconn...
            # Deshabilitar nuevamente las conexiones y dejarlo como estaba
            disallow_db_conn(conn, cursor, dbname)
            logger.info('Deshabilitando conexiones a la base de datos...')
        if success:
            message = 'Copia de seguridad de la base de datos "{}" ' \
                      'completada.'.format(dbname)
            logger_colored(logger, 'info', message, 'green')
        else:
            message = 'La copia de seguridad de la base de datos "{}" ' \
                      'no se pudo completar.'.format(dbname)
            logger_colored(logger, 'warning', message, 'yellow', effect='bold')
    message = 'Copias de seguridad finalizadas.'
    logger_colored(logger, 'info', message, 'green')


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

    # Crear un logger para los mensajes de información
    logger = create_logger()

    # Asignar ruta por defecto al archivo de configuración
    cfg_path = default_cfg_path('dumper/dump.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    parser.add_argument('-c', '--config',
                        help='load a configuration file (.cfg)',
                        default=cfg_path)
    args = parser.parse_args()  # Guardar los parámetros creados

    # Cargar variables del archivo .cfg obtenido a través de args
    bkp_vars = load_dump(logger, args.config)

    # Asegurar la existencia de un directorio donde almacenar las copias de
    # seguridad de PostgreSQL
    if bkp_vars['bkp_path']:  # Si se especificó una ruta en el .cfg...
        bkps_dir = bkp_vars['bkp_path']  # Almacenar esa ruta
    else:  # Si no se especificó una ruta en el .cfg...
        bkps_dir = default_bkps_path()  # Almacenar la ruta por defecto
    create_dir(logger, bkps_dir)  # Crear directorio para las copias

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
        message = 'El usuario especificado para la conexión a PostgreSQL ' \
                  'no tiene rol de superusuario: sólo podrá actuar sobre ' \
                  'las bases de datos de las cuales es propietario.'
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')

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
    bkp_list = get_dbs_to_bkp(logger, dbs_all, bkp_vars)

    # Realizar las nuevas copias de seguridad (dump)
    make_bkps(logger, conn, cursor, bkp_list, bkps_dir, bkp_vars)

    # Cerrar comunicación con la base de datos
    pg_disconnect(logger, conn, cursor)
