#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger de la librería personalizada
# logger.logger (para utilizar un logger que muestre información al usuario)
from logger.logger import Logger
# Importar la funciones pg_connect y pg_disconnect de la librería
# personalizada pg_connection.pg_connection (para conectarse y desconectarse a
# PostgreSQL y poder ejecutar consultas)
from pg_connection.pg_connection import Connection
# Importar la función load_dump de la librería personalizada
# config.config_tools (para obtener datos del archivo config)
from config.config_tools import CfgParser
# Importar la función get_filtered_dbs de la librería personalizada
# db_selector.db_selector (para filtrar listados de bases de datos)
from db_selector.db_selector import DbSelector
# Importar las funciones create_dir, default_bkps_path, default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para crear directorios de forma
# automática y localizar archivos creados por defecto)
from dir_tools.dir_tools import Dir
from pg_tools.pg_tools import PgTools
# Importar la librería argparse (para trabajar con el vector argv fácilmente)
import argparse


# ************************* DEFINICIÓN DE FUNCIONES *************************


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

    # Crear un logger para los mensajes de información
    logger = Logger()

    Dir.is_root(logger)  # Parar la ejecución si el programa lo ejecuta "root"

    # Asignar ruta por defecto al archivo de configuración
    conn_cfg_path = Dir.default_cfg_path('connection/connection.cfg')
    dump_cfg_path = Dir.default_cfg_path('dumper/dump.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    arg_parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    arg_parser.add_argument('-c', '--conn',
                            help='load a configuration file (.cfg) to get the '
                                 'PostgreSQL connection parameters',
                                 default=conn_cfg_path)
    arg_parser.add_argument('-d', '--dump',
                            help='load a configuration file (.cfg) to get the '
                                 'dumper conditions', default=dump_cfg_path)

    args = arg_parser.parse_args()  # Guardar los parámetros creados

    parser = CfgParser(logger)

    # Cargar variables de conexión del archivo .cfg obtenido a través de args
    parser.load_cfg(args.conn)
    parser.parse_pgconn()
    # Cargar variables generales del archivo .cfg obtenido a través de args
    parser.load_cfg(args.dump)
    parser.parse_dump()

    # Asegurar la existencia de un directorio donde almacenar las copias de
    # seguridad de PostgreSQL
    if parser.bkp_vars['bkp_path']:  # Si se especificó una ruta en el .cfg...
        bkps_dir = parser.bkp_vars['bkp_path']  # Almacenar esa ruta
    else:  # Si no se especificó una ruta en el .cfg...
        bkps_dir = Dir.default_bkps_path()  # Almacenar la ruta por defecto
    Dir.create_dir(bkps_dir, logger)  # Crear directorio para las copias

    # Iniciar conexión a la base de datos "template1" con el usuario
    # especificado
    conn = Connection(parser.conn_vars['server'], parser.conn_vars['user'],
                      parser.conn_vars['pwd'], parser.conn_vars['port'],
                      logger)

    # Comprobar si el usuario actualmente conectado es superusuario de
    # PostgreSQL
    pg_superuser = conn.is_pg_superuser()
    if not pg_superuser:  # Si no es superusuario de PostgreSQL...
        # Sólo puede manipular las BDs de las que es propietario
        parser.bkp_vars['db_owner'] = conn.user
        message = 'El usuario especificado para la conexión a PostgreSQL ' \
                  'no tiene rol de superusuario: sólo podrá actuar sobre ' \
                  'las bases de datos de las cuales es propietario.'
        logger.set_view('warning', message, 'yellow', effect='bold')

    # Ejecutar consulta de PostgreSQL y obtener nombres de todas las bases de
    # datos almacenadas, sus permisos de conexión y sus propietarios
    conn.get_cursor_dbs(ex_templates=False,
                        db_owner=parser.bkp_vars['db_owner'])

    dbs_all = []  # Inicializar lista de nombres de las bases de datos
    for record in conn.cursor:  # Para cada registro de la consulta...
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
    logger.set_view('info', message, 'white')

    # Almacenar las bases de datos de las que se realizará una copia de
    # seguridad
    bkp_list = DbSelector.get_filtered_dbs(
        dbs_all, parser.bkp_vars['in_dbs'], parser.bkp_vars['ex_dbs'],
        parser.bkp_vars['in_regex'], parser.bkp_vars['ex_regex'],
        parser.bkp_vars['in_priority'], logger)

    # Realizar las nuevas copias de seguridad (dump)
    PgTools.dump_dbs(conn, bkps_dir, bkp_list, parser.bkp_vars['bkp_type'],
                     parser.bkp_vars['in_forbidden'],
                     parser.bkp_vars['prefix'],
                     parser.bkp_vars['server_alias'],
                     parser.bkp_vars['vacuum'], logger)

    # Cerrar comunicación con la base de datos
    conn.pg_disconnect()
